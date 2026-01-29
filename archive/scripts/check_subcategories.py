"""
Check categories and subcategories in database vs code
"""
import sys
sys.path.insert(0, '/Users/jenslennartsson/Documents/-ai_projects-/adhd_coach/backend')

from app.database import SessionLocal
from app.models.pattern_tracking import PatternCategory
from sqlalchemy import text

db = SessionLocal()

# Check table schema
result = db.execute(text("PRAGMA table_info(pattern_categories)"))
columns = result.fetchall()

print("📋 PATTERN_CATEGORIES TABLE SCHEMA:")
print("=" * 60)
for col in columns:
    print(f"  {col[1]}: {col[2]}")

# Check if subcategories field exists
has_subcategories = any(col[1] == 'subcategories' for col in columns)
print(f"\n❓ Has 'subcategories' field: {has_subcategories}")

print("\n" + "=" * 60)
print("📊 CATEGORIES IN DATABASE:")
print("=" * 60)
categories = db.query(PatternCategory).filter(PatternCategory.user_id == 1).all()
print(f"Total: {len(categories)} categories\n")

for i, cat in enumerate(categories, 1):
    print(f"{i}. {cat.category_name}")

print("\n" + "=" * 60)
print("📚 SUBCATEGORIES IN CODE (ADVANCED_LEARNING_CATEGORIES.py):")
print("=" * 60)

# Load and count from file
with open('/Users/jenslennartsson/Documents/-ai_projects-/adhd_coach/backend/ADVANCED_LEARNING_CATEGORIES.py', 'r') as f:
    content = f.read()
    
# Count patterns
import re
pattern_blocks = re.findall(r'"patterns":\s*\[(.*?)\]', content, re.DOTALL)

total_subpatterns = 0
for block in pattern_blocks:
    count = block.count('"')  # Each pattern has 2 quotes
    total_subpatterns += count // 2

print(f"Total subpatterns defined in code: {total_subpatterns}")

print("\n" + "=" * 60)
print("🔍 CONCLUSION:")
print("=" * 60)
print(f"✅ Main categories in database: {len(categories)}")
print(f"❌ Subcategories in database: {'YES' if has_subcategories else 'NO - Not stored!'}")
print(f"📝 Subcategories in code: {total_subpatterns} patterns defined")
print(f"\n⚠️  ISSUE: Rich subpattern data exists in code but NOT in database!")

db.close()
