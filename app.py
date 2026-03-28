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

# ── Step 1: Owner Setup ───────────────────────────────
st.subheader("👤 Owner Info")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@email.com")
time_available = st.number_input(
    "Time available today (minutes)", min_value=30, max_value=480, value=120
)

if st.button("Save Owner"):
    st.session_state.owner = Owner(name=owner_name, email=owner_email)
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

st.divider()

# ── Step 3: Add Tasks ─────────────────────────────────
st.subheader("📋 Add a Task")

pet_choice = st.selectbox("Assign task to pet", st.session_state.pets if st.session_state.pets else ["No pets yet"])

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
    task_type = st.selectbox("Type", ["walk", "feeding", "medication", "grooming", "other"])
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    frequency = st.number_input("Frequency (times/day)", min_value=1, max_value=10, value=1)
with col3:
    priority = st.number_input("Priority (1=highest)", min_value=1, max_value=5, value=1)
    scheduled_time = st.text_input("Scheduled time (HH:MM)", value="08:00")

if st.button("Add Task"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first!")
    elif pet_choice == "No pets yet":
        st.warning("Please add a pet first!")
    else:
        new_task = Task(
            name=task_title,
            task_type=task_type,
            duration=int(duration),
            frequency=int(frequency),
            priority=int(priority),
            scheduled_time=scheduled_time
        )
        # Find the pet and add the task
        for pet in st.session_state.owner.get_pets():
            if pet.name == pet_choice:
                pet.add_task(new_task)
                st.session_state.tasks.append({
                    "pet": pet_choice,
                    "task": task_title,
                    "time": scheduled_time,
                    "duration": duration,
                    "frequency": frequency,
                    "priority": priority
                })
                st.success(f"Task '{task_title}' added to {pet_choice}!")
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
        scheduler = Scheduler(
            owner=st.session_state.owner,
            time_available=int(time_available)
        )
        schedule = scheduler.generate_schedule()
        conflicts = scheduler.check_conflicts()

        st.markdown(f"### 🗓️ Today's Schedule for {st.session_state.owner.name}")
        if schedule:
            for task in schedule:
                st.markdown(
                    f"**[Priority {task.priority}] {task.name}** | "
                    f"⏰ {task.scheduled_time} | "
                    f"⏱️ {task.duration} mins x {task.frequency}/day | "
                    f"Type: {task.task_type}"
                )
        else:
            st.info("No tasks fit within the available time.")

        if conflicts:
            st.markdown("### ⚠️ Conflicts Detected")
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No scheduling conflicts found!")