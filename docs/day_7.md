# Day 7 — Final analysis, demonstration, and release

The assignment materials are prepared for review. The APA title page's due date
still needs to be supplied before the final submission release. The planned Git
tag `v1.0-assignment` will preserve the release snapshot; it will not indicate
that a course submission has been uploaded.

## Deliverables

- [APA-style Word report](../reports/data_structure_analysis_APA.docx), with
  Shreyashkumar Patel and instructor Jonathan Vanover on its title page.
  Word verifies nine pages: title (1), analysis (2–4), references (5), selected
  tests (6), performance comparison (7), and measured-data charts (8–9).
- [Data structure analysis](../reports/data_structure_analysis.md) with a
  verified [US Letter PDF](../reports/data_structure_analysis.pdf) containing
  three analysis pages and one reference page. Appendices are in the Word report.
- [Implementation guide](implementation_guide.md) explaining all three
  structures, all 20 public operations, UI flow, predictions, and timing.
- [Nine selected test cases](selected_test_cases.md), three per structure,
  with inputs, expected outcomes, and exact pytest commands.
- [README](../README.md) covering setup, every feature, operation examples,
  tests, performance, screenshots, reports, and future development.
- [Demo script](demo_script.md), [MP4 walkthrough](../demo/datastruct-lab-demo.mp4),
  [exact narration transcript](../demo/transcript.md), and
  [WebVTT captions](../demo/captions.vtt).
- [The video run's downloaded benchmark bundle](../demo/benchmark_report.zip).
  This is a separate run from the Day 6 CLI artifacts, so runtimes differ.
- Existing [performance report](../reports/performance_report.md), charts,
  raw samples, and environment metadata remain reproducible.

The 4-minute, 51-second recording uses actual Streamlit interactions with a visible
**Computer-generated narration** label. Microsoft Zira supplies the synthesized
voice. It demonstrates all three structures, complexity predictions, a real
benchmark run, downloads, and both charts. Captions are included in the MP4
and as a separate WebVTT file; sentence timings are approximate.

## Final verification

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
- Word opened the revised APA document and reported nine pages, with exactly
  three analysis pages. Document checks
  verified US Letter paper, one-inch margins, 12-point Times New Roman, double
  body spacing, a page-number field, first-line indents, and hanging reference
  indents. Tables use 11-point text and single spacing for readability.
  In-text citations match the two references. The companion PDF is rendered
  separately from the same analysis text; it excludes the cover and appendices.
- Report measurements match the saved Windows/CPython 3.14.4 run: six operation
  types, four input sizes, 30 trials, 24 summary rows, and 720 raw samples.
  Both embedded charts are the saved project charts. No prediction-accuracy
  percentage or unmeasured deletion runtime is claimed.
- The latest full pytest run passed all 128 cases; the nine highlighted cases
  were individually matched to those results. Runnable implementation examples
  and local documentation links were also checked.
- MP4 duration: 291.42 seconds (4:51); 1280 × 960 H.264 video, AAC audio, and
  an embedded subtitle stream. Full audio/video decoding and Edge playback
  passed. Representative frames were visually reviewed. The separate WebVTT
  file is available for players that do not expose the embedded subtitle track.
- A final CLI repeat produced all 24 cases and six artifacts in an external
  verification directory without replacing the saved assignment data.

## Reproduce the checks

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Follow [the demo script](demo_script.md) for the browser sequence. To run a new
CLI benchmark without replacing the recorded assignment data:

```powershell
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester --output-dir ..\benchmark-repeat
```

## Submission checklist

- Enter the assignment due date on the APA title page.
- Review the three-page analysis, supporting appendices, and video against the
  instructor's rubric; a separate original rubric has not been provided.
- After completing the due date and creating the planned release tag, use that
  tagged repository snapshot for the source-code deliverable.
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
