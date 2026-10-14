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

The `main.py` demonstration exercises sorting, filtering, conflict detection, recurring tasks, and a multi-pet daily schedule. The Streamlit interface in `app.py` connects the backend to pet/task entry, task completion, warnings, and schedule display.

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

## Features

- **Multi-pet care management:** `Owner.add_pet()` and `Pet.add_task()` keep each pet's activities organized, while `Owner.get_all_tasks()` gathers them for scheduling.
- **Chronological sorting:** `Scheduler.sort_by_time()` orders tasks by their `HH:MM` start time and places tasks without a start time last.
- **Task filtering:** `Scheduler.filter_tasks()` filters by pet name, completion status, or both.
- **Conflict warnings:** `Scheduler.find_conflicts()` detects overlapping start-time and duration intervals, including tasks for different pets, and warns without automatically changing the schedule.
- **Recurring tasks:** `Task.next_occurrence()` and `Scheduler.mark_task_complete()` create the next pending daily or weekly task when an occurrence is completed. One-time tasks do not recur.
- **Time-budgeted daily plans:** `Scheduler.generate_schedule()` selects pending tasks due by the chosen date, prioritizing higher-priority and shorter tasks within the owner's available minutes. `Scheduler.explain_plan()` describes the result.

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

## Demo Walkthrough

### Start the app

From the project root, install the dependencies if needed, then launch the interactive UI:

```powershell
python -m streamlit run app.py
```

1. **Set owner preferences:** In the sidebar, enter the owner's name and daily minutes available for pet care.
2. **Add pets:** Use **Add a pet** to register Mochi (dog) and Luna (cat). Both pets can have independent care tasks.
3. **Schedule care tasks:** Under **Add a care task**, choose a pet, enter an activity such as *Morning walk*, select its duration and priority, choose a daily/weekly/one-time frequency, set its first due date, and optionally set a specific start time (for example, 08:00).
4. **Review and filter:** The **Sorted and filtered tasks** table lists tasks in chronological order. Filter by pet or by pending/completed status.
5. **Complete recurring tasks:** Select a pending task and choose **Mark complete**. Daily and weekly activities create a new occurrence for the following day or week, while the completed occurrence remains in the history.
6. **Inspect conflicts:** For example, add Mochi's 20-minute walk at 08:00 and Luna's 10-minute feeding at 08:10, both due today. The app displays a warning identifying the overlapping activities. The owner decides whether to change them; PawPal+ does not automatically reschedule tasks.
7. **Generate a daily plan:** Choose a plan date and click **Generate daily plan**. The app shows tasks that fit the available time budget, chosen by priority and duration. Conflict warnings are separate from the plan selection.

### Command-line demonstration

You can also run the backend demonstration without Streamlit:

```powershell
python main.py
```

Example output from the current `main.py` (dates depend on when the script is run):

```text
All tasks sorted by time
========================
08:00 | Luna: Feed Luna (pending)
10:00 | Luna: Playtime (complete)
14:30 | Mochi: Brush Mochi (pending)
18:00 | Mochi: Evening walk (pending)

Mochi's pending tasks
=====================
18:00 | Mochi: Evening walk (pending)
14:30 | Mochi: Brush Mochi (pending)

All completed tasks
===================
10:00 | Luna: Playtime (complete)

Task conflict warnings
======================
WARNING: Mochi's Give medication (08:00, 10 min) overlaps with Luna's Feed Luna (08:00, 10 min).

Recurring tasks after completion
================================
Evening walk: 2026-10-14 -> 2026-10-15 (daily)
Brush Mochi: 2026-10-14 -> 2026-10-21 (weekly)
Mochi now has 5 tasks, including completed history.

Today's Schedule
================
Daily care plan for Jordan:
- Mochi: Give medication (10 min; high priority)
- Luna: Feed Luna (10 min; high priority)
```

**What this demonstrates:** Sorting returns tasks chronologically, but filtering preserves the original task order rather than sorting it automatically. Conflict warnings identify overlapping activities. Completing recurring tasks schedules future occurrences, which are not selected for today's plan. The final plan selects tasks according to priority, duration, and the owner's 50-minute budget; it does not automatically avoid conflicts.
