"""Demonstrate sorting and filtering tasks across multiple pets."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(tasks):
    """Print pet, time, description, and completion status for each task."""
    for pet, task in tasks:
        status = "complete" if task.completed else "pending"
        print(f"{task.time or '--:--'} | {pet.name}: {task.description} ({status})")


def main():
    """Build sample tasks out of order and demonstrate the scheduler."""
    owner = Owner("Jordan", available_minutes=50)
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    # Intentionally added out of chronological order.
    mochi.add_task(Task("Evening walk", 20, priority="high", time="18:00"))
    luna.add_task(Task("Feed Luna", 10, priority="high", time="08:00"))
    mochi.add_task(Task("Brush Mochi", 15, frequency="weekly", time="14:30"))
    play = Task("Playtime", 25, priority="low", time="10:00")
    play.mark_complete()
    luna.add_task(play)

    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    print("All tasks sorted by time")
    print("=" * 24)
    print_tasks(scheduler.sort_by_time())

    print("\nMochi's pending tasks")
    print("=" * 21)
    print_tasks(scheduler.filter_tasks(pet_name="Mochi", completed=False))

    print("\nAll completed tasks")
    print("=" * 19)
    print_tasks(scheduler.filter_tasks(completed=True))

    print("\nToday's Schedule")
    print("=" * 16)
    print(scheduler.explain_plan(scheduler.generate_schedule()))


if __name__ == "__main__":
    main()
