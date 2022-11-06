import sys

import pygame
from pygame.math import Vector2

# initialize pygame library and sub-modules


# create a list of starting locations for each joint
points = list(map(Vector2, [(100, 300), (200, 300), (300, 300)]))

# define min and max angles each joint can move
max_angles = [130, 0]
min_angles = [-10, -150]

# boundaries which end affector (target) is clamped to ((xlow, xhigh), (ylow, yhigh))
target_bounds = ((101, 300), (200, 390))

# calculate relative positions of each joint and populate angles array with placeholder values
rel_points = []
angles = []


def start_IK():

    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', 20)
    print("control with WASD")

    # create GUI window pane
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)

    for i in range(1, len(points)):
        rel_points.append(points[i] - points[i-1])
        angles.append(0)

    def solve_ik(i, endpoint, target):  # recursively solve for the needed roation of each joint
        if i < len(points) - 2:
            endpoint = solve_ik(i+1, endpoint, target)
        current_point = points[i]

        angle = (endpoint-current_point).angle_to(target-current_point)
        angles[i] += angle

        # honestly have no idea how this works
        # limits the angles of each joint
        angles[i] = min(max(180 - max_angles[i], (angles[i]+180) %
                        360), 180 - min_angles[i]) - 180

        return current_point + (endpoint-current_point).rotate(angle)

    def render():
        black = 0, 0, 0
        white = 255, 255, 255
        blue = 0, 0, 255

        screen.fill(white)

        # draw the arm on screen
        angle = 0
        for i in range(1, len(points)):
            angle += angles[i-1]
            points[i] = points[i-1] + rel_points[i-1].rotate(angle)
        for i in range(1, len(points)):
            prev = points[i-1]
            cur = points[i]
            pygame.draw.aaline(screen, black, prev, cur)
        for point in points:
            pygame.draw.circle(
                screen, black, (int(point[0]), int(point[1])), 5)

        # draw target
        pygame.draw.circle(screen, blue,
                           (int(target[0]), int(target[1])), 5)

        # create debug text and draw to screen
        angle1 = my_font.render(str(round(-angles[0], 3)), False, (0, 0, 0))
        angle2 = my_font.render(str(round(-angles[1], 3)), False, (0, 0, 0))
        coords = my_font.render(str(target), False, (0, 0, 0))
        screen.blit(angle1, (20, 20))
        screen.blit(angle2, (20, 40))
        screen.blit(coords, (20, 60))

        # update display
        pygame.display.flip()

    n = 0
    target = (200, 305)
    while 1:

        # check for x button clicked on GUI window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # move target with WASD
        if pygame.key.get_pressed()[pygame.K_w]:
            target = (target[0], target[1] - 1)
        if pygame.key.get_pressed()[pygame.K_a]:
            target = (target[0] - 1, target[1])
        if pygame.key.get_pressed()[pygame.K_s]:
            target = (target[0], target[1] + 1)
        if pygame.key.get_pressed()[pygame.K_d]:
            target = (target[0] + 1, target[1])

        # limit target vector to vals specified in target_bounds
        target = (min(max(target[0], target_bounds[0][0]),
                      target_bounds[0][1]), min(max(target[1], target_bounds[1][0]), target_bounds[1][1]))

        # create circular left and right bounds
        rel_target = Vector2(target) - points[0]
        if rel_target.magnitude() > 190:
            rel_target.scale_to_length(190)
            rel_target = (points[0] + rel_target)
            target = (int(rel_target.x), int(rel_target.y))
        elif rel_target.magnitude() < 50:
            rel_target.scale_to_length(50)
            rel_target = (points[0] + rel_target)
            target = (int(rel_target.x), int(rel_target.y))

        # use inverse kinematics algorithm
        solve_ik(0, points[-1], target)

        # update display
        render()

        pygame.time.wait(int(1000/60))


if __name__ == '__main__':
    start_IK()
