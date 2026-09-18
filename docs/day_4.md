# Day 4 — Interactive data structure visualizations

## Delivered

- `app.py` launches the Streamlit lab with Home, Stack, Queue, Linked List,
  Complexity Analyzer, Performance, and About navigation.
- Stack: Push, Pop, Peek, Search, Reset, and a vertical TOP diagram.
- Queue: Enqueue, Dequeue, Peek, Search, Reset, and a FRONT/REAR diagram.
- Linked List: Insert, Delete, Search, Traverse, Reset, and HEAD/next/None nodes.
- Each page includes an example experiment and appropriate use cases.
- Signed integer input accepts negatives and duplicates; invalid input and
  empty operations show friendly feedback without changing data.
- Separate structure instances persist across navigation and reruns within a
  browser session. Reset affects only the selected structure. A new session
  starts empty; no disk persistence is provided.
- Complexity Analyzer and Performance are clearly labeled Day 5/6 placeholders.

## Design

Core structure modules remain independent of Streamlit. Stack and Queue expose
`to_list()` shallow snapshots in O(n) time and space; Linked List uses its
existing `traverse()`. Diagrams derive from these snapshots rather than private
storage or a second copy of application state.

`src/visualization/visualizer.py` generates escaped HTML with labels, arrows,
scrollable layouts, and accessible image descriptions. A text panel shows the
same contents. `.streamlit/config.toml` supplies the light theme.

## Run

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the URL Streamlit prints. Use `Ctrl+C` to stop it. On macOS/Linux, use
`.venv/bin/python` in place of the Windows executable path.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: **46 passed** — 23 core, 9 visualization/snapshot, and 14 Streamlit
interaction cases. AppTest checks all pages and controls, input errors, empty
operations, state persistence, independent resets, and session isolation.
Browser checks exercise the running server and inspect desktop/narrow layouts.
See [the test plan](test_plan.md) and [Stack screenshot](../images/day4-stack.png).

## Git milestone

Required commit: `feat: add interactive data structure visualizations`.

Next: Day 5's complexity prediction tool and its tests.
