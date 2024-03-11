import math


def toRobotPosit(noteX, noteY, robotX, robotY, robotRotation):
    noteRotation=math.radians(robotRotation)+math.atan(noteY/noteX)
    noteDisance=math.sqrt(noteX**2+noteY**2)
    return [math.cos(noteRotation)*noteDisance+robotX, math.sin(noteRotation)*noteDisance+robotY]




