# Assignment 1 – Data Structure Learning Tool

## Complete 7-Day Submission Plan

**Project:** Data Structure Learning Tool
**Repository Name:** `dsa-learning-tool`
**Submission Goal:** Complete all required assignment deliverables within 7 days
**Post-Submission Goal:** Continue the same repository as a mini portfolio project
**Primary Language:** Python
**User Interface:** Streamlit
**Testing:** pytest
**Charts:** Matplotlib
**Performance Timing:** `time.perf_counter_ns()`
**Version Control:** Git + GitHub

---

# 1. Assignment Requirements

The completed submission must include:

1. Stack implementation
2. Queue implementation
3. Linked List implementation
4. User interface demonstrating each data structure
5. Complexity analyzer for common operations
6. Visual demonstrations showing appropriate use cases
7. Performance testing
8. Predicted versus actual performance comparison
9. Performance charts
10. One-page analysis
11. Clear code documentation
12. 3–5 minute demo video

---

# 2. Submission Strategy

The project will be developed as:

**Version 1.0 – Assignment Submission**

The first goal is not to build every possible data-structure feature.

The first goal is:

> Complete every instructor requirement correctly, test the application, prepare documentation, and submit a stable Version 1.0.

After submission:

**Version 1.1+ – Mini Project Development**

Additional algorithms, structures, testing, CI/CD, better visualization, and portfolio features can then be added without affecting the submitted assignment.

---

# 3. Final Project Structure

```text
dsa-learning-tool/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   │
│   ├── structures/
│   │   ├── __init__.py
│   │   ├── stack.py
│   │   ├── queue.py
│   │   └── linked_list.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── complexity_analyzer.py
│   │
│   ├── benchmark/
│   │   ├── __init__.py
│   │   └── performance_tester.py
│   │
│   └── visualization/
│       ├── __init__.py
│       └── visualizer.py
│
├── tests/
│   ├── test_stack.py
│   ├── test_queue.py
│   ├── test_linked_list.py
│   └── test_complexity.py
│
├── data/
│   └── benchmark_results.csv
│
├── images/
│   ├── performance_chart.png
│   └── complexity_comparison.png
│
├── reports/
│   ├── performance_report.md
│   └── data_structure_analysis.md
│
└── docs/
    ├── requirements.md
    ├── test_plan.md
    └── demo_script.md
```

---

# 4. Day 1 – Project Foundation

## Major Objective

Create the complete project foundation before programming the data structures.

## Tasks

### Task 1 – Create GitHub Repository

Repository:

```text
dsa-learning-tool
```

Add:

```text
README.md
.gitignore
requirements.txt
```

---

### Task 2 – Create Local Project

Create the project folder and virtual environment.

Example:

```text
dsa-learning-tool/
```

---

### Task 3 – Create Directory Structure

Create:

```text
src/
tests/
docs/
reports/
data/
images/
```

Then create the structure and package folders.

---

### Task 4 – Define Requirements

Create:

```text
docs/requirements.md
```

Document:

* Stack requirements
* Queue requirements
* Linked List requirements
* UI requirements
* Complexity analyzer requirements
* Benchmark requirements
* Reporting requirements

---

### Task 5 – Define Operations

#### Stack

```text
push
pop
peek
search
is_empty
```

#### Queue

```text
enqueue
dequeue
peek
search
is_empty
```

#### Linked List

```text
insert
delete
search
traverse
is_empty
```

---

### Task 6 – Install Dependencies

Initial packages:

```text
streamlit
pytest
matplotlib
pandas
```

---

### Task 7 – Prepare README Skeleton

Sections:

```text
Overview
Features
Technology
Installation
Usage
Project Structure
Testing
Performance Analysis
```

---

## Day 1 Git Commit

```text
chore: initialize data structure learning tool project
```

---

## Day 1 Completion Check

```text
□ Repository created
□ Project folders created
□ Virtual environment working
□ Dependencies installed
□ requirements.txt created
□ requirements.md created
□ README started
□ First Git push completed
```

---

# 5. Day 2 – Stack and Queue

## Major Objective

Complete two of the three required data structures.

---

# Part A – Stack

Create:

```text
src/structures/stack.py
```

Implement:

```text
Stack
push()
pop()
peek()
search()
is_empty()
size()
```

### Stack Concept

```text
TOP
 ↓
[30]
[20]
[10]
```

### Expected Complexity

| Operation | Complexity     |
| --------- | -------------- |
| Push      | O(1) amortized |
| Pop       | O(1)           |
| Peek      | O(1)           |
| Search    | O(n)           |

---

# Part B – Queue

Create:

```text
src/structures/queue.py
```

Implement:

```text
Queue
enqueue()
dequeue()
peek()
search()
is_empty()
size()
```

### Queue Concept

```text
FRONT                      REAR
 ↓                           ↓
[10] → [20] → [30] → [40]
```

### Expected Complexity

| Operation | Complexity |
| --------- | ---------- |
| Enqueue   | O(1)       |
| Dequeue   | O(1)       |
| Peek      | O(1)       |
| Search    | O(n)       |

---

## Documentation

Each method should contain a short docstring explaining:

```text
Purpose
Parameters
Return value
Errors
Expected complexity
```

---

## Day 2 Git Commits

```text
feat: implement stack data structure
```

```text
feat: implement queue data structure
```

---

## Day 2 Completion Check

```text
□ Stack push works
□ Stack pop works
□ Stack peek works
□ Stack search works

□ Queue enqueue works
□ Queue dequeue works
□ Queue peek works
□ Queue search works

□ Empty structure errors handled
□ Docstrings added
□ Code pushed to GitHub
```

---

# 6. Day 3 – Linked List and Unit Tests

## Major Objective

Complete the third required structure and verify all core implementations.

---

# Part A – Node

Create:

```text
Node
```

Attributes:

```text
data
next
```

---

# Part B – Linked List

Create:

```text
src/structures/linked_list.py
```

Implement:

```text
insert()
delete()
search()
traverse()
is_empty()
size()
```

### Visualization Concept

```text
HEAD
 ↓
[10|•] → [20|•] → [30|•] → None
```

---

## Expected Complexity

| Operation       | Complexity |
| --------------- | ---------- |
| Insert at Head  | O(1)       |
| Search          | O(n)       |
| Delete by Value | O(n)       |
| Traverse        | O(n)       |

---

# Part C – Unit Testing

Create:

```text
tests/test_stack.py
tests/test_queue.py
tests/test_linked_list.py
```

Test:

```text
Normal operations
Empty structures
Single-element structures
Duplicate values
Search success
Search failure
Delete missing values
Repeated operations
```

---

## Day 3 Git Commits

```text
feat: implement linked list data structure
```

```text
test: add unit tests for core data structures
```

---

## Day 3 Quality Gate

Do not move forward until:

```text
□ Stack tests pass
□ Queue tests pass
□ Linked List tests pass
□ Empty cases work
□ No major exceptions remain
□ All code pushed
```

---

# 7. Day 4 – User Interface and Visual Demonstrations

## Major Objective

Create the required interactive interface.

---

# Technology

Use:

```text
Streamlit
```

Main entry file:

```text
app.py
```

---

# Navigation

Create:

```text
Home
Stack
Queue
Linked List
Complexity Analyzer
Performance
About
```

---

# Stack UI

Controls:

```text
Enter value
Push
Pop
Peek
Search
Reset
```

Display:

```text
TOP
 ↓
┌─────┐
│ 30  │
├─────┤
│ 20  │
├─────┤
│ 10  │
└─────┘
```

Include:

**When to Use**

Examples:

* Undo functionality
* Browser navigation
* Function calls
* Expression evaluation

---

# Queue UI

Controls:

```text
Enter value
Enqueue
Dequeue
Peek
Search
Reset
```

Display:

```text
FRONT                       REAR
 ↓                            ↓
[10] → [20] → [30] → [40]
```

Use cases:

* Job scheduling
* Print queues
* Customer requests
* Message processing

---

# Linked List UI

Controls:

```text
Enter value
Insert
Delete
Search
Traverse
Reset
```

Display:

```text
HEAD
 ↓
[10] → [20] → [30] → None
```

Use cases:

* Dynamic collections
* Frequent insertion/deletion
* Implementing other data structures
* Memory structures where contiguous storage is unnecessary

---

## Day 4 Git Commit

```text
feat: add interactive data structure visualizations
```

---

## Day 4 Completion Check

```text
□ Streamlit launches
□ Stack is interactive
□ Queue is interactive
□ Linked List is interactive
□ Visual state changes correctly
□ Use cases displayed
□ Invalid operations show friendly messages
□ Code pushed
```

---

# 8. Day 5 – Complexity Prediction Tool

## Major Objective

Build the required Big-O prediction feature.

Create:

```text
src/analysis/complexity_analyzer.py
```

---

# User Inputs

Allow the user to choose:

```text
Data Structure
Operation
Input Size
```

Example:

```text
Data Structure:
Linked List

Operation:
Search

Input Size:
10,000
```

---

# Output

Display:

```text
Predicted Time Complexity: O(n)

Space Complexity: O(n)

Explanation:
Searching a linked list may require traversing
every node before the requested value is found.
```

---

# Initial Complexity Matrix

| Structure   | Insert | Delete | Search |
| ----------- | ------ | ------ | ------ |
| Stack       | O(1)   | O(1)   | O(n)   |
| Queue       | O(1)   | O(1)   | O(n)   |
| Linked List | O(1)*  | O(n)   | O(n)   |

`*` The linked-list insertion result depends on where insertion occurs and implementation details. The application should clearly state the assumed operation, such as insertion at the head.

---

# Educational Explanation

Do not display only:

```text
O(n)
```

Explain:

* What O(n) means
* Why the selected operation has that complexity
* What happens as input size increases

---

# Testing

Create:

```text
tests/test_complexity.py
```

Verify every defined operation returns the expected result.

---

## Day 5 Git Commits

```text
feat: implement complexity prediction analyzer
```

```text
test: add complexity analyzer tests
```

---

## Day 5 Completion Check

```text
□ Data structure selector works
□ Operation selector works
□ Big-O prediction works
□ Explanations appear
□ Complexity values verified
□ Tests pass
□ Analyzer connected to UI
□ Code pushed
```

---

# 9. Day 6 – Performance Testing and Charts

## Major Objective

Compare theoretical complexity with measured runtime.

Create:

```text
src/benchmark/performance_tester.py
```

---

# Test Sizes

Use approximately:

```text
100
1,000
10,000
50,000
```

Increase to 100,000 only if performance remains stable.

---

# Timing

Use:

```python
time.perf_counter_ns()
```

Each operation should run multiple times.

Example:

```text
20–50 trials
```

Calculate:

```text
Average runtime
or
Median runtime
```

---

# Operations to Benchmark

Minimum:

### Stack

```text
Push
Search
```

### Queue

```text
Enqueue
Search
```

### Linked List

```text
Insert
Search
```

If time permits:

```text
Delete
```

---

# Save Results

Create:

```text
data/benchmark_results.csv
```

Fields:

```text
Structure
Operation
Input_Size
Predicted_Complexity
Runtime
```

---

# Charts

At minimum create:

## Chart 1

**Input Size vs Runtime**

This shows how runtime changes as `n` increases.

## Chart 2

**Predicted vs Observed Growth**

Compare expected complexity behavior with measured performance.

Store:

```text
images/performance_chart.png
images/complexity_comparison.png
```

---

# Important Explanation

The report must not claim:

> Big-O predicted that an operation would take exactly 0.5 milliseconds.

Big-O predicts **growth behavior**, not an exact runtime.

The project should compare:

```text
Theoretical Growth
        vs.
Observed Runtime Growth
```

---

# Performance Report

Create:

```text
reports/performance_report.md
```

Include:

1. Purpose
2. Testing environment
3. Test sizes
4. Number of trials
5. Predicted complexities
6. Measured results
7. Charts
8. Interpretation
9. Limitations

---

## Day 6 Git Commits

```text
perf: implement performance benchmarking framework
```

```text
docs: add performance charts and analysis
```

---

## Day 6 Completion Check

```text
□ Benchmarks execute
□ Results save correctly
□ Multiple trials used
□ Charts generated
□ Axes clearly labeled
□ Titles included
□ Big-O interpretation correct
□ Performance report drafted
□ Work pushed
```

---

# 10. Day 7 – Final Report, Documentation, Video, and Submission

## Major Objective

Complete and verify every assignment deliverable.

---

# Part A – One-Page Analysis

Create:

```text
reports/data_structure_analysis.md
```

Then convert/finalize it in the submission format required by the instructor if necessary.

---

## Recommended Structure

### Paragraph 1 – Introduction

Define data structures and explain why structure selection affects software efficiency.

### Paragraph 2 – Stack

Discuss:

```text
LIFO
O(1) push/pop
O(n) search
Appropriate application scenarios
```

### Paragraph 3 – Queue

Discuss:

```text
FIFO
O(1) enqueue/dequeue
Scheduling and message-processing applications
```

### Paragraph 4 – Linked List

Discuss:

```text
Nodes
Pointers
Dynamic storage
Insertion/deletion trade-offs
Search cost
```

### Paragraph 5 – Selection Criteria and Conclusion

Discuss:

```text
Operation frequency
Access pattern
Input size
Memory
Search needs
Insertion/deletion needs
Performance requirements
```

Conclude that no single data structure is optimal for every application.

---

# Part B – Complete README

README should include:

```text
Project Title
Overview
Assignment Purpose
Features
Technologies
Project Structure
Installation
Running the Application
Using Stack
Using Queue
Using Linked List
Complexity Analyzer
Performance Testing
Testing
Screenshots
Future Development
```

---

# Part C – Code Documentation Review

Check:

```text
□ Classes have docstrings
□ Public methods are explained
□ Variable names are clear
□ Comments explain non-obvious logic
□ Unused code removed
□ Debug print statements removed
```

---

# Part D – Final Testing

Run:

```text
pytest
```

Then manually test:

### Stack

```text
Push
Pop
Peek
Search
Reset
```

### Queue

```text
Enqueue
Dequeue
Peek
Search
Reset
```

### Linked List

```text
Insert
Delete
Search
Traverse
Reset
```

### Complexity Analyzer

Test multiple structure-operation combinations.

### Performance Analyzer

Run benchmarks and generate charts again.

---

# Part E – Demo Video

Target:

```text
3–5 minutes
```

Recommended structure:

### 0:00–0:25

Introduce:

* Project name
* Purpose
* Assignment objective

### 0:25–1:05

Demonstrate Stack.

### 1:05–1:45

Demonstrate Queue.

### 1:45–2:25

Demonstrate Linked List.

### 2:25–3:10

Demonstrate Complexity Analyzer.

### 3:10–4:00

Show performance testing.

### 4:00–4:30

Show charts and briefly explain the results.

### 4:30–4:50

Conclusion.

---

# Part F – Release

Create final Git commit:

```text
release: complete assignment one submission
```

Create Git tag:

```text
v1.0-assignment
```

This preserves the exact submitted version before future mini-project development begins.

---

# 11. Final Assignment Quality Gate

Do not submit until every item below is checked.

## Data Structures

```text
□ Stack complete
□ Queue complete
□ Linked List complete
□ Insert operations demonstrated
□ Delete operations demonstrated
□ Search operations demonstrated
```

## Interface

```text
□ Application opens correctly
□ Navigation works
□ Stack visualization works
□ Queue visualization works
□ Linked List visualization works
□ User feedback messages work
```

## Complexity Tool

```text
□ Stack complexity available
□ Queue complexity available
□ Linked List complexity available
□ Insert analyzed
□ Delete analyzed
□ Search analyzed
□ Big-O explanations included
```

## Performance

```text
□ Performance tester works
□ Multiple input sizes tested
□ Multiple trials performed
□ Predicted complexity recorded
□ Actual runtime recorded
□ Chart created
□ Results interpreted correctly
```

## Documentation

```text
□ README complete
□ Code documented
□ One-page analysis complete
□ Performance report complete
□ Requirements documented
```

## Testing

```text
□ Stack tests pass
□ Queue tests pass
□ Linked List tests pass
□ Complexity tests pass
□ Manual UI tests completed
```

## Demo

```text
□ Video is between 3–5 minutes
□ All major features shown
□ Complexity analyzer demonstrated
□ Performance chart shown
□ Audio understandable
```

## GitHub

```text
□ Final code pushed
□ README visible
□ Repository organized
□ No unnecessary files
□ requirements.txt correct
□ v1.0-assignment tagged
```

---

# 12. Daily Deliverable Summary

| Day             | Main Work             | End-of-Day Deliverable                    |
| --------------- | --------------------- | ----------------------------------------- |
| **Day 1** | Setup                 | GitHub repository + requirements          |
| **Day 2** | Stack + Queue         | 2 working structures                      |
| **Day 3** | Linked List + Testing | All 3 structures + tests                  |
| **Day 4** | UI + Visualization    | Interactive learning tool                 |
| **Day 5** | Complexity Analyzer   | Big-O prediction tool                     |
| **Day 6** | Performance           | Benchmark results + charts                |
| **Day 7** | Submission            | Analysis + README + video + final testing |

---

# 13. Assignment Deliverable Mapping

| Instructor Requirement     | Project Deliverable        | Planned Completion |
| -------------------------- | -------------------------- | ------------------ |
| Stack                      | `stack.py`               | Day 2              |
| Queue                      | `queue.py`               | Day 2              |
| Linked List                | `linked_list.py`         | Day 3              |
| Clear documentation        | Docstrings + README        | Days 2–7          |
| User interface             | `app.py`                 | Day 4              |
| Visual demonstrations      | Streamlit interface        | Day 4              |
| Complexity tool            | `complexity_analyzer.py` | Day 5              |
| Insert/delete/search Big-O | Complexity matrix          | Day 5              |
| Performance testing        | `performance_tester.py`  | Day 6              |
| Prediction vs actual       | Benchmark report           | Day 6              |
| Charts                     | PNG performance charts     | Day 6              |
| One-page analysis          | Analysis report            | Day 7              |
| Demo video                 | 3–5 minute recording      | Day 7              |

---

# 14. Submission Version

The final submission should be preserved as:

```text
Data Structure Learning Tool
Version 1.0
```

Git:

```text
v1.0-assignment
```

After the assignment has been submitted, development can continue from the same repository.

Possible future versions:

```text
v1.1 – UI Improvements

v1.2 – Advanced Benchmarking

v1.3 – Interactive Animations

v2.0 – Trees and Hash Tables

v2.1 – Sorting and Searching Algorithms

v3.0 – Portfolio-Level DSA Learning Platform
```

The assignment therefore becomes the **foundation of the mini project**, rather than a separate project that is abandoned after submission.
