#2D inverse kinematics
from pygame.math import Vector2
a = Vector2(200, -100)
b = Vector2(200, 100)
c = a - b
alpha = a.angle_to(b)

points = list(map(Vector2, [(100, 100), (200, 100), (300, 100)]))
target = Vector2(450, 300)

rel_points = []
angles = []

for i in range (1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)

i = len(points)-2 # second-to-last index
endpoint = a
current_point = b

angle = (endpoint-current_point).angle_to(target-current_point)
angles[i] += angle 

def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += angle

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
    pygame.display.flip()

import sys, pygame
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    target = pygame.mouse.get_pos()
    solve_ik(0, points[-1], target)

    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)

    render()
    pygame.time.wait(int(1000/60))
