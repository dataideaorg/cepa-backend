#!/usr/bin/env python
"""
Simple test script to check focus areas setup
Run this from the backend directory: python test_focus_areas.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from focusareas.models import FocusArea

print("=" * 50)
print("FOCUS AREAS DIAGNOSTIC TEST")
print("=" * 50)

# Check if focus areas exist
focus_areas = FocusArea.objects.all()
count = focus_areas.count()

print(f"\nTotal Focus Areas in database: {count}")

if count > 0:
    print("\nFocus Areas found:")
    for fa in focus_areas:
        print(f"  - {fa.title} (slug: {fa.slug}, status: {fa.status})")
        print(f"    Objectives: {fa.objectives.count()}")
        print(f"    Activities: {fa.activities.count()}")
        print(f"    Outcomes: {fa.outcomes.count()}")
        print(f"    Partners: {fa.partners.count()}")
        print(f"    Milestones: {fa.milestones.count()}")
else:
    print("\n⚠️  No focus areas found in database!")
    print("\nTo populate focus areas, run:")
    print("  python manage.py populate_focus_areas")

print("\n" + "=" * 50)
