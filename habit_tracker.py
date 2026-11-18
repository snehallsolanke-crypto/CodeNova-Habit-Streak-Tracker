
import json
import os
from datetime import date

if os.path.exists("habits.json"):
    with open("habits.json", "r") as file:
        habits = json.load(file)
else:
    habits = []


def save_habits():
    with open("habits.json", "w") as file:
        json.dump(habits, file, indent=4)


print("===== PERSONAL HABIT TRACKER =====")
print("Welcome to your Habit Tracker!")


while True:
    print("\n===== HABIT TRACKER MENU =====")
    print("1. Add New Habit")
    print("2. View All Habits")
    print("3. Mark Habit as Completed")
    print("4. Delete Habit")
    print("5. View Habit Streak")
    print("6. Monthly Completion Rate")
    print("7. Exit")

    choice = input("Enter your choice: ")

    # ADD NEW HABIT
    if choice == "1":
        habit_name = input("Enter your new habit: ").strip()

        if habit_name == "":
            print("Habit name cannot be empty!")
        else:
            habit = {
                "name": habit_name,
                "check_ins": []
            }

            habits.append(habit)
            save_habits()

            print("Habit added successfully!")

    # VIEW ALL HABITS
    elif choice == "2":
        if len(habits) == 0:
            print("No habits found!")
        else:
            print("\n===== YOUR HABITS =====")

            for index, habit in enumerate(habits, start=1):
                print(index, ".", habit["name"])

    # MARK HABIT AS COMPLETED
    elif choice == "3":
        if len(habits) == 0:
            print("No habits available!")
        else:
            print("\n===== YOUR HABITS =====")

            for index, habit in enumerate(habits, start=1):
                print(index, ".", habit["name"])

            habit_number = int(input("Enter habit number to complete: "))

            if 1 <= habit_number <= len(habits):
                today = date.today().isoformat()
                selected_habit = habits[habit_number - 1]

                if today not in selected_habit["check_ins"]:
                    selected_habit["check_ins"].append(today)
                    save_habits()
                    print("Habit marked as completed!")
                else:
                    print("Habit already completed today!")
            else:
                print("Invalid habit number!")

    # DELETE HABIT
    elif choice == "4":
        if len(habits) == 0:
            print("No habits to delete!")
        else:
            print("\n===== YOUR HABITS =====")

            for index, habit in enumerate(habits, start=1):
                print(index, ".", habit["name"])

            habit_number = int(input("Enter habit number to delete: "))

            if 1 <= habit_number <= len(habits):
                deleted_habit = habits.pop(habit_number - 1)
                save_habits()
                print(deleted_habit["name"], "deleted successfully!")
            else:
                print("Invalid habit number!")

    # VIEW HABIT STREAK
    elif choice == "5":
        if len(habits) == 0:
            print("No habits found!")
        else:
            print("\n===== YOUR HABITS =====")

            for index, habit in enumerate(habits, start=1):
                print(index, ".", habit["name"])

            habit_number = int(input("Enter habit number: "))

            if 1 <= habit_number <= len(habits):
                selected_habit = habits[habit_number - 1]
                completed_dates = selected_habit["check_ins"]

                current_streak = 0
                check_day = date.today()

                while check_day.isoformat() in completed_dates:
                    current_streak += 1
                    check_day = date.fromordinal(
                        check_day.toordinal() - 1
                    )

                print("Habit:", selected_habit["name"])
                print("Current Streak:", current_streak, "days")
                print("Total completed days:", len(completed_dates))
            else:
                print("Invalid habit number!")

    # MONTHLY COMPLETION RATE
    elif choice == "6":
        if len(habits) == 0:
            print("No habits found!")
        else:
            print("\n===== YOUR HABITS =====")

            for index, habit in enumerate(habits, start=1):
                print(index, ".", habit["name"])

            habit_number = int(input("Enter habit number: "))

            if 1 <= habit_number <= len(habits):
                selected_habit = habits[habit_number - 1]

                current_month = date.today().strftime("%Y-%m")
                completed_days = 0

                for check_date in selected_habit["check_ins"]:
                    if check_date.startswith(current_month):
                        completed_days += 1

                total_days = date.today().day
                rate = (completed_days / total_days) * 100

                print("Habit:", selected_habit["name"])
                print("Completed days this month:", completed_days)
                print("Monthly Completion Rate:", round(rate, 2), "%")
            else:
                print("Invalid habit number!")

    # EXIT
    elif choice == "7":
        print("Thank you for using Habit Tracker!")
        break

    else:
        print("Invalid choice! Please try again.")
