from datetime import date, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task


def test_same_time_different_pets_warns():
    owner = Owner('Jordan', 60)
    dog, cat = Pet('Mochi', 'dog'), Pet('Luna', 'cat')
    dog.add_task(Task('Walk', 20, time='08:00'))
    cat.add_task(Task('Feed', 10, time='08:00'))
    owner.add_pet(dog)
    owner.add_pet(cat)
    warnings = Scheduler(owner).find_conflicts()
    assert len(warnings) == 1
    assert 'Mochi' in warnings[0] and 'Luna' in warnings[0]


def test_partial_overlap_same_pet_warns():
    owner = Owner('Jordan', 60)
    dog = Pet('Mochi', 'dog')
    dog.add_task(Task('Walk', 30, time='09:00'))
    dog.add_task(Task('Groom', 15, time='09:20'))
    owner.add_pet(dog)
    assert len(Scheduler(owner).find_conflicts()) == 1


def test_adjacent_completed_future_and_untimed_tasks_do_not_conflict():
    owner = Owner('Jordan', 60)
    dog = Pet('Mochi', 'dog')
    dog.add_task(Task('Walk', 30, time='09:00'))
    dog.add_task(Task('Feed', 10, time='09:30'))
    dog.add_task(Task('Old', 10, time='09:00', completed=True))
    dog.add_task(Task('Future', 10, time='09:00', due_date=date.today()+timedelta(days=1)))
    dog.add_task(Task('Untimed', 10))
    owner.add_pet(dog)
    assert Scheduler(owner).find_conflicts() == []
