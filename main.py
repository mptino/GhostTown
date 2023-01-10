""" 
Filename: main.py
Purpose: The main file to run Ghost Town. 
Author: Matthew Peres Tino

"""

#####################################################################################################
# Local
from settings import *
from sprites import *

#####################################################################################################

# load control class
game_control = Control()

# load sprites
player = Player()
player_sprite = pg.sprite.Group()
player_sprite.add(player)
enemy_sprite = pg.sprite.Group()
enemy_sprite.add(Enemy(menu = False, player = player))
tree_sprite = pg.sprite.Group()
tree_sprite.add(Tree())

# wave class
wave = Wave(enemy_sprite)

# sprites for menu
enemy_dark_sprite = pg.sprite.Group()
enemy_dark_sprite.add(Enemy(menu = True))

# setting related
run = True 
clock = pg.time.Clock()


########## MENU OPTIONS ###########
while not game_control.start_game:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            game_control.check_click()
        if event.type == ENEMY_SPAWN:
            enemy_dark_sprite.add(Enemy(menu = True))

    # draw menu
    game_control.draw_menu()    

    # menu ghosts
    enemy_dark_sprite.draw(WIN)
    enemy_dark_sprite.update()

    # updates
    game_control.update()
    pg.display.update()
    clock.tick(FPS)


# OUTCOME 1
# quickly check if the user decided to exit instead of play
if game_control.quit_game:
    sys.exit()

# OUTCOME 2
# also check if options was clicked
while game_control.go_to_options:
    print('hello')
    game_control.go_to_options = False

# OUTCOME 3
# now check if play was clicked
########## GAME WILL BEGIN ###########
pg.display.set_caption("Ghost Town - Play") # game name

while not game_control.quit_game:

        for event in pg.event.get():

            # if user quits
            if event.type == pg.QUIT:
                sys.exit()
            
            # spawn enemy
            if event.type == ENEMY_SPAWN:
                enemy_sprite.add(Enemy(menu = False, player = player))
            
            # handle shooting
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()


        # put collisions here for now
        if pg.sprite.spritecollideany(player, enemy_sprite):
            player.curr_health -= 5
            if player.curr_health < 1 : 
                run = False

        if pg.sprite.groupcollide(player.ammo, enemy_sprite, dokilla=True, dokillb=True):
            wave.score += 1


        # drawing stuff
        game_control.draw_game()
        enemy_sprite = wave.update()

        # handle the trees 
        tree_sprite.draw(WIN)

        # draw sprites
        player_sprite.draw(WIN)
        enemy_sprite.draw(WIN) 
        player.ammo.draw(WIN) 

        # sprite updates
        enemy_sprite.update()
        player.update()
        player.ammo.update()
        

        # setting stuff
        pg.display.update()
        clock.tick(FPS)
