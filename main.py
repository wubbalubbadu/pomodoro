from ui import UserInterface
from plan import Plan
from clock import Clock

plan = Plan()
clock = Clock(plan)
ui = UserInterface(clock)
