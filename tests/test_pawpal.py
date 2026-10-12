"""Basic tests for PawPal+ task and pet behavior."""

from pawpal_system import Pet, Task


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