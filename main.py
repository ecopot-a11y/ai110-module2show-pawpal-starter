"""Terminal demonstration of PawPal+'s multi-pet scheduling logic."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    owner = Owner("Jordan", available_minutes=50)
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(Task("Morning walk", 20, frequency="daily", priority="high"))
    luna.add_task(Task("Feed Luna", 10, frequency="daily", priority="high"))
    mochi.add_task(Task("Brush Mochi", 15, frequency="weekly", priority="medium"))
    luna.add_task(Task("Playtime", 25, frequency="daily", priority="low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    print("Today's Schedule")
    print("=" * 16)
    print(scheduler.explain_plan(scheduler.generate_schedule()))


if __name__ == "__main__":
    main()
