from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_daily_recurrence():
    owner = Owner('Jordan', 60)
    pet = Pet('Mochi', 'dog')
    owner.add_pet(pet)
    original = Task('Walk', 20, frequency='daily', due_date=date(2026, 10, 12), time='08:00')
    pet.add_task(original)
    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(pet, original)
    assert original.completed
    assert next_task in pet.tasks
    assert not next_task.completed
    assert next_task is not original
    assert next_task.due_date == date(2026, 10, 13)
    assert next_task.time == '08:00'
    assert next_task not in [task for _, task in scheduler.generate_schedule(date(2026, 10, 12))]
    assert next_task in [task for _, task in scheduler.generate_schedule(date(2026, 10, 13))]
    assert scheduler.mark_task_complete(pet, original) is None
    assert len(pet.tasks) == 2


def test_weekly_recurrence():
    pet = Pet('Luna', 'cat')
    original = Task('Groom', 15, frequency='weekly', due_date=date(2026, 10, 12))
    pet.add_task(original)
    next_task = pet.mark_task_complete(original)
    assert next_task.due_date == date(2026, 10, 19)


def test_one_time_task_does_not_recur():
    pet = Pet('Luna', 'cat')
    task = Task('Vet visit', 30, frequency='once')
    pet.add_task(task)
    assert pet.mark_task_complete(task) is None
    assert len(pet.tasks) == 1
