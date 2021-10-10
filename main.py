import tcod
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from entity import Entity
from procgen import generate_dungeon


def main() -> None:
    # screen dimensions
    screen_width = 80
    screen_height = 50

    # map dimensions
    map_width = 80
    map_height = 45

    # rooms creation parameters
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # load font tileset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # create instance of EventHandler class
    # that will receive events and process them
    event_handler = EventHandler()

    # main character's start coordinates
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # all entities creation
    player = Entity(player_x, player_y, "@", (255, 255, 0))
    npc = Entity(5, 5, "N", (220, 90, 30))
    entities = {npc, player}  # store all entitites in a set

    # create GameMap instance with a dungeons
    # with dungeons dimensions as parameters
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    # create the main game window with parameters:
    # screen dimensions, tileset, title and vsync
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:

        # create the main game console in which
        # all objects will be drawn
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # order="F" is for NumPy vectors

        # GAME LOOP
        while True:

            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
