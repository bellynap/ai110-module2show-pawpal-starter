from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Create Owner ──────────────────────────────────────
owner = Owner(name="Alex", email="alex@email.com")

# ── Create Pets ───────────────────────────────────────
dog = Pet(
    name="Buddy",
    species="Dog",
    date_of_birth=date(2018, 5, 10),
    medical_notes="Allergic to chicken"
)

cat = Pet(
    name="Whiskers",
    species="Cat",
    date_of_birth=date(2020, 3, 15),
    medical_notes=""
)

# ── Create Tasks ──────────────────────────────────────
walk = Task(
    name="Morning Walk",
    task_type="walk",
    duration=30,
    frequency=2,
    priority=1,
    scheduled_time="08:00"
)

feeding = Task(
    name="Feeding",
    task_type="feeding",
    duration=10,
    frequency=3,
    priority=2,
    scheduled_time="08:00"  # intentional conflict for testing!
)

medication = Task(
    name="Medication",
    task_type="medication",
    duration=5,
    frequency=1,
    priority=1,
    scheduled_time="09:00"
)

grooming = Task(
    name="Grooming",
    task_type="grooming",
    duration=20,
    frequency=1,
    priority=3,
    scheduled_time="11:00"
)

# ── Assign Tasks to Pets ──────────────────────────────
dog.add_task(walk)
dog.add_task(medication)
cat.add_task(feeding)
cat.add_task(grooming)

# ── Assign Pets to Owner ──────────────────────────────
owner.add_pet(dog)
owner.add_pet(cat)

# ── Run Scheduler ─────────────────────────────────────
scheduler = Scheduler(owner=owner, time_available=120)

print("\n🐾 PawPal+ Daily Schedule")
print("=" * 35)

schedule = scheduler.generate_schedule()
for task in schedule:
    print(f"[Priority {task.priority}] {task.name} "
          f"| {task.scheduled_time} "
          f"| {task.duration} mins x {task.frequency}/day "
          f"| Type: {task.task_type}")

print("\n⚠️  Conflict Check")
print("=" * 35)
conflicts = scheduler.check_conflicts()
if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found!")

print("\n🐶 Buddy's Age:", dog.get_age(), "years")
print("🐱 Whiskers' Age:", cat.get_age(), "years")