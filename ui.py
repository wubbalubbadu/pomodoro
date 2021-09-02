from tkinter import *
from clock import *
import pandas

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#6fde8b"
WHITE = "white"
FONT_NAME = "Courier"


class UserInterface:
    def __init__(self, clock: Clock):
        self.clock = clock
        self.timer = None

        # fields in settings
        self.row = 0
        self.focus_time_entry = None
        self.short_break_entry = None
        self.long_break_entry = None
        self.cycle_entry = None
        self.project_entries = []

        # window
        self.root = Tk()
        self.root.title("Pomodoro")
        self.root.config(padx=100, pady=50, bg=WHITE)
        self.canvas = Canvas(width=200, height=224, bg=WHITE, highlightthickness=0)
        tomato = PhotoImage(file='tomato.png')
        self.canvas.create_image(100, 112, image=tomato)
        self.timer_text = self.canvas.create_text(100, 130, text=min_to_time(self.clock.get_current_task_length()),
                                                  fill=WHITE, font=(FONT_NAME, 40))
        self.canvas.grid(row=1, column=1)

        # Labels
        self.title = Label(text=self.clock.get_first_task(), fg=GREEN, font=(FONT_NAME, 50))
        self.title.grid(row=0, column=1)
        self.check_mark = Label(fg=GREEN)
        self.check_mark.grid(row=3, column=1)

        # buttons
        self.frame_buttons = Frame()
        self.start_button = Button(self.frame_buttons, text=self.clock.get_first_task(), command=self.start_timer)
        self.start_button.pack()
        reset_button = Button(self.frame_buttons, text="Reset", command=self.reset_timer)
        reset_button.pack()
        report_button = Button(self.frame_buttons, text="Report", command=self.print_report)
        report_button.pack()
        setting_button = Button(self.frame_buttons, text="Setting", command=self.setting)
        setting_button.pack()

        self.frame_buttons.grid(row=2, column=2)

        # radio buttons
        self.task_frame = Frame()
        self.radio_state = StringVar()
        self.display_buttons()
        self.root.mainloop()

    def display_buttons(self):
        self.task_frame.destroy()
        self.task_frame = Frame()
        for (project_num, project_name) in self.clock.get_projects().items():
            radiobutton = Radiobutton(
                self.task_frame,
                text=project_name,
                value=project_name,
                variable=self.radio_state)
            radiobutton.pack()
        self.task_frame.grid(row=2, column=0)

    def start_timer(self):
        if self.clock.start_timer():
            self.title.config(text=self.clock.get_current_task_name(),
                              fg=self.clock.get_current_task_color())
            self.count_down(self.clock.get_current_task_length_sec())

    def reset_timer(self):
        if self.clock.reset_timer():
            self.root.after_cancel(self.timer)
            self.display_paused_time()

    def display_paused_time(self):
        self.canvas.itemconfig(self.timer_text, text=min_to_time(self.clock.get_current_task_length()))

    def count_down(self, count):
        if count > -1:
            self.canvas.itemconfig(self.timer_text, text=sec_to_time(count))
            self.timer = self.root.after(1, self.count_down, count - 1)
        elif count == -1:
            if self.clock.get_current_task_name() == "work":
                self.check_mark.config(text=("✔️ " * self.clock.get_finished_round()))
                with open("data/journal.txt", mode="a") as journal:
                    journal.write(f"{DATE},{TIME},{self.radio_state.get()}, {self.clock.get_work_min()}\n")
            if not self.clock.update_rep():
                self.check_mark.config(text=f"{self.clock.get_cycle()} sessions completed", font=(FONT_NAME, 15),
                                       fg=RED)

            self.start_button.config(text=self.clock.get_current_task_name().lower())
            self.title.config(text=self.clock.get_current_task_name(), fg=self.clock.get_current_task_color())
            self.display_paused_time()

    def print_report(self):
        window = Toplevel(self.root)
        window.title("Report")
        try:
            data = pandas.read_csv("data/journal.txt", sep=",", names=['date', 'time', 'project', 'focus time'])
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
            tally_dict = {}
            print(data)
            for (key, value) in self.clock.get_projects().items():
                task_time = min_to_hour(data[data["project"] == value]["focus time"].sum())
                tally_dict[value] = [task_time]
            print(data[data["project"] == ""])
            other_time = min_to_hour(data[data["project"].isnull()]["focus time"].sum())
            print(other_time)
            tally_dict['Other'] = [other_time]
            print(tally_dict)
            tally = pandas.DataFrame.from_dict(tally_dict)
            tally_data = Label(window, text=tally, font=(FONT_NAME, 15))
            tally_data.grid(row=3, column=0)

            window.mainloop()

    def setting(self):
        self.setting_window = Tk()
        self.setting_window.title("Setting")

        focus_time_label = Label(self.setting_window, text="Focus time: ")
        focus_time_label.grid(row=self.row, column=0)
        self.focus_time_entry = Entry(self.setting_window, width=5)
        self.focus_time_entry.grid(row=self.row, column=1)
        self.focus_time_entry.focus()
        self.focus_time_entry.insert(0, str(self.clock.get_work_min()))
        self.row += 1

        short_break_label = Label(self.setting_window, text="Short break time: ")
        short_break_label.grid(row=self.row, column=0)
        self.short_break_entry = Entry(self.setting_window, width=5)
        self.short_break_entry.grid(row=self.row, column=1)
        self.short_break_entry.insert(0, str(self.clock.get_short_break_min()))
        self.row += 1

        long_break_label = Label(self.setting_window, text="Long break time: ")
        long_break_label.grid(row=self.row, column=0)
        self.long_break_entry = Entry(self.setting_window, width=5)
        self.long_break_entry.grid(row=self.row, column=1)
        self.long_break_entry.insert(0, str(self.clock.get_long_break_min()))
        self.row += 1

        cycle_label = Label(self.setting_window, text="Number of cycles: ")
        cycle_label.grid(row=self.row, column=0)
        self.cycle_entry = Entry(self.setting_window, width=5)
        self.cycle_entry.grid(row=self.row, column=1)
        self.cycle_entry.insert(0, '4')
        self.row += 1

        project_1_label = Label(self.setting_window, text="Project 1: ")
        project_1_label.grid(row=self.row, column=0)
        project_1_entry = Entry(self.setting_window, width=5)
        project_1_entry.insert(0, 'Flute')
        project_1_entry.grid(row=self.row, column=1)
        self.row += 1
        self.project_entries.append(project_1_entry)

        project_2_label = Label(self.setting_window, text="Project 2: ")
        project_2_label.grid(row=self.row, column=0)
        project_2_entry = Entry(self.setting_window, width=5)
        project_2_entry.insert(0, 'CS')
        project_2_entry.grid(row=self.row, column=1)
        self.row += 1
        self.project_entries.append(project_2_entry)

        confirm_button = Button(self.setting_window, text='confirm', command=self.confirm)
        confirm_button.grid(row=0, column=2, columnspan=2)

        add_task_button = Button(self.setting_window, text='add task', command=self.add)
        add_task_button.grid(row=3, column=2, columnspan=2)

        self.setting_window.mainloop()

    def confirm(self):
        with open('data/projects.txt', 'w') as f:
            f.truncate(0)
        with open('data/projects.txt', 'a') as f:
            for project in self.project_entries:
                f.write(f'{project.get()}\n')
        parameters = {
            'work_min': int(self.focus_time_entry.get()),
            'short_break_min': int(self.short_break_entry.get()),
            'long_break_min': int(self.long_break_entry.get()),
            'cycle': int(self.cycle_entry.get())
        }
        self.clock.plan = Plan(**parameters)
        self.display_paused_time()
        self.display_buttons()

    def add(self):
        num_of_projects = len(self.project_entries)
        num_of_projects += 1
        new_project_label = Label(self.setting_window, text=f"Project {num_of_projects}: ")
        new_project_label.grid(row=self.row, column=0)
        new_project_entry = Entry(self.setting_window, width=5)
        new_project_entry.grid(row=self.row, column=1)
        self.project_entries.append(new_project_entry)
        self.row += 1
