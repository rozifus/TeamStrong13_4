# everything to do with the rubies

import pyglet
import settings
import entity
import utils

from utils import Vec2d, Point, Rect

class Ruby(entity.Entity):
    IMAGE = settings.RUBY_IMAGE

class RubyList(object):
    def __init__(self):
        super(RubyList, self).__init__()
        self.rubies = []
        self.visible_rubies = []

    def add_rubies(self, ruby_points):
        for ruby_point in ruby_points:
            x, y = ruby_point
            new_ruby = Ruby()
            new_ruby.gp = Point(x, y)
            self.rubies.append(new_ruby)

    def update_visible(self, viewport):
        self.visible_rubies = []
        for ruby in self.rubies:
            if self.ruby_in_rect(ruby, viewport):
                self.visible_rubies.append(ruby)

    def ruby_in_rect(self, ruby, rect):
        if utils.point_in_rect(ruby.gp, rect):
            result = True
        else:
            result = False

        return result

