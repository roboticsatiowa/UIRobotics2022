import pygame
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class XboxContPublisher(Node):

    def __init__(self):
        super().__init__('Xbox_Controller')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.button_pressed_callback)
        self.i = 0

    def button_pressed_callback(self):
        msg = String()
        msg.data = f"Hello World: {self.i}"
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = XboxContPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


pygame.init()
xboxController = pygame.joystick.Joystick(0)


# def display():
#     while True:
#          # updates the controller input values
#         event_queue = pygame.event.get()
#         for event in event_queue:

#         controlMap = getInputs(xboxController)
        
#         # print each controller input with its value
#         s = ''
#         for item in controlMap:
#             s = '{}\n{}: {}'.format(s, str(item), str(controlMap[item]))
#         print(s)




# def getInputs(controller:pygame.joystick.Joystick) -> dict:
#     '''Returns a dict of each button mapped to its value'''
#     return {
#             "B": bool(controller.get_button(1)),
#             "A": bool(controller.get_button(0)),
#             "X": bool(controller.get_button(2)),
#             "Y": bool(controller.get_button(3)),
#             "LB": bool(xboxController.get_button(4)),
#             "RB": bool(controller.get_button(5)),
#             "BACK": bool(controller.get_button(6)),
#             "START": bool(controller.get_button(7)),
#             "Lstick_pressed": bool(controller.get_button(8)),
#             "Rstick_pressed": bool(controller.get_button(9)),
#             "Lstick_x": round(controller.get_axis(0), 3),
#             "Lstick_y": round(-controller.get_axis(1), 3), #  value inverted so forward is positive
#             "Rstick_x": round(controller.get_axis(2), 3),
#             "Rstick_y": round(-controller.get_axis(3), 3), # value inverted so forward is positive
#             "Ltrig": round((controller.get_axis(4)+1)/2, 3), # value mapped from (-1.0, 1.0) to (0.0, 1.0)
#             "Rtrig": round((controller.get_axis(5)+1)/2, 3), # value mapped from (-1.0, 1.0) to (0.0, 1.0)
#             "dPad_x": controller.get_hat(0)[0], # TODO still not sure how to get D pad values
#             "dPad_y": controller.get_hat(0)[1], # 
#         }