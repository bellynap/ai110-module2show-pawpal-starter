# 🐾 PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner
plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They 
want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## Features

- **Owner & Pet Management:** Add multiple pets with species, date of 
  birth, and medical notes. Age is calculated automatically.
- **Smart Task Scheduling:** Tasks are prioritized by importance and 
  fit within the owner's available time for the day.
- **Conflict Detection:** Warns the owner if two tasks for the same 
  pet are scheduled at the same time, and suggests the next 
  available time slot as a resolution.
- **Sorting & Filtering:** Tasks can be sorted by time or filtered 
  by pet and completion status.
- **Recurring Tasks:** When a task is marked complete, the next 
  occurrence is automatically created for the same time.
- **Time Picker:** Easy AM/PM time selection with support for 
  multiple time slots when a task occurs more than once a day.
- **Schedule Explanation:** The schedule displays each task's 
  priority, pet, time, duration, and type so the owner always 
  knows why each task was chosen and when it happens.

## Smarter Scheduling

PawPal+ includes the following algorithmic features:
- **Priority-based scheduling:** Tasks are sorted by priority (1 = 
  highest) so critical tasks like medication are always scheduled first.
- **Time filtering:** The scheduler fits tasks within the owner's 
  available time, skipping tasks that don't fit.
- **Conflict detection:** Detects when two tasks for the same pet 
  are scheduled at the same time and warns the owner.
- **Next available slot:** Automatically suggests an alternative 
  time slot when a conflict is detected.
- **Recurring tasks:** When a recurring task is marked complete, a 
  new instance is automatically created for the next occurrence.
- **Sorting and filtering:** Tasks can be sorted by time or filtered 
  by pet name and completion status.

## System Architecture

![UML Diagram](uml_final.png)

## Getting Started

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

## Testing PawPal+

Run the test suite with:
```bash
python -m pytest -v
```

Tests cover:
- Task completion status
- Adding tasks to pets
- Sorting tasks by scheduled time
- Recurring task next occurrence
- Conflict detection for same pet
- No false conflicts across different pets

Confidence level: ⭐⭐⭐⭐ (4/5)

## Suggested Workflow

1. Save owner info and set available time
2. Add your pets
3. Add care tasks with priorities and times
4. Generate the daily schedule
5. Check off tasks as you complete them

## Optional Extensions

- ✅ Challenge 1: Next Available Slot algorithm — automatically 
  suggests alternative times when scheduling conflicts are detected
- ✅ Challenge 2: Data Persistence (auto-saves to data.json)
- ✅ Challenge 3: Priority-Based Color Coding (🔴🟡🟢)
- ✅ Challenge 4: Professional UI with emojis, tabs, and checkboxes

## Demo

<a href="/course_images/ai110/demo_screenshot2.png" target="_blank"><img src='/course_images/ai110/demo_screenshot2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>