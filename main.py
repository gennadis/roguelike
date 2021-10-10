import copy
import tcod
import entity_factories
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

    # monsters number in rooms
    max_monsters_per_room = 2

    # load font tileset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # create instance of EventHandler class
    # that will receive events and process them
    event_handler = EventHandler()

    # all entities creation
    player = copy.deepcopy(entity_factories.player)

    # create GameMap instance with a dungeons
    # with dungeons dimensions as parameters
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        player=player,
    )

    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    # create the main game window with parameters:
    # screen dimensions, tileset, title and vsync
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="YARG: Yet Another Roguelike Game",
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
