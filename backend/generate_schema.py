#!/usr/bin/env python3
"""
Generate SQL schema from SQLAlchemy models to verify correctness.
This shows what the database SHOULD look like based on current models.
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

# Add app to path
sys.path.insert(0, '.')

from app.database import Base
from app.models.user import User
from app.models.conversation import Conversation
from app.models.task import Task
from app.models.project import Project
from app.models.goal import Goal
from app.models.backburner import BackburnerItem
from app.models.calendar import CalendarEvent
from app.models.checkin import Checkin
from app.models.metric import Metric
from app.models.milestone import Milestone
from app.models.pattern_category import PatternCategory
from app.models.pattern_observation import PatternObservation
# Skip pattern_tracking - has duplicate PatternCategory definition
from app.models.wheel import WheelCategory, WheelScore
from app.models.work_session import WorkSession

# Create engine (won't actually connect)
engine = create_engine('postgresql://fake:fake@localhost/fake')

print("=" * 80)
print("EXPECTED DATABASE SCHEMA FROM CURRENT MODELS")
print("=" * 80)
print()

# Generate CREATE TABLE statements for all models
for table_name, table in Base.metadata.tables.items():
    print(f"\n--- Table: {table_name} ---")
    create_stmt = CreateTable(table).compile(engine)
    print(str(create_stmt).strip())
    print()

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nTotal tables: {len(Base.metadata.tables)}")
print("\nTables:")
for table_name in sorted(Base.metadata.tables.keys()):
    table = Base.metadata.tables[table_name]
    columns = [col.name for col in table.columns]
    print(f"  {table_name}: {', '.join(columns[:5])}{'...' if len(columns) > 5 else ''}")
