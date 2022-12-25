class RoverTelemetry:
    def __init__(self):
        self.arm = Arm()
        self.status = Status()
        self.pos = Location()

    def update(self, data: str):
        pass


class Arm:
    def __init__(self):
        self.clawTightness = 1.0
        self.clawAngle = 0.0
        self.elbowAngle = 0.0
        self.shoulderAngle = 0.0
        self.rotationAngle = 0.0


class Status:
    def __init__(self):
        self.temp = 0
        self.battery = 1.0


class Location:
    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.heading = 0.0
        self.incline = 0.0
        self.roll = 0.0
