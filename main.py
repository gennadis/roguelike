import tcod
from engine import Engine
from input_handlers import EventHandler
from entity import Entity

def main() -> None:

    # screen size settings
    screen_width = 80
    screen_height = 50

    #load font file
    tileset = tcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
        )
    
    # create an instance of EventHandler class
    # to receive events and  process them
    event_handler = EventHandler()

    # initialize player and new NPC
    # and store them in set
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255))
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2) - 5, 'N', (255, 255, 0))
    entities = {player, npc}

    # create the engine instance, pass vars and use engine methods
    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    # create the screen with such parameters
    with tcod.context.new_terminal(
        screen_width, 
        screen_height, 
        tileset=tileset, 
        title='ROGUELIKE', 
        vsync=True
    ) as context:
        
        # create the console for drawing tiles
        # order='F' means [x, y] order in 2D numpy array
        root_console = tcod.Console(screen_width, screen_height, order='F')
        
        # main game loop
        while True:
            # print @ in colsole
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)



if __name__ == '__main__':
    main()
