# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude to add a third, optional scheduling algorithm to PawPal+: find the earliest free start time for a task of a specified duration within a configurable daily window. I asked it to preserve existing sorting, filtering, conflict detection, recurrence, and scheduling behavior, and to add automated tests.

**What did the agent do?**

- Updated `pawpal_system.py` with `Scheduler.next_available_slot(duration_minutes, on_date, workday_start, workday_end)`.
- Created `tests/test_next_available_slot.py` with tests for an empty day, a gap between tasks, overlapping busy tasks, completed/future/untimed tasks, insufficient room, and invalid duration.
- Updated `ai_interactions.md` with this workflow record.
- The method sorts occupied time intervals, moves the proposed start past occupied intervals, and returns an `HH:MM` time or `None` when no slot fits.

**What did you have to verify or fix manually?**

The assistant's files are drafts until copied into my local repository. I must run `python -m pytest` against my actual project, verify that the new method does not change existing scheduling behavior, and try the new method with realistic pet tasks. I should also confirm that the scheduling window fits my needs; this implementation does not schedule across midnight, change existing task times, or reserve an available slot automatically. No manual corrections have been claimed before local verification.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
