import threading

import inverse_kinematics

ik = threading.Thread(target=inverse_kinematics.start_IK, daemon=True)
ik.start()

while True:
    print(inverse_kinematics.angles)
