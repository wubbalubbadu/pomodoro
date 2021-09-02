from task import Task

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#6fde8b"
WHITE = "white"
FONT_NAME = "Courier"


class Plan:

    def __init__(self, **kwargs):

        self.reps_task_dict = {}
        self.project_dict = {}
        default = {
            'cycle': 4,
            'work_min': 25,
            'short_break_min': 5,
            'long_break_min': 25
        }
        default.update(kwargs)
        self.work_min = default.get('work_min')
        self.short_break_min = default.get('short_break_min')
        self.long_break_min = default.get('long_break_min')
        self.cycle = default.get('cycle')

        try:
            with open('data/projects.txt', 'r') as f:
                project_list = f.read().splitlines()
                if len(project_list) == 0:
                    project_list = ['Flute', 'CS']
            for n in range(len(project_list)):
                self.project_dict[f'task{n+1}'] = project_list[n]
        except FileNotFoundError:
            pass

        for i in range(2 * self.cycle):
            if i % 2 == 0:
                self.reps_task_dict[i] = Task(length=self.work_min,
                                              color=GREEN,
                                              name='work')
            elif i == 2 * self.cycle - 1:
                self.reps_task_dict[i] = Task(length=self.long_break_min,
                                              color=RED,
                                              name='break')
            else:
                self.reps_task_dict[i] = Task(length=self.short_break_min,
                                              color=PINK,
                                              name='break')

    def get_projects(self) -> dict:
        return self.project_dict

    def get_work_min(self) -> int:
        return self.work_min

    def get_short_break_min(self) -> int:
        return self.short_break_min

    def get_long_break_min(self) -> int:
        return self.long_break_min

    def get_cycles(self) -> int:
        return self.cycle
