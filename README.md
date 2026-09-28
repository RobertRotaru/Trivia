# Trivia

A small desktop trivia game written in Python with Tkinter. It pulls ten multiple-choice
questions from the [Open Trivia Database](https://opentdb.com/) API across different topics
and difficulty levels.

An early project (2024), kept for reference.

## Run

```bash
pip install requests
python match_page.py
```

To build a standalone Windows executable: `pyinstaller --onefile --windowed match_page.py`
