from datetime import datetime
from tkinter import *
import pandas

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#6fde8b"
WHITE = "white"
FONT_NAME = "Courier"
CYCLE = 4
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
TASK1 = "flute"
TASK2 = "CS"

reps = 0
counting = False
timer = None

DATE = str(datetime.date(datetime.now()))
TIME = str(datetime.time(datetime.now()))[:8]

reps_dict = {}
for i in range(2 * CYCLE):
    if i % 2 == 0:
        reps_dict[i] = {"time": WORK_MIN,
                        "color": GREEN,
                        "text": "work"}
    elif i == 2 * CYCLE - 1:
        reps_dict[i] = {"time": LONG_BREAK_MIN,
                        "color": RED,
                        "text": "break"}
    else:
        reps_dict[i] = {"time": SHORT_BREAK_MIN,
                        "color": PINK,
                        "text": "break"}


def reset_timer():
    global reps, counting, timer
    if counting:
        root.after_cancel(timer)
        current_min = reps_dict[reps]["time"]
        canvas.itemconfig(timer_text, text=min_to_time(current_min))
        counting = False


def start_timer():
    global reps, counting
    if not counting:
        current_reps = reps_dict[reps]
        current_sec = current_reps["time"] * 60
        title.config(text=current_reps["text"], fg=current_reps["color"])
        count_down(current_sec)


def count_down(count):
    global reps, counting, timer
    if count > -1:
        display_time = f"{count // 60:02d}:{count % 60:02d}"
        canvas.itemconfig(timer_text, text=display_time)
        timer = root.after(1, count_down, count - 1)
        counting = True
    elif count == -1:
        print(reps)
        previous_reps = reps_dict[reps]
        if previous_reps["text"] == "work":
            finished_round = reps // 2 + 1
            check_mark.config(text=("✔️ " * finished_round))
            with open("journal.txt", mode="a") as journal:
                journal.write(f"{DATE},{TIME},{radio_state.get()}, {WORK_MIN}\n")
        if reps < 7:
            reps += 1
        else:
            reps = 0
            check_mark.config(text=f"{CYCLE} sessions completed", font=(FONT_NAME, 15), fg=RED)

        counting = False
        current_reps = reps_dict[reps]
        start_button.config(text=current_reps['text'].lower())
        title.config(text=current_reps["text"], fg=current_reps["color"])

        canvas.itemconfig(timer_text, text=min_to_time(reps_dict[reps]["time"]))


def print_report():
    window = Toplevel(root)
    window.title("Report")
    try:
        data = pandas.read_csv("journal.txt", sep=",", names=['date', 'time', 'project', 'focus time'])
    except FileNotFoundError:
        no_data_label = Label(window, text="No data found.", font=(FONT_NAME, 15))
        no_data_label.grid(row=0, column=0)
    else:
        today_label = Label(window, text=DATE, font=(FONT_NAME, 15))
        today_label.grid(row=0, column=0)
        today_data = Label(window, text=data[data["date"] == DATE][['time', 'project', 'focus time']],
                           font=(FONT_NAME, 15))
        today_data.grid(row=1, column=0)

        tally_label = Label(window, text="TALLY", font=(FONT_NAME, 15))
        tally_label.grid(row=2, column=0)

        task1_time = min_to_hour(data[data["project"] == TASK1]["focus time"].sum())
        task2_time = min_to_hour(data[data["project"] == TASK2]["focus time"].sum())
        other_time = min_to_hour(data[data["project"] == "NaN"]["focus time"].sum())
        tally_dict = {
            TASK1: [task1_time],
            TASK2: [task2_time],
            "Other": [other_time]
        }
        tally = pandas.DataFrame.from_dict(tally_dict)
        tally_data = Label(window, text=tally, font=(FONT_NAME, 15))
        tally_data.grid(row=3, column=0)
        window.mainloop()


def min_to_hour(minute):
    return round(minute / 60, 2)


def min_to_time(minute):
    return f"{minute:02d}:00"


# UI setup
# window
root = Tk()
root.title("Pomodoro")
root.config(padx=100, pady=50, bg=WHITE)
canvas = Canvas(width=200, height=224, bg=WHITE, highlightthickness=0)
tomato = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato)
timer_text = canvas.create_text(100, 130, text=min_to_time(WORK_MIN), fill=WHITE, font=(FONT_NAME, 40))
canvas.grid(row=1, column=1)

# Labels
title = Label(text=reps_dict[0]["text"], fg=GREEN, font=(FONT_NAME, 50))
title.grid(row=0, column=1)
check_mark = Label(fg=GREEN)
check_mark.grid(row=3, column=1)


# buttons
frame_buttons = Frame()
start_button = Button(frame_buttons, text=reps_dict[0]["text"], command=start_timer)
start_button.pack()
reset_button = Button(frame_buttons, text="Reset", command=reset_timer)
reset_button.pack()
report_button = Button(frame_buttons, text="Report", command=print_report)
report_button.pack()
frame_buttons.grid(row=2, column=2)

# radio buttons
task_frame = Frame()
radio_state = StringVar()
radiobutton1 = Radiobutton(task_frame, text=TASK1, value=TASK1, variable=radio_state)
radiobutton2 = Radiobutton(task_frame, text=TASK2, value=TASK2, variable=radio_state)
radiobutton1.pack()
radiobutton2.pack()
task_frame.grid(row=2, column=0)

root.mainloop()
