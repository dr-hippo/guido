import config as cfg
import utilities as utils
import pygame
from pygame.sprite import Sprite
from pygame import Rect, Vector2
from physicsbody import PhysicsBody

pygame.init()


class SnakeCharmer(Sprite, PhysicsBody):
    def __init__(self, scene, position):
        Sprite.__init__(self)
        PhysicsBody.__init__(self, position, velocity=Vector2(0, 0), acceleration=Vector2(0, 0))
        self.scene = scene

        # TODO: probably could refactor this
        self.images = {}
        for imagename in utils.get_filenames("images", "snakecharmer", filetype="png"):
            self.images[imagename] = utils.load_image(imagename, "snakecharmer")

        self.sounds = {}
        for soundname in utils.get_filenames("audio", "snakecharmer", filetype="mp3"):
            self.sounds[soundname] = utils.load_audio(soundname, "snakecharmer", filetype="mp3")

        self.jump_sound_channel = pygame.mixer.find_channel()

        self.image = self.images["right0"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=position)
        self.movingleft = False
        self.movingright = False
        self.image_direction = "right"

        self.time_since_walk_start = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.groundcheck():
                    self.jump()

                if event.key == pygame.K_a:
                    self.movingleft = True
                    self.image_direction = "left"

                if event.key == pygame.K_d:
                    self.movingright = True
                    self.image_direction = "right"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movingleft = False
                    self.time_since_walk_start = 0

                if event.key == pygame.K_d:
                    self.movingright = False
                    self.time_since_walk_start = 0

    def update(self, dt):
        Sprite.update(self)
        PhysicsBody.update(self, dt)

        # change image depending on direction and grounded state
        self.image = self._get_image()

        # TODO: make this use PhysicsBody.addforce() once that works
        if self.movingleft:
            self.position.x -= cfg.SNAKECHARMER_MOVE_SPEED * cfg.GRIDSIZE * dt

        if self.movingright:
            self.position.x += cfg.SNAKECHARMER_MOVE_SPEED * cfg.GRIDSIZE * dt

        if self.movingleft or self.movingright:
            self.time_since_walk_start += dt

        self.rect.midbottom = self.position
        self.handle_collisions()

    def _get_image(self):
        # if grounded, get walk frames, otherwise display jump/fall sprites
        if self.groundcheck():
            # 3 frames, change every 1/6 secs
            frame_index = round(self.time_since_walk_start * 6) % 3
            name = self.image_direction + str(frame_index)

        # if jumping up, display jump frame
        elif self.velocity.y < 0:
            name = self.image_direction + "-jump"

        # otherwise player is falling, display fall frames
        else:
            name = self.image_direction + "-drop"

        return self.images[name]

    def jump(self):
        # TODO: this is a temporary fix, need to make addforce consistent
        self.velocity.y = -cfg.SNAKECHARMER_JUMP_FORCE
        # self.addforce(Vector2(0, -cfg.SNAKECHARMER_JUMP_FORCE), impulse=True)
        self.jump_sound_channel.play(self.sounds["jump"])

    def get_collisions(self):
        collided_tiles = self.scene.data.get_sprite_collisions(self, "Wall", "Apple", "Door")
        collided_snakeblocks = pygame.sprite.spritecollide(self, self.scene.snake[1:], False)
        return [self.rect.clip(c.rect) for c in collided_tiles + collided_snakeblocks]

    def groundcheck(self):
        # check if one pixel beneath left or right bottom corners is ground (wall, snake, or apple)
        rects = [sprite.rect for sprite in self.scene.snake[1:]] + \
                self.scene.data.get_rects("Apple", "Wall", "Door")

        for rect in rects:
            if rect.collidepoint(self.rect.bottomleft) or \
                    rect.collidepoint(Vector2(self.rect.bottomright[0] - 1, self.rect.bottomright[1])):
                return True

        return False

    def handle_collisions(self):
        # if player hits snake head, die
        if pygame.sprite.collide_mask(self, self.scene.snake[0]):
            self.scene.on_death("Snake ate Guido ;(")
            self.sounds["chewed"].play()

        for rect in self.get_collisions():
            # if this has already been resolved, no need to resolve
            if self.rect.clip(rect).size == (0, 0):
                continue

            if rect.w > rect.h:
                if self.rect.top == rect.top:
                    self.velocity.y = 0
                    self.position.y += rect.h
                    self.rect.midbottom = self.position
                    if self.rect.clip(rect).size == (0, 0):
                        continue

                if self.rect.bottom == rect.bottom:
                    self.velocity.y = 0
                    self.position.y -= rect.h
                    self.rect.midbottom = self.position
                    if self.rect.clip(rect).size == (0, 0):
                        continue

            else:
                if self.rect.left == rect.left:
                    self.velocity.x = 0
                    self.position.x += rect.w
                    self.rect.midbottom = self.position
                    if self.rect.clip(rect).size == (0, 0):
                        continue

                if self.rect.right == rect.right:
                    self.velocity.x = 0
                    self.position.x -= rect.w
                    self.rect.midbottom = self.position
                    if self.rect.clip(rect).size == (0, 0):
                        continue
