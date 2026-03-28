# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
A user should be able to 1) add thier pet's basic info, 2) create and manage care tasks with priorities, and 3) generate a daily care plan based on those tasks. So I would have four classes.

- What classes did you include, and what responsibilities did you assign to each?

Thinking through it, I initally decided on 
Owner : Represesnts the app user. Holds : name, email, pets[] 
Can also add and retrive pets.

Pet: Represents the animal being cared for. Holds: name, species, age
Can add and retrieve tasks.

Task: Represents a single care activity like a walk, feeding, or medication. Holds: name, duration, frequency, priority, task_type

Scheduler: Is the brain of the app. Takes the owner's avaialable time and organizes tasks by priority, detects conflicts, and generates a daily care plan : tasks, owner, time_available

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, as I thought through different scenarios and edge cases, I thought it would be good to add a pet DOB so the program automatically updates the pet's age. The pet might also have temporary medical issues so a medical notes section which also made me think, what if the pet has to take medication but only for a week. This led me to add a scheduled_time and and is_recurring into the Task class. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?


My scheduler considers the following constraints:
- Time available: the owner sets how many minutes they have in a day.
  Tasks are only added to the schedule if they fit within that time.
- Priority: tasks are sorted by priority number (1 = most important)
  so critical tasks like medication are always scheduled first.
- Duration and frequency: total time per task is calculated as 
  duration x frequency, so a task done 3 times a day costs more 
  time than one done once.

I decided time and priority mattered most because a pet owner with 
limited time needs to know which tasks absolutely cannot be skipped.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?


One tradeoff my scheduler makes is that it drops lower-priority tasks 
completely if the owner doesn't have enough time, rather than 
shortening them to fit.

For example, a grooming session might get skipped entirely even if 
the owner had 10 minutes left but the task needed 20 minutes. A 
shorter grooming session would still be better than none at all.

This tradeoff is reasonable because it keeps the scheduling logic 
simple and predictable — the owner always knows exactly how long 
each task will take. However, a future improvement could be to allow 
"flexible" tasks like walks and grooming to be shortened when time 
is tight, while keeping "fixed" tasks like medication and feeding 
at their full duration.

Interestingly, the scheduler does not stop after skipping a task — 
it keeps checking remaining tasks, so a smaller lower-priority task 
could still be scheduled after a larger one gets skipped.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI (Claude) throughout this project for:
- Brainstorming the initial class design and catching edge cases 
  I hadn't considered, like using date_of_birth instead of age
- Generating the Mermaid.js UML diagram from our design discussion
- Writing the skeleton and full implementation code for all classes
- Building and connecting the Streamlit UI to the backend

The most helpful prompts were ones where I described a specific 
problem, like how the Scheduler should retrieve tasks from the 
Owner's pets, and got targeted solutions in return.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

**b. Judgment and verification**

During the design phase, AI suggested using `age` as an attribute 
for the Pet class. I questioned this because a hardcoded age would 
need to be manually updated every year. Instead I suggested using 
`date_of_birth` so the age could be calculated automatically using 
`get_age()`.

I also pushed back on the tradeoff explanation when AI used 
medication as an example of a task that might get skipped. I 
recognized that medication is priority 1 and would never be dropped 
by the scheduler, so the example was logically flawed. I asked AI 
to verify the actual code before writing the reflection, which 
confirmed the real tradeoff involved lower-priority tasks like 
grooming instead.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?


I tested two core behaviors:
- Task completion: verified that calling mark_complete() actually 
  changes the task's completed status from False to True.
- Task addition: verified that adding a task to a pet correctly 
  increases that pet's task count.

These tests were important because they confirm the most fundamental 
actions in the app — if marking tasks complete or adding them to pets 
doesn't work, nothing else in the scheduler will work correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?


I am fairly confident the scheduler works for standard cases. 
However, edge cases I would test next include:
- What happens if an owner has no pets or no tasks?
- What if two tasks have the same priority?
- What if the owner's available time is 0?
- What if a task duration is longer than the total time available?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?


I am most satisfied with the conflict detection logic. It correctly 
identifies when two tasks for the same pet overlap in time and 
clearly communicates which tasks are conflicting and at what time.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?


I would improve the conflict detection to flag cross-pet scheduling 
clashes, since the owner still only has two hands regardless of 
which pet needs attention. I would also add the ability to shorten 
flexible tasks like walks instead of skipping them entirely.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


The most important thing I learned is that AI is a great thinking 
partner but not a replacement for critical thinking. Several times 
during this project I caught logical flaws in AI suggestions — like 
using medication as an example of a task that might get skipped, 
when medication is actually the highest priority. Verifying AI 
suggestions against the actual code before accepting them was 
essential.
