# Day 7 — Final analysis, demonstration, and release

The author supplied a refined final report and a new recording on September 20,
2026. The report title page now includes that date. The planned Git tag
`v1.0-assignment` has not been created. Publishing repository changes does not
upload an assignment to the course portal.

## Deliverables

- [Refined final Word report](../reports/DataStruct_Lab_Refined_Final_Report.docx),
  supplied by the author, with Shreyashkumar Patel, Jonathan Vanover, and
  September 20, 2026 on its title page. It contains three tables and two charts.
- [Data structure analysis](../reports/data_structure_analysis.md) with a
  verified [US Letter PDF](../reports/data_structure_analysis.pdf) containing
  three analysis pages and one reference page. These earlier analysis versions
  are not exports of the newly supplied Word report.
- [Implementation guide](implementation_guide.md) explaining all three
  structures, all 20 public operations, UI flow, predictions, and timing.
- [Nine selected test cases](selected_test_cases.md), three per structure,
  with inputs, expected outcomes, and exact pytest commands.
- [README](../README.md) covering setup, every feature, operation examples,
  tests, performance, screenshots, reports, and future development.
- [Current MP4 walkthrough](../demo/datastruct-lab-demo.mp4), approximately 12:08.
  See [recording notes](../demo/README.md) for the distinction between the current
  recording and the historical transcript, captions, and original demo script.
- Existing [performance report](../reports/performance_report.md), charts,
  raw samples, and environment metadata remain reproducible.

The new recording replaces the earlier computer-narrated demonstration. The
repository copy is compressed at the original 1920 × 1032 resolution, with the
original AAC audio stream retained. The uncompressed source recording and the
personal recording guide remain outside the repository. The previous video's
benchmark ZIP was removed by the author.

## Replacement artifact checks

- The supplied Word document opens through python-docx and contains its title
  fields, three tables, and two embedded charts. Its contents were preserved.
- The compressed recording is 728 seconds (12:08), approximately 18.2 MiB,
  with 1920 × 1032 H.264 video and the original AAC audio stream.
- The entire compressed audio/video file decoded without errors. Sampled
  structure and performance-chart frames were inspected for readability.
- The original recording was moved outside the repository; its SHA256 hash
  was verified after the move. No transcript matching the new video was created.
- Relative Markdown file links resolve after the report/video replacements.
- This update changes documents and media only; the previously passing test
  suite was not rerun because application code and tests were unchanged.

## Earlier application and artifact verification

These checks describe the prior verified application and saved benchmark run.
The source code and automated tests were not changed by the report/video update.

- **128 pytest cases passed** on Windows with Python 3.14.4.
- `pip check`: no broken requirements.
- All production classes and public functions/methods have docstrings.
  Removed stale milestone descriptions from About and the visualization package.
  The benchmark CLI's progress output is intentional; no debug prints were found.
- Browser checks exercised Stack Push/Pop/Peek/Search/Reset, Queue
  Enqueue/Dequeue/Peek/Search/Reset, and Linked List
  Insert/Delete/Search/Traverse/Reset, including empty feedback and a missing value.
- Analyzer checks covered Linked List Search, Insert, Traverse, and Stack Push.
- A new default benchmark ran in the browser and both downloads completed.
  Day 6 also verified navigation persistence, unchanged live state, and a
  390-pixel viewport without document overflow.
- Reconstructed all 24 saved medians from 720 raw samples and regenerated
  both tracked PNG charts byte-for-byte from the saved run.
- PDF page count verified as four; the first and third analysis pages were
  rendered and visually inspected for spacing, readability, and overflow.
- Word opened the previous APA document and reported nine pages, with exactly
  three analysis pages. Document checks
  verified US Letter paper, one-inch margins, 12-point Times New Roman, double
  body spacing, a page-number field, first-line indents, and hanging reference
  indents. Tables use 11-point text and single spacing for readability.
  In-text citations match the two references. The companion PDF is rendered
  separately from that earlier analysis text; it excludes the cover and appendices.
  These page-count and formatting checks do not describe the replacement Word file.
- Report measurements match the saved Windows/CPython 3.14.4 run: six operation
  types, four input sizes, 30 trials, 24 summary rows, and 720 raw samples.
  Both embedded charts are the saved project charts. No prediction-accuracy
  percentage or unmeasured deletion runtime is claimed.
- The latest full pytest run passed all 128 cases; the nine highlighted cases
  were individually matched to those results. Runnable implementation examples
  and local documentation links were also checked.
- Previous MP4 duration: 291.42 seconds (4:51); 1280 × 960 H.264 video, AAC audio, and
  an embedded subtitle stream. Full audio/video decoding and Edge playback
  passed. Representative frames were visually reviewed. The separate WebVTT
  file belongs only to that earlier video, which has now been replaced.
- A final CLI repeat produced all 24 cases and six artifacts in an external
  verification directory without replacing the saved assignment data.

## Reproduce the checks

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The [original demo script](demo_script.md) documents the earlier browser sequence.
The author's personal recording guide is outside the repository. To run a new
CLI benchmark without replacing the recorded assignment data:

```powershell
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester --output-dir ..\benchmark-repeat
```

## Submission checklist

- Review the supplied final report and recording against the instructor's rubric;
  a separate original rubric has not been provided. Earlier page-count checks
  apply to the earlier analysis, not the replacement report.
- Use the published commit for the source-code deliverable, or create the planned
  release tag if a tagged snapshot is needed.
- Upload the requested analysis, performance materials, and demo video to the
  course portal, or provide links if the instructor requests links.
- Confirm successful upload in the portal. No portal submission was performed
  by this project workflow.

Planned final release commit message: `release: complete assignment one submission`.
Graphify outputs, caches, and recording tools remain outside the repository in
the sibling `../graphify-out/` directory.

APA formatting basis: American Psychological Association's
[Student Paper Setup Guide](https://my.cgu.edu/writing-rhetoric/wp-content/uploads/sites/9/2021/09/APA-Student-Paper-Setup-Guide.pdf).
Technical references were checked against Morin's *Open data structures: An
introduction* (2013) and the Python 3.14 `collections` documentation.
