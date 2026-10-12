"""PawPal+ backend class skeletons based on the initial UML draft.

Behavior will be implemented in a later phase.
"""


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        pass


class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks: list[CareTask] = []

    def add_task(self, task: "CareTask") -> None:
        pass


class CareTask:
    def __init__(self, title: str, duration_minutes: int, priority: str):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority

    def describe(self) -> str:
        pass


class Scheduler:
    def __init__(self, available_minutes: int):
        self.available_minutes = available_minutes

    def generate_schedule(self, tasks: list[CareTask]) -> list[CareTask]:
        pass

    def explain_plan(self, plan: list[CareTask]) -> str:
        pass
