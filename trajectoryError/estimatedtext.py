import numpy as np
import cv2
import quaternion as q

#轨迹点
def read_e():
    estimated_file = "estimated.txt"

    list_test = []
    time = []
    tx = []
    ty = []
    tz = []
    qx = []
    qy = []
    qz = []
    qw = []
    T = []
    Q = []
    Ow = []

    counte = len(open(estimated_file, "r").readlines())

    print(counte)
    with open(estimated_file, 'r') as f:
        for line in f.readlines():
            time.append(line.split()[0])
            tx.append(line.split()[1])
            ty.append(line.split()[2])
            tz.append(line.split()[3])
            qx.append(line.split()[4])
            qy.append(line.split()[5])
            qz.append(line.split()[6])
            qw.append(line.split()[7])
            T.append((line.split()[1], line.split()[2], line.split()[3]))
            Q.append((line.split()[4], line.split()[5], line.split()[6], line.split()[7]))
    for i in range(counte):
        Ow.append(T[i])
    return Ow, T, Q, counte







