# makes a story progression with 20 or so variable checkpoints
# each checkpoint requires decisions and talking?
# A narrative would have to be made


class Story:
    def __init__(self):
        self.hauntedhousecomplete = 0
        self.swampcomplete = 0
        self.plainscomplete = 0
        self.mountaincomplete = 0
        self.dreamcomplete = 0
        self.revolutioncomplete = 0
        self.storycomplete = 0


# Different scenarios, to spice the game up a little bit.
# 2 diff choices on entrance, 4 inside, 2 on each.
def hauntedhouse():
    vhpick = input('You arrive at a spooky house.\n'
                   'There\'s a green van out front.\n'
                   'Inspect the [v]an or go to the  \n'
                   '[h]ouse and knock on the door?\n')
    if vhpick == 'v':
        pass
    elif vhpick == 'h':
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
