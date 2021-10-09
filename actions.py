# main Action class
class Action:
    pass


# action on escape button pressed
# is Action subclass
class EscapeAction(Action):
    pass


# players movement action class
# is Action subclass
class MovementAction(Action):
    # dx & dy are directions in which player is moveing
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy


if __name__ == "__main__":
    pass
