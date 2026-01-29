"""AI Actions - extract and execute structured actions from AI responses."""
import json
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority, TaskEnergyLevel
from app.models.backburner import BackburnerItem
from app.models.reminder import Reminder


def extract_actions_from_response(ai_response: str) -> list[dict]:
    """
    Extract structured actions from AI response.
    
    The AI can embed JSON actions in its response like:
    ```action
    {"type": "create_project", "title": "Launch Website", "deadline": "2026-02-10"}
    ```
    
    Returns list of action dicts.
    """
    actions = []
    
    # Look for ```action blocks
    action_pattern = r'```action\s*\n(.*?)\n```'
    matches = re.findall(action_pattern, ai_response, re.DOTALL)
    
    for match in matches:
        try:
            action = json.loads(match.strip())
            actions.append(action)
        except json.JSONDecodeError:
            continue
    
    return actions


def execute_action(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """
    Execute a structured action from the AI.
    
    Returns a dict with:
    - success: bool
    - action_type: str
    - details: dict (for Telegram confirmation)
    - error: str (if failed)
    """
    action_type = action.get("type")
    
    try:
        if action_type == "create_project":
            return _create_project(action, user_id, db)
        
        elif action_type == "create_task":
            return _create_task(action, user_id, db)
        
        elif action_type == "create_reminder":
            return _create_reminder(action, user_id, db)
        
        elif action_type == "move_to_backburner":
            return _move_to_backburner(action, user_id, db)
        
        elif action_type == "complete_task":
            return _complete_task(action, user_id, db)
        
        else:
            return {
                "success": False,
                "action_type": action_type,
                "error": f"Unknown action type: {action_type}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "action_type": action_type,
            "error": str(e)
        }


def _create_project(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """Create a new project."""
    title = action.get("title")
    description = action.get("description")
    deadline_str = action.get("deadline")
    estimated_hours = action.get("estimated_hours")
    
    # Parse deadline
    deadline = None
    if deadline_str:
        try:
            deadline = datetime.fromisoformat(deadline_str)
        except:
            # Try parsing relative dates like "in 2 weeks"
            pass
    
    project = Project(
        user_id=user_id,
        title=title,
        description=description,
        deadline=deadline,
        estimated_hours=estimated_hours,
        status=ProjectStatus.ACTIVE
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "success": True,
        "action_type": "create_project",
        "details": {
            "title": project.title,
            "description": project.description,
            "deadline": project.deadline.isoformat() if project.deadline else None,
            "estimated_hours": project.estimated_hours,
            "project_id": project.id
        }
    }


def _create_task(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """Create a new task."""
    title = action.get("title")
    description = action.get("description")
    project_id = action.get("project_id")
    priority_str = action.get("priority")  # May be None
    energy_level_str = action.get("energy_level")  # May be None
    estimated_minutes = action.get("estimated_minutes")
    due_date_str = action.get("due_date")
    
    # Parse priority (only if explicitly provided)
    priority = None
    if priority_str:
        try:
            priority = TaskPriority(priority_str.lower())
        except:
            pass
    
    # Parse energy level (only if explicitly provided)
    energy_level = None
    if energy_level_str:
        try:
            energy_level = TaskEnergyLevel(energy_level_str.lower())
        except:
            pass
    
    # Parse due date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except:
            pass
    
    task = Task(
        user_id=user_id,
        project_id=project_id,
        title=title,
        description=description,
        priority=priority,
        energy_level=energy_level,
        estimated_minutes=estimated_minutes,
        due_date=due_date,
        status=TaskStatus.TODO
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {
        "success": True,
        "action_type": "create_task",
        "details": {
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "energy_level": task.energy_level.value,
            "estimated_minutes": task.estimated_minutes,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "task_id": task.id
        }
    }


def _move_to_backburner(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """Move something to backburner (or create backburner item)."""
    title = action.get("title")
    description = action.get("description")
    reason = action.get("reason")
    context_tags = action.get("context_tags", [])
    project_id = action.get("project_id")
    
    # If project_id provided, move existing project to backburner
    if project_id:
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id
        ).first()
        
        if project:
            project.status = ProjectStatus.BACKBURNER
            project.moved_to_backburner_at = datetime.utcnow()
            project.backburner_reason = reason
            db.commit()
            
            return {
                "success": True,
                "action_type": "move_to_backburner",
                "details": {
                    "title": project.title,
                    "reason": reason,
                    "type": "project"
                }
            }
    
    # Otherwise create new backburner item
    item = BackburnerItem(
        user_id=user_id,
        title=title,
        description=description,
        reason=reason,
        context_tags=context_tags
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return {
        "success": True,
        "action_type": "move_to_backburner",
        "details": {
            "title": item.title,
            "description": item.description,
            "reason": item.reason,
            "type": "idea"
        }
    }


def _complete_task(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """Mark a task as complete."""
    task_id = action.get("task_id")
    
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
    
    if not task:
        return {
            "success": False,
            "action_type": "complete_task",
            "error": "Task not found"
        }
    
    task.status = TaskStatus.DONE
    task.completed_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "action_type": "complete_task",
        "details": {
            "title": task.title,
            "task_id": task.id
        }
    }


def _create_reminder(action: dict, user_id: int, db: Session) -> Dict[str, Any]:
    """Create a reminder (notification, not a task)."""
    message = action.get("message")
    minutes_from_now = action.get("minutes_from_now", 5)
    
    # Calculate remind_at time in UTC
    remind_at_utc = datetime.utcnow() + timedelta(minutes=minutes_from_now)
    
    # Convert to Swedish time for display
    import pytz
    sweden_tz = pytz.timezone('Europe/Stockholm')
    remind_at_sweden = remind_at_utc.replace(tzinfo=pytz.utc).astimezone(sweden_tz)
    
    reminder = Reminder(
        user_id=user_id,
        message=message,
        remind_at=remind_at_utc,
        sent=False
    )
    
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    
    return {
        "success": True,
        "action_type": "create_reminder",
        "details": {
            "message": message,
            "remind_at": remind_at_sweden.strftime("%H:%M"),
            "minutes": minutes_from_now
        }
    }
