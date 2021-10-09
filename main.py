import tcod
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main():
    # screen dimensions
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # load font tileset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # create instance of EventHandler class
    # that will receive events and process them
    event_handler = EventHandler()

    # create the main game window with parameters:
    # screen dimensions, tileset, title and vsync
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="YARG (Yet Another Rouguelike Game)",
        vsync=True,
    ) as context:

        # create the main game console in which
        # all objects will be drawn
        root_console = tcod.Console(
            screen_width, screen_height, order="F"
        )  # order="F" is for NumPy vectors

        # GAME LOOP
        while True:
            # put the players character objet to screen
            root_console.print(x=player_x, y=player_y, string="@")

            # update the game screen
            context.present(root_console)

            # clear the console after each move
            root_console.clear()

            for event in tcod.event.wait():

                # send the event to event_handler dispatch method
                action = event_handler.dispatch(event)

                # if no key was pressed or key was not recognized
                # then skip the game loop
                if action is None:
                    continue

                # if action is instance of MevementAction class then
                # we need to move player's character on the board
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                # if action is instance of EscapeAction then
                # quit the program
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
