import math

from utils import Rect
import settings

class ViewportManager(object):
    """
    The viewport has a deadband so it doesn't jitter on uneven track.
    It also has rate limiting to avoid it moving really jerkily.
    """

    def __init__(self, rect):
        self.rect = rect

    @property
    def y(self):
        return self.rect.y

    def __iter__(self):
        return iter(self.rect)

    def update(self, x, track_height):
        y = self.rect.y

        xnew = x - settings.VIEWPORT_OFFSET_X
        if track_height > 0:
            ynew = track_height - settings.VIEWPORT_OFFSET_Y
        else:
            ynew = y

        ychange = ynew - y

        if not abs(ychange) > settings.VIEWPORT_DEADBAND:
            ychange = 0

        # clip the y delta to the MAX_RATE and add to the original y.
        yactual = math.copysign(min(abs(ychange), settings.VIEWPORT_MAX_RATE), ychange) + y

        self.rect = Rect(xnew, yactual, self.rect.width, self.rect.height)

    def reset(self, rect):
        self.rect = rect
