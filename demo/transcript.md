# Recorded demonstration transcript

This is the historical text used for Microsoft Zira computer-generated narration
in the earlier 4:51 video. It is not a transcript of the current author-supplied
12:08 recording. The matching historical captions are in captions.vtt.
The earlier walkthrough used a separate benchmark run. Its former downloaded
bundle has been removed from the current submission materials.

## Chapters

### 00:00:01 - Introduction

This is DataStruct Lab, a learning tool for C S C five oh six. The project connects Python implementations of stacks, queues, and linked lists with live diagrams, complexity explanations, and measured performance. This walkthrough uses computer-generated narration. We will compare ordering rules, try the operations, and see how theoretical growth relates to actual measurements.

### 00:00:26 - Stack

A stack is last in, first out. We push ten, twenty, and thirty. The newest value, thirty, appears at the top. Peek reads thirty without removing it. Pop removes thirty, leaving twenty at the top. Searching for ten finds the older value without changing the stack. This ordering is useful for undo history and backtracking. Push and pop on this Python list have constant amortized cost, although one resize can cost linear time. Reset clears the structure. Popping an empty stack shows a friendly message.

### 00:01:06 - Queue

A queue is first in, first out. We enqueue ten, twenty, and thirty. Ten is at the front, while thirty is at the rear. Peek reads ten without removing it. Dequeue removes ten because it arrived first. Searching for thirty leaves the remaining values unchanged. This matches printer jobs or requests served in arrival order. The deque implementation supports constant time endpoint operations without shifting every remaining value. A missing search may still examine all values. Reset empties only this queue.

### 00:01:46 - Linked List

A singly linked list stores a value and a next reference in each node. We insert ten, twenty, and thirty at the head. The chain reads thirty, twenty, ten, then None. Traverse returns those values in head to tail order. Searching finds twenty. Deleting twenty connects thirty directly to ten. Relinking is constant work, but finding a node by value can take linear time. Searching for ninety-nine shows a miss. Head insertion is constant time. Reset removes the entire chain.

### 00:02:26 - Complexity Analyzer

The Complexity Analyzer covers all twenty public operations. For linked list search at ten thousand values, worst case time is O of n. Existing storage is also O of n, while auxiliary workspace is constant. Switch to head insertion: time becomes O of one. Traversal takes linear time and returns a new list using linear result space. For stack push, the analyzer distinguishes constant amortized cost from a worst single resize taking linear time. The chart illustrates growth at n, twice n, and four times n. These are predictions, not measured runtimes.

### 00:03:11 - Performance Testing

The Performance page measures six operation types at each selected size. We use one hundred, one thousand, ten thousand, and fifty thousand elements, with thirty timed trials per case. Clicking Run benchmarks collects real measurements. Each call starts with a fresh fixture. Setup, verification, and charts stay outside the timer. Three untimed warmups precede the samples. Searches use an absent value, so they inspect the complete structure. The table reports median nanoseconds and sample variability. Twenty-four cases produce seven hundred twenty samples. Downloads include the summary, raw trials, environment metadata, charts, and report. Your live structures stay unchanged.

### 00:04:01 - Charts and Interpretation

The runtime chart separates single insertions from missing value searches. Search time grows as more values are examined. Shading shows the middle half of the samples. The comparison chart normalizes each series to its own smallest input. It compares growth rather than absolute speed. Clock overhead, allocation, and background activity affect short timings. These measurements do not prove Big O bounds or establish amortized cost from isolated pushes.

### 00:04:31 - Conclusion

Choose a structure according to access order, operation frequency, input size, and memory needs. The repository includes documented implementations, one hundred twenty-eight passing tests, a one-page analysis, and reproducible performance reports. No single data structure is best for every workload. Thank you for watching.
