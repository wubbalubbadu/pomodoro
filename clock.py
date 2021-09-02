from datetime import datetime
from plan import Plan

DATE = str(datetime.date(datetime.now()))
TIME = str(datetime.time(datetime.now()))[:8]


def min_to_time(minute):
    return sec_to_time(minute * 60)


def sec_to_time(sec):
    return f"{sec // 60:02d}:{sec % 60:02d}"


def min_to_hour(minute):
    return round(minute / 60, 2)


class Clock:

    def __init__(self, plan: Plan):
        self.counting = False
        self.reps = 0
        self.plan = plan
        self.display_time = None

    def reset_timer(self):
        if self.counting:
            self.counting = False
            return True
        return False

    def start_timer(self):
        # shouldn't start timer if it's still counting
        if self.counting:
            return False
        # else start counting
        self.counting = True
        return True

    def update_rep(self) -> bool:
        self.counting = False
        if self.reps < 7:
            self.reps += 1
            return True
        self.reps = 0
        return False

    def is_counting(self) -> bool:
        return self.counting

    def get_first_task(self) -> str:
        return self.plan.reps_task_dict[0].get_name()

    def get_work_min(self) -> int:
        return self.plan.get_work_min()

    def get_short_break_min(self) -> int:
        return self.plan.get_short_break_min()

    def get_long_break_min(self) -> int:
        return self.plan.get_long_break_min()

    def get_projects(self) -> dict:
        return self.plan.get_projects()

    def get_current_task_name(self) -> str:
        return self.plan.reps_task_dict[self.reps].get_name()

    def get_current_task_length(self) -> int:
        return self.plan.reps_task_dict[self.reps].get_length()

    def get_current_task_color(self) -> int:
        return self.plan.reps_task_dict[self.reps].get_color()

    def get_current_task_length_sec(self) -> int:
        return self.get_current_task_length() * 60

    def get_finished_round(self) -> int:
        return self.reps // 2 + 1

    def get_cycle(self) -> int:
        return self.plan.get_cycles()
