import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session State Setup ────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ── Helper: Convert 12hr to 24hr ──────────────────────
def to_24hr(hour: int, minute: int, ampm: str) -> str:
    if ampm == "AM":
        h = 0 if hour == 12 else hour
    else:
        h = 12 if hour == 12 else hour + 12
    return f"{h:02d}:{minute:02d}"

# ── Step 1: Owner Setup ───────────────────────────────
st.subheader("👤 Owner Info")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@email.com")
time_available = st.number_input(
    "Time available today (minutes)", min_value=30, max_value=480, value=120
)

if st.button("Save Owner"):
    st.session_state.owner = Owner(name=owner_name, email=owner_email)
    st.session_state.pets = []
    st.session_state.tasks = []
    st.success(f"Owner '{owner_name}' saved!")

st.divider()

# ── Step 2: Add a Pet ─────────────────────────────────
st.subheader("🐶 Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
dob = st.date_input("Date of birth", value=date(2020, 1, 1))
medical_notes = st.text_input("Medical notes (optional)", value="")

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first!")
    elif pet_name in st.session_state.pets:
        st.warning(f"A pet named '{pet_name}' already exists!")
    else:
        new_pet = Pet(
            name=pet_name,
            species=species,
            date_of_birth=dob,
            medical_notes=medical_notes
        )
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pets.append(pet_name)
        st.success(f"Pet '{pet_name}' added! Age: {new_pet.get_age()} years")

if st.session_state.pets:
    st.write("Current pets:", ", ".join(st.session_state.pets))
    pet_to_delete = st.selectbox("Select a pet to remove",
                                  ["None"] + st.session_state.pets)
    if st.button("Remove Pet") and pet_to_delete != "None":
        st.session_state.owner.pets = [
            p for p in st.session_state.owner.get_pets()
            if p.name != pet_to_delete
        ]
        st.session_state.pets.remove(pet_to_delete)
        st.session_state.tasks = [
            t for t in st.session_state.tasks
            if t["pet"] != pet_to_delete
        ]
        st.success(f"Removed {pet_to_delete}!")

st.divider()

# ── Step 3: Add Tasks ─────────────────────────────────
st.subheader("📋 Add a Task")

pet_choice = st.selectbox(
    "Assign task to pet",
    st.session_state.pets if st.session_state.pets else ["No pets yet"]
)

col1, col2, col3 = st.columns(3)
with col1:
    task_type = st.selectbox(
        "Task type", ["walk", "feeding", "medication", "grooming", "other"]
    )
    task_title = st.text_input(
        "Custom name (optional)",
        placeholder=f"Leave blank to use '{task_type}'"
    )
    if not task_title:
        task_title = task_type.capitalize()
with col2:
    duration = st.number_input(
        "Duration (minutes)", min_value=1, max_value=240, value=20
    )
    frequency = st.number_input(
        "Frequency (times/day)", min_value=1, max_value=10, value=1
    )
with col3:
    priority = st.number_input(
        "Priority (1=highest)", min_value=1, max_value=5, value=1
    )

# ── Time Picker (one per frequency) ───────────────────
st.write("⏰ Scheduled times")
scheduled_times = []
for i in range(int(frequency)):
    st.caption(f"Occurrence {i + 1}")
    tcol1, tcol2, tcol3 = st.columns(3)
    with tcol1:
        t_hour = st.selectbox(
            "Hour", list(range(1, 13)),
            index=7, key=f"hour_{i}"
        )
    with tcol2:
        t_minute = st.selectbox(
            "Minute", [0, 15, 30, 45],
            format_func=lambda x: f"{x:02d}",
            key=f"minute_{i}"
        )
    with tcol3:
        t_ampm = st.selectbox(
            "AM / PM", ["AM", "PM"],
            key=f"ampm_{i}"
        )
    scheduled_times.append(to_24hr(t_hour, t_minute, t_ampm))
    st.caption(f"⏰ {scheduled_times[-1]}")

# Use first time as primary, store all times
scheduled_time = scheduled_times[0]

if st.button("Add Task"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first!")
    elif pet_choice == "No pets yet":
        st.warning("Please add a pet first!")
    else:
        for pet in st.session_state.owner.get_pets():
            if pet.name == pet_choice:
                for i, t in enumerate(scheduled_times):
                    new_task = Task(
                        name=f"{task_title}" if len(scheduled_times) == 1
                             else f"{task_title} ({i + 1})",
                        task_type=task_type,
                        duration=int(duration),
                        frequency=1,  # each slot is its own occurrence
                        priority=int(priority),
                        scheduled_time=t
                    )
                    pet.add_task(new_task)
                    st.session_state.tasks.append({
                        "pet": pet_choice,
                        "task": new_task.name,
                        "time": t,
                        "duration": duration,
                        "frequency": 1,
                        "priority": priority
                    })
                st.success(
                    f"Added {len(scheduled_times)} occurrence(s) of "
                    f"'{task_title}' to {pet_choice}!"
                )
                break

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)

st.divider()

# ── Step 4: Generate Schedule ─────────────────────────
st.subheader("📅 Generate Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first!")
    elif not st.session_state.tasks:
        st.warning("Please add some tasks first!")
    else:
        st.session_state.schedule_generated = True

if st.session_state.get("schedule_generated") and st.session_state.owner:
    scheduler = Scheduler(
        owner=st.session_state.owner,
        time_available=int(time_available)
    )

    # ── Conflicts ─────────────────────────────────
    conflicts = scheduler.check_conflicts()
    if conflicts:
        st.markdown("### ⚠️ Scheduling Conflicts")
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("✅ No scheduling conflicts found!")

    # ── Priority Schedule ──────────────────────────
    st.markdown(
        f"### 🗓️ Today's Schedule for {st.session_state.owner.name}"
    )
    schedule = scheduler.generate_schedule()
    if schedule:
        for pet in st.session_state.owner.get_pets():
            for task in pet.get_tasks():
                if task in schedule:
                    st.markdown(
                        f"**[Priority {task.priority}] {task.name}** | "
                        f"🐾 {pet.name} | "
                        f"⏰ {task.scheduled_time} | "
                        f"⏱️ {task.duration} mins x "
                        f"{task.frequency}/day | "
                        f"Type: {task.task_type}"
                    )
    else:
        st.info("No tasks fit within the available time.")

    # ── Tasks Sorted by Time with Checkboxes ───────
    st.markdown("### ⏰ Tasks Sorted by Time")
    st.caption("Check off tasks as you complete them!")
    sorted_tasks = scheduler.sort_by_time()

    if sorted_tasks:
        for pet in st.session_state.owner.get_pets():
            for task in pet.get_tasks():
                if task in sorted_tasks:
                    col_check, col_info = st.columns([1, 9])
                    with col_check:
                        done = st.checkbox(
                            "",
                            value=task.completed,
                            key=f"cb_{pet.name}_{task.name}_{task.scheduled_time}"
                        )
                    with col_info:
                        strike = "~~" if done else ""
                        st.markdown(
                            f"{strike}**{task.scheduled_time}** | "
                            f"🐾 {pet.name} | "
                            f"{task.name} | "
                            f"{task.duration} mins x {task.frequency}/day | "
                            f"Type: {task.task_type}{strike}"
                        )
                    if done and not task.completed:
                        task.mark_complete()
                        next_task = task.next_occurrence()
                        if next_task:
                            pet.add_task(next_task)
                            st.session_state.tasks.append({
                                "pet": pet.name,
                                "task": next_task.name,
                                "time": next_task.scheduled_time,
                                "duration": next_task.duration,
                                "frequency": next_task.frequency,
                                "priority": next_task.priority
                            })
                            st.success(
                                f"✅ '{task.name}' complete! "
                                f"Next occurrence at {next_task.scheduled_time}"
                            )

    # ── Incomplete Tasks ───────────────────────────
    incomplete = scheduler.filter_tasks(completed=False)
    st.markdown(f"### 📋 Incomplete Tasks: {len(incomplete)}")
    for pet in st.session_state.owner.get_pets():
        for task in pet.get_tasks():
            if not task.completed:
                st.markdown(
                    f"- **{pet.name}**: {task.name} "
                    f"at {task.scheduled_time}"
                )