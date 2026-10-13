"""Basic tests for PawPal+ task and pet behavior."""

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task("Morning walk", 20, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "dog")
    task = Task("Feeding", 10)
    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task

def test_sorting_correctness():
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Evening walk", 20, time="18:00"))
    pet.add_task(Task("Breakfast", 10, time="08:00"))
    pet.add_task(Task("Lunch", 10, time="12:00"))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()

    descriptions = [task.description for pet, task in sorted_tasks]

    assert descriptions == [
        "Breakfast",
        "Lunch",
        "Evening walk",
    ]