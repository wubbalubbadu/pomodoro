class Task:
    def __init__(self, length, color, name):
        self.length = length
        self.color = color
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_length(self) -> str:
        return self.length

    def get_color(self) -> str:
        return self.color
