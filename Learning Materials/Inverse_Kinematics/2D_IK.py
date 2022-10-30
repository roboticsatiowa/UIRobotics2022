from math import cos, pi, sin, sqrt

import py
import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])


def drawScreen():
    screen.fill((255, 255, 255))

    arm_len = 100
    forearm_len = 100
    shoulder_pos = (250, 450)

    target = pygame.mouse.get_pos()
    magnitude = sqrt((target[0] - shoulder_pos[0])**2
                     + (target[1] - shoulder_pos[1])**2)

    if magnitude > 200:
        target = (200 * (target[0] - shoulder_pos[0])/magnitude + shoulder_pos[0],
                  200 * (target[1] - shoulder_pos[1])/magnitude + shoulder_pos[1])

    shoulder_angle = -pi/2
    elbow_angle = -pi/2

    elbow_pos = (arm_len*cos(shoulder_angle) +
                 shoulder_pos[0], arm_len*sin(shoulder_angle) + shoulder_pos[1])

    claw_pos = (forearm_len*cos(elbow_angle) +
                elbow_pos[0], forearm_len*sin(elbow_angle) +
                elbow_pos[1])

    # draw all the stuff to the screen
    pygame.draw.circle(screen, (0, 0, 255), target, 5)
    pygame.draw.circle(screen, (0, 0, 0), shoulder_pos, 5)
    pygame.draw.circle(screen, (0, 0, 0), elbow_pos, 5)
    pygame.draw.circle(screen, (0, 0, 0), claw_pos, 5)
    pygame.draw.line(screen, (0, 0, 0), shoulder_pos, elbow_pos, 2)
    pygame.draw.line(screen, (0, 0, 0), elbow_pos, claw_pos, 2)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawScreen()
    pygame.display.flip()


pygame.quit()
