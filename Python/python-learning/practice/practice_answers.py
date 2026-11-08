"""
Interview practice: Python answers for problems 1 to 9.

Run it:   python practice_answers.py
If everything is correct you will see "All checks passed".

"""

import sqlite3
import time
from collections import Counter, defaultdict, deque

# ---------------------------------------------------------------
# Problem 1: Dedupe, keep order
# C#:  HashSet<int> seen + List<int> result
# ---------------------------------------------------------------
def dedupe(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
assert dedupe([]) == []
# Shortcut worth mentioning (keeps order in modern Python):
assert list(dict.fromkeys([3, 1, 3, 2, 1])) == [3, 1, 2]


# ---------------------------------------------------------------
# Problem 2: Word count (+ top N words)
# C#:  Dictionary<string,int> + GetValueOrDefault
# ---------------------------------------------------------------
def word_count(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text, n=2):
    # Counter does the counting; most_common sorts by count
    return Counter(text.split()).most_common(n)


assert word_count("the cat and the hat") == {"the": 2, "cat": 1, "and": 1, "hat": 1}
assert top_words("the cat and the hat", 1) == [("the", 2)]


# ---------------------------------------------------------------
# Problem 3: Group by status
# C#:  Dictionary<string, List<string>>  (or LINQ GroupBy)
# ---------------------------------------------------------------
def group_by_status(tasks):
    groups = defaultdict(list)          # missing key -> starts as empty list
    for task in tasks:
        groups[task["status"]].append(task["title"])
    return dict(groups)


sample_tasks = [
    {"title": "A", "status": "done"},
    {"title": "B", "status": "open"},
    {"title": "C", "status": "done"},
]
assert group_by_status(sample_tasks) == {"done": ["A", "C"], "open": ["B"]}


# ---------------------------------------------------------------
# Problem 4: Two sum (one pass with a dictionary)
# ---------------------------------------------------------------
def two_sum(nums, target):
    seen = {}                           # number -> index
    for i, n in enumerate(nums):        # enumerate gives index AND value
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i                     # store AFTER checking
    return []


assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([1, 2], 10) == []


# Simple version (check every pair), good to say first in an interview:
def two_sum_slow(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


assert two_sum_slow([2, 7, 11, 15], 9) == [0, 1]


# ---------------------------------------------------------------
# Problem 5: Clean emails
# ---------------------------------------------------------------
def clean_emails(raw):
    unique = set()
    for item in raw:
        if not item or not item.strip():    # skips None and empty strings
            continue
        email = item.strip().lower()
        if "@" not in email:                # very simple validity check
            continue
        unique.add(email)
    return sorted(unique)


assert clean_emails([" Bob@X.com ", "alice@y.com", "", None, "bob@x.com"]) == [
    "alice@y.com",
    "bob@x.com",
]


# ---------------------------------------------------------------
# Problem 6: Retry with backoff
# ---------------------------------------------------------------
def retry(fn, attempts=3, delay=0.1):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if attempt == attempts:
                raise                       # out of attempts: let the error out
            time.sleep(delay)
            delay *= 2                      # backoff: wait twice as long next time


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ValueError("boom")
    return "ok"


assert retry(flaky, attempts=3, delay=0.01) == "ok"
assert calls["n"] == 3

try:
    retry(lambda: 1 / 0, attempts=2, delay=0.01)
    raise AssertionError("retry should have raised")
except ZeroDivisionError:
    pass


# ---------------------------------------------------------------
# Problem 7: Rate limiter (sliding window)
# C#:  Queue<DateTime>
# ---------------------------------------------------------------
class RateLimiter:
    def __init__(self, max_calls, window_seconds):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = deque()                # times of recent allowed calls

    def allow(self):
        now = time.monotonic()
        # forget calls that are older than the window
        while self.calls and now - self.calls[0] >= self.window:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True


limiter = RateLimiter(max_calls=2, window_seconds=0.2)
assert limiter.allow() is True
assert limiter.allow() is True
assert limiter.allow() is False
time.sleep(0.25)
assert limiter.allow() is True


# ---------------------------------------------------------------
# Problem 8: GET /tasks?done=true  (add this to your FastAPI app)
# ---------------------------------------------------------------
PROBLEM_8_ANSWER = '''
@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(done: bool | None = None, db: Session = Depends(get_db)):
    query = select(models.Task).order_by(models.Task.id)
    if done is not None:
        query = query.where(models.Task.done == done)
    return db.scalars(query).all()
'''

PROBLEM_8_TEST = '''
def test_filter_by_done():
    client.post("/tasks", json={"title": "A"})
    task_id = client.post("/tasks", json={"title": "B"}).json()["id"]
    client.put(f"/tasks/{task_id}", json={"done": True})

    done = client.get("/tasks", params={"done": True}).json()
    assert [t["title"] for t in done] == ["B"]
'''


# ---------------------------------------------------------------
# Problem 9: SQL (checked here with SQLite, same SQL works in Postgres)
# ---------------------------------------------------------------
SQL_A = "SELECT done, COUNT(*) AS total FROM tasks GROUP BY done ORDER BY done;"
SQL_B = "SELECT id, title FROM tasks ORDER BY created_at DESC, id DESC LIMIT 5;"
# (c) Speeding up filtering by done:
#   CREATE INDEX ix_tasks_done ON tasks (done);
# Better, because done has only two values (low selectivity):
#   CREATE INDEX ix_tasks_open ON tasks (created_at) WHERE done = false;  -- Postgres partial index
# Always confirm with:  EXPLAIN ANALYZE <your query>;

db = sqlite3.connect(":memory:")
db.execute(
    "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER, created_at TEXT)"
)
db.executemany(
    "INSERT INTO tasks (title, done, created_at) VALUES (?, ?, ?)",
    [
        ("t1", 0, "2026-10-01"),
        ("t2", 1, "2026-10-02"),
        ("t3", 0, "2026-10-03"),
        ("t4", 1, "2026-10-04"),
        ("t5", 0, "2026-10-05"),
        ("t6", 0, "2026-10-06"),
    ],
)
assert db.execute(SQL_A).fetchall() == [(0, 4), (1, 2)]
assert [row[1] for row in db.execute(SQL_B)] == ["t6", "t5", "t4", "t3", "t2"]

print("All checks passed")
