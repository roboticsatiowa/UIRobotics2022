from controller import Robot, DistanceSensor, Motor
import sys
import numpy as np

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

# initialize devices
ps = []
psNames = [
   "shoulder_xy_sensor", 'shoulder_yz_sensor'
]

for i in range(2):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)
    
ps.append(robot.getDevice('elbow_sensor'))

elbow_ps = robot.getDevice('elbow_sensor')
elbow_ps.enable(TIME_STEP)

shoulder_xy = robot.getDevice('shoulder_xy_motor')
shoulder_yz = robot.getDevice('shoulder_yz_motor')
elbow = robot.getDevice('elbow_motor')
# elbow = robot.getDevice('joint_3')

shoulder_xy.setPosition(float('inf'))
shoulder_xy.setVelocity(0.0)
    
shoulder_yz.setPosition(float('inf'))
shoulder_yz.setVelocity(0.0)

elbow.setPosition(float('inf'))
elbow.setVelocity(0.0)

motors = [shoulder_xy, shoulder_yz, elbow]

    
    
def is_close(ik_angles, tol, target, pos):
    current_pos, endpoint = ik_angles(target, pos)
        
    lazy_susan, shoulder, elbow = False, False, False
        
    for i in range(0, len(current_pos)):
        diff[i] = current_pos[i] - endpoint[i]
        
        if np.abs(diff[0]) < tol:
            lazy_susan = True
         
         
        if np.abs(diff[1]) < tol:
         shoulder = True
        
        if np.abs(diff[2]) < tol:
         elbow = True
 
    return diff, lazy_susan, shoulder, elbow
     
     
def motor_control(ik_angles, is_close, motors):
    diff, lazy_susan, shoulder, elbow_joint = is_close(ik_angles(target, pos), tol)
     
    (shoulder_xy, shoulder_yz, elbow) = motors
    
    if lazy_susan:
        shoulder_xy.setVelocity(0.0)
    elif diff[0] > 0 and not lazy_susan:
        shoulder_xy.setVelocity(-1.0)
    else:
        shoulder_xy.setVelocity(1.0)
        
    if shoulder:
        shoulder_yz.setVelocity(0.0)
    elif diff[1] > 0 and not shoulder:
        shoulder_yz.setVelocity(-1.0)
    else:
        shoulder_yz.setVelocity(1.0)
    
    if elbow_joint:
        elbow.setVelocity(0.0)
    elif diff[2] > 0 and not elbow_joint:
        elbow.setVelocity(1.0)
    else:
        elbow.setVelocity(1.0)
     
            
   # set target to enpoint angles using ik_angles
   # target = np.array([.8, -.67, -.34])

def motorControl(pos, target, motors, tol):

    (shoulder_xy, shoulder_yz, elbow) = motors
    
    def ik_angles(target, pos):
        a = 0.4 # 15 in on rover
        b = 0.4 # 11 in on rover
        cnorm = np.sqrt(a**2 + b**2)
        c = np.sqrt(target[1]**2 + target[2]**2)
        
        if (c > cnorm):
            c = cnorm
        
        if target[1] == 0:
            target = 0.001
        phi = np.arctan(target[2]/target[1])
        beta = np.arccos((a**2 + c**2 - b**2)/(2*a*c))
        # direction_norm = direction / np.linalg.norm(direction)
        # Calculate the joint angles required to align the end effector with the direction vector
        theta1 = np.arctan(target[0] / target[1])
        theta2 = phi + beta
        theta3 = np.arccos((a**2 + b**2 - c**2)/(2*a*b))

        angles = np.array([theta1, theta2, theta3])
        print('ik: ', angles)
        return angles
         
    angles = ik_angles(target, pos)
  
    print(angles)
    def is_close(pos, angles, tol):
        # lazy_susan, shoulder, elbow = False, False, False
        is_done = [False, False, False]
        diff = [float('inf'), float('inf'), float('inf')]
        i = 0
        for i in range(len(pos)):
            diff[i] = pos[i] - angles[i]
            
            if np.abs(diff[i]) < tol:
                is_done[i] = True
            
        
        print('is close: ', diff, is_done)
        return diff, is_done
    
    diff, isClose = is_close(pos, angles, tol)
    # print(diff)
    # print(isClose)
    (lazy_susan, shoulder, elbow_joint) = isClose
    
    
    if lazy_susan:
        shoulder_xy.setVelocity(0.0)
    elif diff[0] > 0 and not lazy_susan:
        shoulder_xy.setVelocity(-1.0)
    else:
        shoulder_xy.setVelocity(1.0)
        
    if shoulder:
        shoulder_yz.setVelocity(0.0)
    elif diff[1] > 0 and not shoulder:
        shoulder_yz.setVelocity(-1.0)
    else:
        shoulder_yz.setVelocity(1.0)
    
    if elbow_joint:
        elbow.setVelocity(0.0)
    elif diff[2] > 0 and not elbow_joint:
        elbow.setVelocity(-1.0)
    else:
        elbow.setVelocity(1.0)
        
    return 

    
target = np.array([-.13, .24, .09])
    
# feedback loop: step simulation until receiving an exit event
while robot.step(TIME_STEP) != -1:
    # read sensors outputs
    
    
    current_pos = np.array([ps[0].getValue(), ps[1].getValue(), ps[2].getValue()])
    # elbow.setVelocity(1.0)
    # for i in ps:
       # print('shoulder_xy: ', ps[0].getValue())
       # print('shoulder_yz', ps[1].getValue())
       # print('elbow: ', ps[2].getValue())
       # print('yz: ', ps[1].getValue())
    
    
    motorControl(current_pos, target, motors, 0.1)
    # motor_control(ik, isclose, motors)  
    
    
    
    
    
    
 # def solve_ik(i, endpoint, target):
    # if i < len(points) - 2:
        # endpoint = solve_ik(i+1, endpoint, target)
    # current_point = points[i] 
    
    
# def solve_ik_3d(i, endpoint, target, points):
    # if i < len(points) - 3:
        # endpoint = solve_ik_3d(i+1, endpoint, target, points)
    
    # current_point = points[i]
    
    # calculate the distance and direction between the current point and the endpoint
    # distance = math.sqrt((endpoint[0]-current_point[0])**2 + (endpoint[1]-current_point[1])**2 + (endpoint[2]-current_point[2])**2)
    # direction = [(endpoint[0]-current_point[0])/distance, (endpoint[1]-current_point[1])/distance, (endpoint[2]-current_point[2])/distance]
    
    # calculate the new position of the current point based on the target and direction
    # new_point = [target[0] - direction[0]*distance, target[1] - direction[1]*distance, target[2] - direction[2]*distance]
    
    # update the points list with the new position of the current point
    # points[i] = new_point
    
    # return endpoint

