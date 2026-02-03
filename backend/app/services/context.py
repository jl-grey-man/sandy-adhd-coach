"""Context builders - get current state for AI responses."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.models.backburner import BackburnerItem

from app.services.time_intelligence import TimeIntelligence
from app.services.pattern_recognition import PatternRecognizer


def build_context_for_ai(user_id: int, db: Session, include_intelligence: bool = True) -> dict:
    """
    Build context about user's current projects, tasks, backburner items, AND learned patterns.
    This gets passed to the AI so it knows what the user is working on and what it has learned.
    
    Args:
        user_id: User ID
        db: Database session
        include_intelligence: Include time intelligence and pattern recognition (default: True)
    """
    
    # Get active projects
    active_projects = db.query(Project).filter(
        Project.user_id == user_id,
        Project.status == ProjectStatus.ACTIVE
    ).order_by(Project.deadline.asc().nullslast()).all()
    
    # Get all incomplete tasks
    incomplete_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status != TaskStatus.DONE
    ).order_by(Task.due_date.asc().nullslast(), Task.priority.desc()).all()
    
    # Get backburner items
    backburner = db.query(BackburnerItem).filter(
        BackburnerItem.user_id == user_id
    ).order_by(BackburnerItem.created_at.desc()).limit(5).all()
    
    # MEMORY: Get confirmed patterns from NEW pattern system
    from app.services.pattern_learning import PatternLearningService
    from app.services.exploration import ExplorationService
    
    learner = PatternLearningService(user_id, db)
    explorer = ExplorationService(user_id, db)
    
    # Get high confidence patterns (80%+)
    confirmed_patterns = learner.get_confirmed_patterns(min_confidence=80)
    
    # Get exploration status (categories still learning)
    exploration_categories = explorer.get_all_categories_status()
    learning_categories = [c for c in exploration_categories if c['confidence'] < 80]
    
    # Format for AI
    context = {
        "current_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "active_projects": [],
        "tasks": [],
        "backburner": [],
        "learned_patterns": [],
        "exploration_status": []
    }
    
    # Add intelligence if requested
    if include_intelligence:
        time_intel = TimeIntelligence(user_id, db)
        pattern_recognizer = PatternRecognizer(user_id, db)
        
        # Capacity analysis
        capacity = time_intel.get_capacity_summary()
        context["capacity"] = capacity
        
        # Pattern insights
        patterns = pattern_recognizer.detect_repeated_intentions(days=7)
        if patterns:
            context["patterns"] = patterns
        
        completion_stats = pattern_recognizer.analyze_task_completion_rate(days=30)
        context["completion_stats"] = completion_stats
        
        # Accountability message
        accountability = pattern_recognizer.generate_accountability_message()
        if accountability:
            context["accountability_message"] = accountability
    
    # Format projects
    for project in active_projects:
        project_data = {
            "id": project.id,
            "title": project.name,  # Project model uses 'name' not 'title'
            "description": project.description,
            "deadline": project.deadline.strftime("%Y-%m-%d") if project.deadline else None,
            "estimated_hours": project.estimated_hours,
            "days_until_deadline": (project.deadline - datetime.utcnow()).days if project.deadline else None
        }
        context["active_projects"].append(project_data)
    
    # Format tasks
    for task in incomplete_tasks:
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "energy_level": task.energy_level.value,
            "estimated_minutes": task.estimated_minutes,
            "status": task.status.value,
            "project_id": task.project_id,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None
        }
        context["tasks"].append(task_data)
    
    # Format backburner
    for item in backburner:
        context["backburner"].append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "reason": item.reason
        })
    
    # Format confirmed patterns from NEW system
    for pattern in confirmed_patterns:
        context["learned_patterns"].append({
            "category": pattern['category'],
            "hypothesis": pattern['hypothesis'],
            "confidence": pattern['confidence']
        })
    
    # Format exploration status from NEW system
    for category in learning_categories[:5]:  # Top 5 categories still learning
        context["exploration_status"].append({
            "category": category['category'],
            "description": category['description'],
            "confidence": category['confidence'],
            "observations": category['observations']
        })
    
    return context


def format_context_for_prompt(context: dict) -> str:
    """Format context as readable text for AI prompt."""
    
    lines = []
    
    lines.append(f"TODAY'S DATE: {context['current_date']}")
    lines.append("")
    
    # CONFIRMED PATTERNS (Memory Integration) - Present as working theories
    if context.get("learned_patterns"):
        lines.append("WORKING HYPOTHESES ABOUT JENS (Stay curious, invite challenge):")
        lines.append("")
        for p in context["learned_patterns"][:10]:
            category_name = p['category'].replace('_', ' ').title()
            confidence = p['confidence']
            
            # Confidence phrasing
            if confidence < 70:
                phrase = "Might be noticing"
            elif confidence < 85:
                phrase = "Think I'm seeing"
            elif confidence < 95:
                phrase = "Pattern seems to be"
            else:
                phrase = "Consistently happens"
            
            lines.append(f"  • {phrase}: {p['hypothesis']}")
            lines.append(f"    [{category_name}, {confidence}% confidence, based on {p.get('supporting_observations', '?')} observations]")
        lines.append("")
        lines.append("  Remember: These are theories to test, not facts. Stay open to being wrong!")
        lines.append("")
    
    # EXPLORATION STATUS (What you're still learning)
    if context.get("exploration_status"):
        lines.append("AREAS YOU'RE STILL LEARNING:")
        for t in context["exploration_status"]:
            category_name = t['category'].replace('_', ' ').title()
            lines.append(f"  - {category_name}: {t['confidence']}% confident ({t['observations']} observations)")
        lines.append("")
    
    # Capacity summary
    if context.get("capacity"):
        cap = context["capacity"]
        lines.append("CAPACITY ANALYSIS:")
        lines.append(f"  Status: {cap['status'].upper()}")
        lines.append(f"  {cap['message']}")
        if cap.get("recommendation"):
            lines.append(f"  Recommendation: {cap['recommendation']}")
        lines.append("")
    
    # Accountability patterns
    if context.get("accountability_message"):
        lines.append("PATTERN ALERT:")
        lines.append(f"  {context['accountability_message']}")
        lines.append("")
    
    # Active projects
    if context["active_projects"]:
        lines.append("ACTIVE PROJECTS:")
        for p in context["active_projects"]:
            deadline_str = f" (deadline: {p['deadline']}, {p['days_until_deadline']} days)" if p['deadline'] else ""
            lines.append(f"  - {p['title']}{deadline_str}")
        lines.append("")
    
    # Tasks
    if context["tasks"]:
        lines.append("CURRENT TASKS:")
        for t in context["tasks"]:
            status_emoji = "⏳" if t["status"] == "in_progress" else "📋"
            priority_str = f" [{t['priority']}]" if t['priority'] != 'medium' else ""
            time_str = f" ({t['estimated_minutes']}min)" if t['estimated_minutes'] else ""
            lines.append(f"  {status_emoji} {t['title']}{priority_str}{time_str}")
        lines.append("")
    else:
        lines.append("CURRENT TASKS: None")
        lines.append("")
        lines.append("")
    
    # Backburner
    if context["backburner"]:
        lines.append("BACKBURNER IDEAS:")
        for b in context["backburner"]:
            lines.append(f"  💡 {b['title']}")
        lines.append("")
    
    return "\n".join(lines)

