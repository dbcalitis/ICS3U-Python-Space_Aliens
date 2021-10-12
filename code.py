#!/usr/bin/env python3

# Created by: Daria Bernice Calitis
# Created on: Oct 2021
# This program is the "Space Aliens" program on the PyBadge

import ugame
import stage
import time
import random
import board
import neopixel

import constants


def splash_scene():
    # this function is the splash scene

    # get sound ready
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # image banks for CircuitPython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # set the background to image 0 in the image Bank
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    # used this program to split the image into tile: 
    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # create a stage for the background to show up on
    # and set the fram rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers of all sprites, items show up in order
    game.layers = [background]
    # render all sprites
    #   most likely you will only render the background once per game game_scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # Wait for 2 seconds
        time.sleep(2.0)
        menu_scene()

    # repeat forever, game Loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START:
            game_scene()

        # redraw sprites
        game.tick()


def menu_scene():
    # this function is the menu scene

    # image banks for CircuitPython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # add text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # set the background to image 0 in the image Bank
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    # create a stage for the background to show up on
    # and set the fram rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers of all sprites, items show up in order
    game.layers = text + [background]
    # render all sprites
    #   most likely you will only render the background once per game game_scene
    game.render_block()

    # repeat forever, game Loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START:
            game_scene()

        # redraw sprites
        game.tick()


def game_scene():
    # this function is the main game game_scene

    def show_alien():
        # this function takes an alien from off screen and moves it on screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(
                    random.randint(0 + constants.SPRITE_SIZE,
                                   constants.SCREEN_X - constants.SPRITE_SIZE),
                                   constants.OFF_TOP_SCREEN)
                break

    # for score
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0,0)
    score_text.move(1,1)
    score_text.text("Score: {0}".format(score))

    # image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # buttons that you want to keep the state of information of
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    boom_sound = open("boom.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # set the background to image 0 in the image Bank
    #   and the size (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_X):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # a sprite that will be updated every frame
    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_sprites, 9,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)
        aliens.append(a_single_alien)
    # place 1 alien on the screen
    show_alien()

    # create list of lasers for when we shoot
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_sprites, 10,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)
        lasers.append(a_single_laser)

    # the 5 pixels on the PyBadge
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, auto_write=False)
    for pixel in range(5):
        pixels[pixel] = (0, 10, 0)
    pixels.show()
    
    # create a stage for the background to show up on
    # and set the fram rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers of all sprites, items show up in order
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    # render all sprites
    #   most likely you will only render the background once per game game_scene
    game.render_block()

    # repeat forever, game Loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # A button
        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        # B button
        if keys & ugame.K_X:
            pass
        if keys & ugame.K_START:
            pass
        if keys & ugame.K_SELECT:
            pass
        if keys & ugame.K_RIGHT:
            if ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + constants.SHIP_SPEED, ship.y)
            else:
                ship.move(ship.x, ship.y)  # stays in the same position as before
        if keys & ugame.K_LEFT:
            if ship.x > 0:
                ship.move(ship.x - constants.SHIP_SPEED, ship.y)
            else:
                ship.move(ship.x, ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass
        
        
        # update game logic
        if a_button == constants.button_state["button_just_pressed"]:
            # fire a laser, if we have enough power (have not used up all the lasers)
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x <= -1: # checks if it's off the screen
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break
        
        # moves the lasers
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > -1: # checks if it's on the screen
                lasers[laser_number].move(lasers[laser_number].x,
                                          lasers[laser_number].y -
                                          constants.LASER_SPEED)
                # checks if there is a laser on the screen
                for laser in range(len(lasers)):
                    if lasers[laser].x > -1 :
                        for pixel in range(len(pixels)):
                            if pixels[pixel] == (10, 10, 0) or all(lasers[laser_num].x > constants.OFF_SCREEN_X for laser_num in range(len(lasers))):
                                break
                            pixels[pixel] = (10, 10, 0) # lights turn yellow
                            pixels.show()
                
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN: # checks if it's off the screen
                    lasers[laser_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)

        # checks if the lasers are full
        if all(lasers[laser].x == constants.OFF_SCREEN_X for laser in range(len(lasers))):
            for pixel in range(len(pixels)):
                if pixels[pixel] == (0, 10, 0):
                    break
                pixels[pixel] = (0, 10, 0) # lights turn green
                pixels.show()
        
        # checks if it's out of lasers
        if all(lasers[laser].x > constants.OFF_SCREEN_X for laser in range(len(lasers))):
            for pixel in range(len(pixels)):
                if pixels[pixel] == (10, 0, 0):
                    break
                pixels[pixel] = (10, 0, 0) # lights turn red
                pixels.show()
        
        # each frame move the aliens down, that are on the screen
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x,
                                          aliens[alien_number].y +
                                          constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
                    show_alien()
                    score -= 1
                    if score < 0:
                        score = 0
                    score_text.clear()
                    score_text.cursor(0,0)
                    score_text.move(1,1)
                    score_text.text("Score: {0}".format(score))

        # each frame check if any of the lasers are touching any of the aliens
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        if stage.collide(lasers[laser_number].x + 6, lasers[laser_number].y + 2,
                                         lasers[laser_number].x + 11, lasers[laser_number].y + 12,
                                         aliens[alien_number].x + 1 , aliens[alien_number].y,
                                         aliens[alien_number].x + 15, aliens[alien_number].y + 15):
                            # you hit an alien
                            aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            show_alien()
                            score += 1
                            score_text.clear()
                            score_text.cursor(0,0)
                            score_text.move(1,1)
                            score_text.text("Score: {0}".format(score))
        # redraw sprites
        game.render_sprites(lasers + [ship] + aliens)
        game.tick()

if __name__ == "__main__":
    splash_scene()
