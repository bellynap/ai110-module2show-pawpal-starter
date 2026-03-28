from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Verify that mark_complete() changes the task's status."""
    task = Task(
        name="Walk",
        task_type="walk",
        duration=30,
        frequency=1,
        priority=1,
        scheduled_time="08:00"
    )
    assert task.is_complete() == False
    task.mark_complete()
    assert task.is_complete() == True

def test_pet_task_addition():
    """Verify that adding a task to a pet increases its task count."""
    pet = Pet(
        name="Buddy",
        species="Dog",
        date_of_birth=date(2018, 5, 10)
    )
    assert len(pet.get_tasks()) == 0
    task = Task(
        name="Feeding",
        task_type="feeding",
        duration=10,
        frequency=3,
        priority=2,
        scheduled_time="09:00"
    )
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1