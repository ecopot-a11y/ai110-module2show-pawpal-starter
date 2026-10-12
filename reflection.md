# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
For my initial PawPal+ system design, I chose four main classes: Owner, Pet, CareTask, and Scheduler. I wanted to keep the design simple while ensuring that the application could help pet owners organize daily care activities.

The Owner class stores the owner's name, available time, and list of pets. Its add_pet() method allows the owner to register pets in the system. The Pet class stores the pet's name, species, and associated care tasks. Its add_task() method allows activities such as walking, feeding, grooming, and medication to be assigned to a pet.

The CareTask class represents individual pet care activities. It stores the task's title, estimated duration, and priority. Its describe() method is intended to provide information about the task.

Finally, the Scheduler class is responsible for organizing tasks into a daily care plan. It stores the owner's available time and includes generate_schedule() and explain_plan() methods. These methods will eventually select appropriate tasks based on available time and priority and explain the scheduling decisions.

My UML diagram shows that one owner can have multiple pets, each pet can have multiple care tasks, and the scheduler uses those tasks to create a daily plan.

**b. Design changes**

After reviewing my initial UML diagram and the class skeletons in pawpal_system.py, I identified a few areas that might need improvement as the project develops.

One potential issue is the relationship between the Pet and Scheduler classes. Although each pet maintains a list of care tasks, the scheduler needs a reliable way to access the tasks associated with the correct pet. Without this connection, it could become difficult to generate accurate schedules for owners with multiple pets.

Another consideration is that the CareTask class currently stores duration and priority but does not include preferred scheduling times or recurring task information. These additional attributes could eventually help the system handle activities such as morning walks or medications that must occur at specific times.

I also recognized that the Scheduler class will need to handle situations where the total duration of requested tasks exceeds the owner's available time. The scheduling logic should prioritize important activities and explain why certain tasks could not be included.

For now, I decided to keep the original four-class structure rather than introduce additional classes or unnecessary complexity. I have identified these possible improvements for the implementation phase, but I have not yet changed the class skeletons. This approach allows me to develop and test the basic scheduling functionality before deciding whether the design needs further modifications.

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

I used pytest to create two automated tests for my PawPal+ application. The first test verified that calling `mark_complete()` changes a task's completion status from False to True. The second test verified that adding a task to a pet increases the number of tasks associated with that pet. Both tests passed successfully using Python 3.13.7 and pytest 9.1.1, with a total execution time of 0.18 seconds. These results confirmed that the basic task management functionality was working as expected.

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
