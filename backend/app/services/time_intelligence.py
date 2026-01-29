"""Time Intelligence - calculate available time, detect conflicts, manage capacity."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.models.milestone import Milestone


class TimeIntelligence:
    """Analyzes time commitments and capacity."""
    
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
    
    def analyze_project_feasibility(self, project_id: int) -> Dict:
        """
        Analyze if a project is feasible given current workload.
        
        Returns:
            - is_feasible: bool
            - hours_needed: int
            - hours_available: int
            - conflicts: list of conflicting projects
            - recommendation: str
        """
        project = self.db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == self.user_id
        ).first()
        
        if not project or not project.deadline:
            return {"is_feasible": None, "reason": "No deadline set"}
        
        # Calculate days until deadline
        days_until = (project.deadline - datetime.utcnow()).days
        
        if days_until < 0:
            return {
                "is_feasible": False,
                "reason": "Deadline has passed",
                "recommendation": "Update deadline or move to backburner"
            }
        
        # Get hours needed
        hours_needed = project.estimated_hours or 0
        
        # Calculate available hours (assume 4 productive hours per day for ADHD)
        available_hours_total = days_until * 4
        
        # Get other active projects competing for time
        other_projects = self.db.query(Project).filter(
            and_(
                Project.user_id == self.user_id,
                Project.id != project_id,
                Project.status == ProjectStatus.ACTIVE,
                Project.deadline.isnot(None),
                Project.deadline <= project.deadline
            )
        ).all()
        
        # Calculate committed hours
        committed_hours = sum(p.estimated_hours or 0 for p in other_projects)
        
        # Available hours for THIS project
        available_hours = available_hours_total - committed_hours
        
        # Check feasibility
        is_feasible = available_hours >= hours_needed
        
        conflicts = []
        if not is_feasible:
            for p in other_projects:
                conflicts.append({
                    "project": p.title,
                    "deadline": p.deadline.strftime("%Y-%m-%d"),
                    "hours": p.estimated_hours
                })
        
        # Generate recommendation
        if is_feasible:
            recommendation = f"Feasible. You have {available_hours}h available for {hours_needed}h of work."
        else:
            shortfall = hours_needed - available_hours
            recommendation = f"Overloaded by {shortfall}h. Consider moving '{project.title}' to backburner or pushing deadline."
        
        return {
            "is_feasible": is_feasible,
            "hours_needed": hours_needed,
            "hours_available": available_hours,
            "days_until_deadline": days_until,
            "conflicts": conflicts,
            "recommendation": recommendation
        }
    
    def get_capacity_summary(self) -> Dict:
        """
        Get overall capacity summary for user.
        
        Returns current workload vs. realistic capacity.
        """
        # Get all active projects with deadlines
        projects = self.db.query(Project).filter(
            and_(
                Project.user_id == self.user_id,
                Project.status == ProjectStatus.ACTIVE,
                Project.deadline.isnot(None)
            )
        ).order_by(Project.deadline.asc()).all()
        
        if not projects:
            return {
                "status": "clear",
                "message": "No active projects with deadlines"
            }
        
        # Find earliest deadline
        earliest_deadline = projects[0].deadline
        days_until = (earliest_deadline - datetime.utcnow()).days
        
        # Calculate total hours needed
        total_hours = sum(p.estimated_hours or 0 for p in projects)
        
        # Available hours (4 productive hours/day)
        available_hours = days_until * 4
        
        if total_hours <= available_hours:
            return {
                "status": "healthy",
                "message": f"Manageable workload: {total_hours}h needed, {available_hours}h available",
                "total_hours": total_hours,
                "available_hours": available_hours,
                "utilization": round(total_hours / available_hours * 100, 1)
            }
        else:
            overload = total_hours - available_hours
            return {
                "status": "overloaded",
                "message": f"Overloaded: {total_hours}h needed but only {available_hours}h available",
                "total_hours": total_hours,
                "available_hours": available_hours,
                "overload_hours": overload,
                "utilization": round(total_hours / available_hours * 100, 1),
                "recommendation": "Consider moving some projects to backburner"
            }
    
    def suggest_backburner_candidates(self) -> List[Dict]:
        """
        Suggest projects that could be moved to backburner.
        
        Criteria:
        - Low recent activity
        - Flexible deadline
        - Not time-critical
        """
        projects = self.db.query(Project).filter(
            and_(
                Project.user_id == self.user_id,
                Project.status == ProjectStatus.ACTIVE
            )
        ).all()
        
        candidates = []
        
        for project in projects:
            # Score based on various factors
            score = 0
            reasons = []
            
            # No deadline = could wait
            if not project.deadline:
                score += 2
                reasons.append("No urgent deadline")
            
            # Far deadline = could wait
            elif project.deadline:
                days_until = (project.deadline - datetime.utcnow()).days
                if days_until > 60:
                    score += 1
                    reasons.append(f"Deadline is {days_until} days away")
            
            # Check task activity
            tasks = self.db.query(Task).filter(
                Task.project_id == project.id
            ).all()
            
            if not tasks:
                score += 1
                reasons.append("No tasks created yet")
            elif all(t.status == TaskStatus.TODO for t in tasks):
                score += 1
                reasons.append("No tasks started")
            
            if score >= 2:
                candidates.append({
                    "project_id": project.id,
                    "project_title": project.title,
                    "score": score,
                    "reasons": reasons
                })
        
        # Sort by score
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        return candidates
    
    def generate_milestone_reminders(self, project_id: int) -> List[Dict]:
        """
        Generate milestone check-in dates for a project.
        
        Strategy:
        - Weekly check-ins for projects > 2 weeks
        - Mid-point check-in for projects 1-2 weeks
        - Daily check-ins for projects < 1 week
        """
        project = self.db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == self.user_id
        ).first()
        
        if not project or not project.deadline:
            return []
        
        days_until = (project.deadline - datetime.utcnow()).days
        milestones = []
        
        if days_until <= 0:
            return []
        
        elif days_until <= 7:
            # Daily check-ins for urgent projects
            for i in range(1, days_until):
                check_date = datetime.utcnow() + timedelta(days=i)
                milestones.append({
                    "date": check_date,
                    "message": f"Daily check: {project.title} - {days_until - i} days left"
                })
        
        elif days_until <= 14:
            # Mid-point check-in
            midpoint = datetime.utcnow() + timedelta(days=days_until // 2)
            milestones.append({
                "date": midpoint,
                "message": f"Halfway point: {project.title}"
            })
        
        else:
            # Weekly check-ins
            weeks = days_until // 7
            for i in range(1, weeks + 1):
                check_date = datetime.utcnow() + timedelta(weeks=i)
                milestones.append({
                    "date": check_date,
                    "message": f"Week {i} check: {project.title}"
                })
        
        return milestones
    
    def create_milestones_for_project(self, project_id: int):
        """Create milestone records in database."""
        milestones_data = self.generate_milestone_reminders(project_id)
        
        for m_data in milestones_data:
            milestone = Milestone(
                project_id=project_id,
                check_in_date=m_data["date"],
                message=m_data["message"],
                completed=False
            )
            self.db.add(milestone)
        
        self.db.commit()
