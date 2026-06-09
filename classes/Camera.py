from classes.Maths import Vec2D


class Camera:
    VIEWPORT_TILES = 20
    FOLLOW_TILE = 10

    def __init__(self, pos, entity):
        self.pos = Vec2D(pos.x, pos.y)
        self.entity = entity
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32

    def move(self):
        xPosFloat = self.entity.getPosIndexAsFloat().x
        levelLength = getattr(self.entity.levelObj, "levelLength", self.VIEWPORT_TILES)
        maxOffset = max(0, levelLength - self.VIEWPORT_TILES)
        cameraOffset = min(max(xPosFloat - self.FOLLOW_TILE, 0), maxOffset)

        self.pos.x = -cameraOffset
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32
