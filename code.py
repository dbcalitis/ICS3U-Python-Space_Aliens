#!/usr/bin/env python3

# Created by: Daria Bernice Calitis
# Created on: Oct 2021
# This program is the "Space Aliens" program on the PyBadge

import ugame
import stage

import constants

def game_scene():
    # this function is the main game game_scene

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
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # set the background to image 0 in the image Bank
    #   and the size (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # a sprite that will be updated every frame
    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    alien = stage.Sprite(image_bank_sprites, 9,
                         int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
                         16)
    # create a stage for the background to show up on
    # and set the fram rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers of all sprites, items show up in order
    game.layers = [ship] + [alien] + [background]
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
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)
            else:
                ship.move(ship.x, ship.y)  # stays in the same position as before
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 1, ship.y)
            else:
                ship.move(ship.x, ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass
        
        
        # update game logic
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # redraw sprites
        game.render_sprites([ship])
        game.tick()

if __name__ == "__main__":
    game_scene()
