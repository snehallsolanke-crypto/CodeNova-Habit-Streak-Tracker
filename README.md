# Personal Habit & Daily Streak Tracker

A beginner-friendly command-line app for recording habits, checking in with timestamps, and reviewing streak and monthly completion progress. It was created for the CodeNova Python Programming Internship.

## Features

- Create, view, and delete habits.
- Choose Daily, Weekdays (Monday–Friday), or Weekly targets.
- Save dated check-ins with local timezone timestamps; duplicate daily check-ins are rejected.
- Review current and longest streaks and see when a scheduled target was missed.
- Calculate a monthly completion rate from scheduled target days or weeks.
- Validate menu selections, habit numbers, and `YYYY-MM` input.
- Persist data in structured `habits.json`; old date-only check-ins are upgraded when loaded and saved.
- Includes two labeled sample habits with historical check-ins and active streaks.

## Installation and execution

Requires Python 3. No third-party packages are needed.

1. Open a terminal in this folder (`Habit_Streak_Tracker`).
2. Run `py habit_tracker.py` on Windows, or `python3 habit_tracker.py` on macOS/Linux.
3. Choose **7** to exit.

## Menu guide

1. **Add habit** — enter a name and select Daily, Weekdays, or Weekly.
2. **View habits** — list each habit and its target frequency.
3. **Check in today** — record today's date and timestamp once.
4. **Delete habit** — select a habit and confirm with `y`.
5. **View streaks** — show current streak, longest streak, and missed-target status.
6. **Monthly completion rate** — select a habit and enter `YYYY-MM`, or press Enter for this month.
7. **Exit** — close the program.

## Streak and rate calculations

- **Current streak:** counts consecutive scheduled target periods through today. Daily habits require each calendar day; Weekdays skip Saturday and Sunday; Weekly habits need at least one check-in in each consecutive ISO calendar week. If a due period has been missed, the current streak is zero. If today's target has not yet been completed, a run remains active until the scheduled period ends.
- **Longest streak:** finds the largest unbroken sequence in the full check-in history, applying the same daily, weekday, or weekly schedule. Weekday weekends do not break a run. Weekly periods use ISO weeks, including year boundaries.
- **Monthly completion rate:** `completed scheduled periods ÷ scheduled periods through the selected date × 100`. The current month counts only through today; past months count their full calendar month. For Weekly habits, each ISO week intersecting the month contributes one target period.

## Sample output

```text
5. View streaks
Choose an option: 5
1. Daily Exercise (Daily)
2. reading book (Daily)
3. Sample: Morning Walk (Daily)
4. Sample: Weekday Reading (Weekdays)
Habit number: 3
Sample: Morning Walk: current streak 5, longest streak 5 target periods
Status: Active or not yet due
```

## Screenshots

The original project screenshots are included below.

| Menu | Add habit | Habit list |
|---|---|---|
| ![Main menu](Habit_Streak_Tracker/Habit_Streak_Tracker/menu.png) | ![Add habit](Habit_Streak_Tracker/Habit_Streak_Tracker/add-habit.png) | ![All habits](Habit_Streak_Tracker/Habit_Streak_Tracker/all-habits.png) |

| Streak view | Monthly rate |
|---|---|
| ![Streak view](Habit_Streak_Tracker/Habit_Streak_Tracker/streak.png) | ![Monthly completion rate](Habit_Streak_Tracker/Habit_Streak_Tracker/monthly-rate.png) |

## Data and backup

`habits.json` stores each habit's name, frequency, and check-ins (`date` and `timestamp`). A pre-migration copy of the original data is preserved as `habits.json.backup`.

## Developer

Snehal Solanke — CodeNova Python Programming Internship.

