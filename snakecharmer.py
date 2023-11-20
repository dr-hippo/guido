import config as cfg
import utilities as utils
import pygame
from pygame.sprite import Sprite, Group
from pygame import Rect, Vector2
from physicsbody import PhysicsBody

pygame.init()


class SnakeCharmer(Sprite, PhysicsBody):
    def __init__(self, scene, position):
        Sprite.__init__(self)
        PhysicsBody.__init__(self, position, velocity=Vector2(0, 0), acceleration=Vector2(0, 0))
        self.scene = scene
        self.image = utils.load_image("snakecharmer", "snakecharmer")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=position)
        self.movingleft = False
        self.movingright = False
        self.intersecting_rects = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    # jump
                    self.addforce(Vector2(0, -cfg.SNAKECHARMER_JUMP_FORCE), impulse=True)

                if event.key == pygame.K_a:
                    self.movingleft = True

                if event.key == pygame.K_d:
                    self.movingright = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movingleft = False

                if event.key == pygame.K_d:
                    self.movingright = False

    def update(self, dt):
        Sprite.update(self)
        PhysicsBody.update(self, dt)
        if self.movingleft:
            self.position.x -= cfg.SNAKECHARMER_MOVE_SPEED * cfg.GRIDSIZE * dt

        if self.movingright:
            self.position.x += cfg.SNAKECHARMER_MOVE_SPEED * cfg.GRIDSIZE * dt

        self.position.y = pygame.math.clamp(self.position.y, 0, pygame.display.get_surface().get_rect().h)
        self.rect.midbottom = self.position
        self.handle_collisions()

    def get_collisions(self):
        collided_tiles = pygame.sprite.spritecollide(self, self.scene.data.groups["wall"], False)
        collided_apples = pygame.sprite.spritecollide(self, self.scene.data.groups["apple"], False)
        collided_snakeblocks = pygame.sprite.spritecollide(self, self.scene.snake.blocks.sprites()[1:], False)
        return [self.rect.clip(c.rect) for c in collided_tiles + collided_apples + collided_snakeblocks]

    def get_collision_directions(self, rect):
        return {
            "up": self.rect.top == rect.top,
            "down": self.rect.bottom == rect.bottom,
            "left": self.rect.left == rect.left,
            "right": self.rect.right == rect.right
        }

    def groundcheck(self):
        # check if one pixel beneath left or right bottom corners is ground
        return

    def handle_collisions(self):
        # if player hits snake head, die
        if pygame.sprite.collide_mask(self, self.scene.snake.blocks.sprites()[0]):
            self.scene.on_death("Snake ate Guido ;(")

        # if player reaches a goal flag, go to next level
        if pygame.sprite.spritecollideany(self, self.scene.data.groups["goal"], pygame.sprite.collide_mask):
            self.scene.to_nextlevel()

        self.intersecting_rects = self.get_collisions()

        iteration_count = 0
        for rect in self.intersecting_rects:
            # if this has already been resolved, no need to resolve
            if self.rect.clip(rect).size == (0, 0):
                continue

            if self.get_collision_directions(rect)["up"]:
                self.velocity = Vector2(0, 0)
                self.position.y += rect.h
                self.rect.midbottom = self.position
                if self.rect.clip(rect).size == (0, 0):
                    continue

            if self.get_collision_directions(rect)["down"]:
                self.velocity = Vector2(0, 0)
                self.position.y -= rect.h
                self.rect.midbottom = self.position
                if self.rect.clip(rect).size == (0, 0):
                    continue

            if self.get_collision_directions(rect)["left"]:
                self.position.x += rect.w
                self.rect.midbottom = self.position
                if self.rect.clip(rect).size == (0, 0):
                    continue

            if self.get_collision_directions(rect)["right"]:
                self.position.x -= rect.w
                self.rect.midbottom = self.position
                if self.rect.clip(rect).size == (0, 0):
                    continue

            self.intersecting_rects = self.get_collisions()

            iteration_count += 1
            if iteration_count > 100:
                raise SystemExit("Infinite loop while resolving collision")
