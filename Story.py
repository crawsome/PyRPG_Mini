# makes a story progression with 20 or so variable checkpoints
# each checkpoint requires decisions and talking?
# A narrative would have to be made
import textwrap

import Game


class TheStory:
    def __init__(self):
        Chapter1 = Chapter(1, 'Haunted House', 'd', 'o', 'e')
        pass


class Chapter:
    def __init__(self, chapnum, chapname, answer1, answer2, answer3, story1, story2, story3):
        self.chapternum = chapnum
        self.chaptername = chapname
        self.ans1 = answer1
        self.ans2 = answer2
        self.ans3 = answer3
        self.story1 = story1
        self.story2 = story2
        self.story3 = story3
        self.done = False
        pass

    def story1(self):
        wrapstring = textwrap.wrap(self.story1, width=48)
        for line in wrapstring:
            Game.centerprint(line)

    def story2(self):
        pass

    def story3(self):
        pass


# Different scenarios, to spice the game up a little bit.
# 2 diff choices on entrance, 4 inside, 2 on each.
def hauntedhouse():
    pass


def swamp():
    pass


def plains():
    pass


def mountain():
    pass


def dream():
    pass


def revolution():
    pass


def future():
    pass


def story():
    pass
