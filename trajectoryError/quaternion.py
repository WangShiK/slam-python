import numpy as np
import math
from scipy.spatial.transform import Rotation as R
import cv2


#四元数到旋转矩阵
def Quat2R(Rq):
    r = R.from_quat(Rq)
    rm = r.as_matrix()
    return rm


#四元数到欧拉角
def Quat2E(Rq):
    r = R.from_quat(Rq)
    euler = r.as_euler('zyx', degrees=True)
    return euler

#从旋转矩阵到四元数
def Rm2quat(Rm):
    q = R.from_matrix(Rm)
    quat = q.as_quat()
    q_inv = q.inv()
    q_inv = q_inv.as_quat()
    return quat, q_inv

#旋转矩阵到欧拉角
def Rm2E(Rm):
    q = R.from_matrix(Rm)
    euler_2mat = q.as_euler('zyx', degrees=True)
    return euler_2mat

#欧拉角到旋转矩阵
def euler2Rm(euler):
    r = R.from_euler('zyx', euler, degrees=True)
    Rm = r.as_matrix()
    return Rm

#欧拉角到四元数
def euler2quat(euler):
    r = R.from_euler('zyx', euler, degrees=True)
    quat = r.as_quat()
    return quat

#OpenCV库有一个函数提供了罗德里格斯公式Rodrigues()
#angle是旋转角度, v_q是四元数
def angleratotionX(angle):
    pi_m = angle / 180
    angle = pi_m * np.pi
    ax1 = np.cos(angle)
    ax2 = np.sin(angle)
    n = np.array([[angle,0,0]], np.float)
    rx = np.array([[1, 0, 0], [0, ax1, -ax2], [0, ax2, ax1]])
    v_q = R.from_rotvec(n)
    v_q = v_q.as_quat()
    return rx, v_q
        
def angleratotionY(angle):
    pi_m = angle / 180
    angle = pi_m * np.pi
    ay1 = np.cos(angle)
    ay2 = np.sin(angle)
    b = np.array([[0, angle, 0]], np.float)
    ry = np.array([[ay1, 0, ay2], [0, 1, 0], [-ay2, 0, ay1]])
    v_b = R.from_rotvec(b)
    v_b = v_b.as_quat()
    return ry, v_b

def angleratotionZ(angle):
    pi_m = angle / 180
    angle = pi_m * np.pi
    az1 = np.cos(angle)
    az2 = np.sin(angle)
    c = np.array([[0, 0, angle]], np.float)
    rz = np.array([[az1, -az2, 0], [az2, az1, 0], [0, 0 , 1]])
    c = np.array([[0, 0, angle]], np.float32)
    v_c = R.from_rotvec(c)
    v_c = v_c.as_quat()
    return rz, v_c

#旋转矩阵到旋转向量
def R2Vector(matrix):
    v = cv2.Rodrigues(matrix)
    v = v[0]
    return v


def matrix(vec):
    v2r = vec
    FR = np.matrix([[0, -v2r[2], v2r[1]],
                    [v2r[2], 0, -v2r[0]],
                    [-v2r[1], v2r[0], 0]])
    return FR

