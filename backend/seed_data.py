"""Seed realistic data for testing time intelligence and pattern recognition."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority, TaskEnergyLevel
from app.models.backburner import BackburnerItem
from app.models.conversation import Conversation


def seed_test_data():
    """Add realistic ADHD entrepreneur scenario."""
    
    db = next(get_db())
    
    try:
        # Get the user (assuming user@example.com exists)
        user = db.query(User).filter(User.email == "user@example.com").first()
        
        if not user:
            print("❌ User not found")
            return
        
        print(f"✅ Found user: {user.email}")
        
        # SCENARIO: Overloaded entrepreneur with multiple projects
        
        # PROJECT 1: Launch Website (urgent, deadline in 2 weeks)
        website = Project(
            user_id=user.id,
            title="Launch Website",
            description="Complete website redesign and launch",
            deadline=datetime.utcnow() + timedelta(days=14),
            estimated_hours=40,
            status=ProjectStatus.ACTIVE
        )
        db.add(website)
        db.flush()
        
        # PROJECT 2: Podcast Launch (deadline in 3 weeks)
        podcast = Project(
            user_id=user.id,
            title="Start Podcast",
            description="Launch podcast series about entrepreneurship",
            deadline=datetime.utcnow() + timedelta(days=21),
            estimated_hours=30,
            status=ProjectStatus.ACTIVE
        )
        db.add(podcast)
        db.flush()
        
        # PROJECT 3: Write Book (deadline in 6 weeks - should go to backburner)
        book = Project(
            user_id=user.id,
            title="Write Book",
            description="Finish book on ADHD entrepreneurship",
            deadline=datetime.utcnow() + timedelta(days=42),
            estimated_hours=60,
            status=ProjectStatus.ACTIVE
        )
        db.add(book)
        db.flush()
        
        # PROJECT 4: No deadline project (backburner candidate)
        course = Project(
            user_id=user.id,
            title="Create Online Course",
            description="Course on productivity for ADHD",
            deadline=None,
            estimated_hours=50,
            status=ProjectStatus.ACTIVE
        )
        db.add(course)
        db.flush()
        
        print(f"✅ Created 4 projects (total: 180 hours needed)")
        
        # TASKS - mix of priorities and states
        
        # Website tasks
        tasks_data = [
            # Website (some completed, some stuck)
            ("Fix header design", website.id, TaskPriority.HIGH, TaskEnergyLevel.MEDIUM, 60, TaskStatus.DONE, -2),
            ("Write homepage copy", website.id, TaskPriority.HIGH, TaskEnergyLevel.HIGH, 120, TaskStatus.TODO, -5),  # STUCK
            ("Set up hosting", website.id, TaskPriority.HIGH, TaskEnergyLevel.LOW, 30, TaskStatus.TODO, -4),  # STUCK
            ("Test mobile responsiveness", website.id, TaskPriority.MEDIUM, TaskEnergyLevel.MEDIUM, 90, TaskStatus.TODO, -1),
            
            # Podcast
            ("Buy microphone", podcast.id, TaskPriority.HIGH, TaskEnergyLevel.LOW, 30, TaskStatus.DONE, -3),
            ("Record first episode", podcast.id, TaskPriority.HIGH, TaskEnergyLevel.HIGH, 180, TaskStatus.TODO, -1),
            ("Create podcast artwork", podcast.id, TaskPriority.MEDIUM, TaskEnergyLevel.MEDIUM, 120, TaskStatus.TODO, -1),
            
            # Book
            ("Outline chapters", book.id, TaskPriority.MEDIUM, TaskEnergyLevel.HIGH, 240, TaskStatus.TODO, -7),  # STUCK
            ("Write chapter 1", book.id, TaskPriority.MEDIUM, TaskEnergyLevel.HIGH, 300, TaskStatus.TODO, -6),  # STUCK
            
            # Course
            ("Research competitors", course.id, TaskPriority.LOW, TaskEnergyLevel.MEDIUM, 120, TaskStatus.TODO, -10),  # STUCK
            
            # Standalone tasks (no project)
            ("Email accountant about taxes", None, TaskPriority.HIGH, TaskEnergyLevel.LOW, 15, TaskStatus.TODO, -8),  # STUCK
            ("Call insurance company", None, TaskPriority.MEDIUM, TaskEnergyLevel.LOW, 20, TaskStatus.TODO, -6),  # STUCK
            ("Organize desk", None, TaskPriority.LOW, TaskEnergyLevel.LOW, 30, TaskStatus.TODO, -3),
        ]
        
        for title, proj_id, priority, energy, minutes, status, days_ago in tasks_data:
            task = Task(
                user_id=user.id,
                project_id=proj_id,
                title=title,
                priority=priority,
                energy_level=energy,
                estimated_minutes=minutes,
                status=status,
                created_at=datetime.utcnow() + timedelta(days=days_ago)
            )
            
            if status == TaskStatus.DONE:
                task.completed_at = datetime.utcnow() + timedelta(days=days_ago + 1)
            
            db.add(task)
        
        print(f"✅ Created {len(tasks_data)} tasks (7 stuck, 2 completed)")
        
        # BACKBURNER IDEAS
        backburner_items = [
            ("Learn to play guitar", "Been thinking about this for years", "Not urgent, just a dream"),
            ("Build SaaS product", "Product idea for ADHD tools", "Need to focus on current projects first"),
            ("Start YouTube channel", "Video content creation", "Too much on plate already"),
        ]
        
        for title, desc, reason in backburner_items:
            item = BackburnerItem(
                user_id=user.id,
                title=title,
                description=desc,
                reason=reason,
                context_tags=["someday", "idea"]
            )
            db.add(item)
        
        print(f"✅ Created {len(backburner_items)} backburner items")
        
        # CONVERSATION HISTORY - showing procrastination patterns
        procrastination_convos = [
            ("I need to email the accountant about taxes", -8),
            ("I should really email the accountant soon", -6),
            ("I'll email the accountant tomorrow", -4),
            ("I need to call the insurance company", -7),
            ("I should call insurance this week", -5),
            ("I'll call insurance later today", -3),
            ("I need to write the homepage copy", -5),
            ("I should work on the homepage copy soon", -3),
            ("I'll write the copy tomorrow", -2),
        ]
        
        for message, days_ago in procrastination_convos:
            conv = Conversation(
                user_id=user.id,
                user_message=message,
                ai_response="What's stopping you from doing that now?",
                session_id="test_session",
                created_at=datetime.utcnow() + timedelta(days=days_ago)
            )
            db.add(conv)
        
        print(f"✅ Created {len(procrastination_convos)} procrastination conversations")
        
        db.commit()
        print("\n" + "="*50)
        print("✅ SEEDED TEST DATA!")
        print("="*50)
        print("\nSCENARIO:")
        print("  - 4 active projects (180 hours total)")
        print("  - 14 days until first deadline")
        print("  - Only ~56 hours available (14 days × 4 hours/day)")
        print("  - OVERLOADED by 124 hours!")
        print("  - 7 tasks stuck for > 3 days")
        print("  - Clear procrastination patterns (email, insurance, copy)")
        print("  - 3 backburner ideas")
        print("\nNow ask the bot:")
        print("  'Am I overloaded?'")
        print("  'What am I avoiding?'")
        print("  'Show me my stuck tasks'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_test_data()
