import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habits.json")
FREQUENCIES = ("Daily", "Weekdays", "Weekly")


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def normalize_habits(items):
    if not isinstance(items, list):
        raise ValueError("Expected a list of habits")
    result = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        frequency = item.get("frequency", "Daily")
        if frequency not in FREQUENCIES:
            frequency = "Daily"
        check_ins, seen = [], set()
        for entry in item.get("check_ins", []):
            day_text = entry if isinstance(entry, str) else entry.get("date") if isinstance(entry, dict) else None
            day = parse_date(day_text)
            if not day or day_text in seen:
                continue
            seen.add(day_text)
            timestamp = entry.get("timestamp", "") if isinstance(entry, dict) else ""
            check_ins.append({"date": day.isoformat(), "timestamp": timestamp or day.isoformat() + "T12:00:00"})
        result.append({"name": item["name"].strip() or "Unnamed habit", "frequency": frequency, "check_ins": sorted(check_ins, key=lambda x: x["date"])})
    return result


def load_habits():
    try:
        with open(DATA_FILE, encoding="utf-8") as file:
            return normalize_habits(json.load(file))
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("Could not load habits.json:", error)
        return []


habits = load_habits()


def save_habits():
    temp = DATA_FILE + ".tmp"
    with open(temp, "w", encoding="utf-8") as file:
        json.dump(habits, file, indent=4)
    os.replace(temp, DATA_FILE)


def completed(habit):
    return {parse_date(row["date"]) for row in habit["check_ins"] if parse_date(row["date"]) is not None}


def targets(habit, start, end):
    result, week_seen = [], set()
    day = start
    while day <= end:
        if habit["frequency"] == "Daily":
            result.append(day)
        elif habit["frequency"] == "Weekdays" and day.weekday() < 5:
            result.append(day)
        elif habit["frequency"] == "Weekly":
            week = day.isocalendar()[:2]
            if week not in week_seen:
                result.append(day)
                week_seen.add(week)
        day += timedelta(days=1)
    return result


def current_streak(habit, today=None):
    today = today or date.today()
    done = completed(habit)
    due = [day for day in targets(habit, min(done, default=today), today)]
    # Weekly target is represented by any completed day in that ISO week.
    if habit["frequency"] == "Weekly":
        weeks_done = {day.isocalendar()[:2] for day in done if day <= today}
        cursor = today.isocalendar()[:2]
        streak = 0
        while cursor in weeks_done:
            streak += 1
            monday = date.fromisocalendar(cursor[0], cursor[1], 1) - timedelta(days=7)
            cursor = monday.isocalendar()[:2]
        return streak
    streak = 0
    for day in reversed(due):
        if day not in done:
            break
        streak += 1
    return streak


def longest_streak(habit):
    done = sorted(completed(habit))
    if not done:
        return 0
    if habit["frequency"] == "Weekly":
        periods = sorted({d.isocalendar()[:2] for d in done})
        best = run = 1
        for a, b in zip(periods, periods[1:]):
            gap = date.fromisocalendar(*b, 1) - date.fromisocalendar(*a, 1)
            run = run + 1 if gap.days == 7 else 1
            best = max(best, run)
        return best
    best = run = 1
    previous = done[0]
    for day in done[1:]:
        gap = (day - previous).days
        allowed = gap == 1 if habit["frequency"] == "Daily" else gap <= 3 and all((previous + timedelta(days=n)).weekday() >= 5 for n in range(1, gap))
        run = run + 1 if allowed else 1
        best, previous = max(best, run), day
    return best


def monthly_rate(habit, year, month):
    first = date(year, month, 1)
    if (year, month) == (date.today().year, date.today().month):
        end = date.today()
    else:
        end = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    due = targets(habit, first, end)
    done = completed(habit)
    count = sum(day in done for day in due)
    return count, len(due), count * 100 / len(due) if due else 0


def choose_habit():
    for i, habit in enumerate(habits, 1):
        print(f"{i}. {habit['name']} ({habit['frequency']})")
    raw = input("Habit number: ").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= len(habits):
        print("Enter a valid habit number.")
        return None
    return int(raw) - 1


def main():
    print("===== PERSONAL HABIT & DAILY STREAK TRACKER =====")
    while True:
        print("\n1. Add habit\n2. View habits\n3. Check in today\n4. Delete habit\n5. View streaks\n6. Monthly completion rate\n7. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = input("Habit name: ").strip()
            if not name:
                print("Habit name cannot be empty.")
                continue
            print("1. Daily  2. Weekdays  3. Weekly")
            freq = input("Frequency: ").strip()
            if freq not in ("1", "2", "3"):
                print("Invalid frequency.")
                continue
            habits.append({"name": name, "frequency": FREQUENCIES[int(freq)-1], "check_ins": []})
            save_habits()
            print("Habit added.")
        elif choice == "2":
            print("No habits found." if not habits else "\n".join(f"{i}. {h['name']} ({h['frequency']})" for i, h in enumerate(habits, 1)))
        elif choice in ("3", "4", "5", "6"):
            if not habits:
                print("No habits found.")
                continue
            index = choose_habit()
            if index is None:
                continue
            habit = habits[index]
            if choice == "3":
                today = date.today()
                if habit["frequency"] == "Weekdays" and today.weekday() >= 5:
                    print("Today is not a scheduled weekday.")
                elif today in completed(habit):
                    print("Already checked in today.")
                else:
                    habit["check_ins"].append({"date": today.isoformat(), "timestamp": datetime.now().astimezone().isoformat(timespec="seconds")})
                    save_habits()
                    print("Check-in saved.")
            elif choice == "4":
                if input(f"Delete {habit['name']}? (y/N): ").strip().lower() == "y":
                    habits.pop(index)
                    save_habits()
                    print("Habit deleted.")
            elif choice == "5":
                streak = current_streak(habit)
                print(f"{habit['name']}: current streak {streak}, longest streak {longest_streak(habit)} target periods")
                print("Status:", "Missed target; streak broken" if completed(habit) and streak == 0 else "Active or not yet due")
            else:
                raw = input(f"Month YYYY-MM (default {date.today():%Y-%m}): ").strip() or date.today().strftime("%Y-%m")
                try:
                    selected = datetime.strptime(raw, "%Y-%m").date()
                    if selected.strftime("%Y-%m") != raw:
                        raise ValueError
                    done, due, rate = monthly_rate(habit, selected.year, selected.month)
                    print(f"{done}/{due} scheduled completions = {rate:.2f}%")
                except ValueError:
                    print("Invalid month. Use YYYY-MM, for example 2026-11.")
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1 through 7.")


if __name__ == "__main__":
    main()
