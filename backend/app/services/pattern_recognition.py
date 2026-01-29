"""Pattern Recognition - track behavior patterns, procrastination, context switching."""
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.conversation import Conversation
from app.models.task import Task, TaskStatus
from app.models.project import Project


class PatternRecognizer:
    """Identifies behavioral patterns from user's history."""
    
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
    
    def detect_repeated_intentions(self, days: int = 7) -> List[Dict]:
        """
        Detect when user mentions the same task/intention multiple times.
        
        Looks for:
        - "I'll do X later" patterns
        - Repeated mentions without action
        - Tasks created but never started
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get recent conversations
        conversations = self.db.query(Conversation).filter(
            and_(
                Conversation.user_id == self.user_id,
                Conversation.created_at >= since_date
            )
        ).order_by(Conversation.created_at.desc()).all()
        
        # Keywords that indicate procrastination
        procrastination_phrases = [
            "later",
            "tomorrow",
            "soon",
            "need to",
            "should",
            "gonna",
            "going to",
            "will do"
        ]
        
        # Track mentions of activities
        mentions = defaultdict(list)
        
        for conv in conversations:
            message_lower = conv.user_message.lower()
            
            # Check for procrastination language
            for phrase in procrastination_phrases:
                if phrase in message_lower:
                    # Extract the thing they're putting off
                    # Simple extraction: words after the phrase
                    words = message_lower.split()
                    if phrase in words:
                        idx = words.index(phrase)
                        if idx + 1 < len(words):
                            activity = " ".join(words[idx+1:idx+4])  # Next 3 words
                            mentions[activity].append({
                                "date": conv.created_at,
                                "phrase": phrase,
                                "full_message": conv.user_message[:100]
                            })
        
        # Find repeated patterns (mentioned 3+ times)
        patterns = []
        for activity, mention_list in mentions.items():
            if len(mention_list) >= 3:
                patterns.append({
                    "activity": activity,
                    "mention_count": len(mention_list),
                    "first_mention": mention_list[-1]["date"],
                    "last_mention": mention_list[0]["date"],
                    "days_repeating": (mention_list[0]["date"] - mention_list[-1]["date"]).days,
                    "sample_phrases": [m["phrase"] for m in mention_list[:3]]
                })
        
        return patterns
    
    def analyze_task_completion_rate(self, days: int = 30) -> Dict:
        """
        Analyze task completion patterns.
        
        Returns:
        - Completion rate
        - Average time to complete
        - Tasks that get stuck
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all tasks created in period
        all_tasks = self.db.query(Task).filter(
            and_(
                Task.user_id == self.user_id,
                Task.created_at >= since_date
            )
        ).all()
        
        if not all_tasks:
            return {
                "completion_rate": 0,
                "message": "No tasks in period"
            }
        
        completed = [t for t in all_tasks if t.status == TaskStatus.DONE]
        in_progress = [t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]
        todo = [t for t in all_tasks if t.status == TaskStatus.TODO]
        
        completion_rate = len(completed) / len(all_tasks) * 100
        
        # Calculate average time to completion
        completion_times = []
        for task in completed:
            if task.completed_at:
                time_to_complete = (task.completed_at - task.created_at).total_seconds() / 3600
                completion_times.append(time_to_complete)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Identify stuck tasks (created > 7 days ago, still TODO)
        stuck_threshold = datetime.utcnow() - timedelta(days=7)
        stuck_tasks = [
            t for t in todo
            if t.created_at < stuck_threshold
        ]
        
        return {
            "completion_rate": round(completion_rate, 1),
            "total_tasks": len(all_tasks),
            "completed": len(completed),
            "in_progress": len(in_progress),
            "todo": len(todo),
            "avg_completion_hours": round(avg_completion_time, 1),
            "stuck_tasks": [
                {
                    "title": t.title,
                    "days_stuck": (datetime.utcnow() - t.created_at).days,
                    "priority": t.priority.value
                }
                for t in stuck_tasks
            ]
        }
    
    def detect_context_switching(self, days: int = 7) -> Dict:
        """
        Detect how often user switches between projects/topics.
        
        High context switching = ADHD red flag.
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        conversations = self.db.query(Conversation).filter(
            and_(
                Conversation.user_id == self.user_id,
                Conversation.created_at >= since_date
            )
        ).order_by(Conversation.created_at.asc()).all()
        
        if len(conversations) < 5:
            return {"switches": 0, "message": "Not enough data"}
        
        # Get active projects
        projects = self.db.query(Project).filter(
            Project.user_id == self.user_id
        ).all()
        
        project_titles = [p.title.lower() for p in projects]
        
        # Track which project each conversation mentions
        conversation_projects = []
        for conv in conversations:
            msg_lower = conv.user_message.lower()
            mentioned_project = None
            
            for title in project_titles:
                if title in msg_lower:
                    mentioned_project = title
                    break
            
            conversation_projects.append(mentioned_project)
        
        # Count switches (when project changes between consecutive messages)
        switches = 0
        for i in range(1, len(conversation_projects)):
            prev = conversation_projects[i-1]
            curr = conversation_projects[i]
            
            if prev and curr and prev != curr:
                switches += 1
        
        switch_rate = switches / len(conversations) * 100 if conversations else 0
        
        # Classify
        if switch_rate > 40:
            assessment = "Very high context switching (ADHD pattern)"
        elif switch_rate > 20:
            assessment = "Moderate context switching"
        else:
            assessment = "Focused work pattern"
        
        return {
            "switches": switches,
            "total_conversations": len(conversations),
            "switch_rate": round(switch_rate, 1),
            "assessment": assessment
        }
    
    def identify_productive_times(self) -> Dict:
        """
        Identify when user is most productive based on task completion times.
        """
        # Get completed tasks
        completed = self.db.query(Task).filter(
            and_(
                Task.user_id == self.user_id,
                Task.status == TaskStatus.DONE,
                Task.completed_at.isnot(None)
            )
        ).all()
        
        if len(completed) < 10:
            return {"message": "Not enough completed tasks to analyze"}
        
        # Group by hour of day
        hour_counts = defaultdict(int)
        for task in completed:
            hour = task.completed_at.hour
            hour_counts[hour] += 1
        
        # Find peak hours
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        peak_hours = sorted_hours[:3]
        
        # Format hours
        peak_times = []
        for hour, count in peak_hours:
            time_str = f"{hour:02d}:00-{(hour+1):02d}:00"
            peak_times.append({
                "time": time_str,
                "completions": count
            })
        
        return {
            "peak_productive_times": peak_times,
            "total_completions": len(completed),
            "recommendation": f"Schedule important work during {peak_times[0]['time']}"
        }
    
    def generate_accountability_message(self) -> str:
        """
        Generate accountability message based on detected patterns.
        
        This is what the AI can use to call out patterns.
        """
        patterns = self.detect_repeated_intentions(days=7)
        completion_stats = self.analyze_task_completion_rate(days=30)
        
        messages = []
        
        # Repeated intentions
        if patterns:
            for pattern in patterns[:2]:  # Top 2 patterns
                messages.append(
                    f"You've mentioned '{pattern['activity']}' {pattern['mention_count']} times "
                    f"over {pattern['days_repeating']} days without starting it."
                )
        
        # Stuck tasks
        if completion_stats.get("stuck_tasks"):
            stuck = completion_stats["stuck_tasks"][:2]
            for task in stuck:
                messages.append(
                    f"'{task['title']}' has been sitting for {task['days_stuck']} days."
                )
        
        # Low completion rate
        if completion_stats.get("completion_rate", 100) < 30:
            messages.append(
                f"Your task completion rate is {completion_stats['completion_rate']}% this month."
            )
        
        return "\n".join(messages) if messages else ""
