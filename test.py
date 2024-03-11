import math


def toRobotPosit(noteX, noteY, robotX, robotY, roboRotation):
    roboRotation=math.radians(roboRotation)

    noteRotation=[(math.cos(roboRotation)+math.sin(roboRotation))*noteX+robotX, (math.cos(roboRotation)-math.sin(roboRotation))*noteY+robotY]

    

    return noteRotation





print(toRobotPosit(1, 1, 0, 0, 60))
