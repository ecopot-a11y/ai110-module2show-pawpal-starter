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

## Testing PawPal+

Run the full automated test suite from the project root:

```powershell
python -m pytest
```

The nine tests cover task completion and addition (2), chronological sorting (1), daily and weekly recurrence plus one-time tasks (3), and conflict detection for same-time, overlapping, and non-conflicting tasks (3).

### Successful test run

The following is the actual output from the successful `python -m pytest -v` run (the verbose form of the command above):

```text
========================= test session starts ==========================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\COD\Documents\AI110\ai110-module2show-pawpal-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\COD\Documents\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 9 items

test_conflicts.py::test_same_time_different_pets_warns PASSED     [ 11%]
test_conflicts.py::test_partial_overlap_same_pet_warns PASSED     [ 22%]
test_conflicts.py::test_adjacent_completed_future_and_untimed_tasks_do_not_conflict PASSED [ 33%]
test_recurrence.py::test_daily_recurrence PASSED                  [ 44%]
test_recurrence.py::test_weekly_recurrence PASSED                 [ 55%]
test_recurrence.py::test_one_time_task_does_not_recur PASSED      [ 66%]
tests/test_pawpal.py::test_task_completion PASSED                 [ 77%]
tests/test_pawpal.py::test_task_addition PASSED                   [ 88%]
tests/test_pawpal.py::test_sorting_correctness PASSED             [100%]

========================== 9 passed in 0.32s ===========================
```

### Confidence level: ★★★★☆ (4/5 stars)

All nine automated tests passed, giving me confidence in task management, sorting, recurrence, and conflict detection. I am not assigning five stars because overnight scheduling edge cases and end-to-end Streamlit behavior have not yet been fully tested.

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
