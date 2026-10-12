# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation Summary

PawPal+ uses four Python classes in `pawpal_system.py`. `Task` represents an activity with a description, duration, frequency, priority, and completion status. `Pet` holds a pet's details and tasks, while `Owner` manages multiple pets and combines their tasks using `get_all_tasks()`. `Scheduler` calls that owner method, skips completed tasks, sorts remaining tasks by priority and shorter duration, and selects activities that fit within the owner's available time. Its `explain_plan()` method formats the schedule for display.

The `main.py` demonstration creates two pets and prints their combined daily schedule. The pytest tests verify task completion and task addition. Daily and weekly recurrence is now implemented; the Streamlit interface is a separate integration step.

## 🖥️ Sample Output

Run the multi-pet scheduler demonstration:

```powershell
python main.py
```

Verified terminal output:

```text
Today's Schedule
================
Daily care plan for Jordan:
- Luna: Feed Luna (10 min; high priority)
- Mochi: Morning walk (20 min; high priority)
- Mochi: Brush Mochi (15 min; medium priority)
```

The owner has two pets and four candidate tasks. With 50 available minutes, the scheduler includes three tasks totaling 45 minutes and leaves out the lower-priority 25-minute playtime task. Daily and weekly tasks now generate their next occurrence when completed through the pet or scheduler.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ supports scheduling across multiple pets by collecting `(Pet, Task)` pairs through `Owner.get_all_tasks()`.

| Feature | Method(s) | Behavior |
|---|---|---|
| Sorting by time | `Scheduler.sort_by_time()` | Orders all pets' tasks by `HH:MM` start time using `sorted()` and a lambda; untimed tasks come last. |
| Filtering | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Returns tasks for a chosen pet, completion status, or both. Pet-name matching ignores case. |
| Conflict detection | `Scheduler.find_conflicts(on_date=None)` | Checks overlapping time intervals across pets and returns warning strings. It ignores completed, untimed, and future-dated tasks and does not automatically reschedule them. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.mark_task_complete()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task through the pet/scheduler creates a new pending occurrence 1 or 7 days after the original due date. The completed task remains in history. |
| Daily plan | `Scheduler.generate_schedule()` | Chooses pending tasks due by the selected date using priority, duration, and the owner's available-minute budget. |

Sorting, filtering, conflict warnings, and daily-plan selection are separate operations. The daily plan does not automatically resolve conflicting appointment times.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
