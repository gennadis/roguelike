class Action:
    pass


# escape key press
class EscapeAction(Action):
    pass


# player movement
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
