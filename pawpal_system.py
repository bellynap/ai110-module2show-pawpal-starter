from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

# ── Task ──────────────────────────────────────────────
@dataclass
class Task:
    name: str
    task_type: str
    duration: int          # in minutes
    frequency: int         # times per day
    priority: int          # 1 = highest
    scheduled_time: str    # e.g. "08:00"
    is_recurring: bool = True
    completed: bool = False

    def is_complete(self) -> bool:
        """Check if the task is completed."""
        return self.completed

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


# ── Pet ───────────────────────────────────────────────
@dataclass
class Pet:
    name: str
    species: str
    date_of_birth: date
    medical_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def get_age(self) -> int:
        """Calculate age from date of birth."""
        today = date.today()
        return today.year - self.date_of_birth.year

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


# ── Owner ─────────────────────────────────────────────
class Owner:
    def __init__(self, name: str, email: str):
        """Initialize an owner with a name, email, and empty pet list."""
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


# ── Scheduler ─────────────────────────────────────────
class Scheduler:
    def __init__(self, owner: Owner, time_available: int):
        """Initialize scheduler with an owner and available time in minutes."""
        self.owner = owner
        self.time_available = time_available
        self.tasks: List[Task] = []

    def prioritize_tasks(self) -> List[Task]:
        """Sort all tasks by priority (1 = highest)."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.priority)

    def check_conflicts(self) -> List[str]:
        """Detect tasks scheduled at the same time."""
        conflicts = []
        seen_times = {}
        for task in self.owner.get_all_tasks():
            if task.scheduled_time in seen_times:
                conflicts.append(
                    f"Conflict: '{task.name}' and "
                    f"'{seen_times[task.scheduled_time]}' "
                    f"are both scheduled at {task.scheduled_time}"
                )
            else:
                seen_times[task.scheduled_time] = task.name
        return conflicts

    def generate_schedule(self) -> List[Task]:
        """Generate a daily schedule based on priority and available time."""
        prioritized = self.prioritize_tasks()
        schedule = []
        time_used = 0
        for task in prioritized:
            total_time = task.duration * task.frequency
            if time_used + total_time <= self.time_available:
                schedule.append(task)
                time_used += total_time
        return schedule