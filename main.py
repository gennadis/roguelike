import tcod

def main() -> None:

    # screen size settings
    screen_width = 80
    screen_height = 50

    # put the @ in the very middle
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    #load font file
    tileset = tcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
        )
    
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
            root_console.print(x=player_x, y=player_y, string='@')

            # this updates the screen
            context.present(root_console)

            for event in tcod.event.wait():
                if event.type == 'QUIT':
                    raise SystemExit()



if __name__ == '__main__':
    main()
