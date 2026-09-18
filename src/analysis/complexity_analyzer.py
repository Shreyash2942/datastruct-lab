"""Implementation-specific Big-O predictions, independent of the UI.

Bounds assume constant-cost equality and fixed-size value references. They
describe growth, not exact instruction counts, elapsed time, or byte usage.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ComplexityRule:
    """Time/space bounds and rationale for one implemented operation."""

    time: str
    best_time: str
    worst_time: str
    auxiliary_space: str
    result_space: str
    explanation: str


@dataclass(frozen=True)
class ComplexityPrediction:
    """Validated selection with immutable bounds and illustrative growth data."""

    structure: str
    operation: str
    input_size: int
    rule: ComplexityRule
    storage_space: str
    growth_explanation: str
    growth_points: tuple[tuple[int, int], ...]


def _constant(explanation: str) -> ComplexityRule:
    return ComplexityRule("O(1)", "O(1)", "O(1)", "O(1)", "O(1)", explanation)


def _scan(explanation: str) -> ComplexityRule:
    return ComplexityRule("O(n)", "O(1)", "O(n)", "O(1)", "O(1)", explanation)


def _snapshot(explanation: str) -> ComplexityRule:
    return ComplexityRule("O(n)", "O(n)", "O(n)", "O(1)", "O(n)", explanation)


_RULES = {
    "Stack": {
        "push": ComplexityRule("O(1) amortized", "O(1)", "O(n)", "O(n) during resize", "O(1)",
            "Push appends at the end of the Python list, which is the top. Most pushes do constant work. Occasional resizing can move n references, so a single push can take O(n), while a sequence has O(1) amortized cost per push. A resize can temporarily require O(n) extra allocation."),
        "pop": ComplexityRule("O(1) amortized", "O(1)", "O(n)", "O(n) during resize", "O(1)",
            "Pop removes the last list element without shifting the remaining values. Occasional shrinking can resize the backing array, making a single pop O(n); the amortized cost is O(1). A resize can temporarily require O(n) extra allocation. An empty pop raises IndexError in O(1)."),
        "peek": _constant("Peek reads the last list element directly without removing it. An empty stack raises IndexError in O(1)."),
        "search": _scan("Search compares values from top to bottom. A match at the top takes O(1); a missing value or match at the bottom may require checking all n values, taking O(n)."),
        "is_empty": _constant("The underlying Python list exposes whether its stored length is zero; no traversal is needed."),
        "size": _constant("Python stores the list length, so size reads a count without visiting the values."),
        "to_list": _snapshot("The snapshot copies all n value references into a new list in top-to-bottom order. It allocates O(n) result space; the values themselves are not deep-copied."),
    },
    "Queue": {
        "enqueue": _constant("Enqueue appends at the rear of collections.deque. It does not shift existing values or copy the whole queue."),
        "dequeue": _constant("Dequeue removes the front of collections.deque without shifting remaining values. An empty queue raises IndexError in O(1)."),
        "peek": _constant("Peek reads the deque's front endpoint directly. It leaves the queue unchanged; an empty queue raises IndexError in O(1)."),
        "search": _scan("Search compares values from front to rear. A front match takes O(1); a rear match or missing value may require checking all n values, taking O(n)."),
        "is_empty": _constant("The deque records its length, so checking whether it is empty does not traverse its values."),
        "size": _constant("The deque maintains a count, so size returns it without traversal."),
        "to_list": _snapshot("The snapshot copies all n value references into a new list in front-to-rear order. Its result needs O(n) space, with O(1) traversal bookkeeping outside the result."),
    },
    "Linked List": {
        "insert": _constant("Insert always adds at the head: create one node, point it to the old head, and update the head and count. No traversal is required. This bound does not describe insertion at an arbitrary position."),
        "delete": _scan("Delete searches from the head and unlinks the first matching node. A head match takes O(1); a tail match or missing value can require visiting n nodes. Relinking known neighbors takes O(1), but finding them makes deletion by value O(n) in the worst case."),
        "search": _scan("Search follows next references from head to tail. A head match takes O(1); a tail match or missing value can require visiting every node, taking O(n)."),
        "traverse": _snapshot("Traverse visits all n nodes from head to tail and collects their value references into a new Python list. It needs O(n) result space and O(1) traversal bookkeeping. Values are shared, not deep-copied."),
        "is_empty": _constant("Checking whether the head reference is None takes constant work, regardless of the list length."),
        "size": _constant("The implementation maintains an element count during insertion and deletion, so size reads that count in O(1)."),
    },
}


def supported_structures() -> tuple[str, ...]:
    """Return supported display names in UI order; no arguments or mutation."""
    return tuple(_RULES)


def supported_operations(structure: str) -> tuple[str, ...]:
    """Return public operation names; raise ValueError for an unknown structure."""
    if not isinstance(structure, str) or structure not in _RULES:
        raise ValueError("Choose Stack, Queue, or Linked List.")
    return tuple(_RULES[structure])


def analyze_complexity(structure: str, operation: str, input_size: int) -> ComplexityPrediction:
    """Predict growth for a supported operation on a positive integer size.

    Raises ValueError for unsupported names or a nonpositive/noninteger size
    (including bool). Creates only three growth points, never an n-element
    structure. The points normalize the chosen O(1) or O(n) model to 1 at n;
    they are illustrative ratios, not measured times or exact operation counts.
    """
    operations = supported_operations(structure)
    if not isinstance(operation, str) or operation not in operations:
        raise ValueError(f"Unsupported operation for {structure}: choose {', '.join(operations)}.")
    if isinstance(input_size, bool) or not isinstance(input_size, int) or input_size < 1:
        raise ValueError("Input size must be a positive integer.")
    rule = _RULES[structure][operation]
    linear = rule.time == "O(n)"
    if linear:
        growth = (f"O(n) means linear growth. Starting with n = {input_size:,}, the illustrative model doubles its work at {input_size * 2:,} values and quadruples it at {input_size * 4:,}. This uses the stated worst-case bound for searches/deletion and the full-copy bound for traversal/snapshots.")
    else:
        growth = (f"O(1) means constant growth: increasing n from {input_size:,} to {input_size * 2:,} or {input_size * 4:,} does not increase the work in this illustrative model.")
        if "amortized" in rule.time:
            growth += " This is an amortized model across a sequence of operations; individual resizing operations can still take O(n)."
    growth += " Big-O describes scaling, not exact runtime, operation counts, or bytes."
    points = tuple((input_size * factor, factor if linear else 1) for factor in (1, 2, 4))
    return ComplexityPrediction(structure, operation, input_size, rule, "O(n)", growth, points)
