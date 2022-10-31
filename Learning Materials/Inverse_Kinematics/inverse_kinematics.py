import sys
import time

import pygame
from pygame.math import Vector2

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)

size = width, height = 600, 600
screen = pygame.display.set_mode(size)

points = list(map(Vector2, [(300, 300), (400, 300),
              (500, 300)]))
target_speed = Vector2(3, 3)

rel_points = []
angles = []

max_angles = [90, -10, -10]  # Adjust for limited angles
min_angles = [10, -120, -120]

for i in range(1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)


def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += angle

    # honestly have no idea how this works
    angles[i] = min(max(180 - max_angles[i], (angles[i]+180) %
                    360), 180 - min_angles[i]) - 180

    return current_point + (endpoint-current_point).rotate(angle)


def render():
    black = 0, 0, 0
    white = 255, 255, 255

    screen.fill(white)
    for i in range(1, len(points)):
        prev = points[i-1]
        cur = points[i]
        pygame.draw.aaline(screen, black, prev, cur)
    for point in points:
        pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 5)
    pygame.draw.circle(screen, black, (int(target[0]), int(target[1])), 10)
    text_surface = my_font.render(str(angles[1]), False, (0, 0, 0))
    screen.blit(text_surface, (20, 20))
    pygame.display.flip()


n = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # points = list(map(Vector2, [(300, 300), (400, 300),
    #                             (500, 300), (540, 300)]))
    target = pygame.mouse.get_pos()
    target = (min(max(target[0], 400), 470), min(max(target[1], 200), 350))
    solve_ik(0, points[-1], target)
    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)

    render()

    pygame.time.wait(int(1000/60))
