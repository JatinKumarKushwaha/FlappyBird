import pygame


# Collisions with rectangles
def collision_rect(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# Collisions with sprite
def collision_sprite(player, obstacle_group):
    # If player is empty return False
    if not player:
        return False

    if pygame.sprite.spritecollide(player, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True
