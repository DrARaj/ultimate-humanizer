"""Generate the AI set with `claude -p --model haiku`, one passage per human-wiki topic.
Run after fetch_data.py, from the repo root: python evals/gen_ai.py   (merges manifest.csv; uses your Claude Code login; 40 calls)"""
import csv, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import TOPICS, DATA

PROMPT = "Write one encyclopedic paragraph of about 150 words about {topic}."

rows = []
for i, t in enumerate(TOPICS, 1):
    out = DATA / f"ai{i:02d}.txt"
    if not out.exists():
        # neutral cwd so no project instructions leak into the prompt context
        r = subprocess.run(["claude", "-p", "--model", "haiku", PROMPT.format(topic=t)],
                           capture_output=True, text=True, encoding="utf-8",
                           cwd=tempfile.gettempdir(), timeout=180)
        text = r.stdout.strip()
        if r.returncode or not text:
            sys.exit(f"claude -p failed for {t}: {r.stderr[:200]}")
        out.write_text(text + "\n", encoding="utf-8")
    text = out.read_text(encoding="utf-8")
    rows.append([f"ai{i:02d}", "ai", "claude -p --model haiku", "generated, no claim", time.strftime("%Y-%m-%d"), t, len(text.split())])
human = list(csv.reader(open(DATA / "manifest_human.csv", encoding="utf-8")))  # written by fetch_data.py
with open(DATA / "manifest.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(human + rows)
print(len(rows), "ai passages")
