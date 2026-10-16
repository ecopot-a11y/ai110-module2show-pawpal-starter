"""PawPal+ backend: pet care tasks and a multi-pet daily planner."""

from __future__ import annotations

from datetime import date, datetime, timedelta


class Task:
    """A care activity assigned to a pet."""

    def __init__(
        self,
        description: str,
        duration_minutes: int,
        frequency: str = "daily",
        priority: str = "medium",
        completed: bool = False,
        time: str | None = None,
        due_date: date | None = None,
    ) -> None:
        """Initialize a care task with its timing, priority, and status."""
        if not description.strip():
            raise ValueError("Task description cannot be empty.")
        if duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if priority not in {"low", "medium", "high"}:
            raise ValueError("Priority must be low, medium, or high.")
        self.description = description.strip()
        self.duration_minutes = duration_minutes
        if frequency not in {"daily", "weekly", "once"}:
            raise ValueError("Frequency must be daily, weekly, or once.")
        self.frequency = frequency
        self.priority = priority
        if time is not None:
            from datetime import datetime
            try:
                datetime.strptime(time, "%H:%M")
                if len(time) != 5:
                    raise ValueError
            except ValueError:
                raise ValueError("Time must be in 24-hour HH:MM format.") from None
        self.completed = completed
        self.time = time
        self.due_date = due_date if due_date is not None else date.today()

    def mark_complete(self) -> None:
        """Mark this care task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task | None:
        """Create the next unfinished occurrence of a recurring task."""
        days = {"daily": 1, "weekly": 7}.get(self.frequency)
        if days is None:
            return None
        return Task(
            self.description, self.duration_minutes,
            frequency=self.frequency, priority=self.priority,
            time=self.time, due_date=self.due_date + timedelta(days=days),
        )

    def describe(self) -> str:
        """Return a readable summary of this care task."""
        status = "done" if self.completed else "pending"
        return (f"{self.description} ({self.duration_minutes} min, "
                f"{self.frequency}, {self.priority}, {status})")


class Pet:
    """A pet and the tasks needed to care for it."""

    def __init__(self, name: str, species: str) -> None:
        """Initialize a pet and its empty task list."""
        self.name = name
        self.species = species
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete an owned task and append its next occurrence, if recurring."""
        if task not in self.tasks:
            raise ValueError("Task does not belong to this pet.")
        if task.completed:
            return None
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


class Owner:
    """An owner of one or more pets."""

    def __init__(self, name: str, available_minutes: int) -> None:
        """Initialize an owner with a daily time budget."""
        if available_minutes < 0:
            raise ValueError("Available minutes cannot be negative.")
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs across ALL pets, preserving ownership."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Choose pending tasks across all pets within the owner's time budget."""

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner) -> None:
        """Connect the scheduler to an owner."""
        self.owner = owner

    def mark_task_complete(self, pet: Pet, task: Task) -> Task | None:
        """Complete a task for an owner's pet and schedule its recurrence."""
        if pet not in self.owner.pets:
            raise ValueError("Pet does not belong to this owner.")
        return pet.mark_task_complete(task)

    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        """Return all pets' tasks in start-time order, with untimed tasks last."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda item: item[1].time if item[1].time is not None else "99:99",
        )

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet, Task]]:
        """Return tasks matching the requested pet and completion status."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if (pet_name is None or pet.name.casefold() == pet_name.casefold())
            and (completed is None or task.completed == completed)
        ]

    def find_conflicts(self, on_date: date | None = None) -> list[str]:
        """Warn about overlapping unfinished timed tasks due on a given date."""
        day = on_date if on_date is not None else date.today()
        timed_tasks = []
        for pet, task in self.owner.get_all_tasks():
            if task.completed or task.time is None or task.due_date > day:
                continue
            start = datetime.strptime(task.time, "%H:%M")
            end = start + timedelta(minutes=task.duration_minutes)
            timed_tasks.append((pet, task, start, end))

        timed_tasks.sort(key=lambda item: item[2])
        warnings = []
        for index, (pet_a, task_a, start_a, end_a) in enumerate(timed_tasks):
            for pet_b, task_b, start_b, end_b in timed_tasks[index + 1:]:
                if start_b >= end_a:
                    break
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"WARNING: {pet_a.name}'s {task_a.description} "
                        f"({task_a.time}, {task_a.duration_minutes} min) "
                        f"overlaps with {pet_b.name}'s {task_b.description} "
                        f"({task_b.time}, {task_b.duration_minutes} min)."
                    )
        return warnings

    def next_available_slot(
        self, duration_minutes: int, on_date: date | None = None,
        workday_start: str = "08:00", workday_end: str = "20:00",
    ) -> str | None:
        """Find the earliest free start time within a daily scheduling window.

        Existing incomplete, timed tasks due by on_date block their full durations.
        Untimed and completed tasks do not block slots. Returns HH:MM or None.
        """
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")
        day = on_date if on_date is not None else date.today()
        try:
            start = datetime.strptime(workday_start, "%H:%M")
            end = datetime.strptime(workday_end, "%H:%M")
        except ValueError:
            raise ValueError("Window times must use HH:MM format.") from None
        if end <= start:
            raise ValueError("Window end must be later than window start.")

        busy = []
        for _, task in self.owner.get_all_tasks():
            if task.completed or task.time is None or task.due_date > day:
                continue
            task_start = datetime.strptime(task.time, "%H:%M")
            task_end = task_start + timedelta(minutes=task.duration_minutes)
            if task_end > start and task_start < end:
                busy.append((task_start, task_end))
        busy.sort(key=lambda interval: interval[0])

        candidate = start
        needed = timedelta(minutes=duration_minutes)
        for task_start, task_end in busy:
            if candidate + needed <= task_start:
                return candidate.strftime("%H:%M")
            if task_end > candidate:
                candidate = task_end
            if candidate + needed > end:
                return None
        return candidate.strftime("%H:%M") if candidate + needed <= end else None

    def generate_schedule(self, on_date: date | None = None) -> list[tuple[Pet, Task]]:
        """Select unfinished tasks from all pets within the time budget."""
        today = on_date if on_date is not None else date.today()
        candidates = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.completed and task.due_date <= today
        ]
        candidates.sort(
            key=lambda item: (
                self.PRIORITY_ORDER[item[1].priority],
                item[1].duration_minutes,
            )
        )
        remaining = self.owner.available_minutes
        plan: list[tuple[Pet, Task]] = []
        for pet, task in candidates:
            if task.duration_minutes <= remaining:
                plan.append((pet, task))
                remaining -= task.duration_minutes
        return plan

    def explain_plan(self, plan: list[tuple[Pet, Task]]) -> str:
        """Format the selected tasks as a readable daily plan."""
        if not plan:
            return "No pending tasks fit in the available time."
        lines = [f"Daily care plan for {self.owner.name}:"]
        for pet, task in plan:
            lines.append(
                f"- {pet.name}: {task.description} "
                f"({task.duration_minutes} min; {task.priority} priority)"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    owner = Owner("Jordan", available_minutes=45)
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    dog.add_task(Task("Morning walk", 20, priority="high"))
    cat.add_task(Task("Feed Luna", 10, priority="high"))
    dog.add_task(Task("Brush Mochi", 15, priority="medium"))
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    print(scheduler.explain_plan(scheduler.generate_schedule()))
