#!/usr/bin/env python
#
# Name:    kittr.py
# Author:  Mike Pietruszka
# Date:    Mar 3rd, 2017
# Summary: kittr: Get random pics of kitties from Reddit
#

from __future__ import print_function
from sopel import module, tools
from random import randint
import random
import config
try:
    import praw
except ImportError:
    print("Could not find praw Reddit library. Exiting.")

'''
Define some memory dicts/lists for keeping track of pics that were already used
'''
def setup(bot):
    bot.memory['kitty_pics'] = []

'''
kittr setup; here we pull the kitty pics from Reddit.
'''
@module.interval(900)
def kittr_setup(bot):
    r = praw.Reddit(user_agent='sopel_get_kitty_pic')
    kitty_subreddits = ['aww', 'kitties', 'cats']
    global kitty_links
    kitty_links = {}

    for sub in kitty_subreddits:
        r_posts = r.get_subreddit(sub).get_new(limit=15)
        # each picture has an id, title, and a url; the id is the key and
        # title and url are values
        kitty_links = {s.id: [s.title, s.url] for s in r_posts}

    if len(kitty_links) > 0:
        print(kittr_setup.__name__ + " - Grabbed latest batch of kitty pics")

    return kitty_links

'''
Sample command to get kitty pics and check them against the memory. Memory is
necessary so we don't get repeats. We hold maximum of 15 pics in the memory.
'''
@module.rate(20)
@module.commands('kittypic')
def kittr_get_pic(bot, trigger):
    try:
        pics = kitty_links

        # first we pick a random pic, then we check if it is in the memory and if
        # the memory is full for each type of pics.
        while True:
            pic = random.choice(pics.keys())
            print(pic)
            if pic in bot.memory['kitty_pics']:
                pass
            elif len(bot.memory['kitty_pics']) >= 15:
                bot.say("Hold on, the kitties are coming!")
                break
            else:
                rand_submission = "Aww... [" + pics[pic][0] + "] " + pics[pic][1]
                print(kittr_get_pic.__name__ + " - " + rand_submission)
                bot.say(rand_submission)
                bot.memory['kitty_pics'].append(pic)
                break
    except (KeyError, IndexError, NameError) as err:
        if 'kittypic' in trigger.group(0):
            errmsg = "Got no kitties yet or got an error: " + str(err)
        else:
            print(trigger.group(0))
            errmsg = "Hold on, the kitties are coming!"
        bot.say(errmsg)
        dummy_arg = None
        kittr_setup(dummy_arg)
