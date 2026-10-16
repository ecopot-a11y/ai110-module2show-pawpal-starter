"""Tests for the optional earliest-free-slot scheduling capability."""
from datetime import date, timedelta
import pytest
from pawpal_system import Owner, Pet, Scheduler, Task

DAY = date(2026, 10, 16)

def make_scheduler(*tasks):
    owner = Owner('Jordan', 120)
    pet = Pet('Mochi', 'dog')
    for task in tasks:
        pet.add_task(task)
    owner.add_pet(pet)
    return Scheduler(owner)

def task(name, time, minutes, **kwargs):
    return Task(name, minutes, time=time, due_date=DAY, **kwargs)

def test_empty_day_returns_window_start():
    assert make_scheduler().next_available_slot(30, DAY) == '08:00'

def test_finds_gap_between_busy_tasks():
    scheduler = make_scheduler(task('Walk', '08:00', 30), task('Feed', '09:00', 30))
    assert scheduler.next_available_slot(20, DAY) == '08:30'

def test_overlapping_tasks_are_handled():
    scheduler = make_scheduler(task('Walk', '08:00', 40), task('Feed', '08:20', 40))
    assert scheduler.next_available_slot(15, DAY) == '09:00'

def test_ignores_completed_future_and_untimed():
    scheduler = make_scheduler(task('Done', '08:00', 30, completed=True),
        Task('Tomorrow', 30, time='08:00', due_date=DAY + timedelta(days=1)),
        Task('Untimed', 20, due_date=DAY))
    assert scheduler.next_available_slot(20, DAY) == '08:00'

def test_no_room_returns_none():
    scheduler = make_scheduler(task('Long walk', '08:00', 60))
    assert scheduler.next_available_slot(20, DAY, '08:00', '09:00') is None

def test_invalid_duration_rejected():
    with pytest.raises(ValueError):
        make_scheduler().next_available_slot(0, DAY)
