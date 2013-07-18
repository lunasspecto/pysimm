# -*- coding: utf-8 -*-

# pyglet_console: to become a module for providing a pyglet console interface
# for pysimm.

import pyglet

class PygletConsole(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        kwargs = dict(kwargs)
        self.storyname = kwargs.pop('storyname', 'stuff')
        super(PygletConsole, self).__init__(args[0], args[1], **kwargs)
