import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler, save_to_json, load_from_json

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Helper Functions ───────────────────────────────────
def to_24hr(hour: int, minute: int, ampm: str) -> str:
    if ampm == "AM":
        h = 0 if hour == 12 else hour
    else:
        h = 12 if hour == 12 else hour + 12
    return f"{h:02d}:{minute:02d}"

def task_type_emoji(task_type: str) -> str:
    emojis = {
        "walk": "🦮", "feeding": "🍖", "medication": "💊",
        "grooming": "✂️", "other": "📌"
    }
    return emojis.get(task_type, "📌")

def priority_color(priority: int) -> str:
    return {1: "🔴", 2: "🟡"}.get(priority, "🟢")

def autosave():
    """Save data to JSON if owner exists."""
    if st.session_state.owner:
        save_to_json(st.session_state.owner)

# ── Session State Setup ────────────────────────────────
if "owner" not in st.session_state:
    owner, pets, tasks = load_from_json()
    st.session_state.owner = owner
    st.session_state.pets = pets
    st.session_state.tasks = tasks
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0
if "pet_name_input" not in st.session_state:
    st.session_state.pet_name_input = ""
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

# ── Tab styling ────────────────────────────────────────
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2d2d2d;
        border-radius: 8px 8px 0px 0px;
        padding: 8px 16px;
        border: 1px solid #444;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b;
        border-color: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Owner", "🐶 Pets", "📋 Tasks", "📅 Schedule"
])

# ══════════════════════════════════════════════════════
# TAB 1: OWNER
# ══════════════════════════════════════════════════════
with tab1:
    st.subheader("👤 Owner Info")
    col1, col2 = st.columns(2)
    with col1:
        owner_name = st.text_input("Name",
            value=st.session_state.owner.name if st.session_state.owner else "")
    with col2:
        owner_email = st.text_input("Email",
            value=st.session_state.owner.email if st.session_state.owner else "")
    
    time_available = st.slider(
        "Time available today (minutes)", 
        min_value=30, max_value=480, value=120, step=15
    )

    if st.button("Save Owner ➡️"):
        if owner_name == "":
            st.warning("Please enter a name!")
        else:
            st.session_state.owner = Owner(name=owner_name, email=owner_email)
            st.session_state.pets = []
            st.session_state.tasks = []
            autosave()
            st.success("✅ Owner saved! Head to the 🐶 **Pets** tab next.")
            st.balloons()

    if st.session_state.owner:
        st.info(f"Current owner: **{st.session_state.owner.name}** | "
                f"⏱️ {time_available} mins available today")

# ══════════════════════════════════════════════════════
# TAB 2: PETS
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("🐶 Manage Pets")
    
    if st.session_state.owner is None:
        st.warning("Please save an owner first in the Owner tab!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            pet_name = st.text_input("Pet name",
                value=st.session_state.pet_name_input,
                key="pet_input")
            species = st.selectbox("Species", ["dog", "cat", "other"])
        with col2:
            dob = st.date_input("Date of birth", value=date(2020, 1, 1))
            medical_notes = st.text_input("Medical notes (optional)")

        if st.button("Add Pet"):
            if pet_name in st.session_state.pets:
                st.warning(f"'{pet_name}' already exists!")
            elif pet_name == "":
                st.warning("Please enter a pet name!")
            else:
                new_pet = Pet(name=pet_name, species=species,
                             date_of_birth=dob, medical_notes=medical_notes)
                st.session_state.owner.add_pet(new_pet)
                st.session_state.pets.append(pet_name)
                st.session_state.pet_name_input = ""
                autosave()
                st.success(f"✅ '{pet_name}' added! Add another or go to 📋 **Tasks**.")

        if st.session_state.pets:
            st.divider()
            st.markdown("**Current Pets:**")
            for pet in st.session_state.owner.get_pets():
                col_name, col_age, col_notes = st.columns([2, 1, 2])
                with col_name:
                    st.markdown(f"🐾 **{pet.name}** ({pet.species})")
                with col_age:
                    st.markdown(f"Age: {pet.get_age()}")
                with col_notes:
                    st.markdown(f"📝 {pet.medical_notes or 'No notes'}")

            st.divider()
            pet_to_delete = st.selectbox("Remove a pet",
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
                autosave()
                st.success(f"Removed {pet_to_delete}!")

# ══════════════════════════════════════════════════════
# TAB 3: TASKS
# ══════════════════════════════════════════════════════
with tab3:
    st.subheader("📋 Add a Task")

    if not st.session_state.pets:
        st.warning("Please add a pet first in the Pets tab!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            pet_choice = st.selectbox("Assign to pet", st.session_state.pets)
            task_type = st.selectbox(
                "Task type", ["walk", "feeding", "medication", "grooming", "other"]
            )
            task_title = st.text_input(
                "Custom name (optional)",
                placeholder="Leave blank to use task type"
            )
            if not task_title:
                task_title = task_type.capitalize()
        with col2:
            duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
            frequency = st.number_input("Frequency (times/day)", min_value=1, max_value=10, value=1)
            priority = st.number_input("Priority (1=highest)", min_value=1, max_value=5, value=1)

        st.write("⏰ Scheduled time(s)")
        scheduled_times = []
        for i in range(int(frequency)):
            st.caption(f"Occurrence {i + 1}")
            tcol1, tcol2, tcol3 = st.columns(3)
            with tcol1:
                t_hour = st.selectbox("Hour", list(range(1, 13)),
                                      index=7, key=f"hour_{i}")
            with tcol2:
                t_minute = st.selectbox("Minute", [0, 15, 30, 45],
                    format_func=lambda x: f"{x:02d}", key=f"minute_{i}")
            with tcol3:
                t_ampm = st.selectbox("AM/PM", ["AM", "PM"], key=f"ampm_{i}")
            scheduled_times.append(to_24hr(t_hour, t_minute, t_ampm))
            st.caption(f"⏰ {scheduled_times[-1]}")

        if st.button("Add Task"):
            for pet in st.session_state.owner.get_pets():
                if pet.name == pet_choice:
                    for i, t in enumerate(scheduled_times):
                        name = task_title if len(scheduled_times) == 1 \
                               else f"{task_title} ({i + 1})"
                        new_task = Task(name=name, task_type=task_type,
                                       duration=int(duration), frequency=1,
                                       priority=int(priority), scheduled_time=t)
                        pet.add_task(new_task)
                        st.session_state.tasks.append({
                            "pet": pet_choice, "task": name,
                            "time": t, "duration": duration,
                            "frequency": 1, "priority": priority
                        })
                    autosave()
                    st.success(f"Added {len(scheduled_times)} occurrence(s) of "
                              f"'{task_title}' to {pet_choice}!")
                    break

        if st.session_state.tasks:
            st.divider()
            st.markdown("**Current Tasks:**")
            st.table(st.session_state.tasks)

# ══════════════════════════════════════════════════════
# TAB 4: SCHEDULE
# ══════════════════════════════════════════════════════
with tab4:
    st.subheader("📅 Generate Schedule")

    if st.session_state.owner is None:
        st.warning("Please set up your owner and pets first!")
    elif not st.session_state.tasks:
        st.warning("Please add some tasks first!")
    else:
        time_available_schedule = st.slider(
            "Adjust available time (minutes)",
            min_value=30, max_value=480, value=120, step=15
        )

        if st.button("Generate Schedule"):
            st.session_state.schedule_generated = True

        if st.session_state.schedule_generated:
            scheduler = Scheduler(
                owner=st.session_state.owner,
                time_available=int(time_available_schedule)
            )

            conflicts = scheduler.check_conflicts()
            if conflicts:
                st.markdown("### ⚠️ Scheduling Conflicts")
                for conflict in conflicts:
                    st.warning(conflict)
                
                st.markdown("### 🔄 Suggested Resolutions")
                for pet in st.session_state.owner.get_pets():
                    seen_times = {}
                    for task in pet.get_tasks():
                        if task.scheduled_time in seen_times:
                            next_slot = scheduler.find_next_available_slot(task)
                            st.info(
                                f"💡 **{task.name}** for {pet.name} conflicts at "
                                f"{task.scheduled_time}. "
                                f"Suggested next available slot: **{next_slot}**"
                            )
                        else:
                            seen_times[task.scheduled_time] = task.name
            else:
                st.success("✅ No scheduling conflicts found!")

            st.markdown(
                f"### 🗓️ Today's Schedule for {st.session_state.owner.name}"
            )
            schedule = scheduler.generate_schedule()
            if schedule:
                for pet in st.session_state.owner.get_pets():
                    for task in pet.get_tasks():
                        if task in schedule:
                            st.markdown(
                                f"{priority_color(task.priority)} "
                                f"{task_type_emoji(task.task_type)} "
                                f"**{task.name}** | 🐾 {pet.name} | "
                                f"⏰ {task.scheduled_time} | "
                                f"⏱️ {task.duration} mins x {task.frequency}/day"
                            )
            else:
                st.info("No tasks fit within the available time.")

            st.markdown("### ⏰ Tasks Sorted by Time")
            st.caption("Check off tasks as you complete them!")
            sorted_tasks = scheduler.sort_by_time()

            if sorted_tasks:
                for pet in st.session_state.owner.get_pets():
                    for task in pet.get_tasks():
                        if task in sorted_tasks:
                            col_check, col_info = st.columns([1, 9])
                            with col_check:
                                done = st.checkbox("", value=task.completed,
                                    key=f"cb_{pet.name}_{task.name}_{task.scheduled_time}")
                            with col_info:
                                strike = "~~" if done else ""
                                st.markdown(
                                    f"{strike}{priority_color(task.priority)} "
                                    f"**{task.scheduled_time}** | 🐾 {pet.name} | "
                                    f"{task_type_emoji(task.task_type)} {task.name} | "
                                    f"{task.duration} mins x {task.frequency}/day{strike}"
                                )
                            if done and not task.completed:
                                task.mark_complete()
                                next_task = task.next_occurrence()
                                if next_task:
                                    pet.add_task(next_task)
                                    st.session_state.tasks.append({
                                        "pet": pet.name, "task": next_task.name,
                                        "time": next_task.scheduled_time,
                                        "duration": next_task.duration,
                                        "frequency": next_task.frequency,
                                        "priority": next_task.priority
                                    })
                                    st.success(f"✅ '{task.name}' complete! "
                                              f"Next at {next_task.scheduled_time}")

            st.markdown("### 📋 Sorted Task Table")
            table_data = []
            for pet in st.session_state.owner.get_pets():
                for task in pet.get_tasks():
                    if task in sorted_tasks:
                        table_data.append({
                            "Priority": f"{priority_color(task.priority)} {task.priority}",
                            "Type": f"{task_type_emoji(task.task_type)} {task.task_type}",
                            "Task": task.name, "Pet": f"🐾 {pet.name}",
                            "Time": task.scheduled_time,
                            "Duration": f"{task.duration} mins",
                            "Frequency": f"{task.frequency}x/day"
                        })
            table_data.sort(key=lambda x: x["Time"])
            st.table(table_data)

            incomplete = scheduler.filter_tasks(completed=False)
            st.markdown(f"### 📋 Incomplete Tasks: {len(incomplete)}")
            for pet in st.session_state.owner.get_pets():
                for task in pet.get_tasks():
                    if not task.completed:
                        st.markdown(f"- **{pet.name}**: {task.name} "
                                   f"at {task.scheduled_time}")
    
    st.divider()
    if st.button("🗑️ Clear All Data"):
        st.session_state.owner = None
        st.session_state.pets = []
        st.session_state.tasks = []
        st.session_state.schedule_generated = False
        import os
        if os.path.exists("data.json"):
            os.remove("data.json")
        st.success("Data cleared!")