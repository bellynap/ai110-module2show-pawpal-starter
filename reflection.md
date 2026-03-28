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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
