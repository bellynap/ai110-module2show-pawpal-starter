from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Helper to create a standard task ──────────────────
def make_task(name="Walk", task_type="walk", duration=30,
              frequency=1, priority=1, scheduled_time="08:00"):
    return Task(name=name, task_type=task_type, duration=duration,
                frequency=frequency, priority=priority,
                scheduled_time=scheduled_time)

# ── Original Tests ─────────────────────────────────────
def test_task_completion():
    """Verify that mark_complete() changes the task's status."""
    task = make_task()
    assert task.is_complete() == False
    task.mark_complete()
    assert task.is_complete() == True

def test_pet_task_addition():
    """Verify that adding a task to a pet increases its task count."""
    pet = Pet(name="Buddy", species="Dog", date_of_birth=date(2018, 5, 10))
    assert len(pet.get_tasks()) == 0
    pet.add_task(make_task())
    assert len(pet.get_tasks()) == 1

# ── New Tests ──────────────────────────────────────────
def test_sort_by_time():
    """Verify tasks are returned in chronological order."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog", date_of_birth=date(2018, 5, 10))
    pet.add_task(make_task(name="Grooming", scheduled_time="11:00"))
    pet.add_task(make_task(name="Medication", scheduled_time="09:00"))
    pet.add_task(make_task(name="Walk", scheduled_time="08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, time_available=120)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times)

def test_recurring_task_next_occurrence():
    """Confirm that marking a recurring task complete creates a new instance."""
    task = make_task(name="Walk")
    task.mark_complete()
    assert task.is_complete() == True
    next_task = task.next_occurrence()
    assert next_task is not None
    assert next_task.completed == False
    assert next_task.name == "Walk"
    assert next_task.scheduled_time == "08:00"

def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times for the same pet."""
    owner = Owner(name="Alex", email="alex@email.com")
    pet = Pet(name="Buddy", species="Dog", date_of_birth=date(2018, 5, 10))
    pet.add_task(make_task(name="Walk", scheduled_time="08:00"))
    pet.add_task(make_task(name="Medication", scheduled_time="08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, time_available=120)
    conflicts = scheduler.check_conflicts()
    assert len(conflicts) > 0
    assert "Buddy" in conflicts[0]

def test_no_conflict_different_pets():
    """Verify no conflict is raised for same time across different pets."""
    owner = Owner(name="Alex", email="alex@email.com")
    dog = Pet(name="Buddy", species="Dog", date_of_birth=date(2018, 5, 10))
    cat = Pet(name="Whiskers", species="Cat", date_of_birth=date(2020, 3, 15))
    dog.add_task(make_task(name="Walk", scheduled_time="08:00"))
    cat.add_task(make_task(name="Feeding", scheduled_time="08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner=owner, time_available=120)
    conflicts = scheduler.check_conflicts()
    assert len(conflicts) == 0