#!/usr/bin/env python3

"""
This script allows you to manually control the simulator
using the keyboard arrows.
"""

import sys
import argparse
import pyglet
import math
from pyglet.window import key
import numpy as np
import gym
import gym_miniworld

parser = argparse.ArgumentParser()
parser.add_argument('--env-name', default='MiniWorld-Hallway-v0')
parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
parser.add_argument('--no-time-limit', action='store_true', help='ignore time step limits')
args = parser.parse_args()

env = gym.make(args.env_name)
env.reset()

if args.no_time_limit:
    env.max_episode_steps = math.inf

# Create the display window
env.render('pyglet')

@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """

    if symbol == key.BACKSPACE or symbol == key.SLASH:
        print('RESET')
        env.reset()
        env.render('pyglet')
        return

    if symbol == key.ESCAPE:
        env.close()
        sys.exit(0)

    action = None
    num_repeat = 1

    if symbol == key.UP:
        action = env.actions.move_forward
        if key_handler[key.LSHIFT] or key_handler[key.RSHIFT]:
            num_repeat = 3
    elif symbol == key.DOWN:
        action = env.actions.move_back
        if key_handler[key.LSHIFT] or key_handler[key.RSHIFT]:
            num_repeat = 3
    elif symbol == key.LEFT:
        action = env.actions.turn_left
    elif symbol == key.RIGHT:
        action = env.actions.turn_right
    elif symbol == key.PAGEUP or symbol == key.P:
        action = env.actions.pickup
    elif symbol == key.PAGEDOWN or symbol == key.D:
        action = env.actions.drop

    if action != None:
        for _ in range(num_repeat):
            obs, reward, done, info = env.step(action)
            #print('step_count = %s, reward=%.2f' % (env.unwrapped.step_count, reward))

            if done:
                print('done! reward={:.2f}'.format(reward))
                env.reset()
                break

        env.render('pyglet')

@env.unwrapped.window.event
def on_close():
    pyglet.app.exit()

# Register a keyboard handler
key_handler = key.KeyStateHandler()
env.unwrapped.window.push_handlers(key_handler)

# Enter main event loop
pyglet.app.run()

env.close()
