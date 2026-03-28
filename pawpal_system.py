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

    def next_occurrence(self) -> "Task":
        """Create a new instance of this task for the next occurrence."""
        if not self.is_recurring:
            return None
        return Task(
            name=self.name,
            task_type=self.task_type,
            duration=self.duration,
            frequency=self.frequency,
            priority=self.priority,
            scheduled_time=self.scheduled_time,  # keep original time
            is_recurring=self.is_recurring,
            completed=False
        )


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
        """Detect tasks scheduled at the same time, grouped by pet."""
        conflicts = []
        for pet in self.owner.get_pets():
            seen_times = {}
            for task in pet.get_tasks():
                if task.scheduled_time in seen_times:
                    conflicts.append(
                        f"Conflict for {pet.name}: '{task.name}' and "
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

    def sort_by_time(self) -> List[Task]:
        """Sort all tasks by scheduled time (HH:MM format)."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.scheduled_time)

    def filter_tasks(self, pet_name: str = None, 
                    completed: bool = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        filtered = []
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                if pet_name and pet.name != pet_name:
                    continue
                if completed is not None and task.completed != completed:
                    continue
                filtered.append(task)
        return filtered

    def find_next_available_slot(self, task: Task) -> str:
        """Find the next available time slot if a task has a conflict."""
        # Get all currently scheduled times
        scheduled_times = [
            t.scheduled_time 
            for t in self.owner.get_all_tasks() 
            if t != task
        ]
        
        # Generate time slots in 30 min increments
        from datetime import datetime, timedelta
        base = datetime.strptime(task.scheduled_time, "%H:%M")
        
        for i in range(1, 24):  # check up to 24 slots ahead
            candidate = base + timedelta(minutes=30 * i)
            candidate_str = candidate.strftime("%H:%M")
            if candidate_str not in scheduled_times:
                return candidate_str
        
        return task.scheduled_time  # fallback to original if no slot found


import json
from datetime import date

def save_to_json(owner: Owner, filepath: str = "data.json") -> None:
    """Save owner, pets, and tasks to a JSON file."""
    data = {
        "owner": {
            "name": owner.name,
            "email": owner.email
        },
        "pets": [
            {
                "name": pet.name,
                "species": pet.species,
                "date_of_birth": pet.date_of_birth.isoformat(),
                "medical_notes": pet.medical_notes,
                "tasks": [
                    {
                        "name": task.name,
                        "task_type": task.task_type,
                        "duration": task.duration,
                        "frequency": task.frequency,
                        "priority": task.priority,
                        "scheduled_time": task.scheduled_time,
                        "is_recurring": task.is_recurring,
                        "completed": task.completed
                    }
                    for task in pet.get_tasks()
                ]
            }
            for pet in owner.get_pets()
        ]
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_from_json(filepath: str = "data.json"):
    """Load owner, pets, and tasks from a JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None, [], []

    owner = Owner(name=data["owner"]["name"], email=data["owner"]["email"])
    pets_list = []
    tasks_list = []

    for pet_data in data["pets"]:
        pet = Pet(
            name=pet_data["name"],
            species=pet_data["species"],
            date_of_birth=date.fromisoformat(pet_data["date_of_birth"]),
            medical_notes=pet_data["medical_notes"]
        )
        for task_data in pet_data["tasks"]:
            task = Task(
                name=task_data["name"],
                task_type=task_data["task_type"],
                duration=task_data["duration"],
                frequency=task_data["frequency"],
                priority=task_data["priority"],
                scheduled_time=task_data["scheduled_time"],
                is_recurring=task_data["is_recurring"],
                completed=task_data["completed"]
            )
            pet.add_task(task)
            tasks_list.append({
                "pet": pet.name,
                "task": task.name,
                "time": task.scheduled_time,
                "duration": task.duration,
                "frequency": task.frequency,
                "priority": task.priority
            })
        owner.add_pet(pet)
        pets_list.append(pet.name)

    return owner, pets_list, tasks_list