# Assignment 1 demonstration script

Target length: **4 minutes 50 seconds**. Run the app from the repository root,
open the local URL, and begin with a fresh browser session. Use a readable
desktop viewport. Explain what each operation changes while its result is visible.

## 0:00–0:25 — Introduction

Show Home. Say: “DataStruct Lab demonstrates how stacks, queues, and linked lists
organize values. This CSC506 project connects Python implementations with live
diagrams, complexity explanations, and measured performance. We will compare
their ordering rules and the cost of their operations.”

## 0:25–1:05 — Stack

Open Stack. Push 10, 20, and 30. Point out TOP and the count of three.
Peek, then Pop: both identify 30, but only Pop removes it. Search for 10.
Reset, then Pop to show friendly empty feedback.

Say: “A stack is last in, first out, like undo history. Peek leaves the stack
unchanged. This list-backed implementation has O(1) amortized push and pop;
an individual resize can cost O(n). A missing search may inspect every value.”

## 1:05–1:45 — Queue

Open Queue. Enqueue 10, 20, and 30. Point out FRONT and REAR. Peek shows 10;
Dequeue removes 10. Search for 30, then Reset.

Say: “A queue serves the oldest value first. This is FIFO, useful for printer
jobs or requests processed in arrival order. The deque-backed endpoints take
O(1) time without shifting all remaining values. Searching is O(n) worst case.”

## 1:45–2:25 — Linked List

Open Linked List. Insert 10, 20, and 30. The diagram reads HEAD → 30 → 20 → 10 →
None. Traverse, search for 20, then delete 20. The remaining links connect 30
to 10. Search for 99 to show a miss, then Reset.

Say: “Each node holds a value and a reference to the next node. Head insertion
is O(1). Deletion by value must first locate the node, so it can take O(n), even
though changing the links is constant work. Traversal creates a separate list.”

## 2:25–3:10 — Complexity Analyzer

Choose Linked List, Search, n = 10,000. Show O(n) time, O(n) stored data, and O(1)
auxiliary space. Change to Insert (at head), then Traverse. Finally show Stack
Push and its amortized versus worst-single-operation bounds.

Say: “The analyzer covers all twenty public operations. Time, existing storage,
temporary workspace, and returned-result space are different quantities.
The chart illustrates growth at n, twice n, and four times n. It does not time
the operation or allocate that many values. Big-O is a growth model.”

## 3:10–4:00 — Performance testing

Open Performance. Keep sizes 100, 1,000, 10,000, and 50,000 and 30 trials.
Click Run benchmarks. Show the completed table and both download buttons.
Download CSV and the full report bundle.

Say: “Six operation types across four sizes give twenty-four cases and seven
hundred twenty measured samples. Each call gets a fresh fixture. Setup and
rendering are excluded from the timer; three warmups precede thirty timed
trials per case. Search uses an absent value. Runtime is median nanoseconds.
Downloads include raw samples, environment metadata, charts, and the report.
The experiment preserves the live structures.”

## 4:00–4:30 — Charts and interpretation

Show the two runtime panels and the six normalized comparison panels. Describe
the run currently displayed; its numbers may differ from the saved CLI run.

Say: “Search time increases as more values must be examined. Short insertion
measurements are sensitive to clock overhead and allocation. Shading shows the
middle half of samples. The comparison chart divides each series by its own
smallest-input median, so it compares growth, not absolute speed. A mismatch
does not disprove Big-O; one machine's timings are not universal.”

## 4:30–4:50 — Conclusion

Return to Home or About. Say: “Choose a structure according to access order,
operation frequency, input size, and memory needs. The repository includes the
implementations, tests, a one-page analysis, and reproducible performance results.
No single data structure is best for every workload.”

## Recording check

- Keep the final recording between 3 and 5 minutes, with readable text and clear audio.
- Demonstrate actual state changes, predictions, a benchmark run, and both charts.
- Verify playback from beginning to end before uploading it with the assignment.
- If using generated narration, identify it as computer-generated; do not present
  it as the student's own voice.
