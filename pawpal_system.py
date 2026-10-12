"""PawPal+ backend: pet care tasks and a multi-pet daily planner."""

from __future__ import annotations


class Task:
    """A care activity assigned to a pet."""

    def __init__(
        self,
        description: str,
        duration_minutes: int,
        frequency: str = "daily",
        priority: str = "medium",
        completed: bool = False,
    ) -> None:
        if not description.strip():
            raise ValueError("Task description cannot be empty.")
        if duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if priority not in {"low", "medium", "high"}:
            raise ValueError("Priority must be low, medium, or high.")
        self.description = description.strip()
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = priority
        self.completed = completed

    def mark_complete(self) -> None:
        self.completed = True

    def describe(self) -> str:
        status = "done" if self.completed else "pending"
        return (f"{self.description} ({self.duration_minutes} min, "
                f"{self.frequency}, {self.priority}, {status})")


class Pet:
    """A pet and the tasks needed to care for it."""

    def __init__(self, name: str, species: str) -> None:
        self.name = name
        self.species = species
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


class Owner:
    """An owner of one or more pets."""

    def __init__(self, name: str, available_minutes: int) -> None:
        if available_minutes < 0:
            raise ValueError("Available minutes cannot be negative.")
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs across ALL pets, preserving ownership."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Choose pending tasks across all pets within the owner's time budget."""

    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_schedule(self) -> list[tuple[Pet, Task]]:
        """Schedule pending tasks by priority, then shorter duration.

        Frequency is recorded on tasks, but this first version assumes tasks
        passed in are due today; it does not calculate recurrence dates.
        """
        candidates = [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.completed
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
