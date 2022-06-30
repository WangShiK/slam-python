import numpy as np
import quaternion as q
import cv2

class SO3():

    def __init__(self, matrix):

        self.M = matrix

    def log(self):
        
        error = 0.0000001
        if np.linalg.norm(np.eye(3) - self.M) < error:
            # case theta == 0
            return so3(vector=np.array([0, 0, 0]))
        elif np.abs(np.trace(self.M) + 1) < error:
            # case theta == pi
            if self.M[0, 0] > 0:
                w = 1 / np.sqrt(2 * (1 + self.M[0, 0])) * np.array([1 + self.M[0, 0], self.M[1, 0], self.M[2, 0]])  # wx
            elif self.M[1, 1] > error:
                w = 1 / np.sqrt(2 * (1 + self.M[1, 1])) * np.array([self.M[0, 1], 1 + self.M[1, 1], self.M[2, 1]])  # wy
            else:
                w = 1 / np.sqrt(2 * (1 + self.M[2, 2])) * np.array([self.M[0, 2], self.M[1, 2], 1 + self.M[2, 2]])  # wz
            w = np.pi * w
            return so3(vector=w)
        else:
            cs = (np.trace(self.M) - 1) / 2
            theta = np.arccos(cs)
            sn = np.sin(theta)
            logR = theta / (2 * sn) * (self.M - self.M.T)
            return so3(vector=np.array([logR[2, 1], logR[0, 2], logR[1, 0]]))

    def matrix(self):
        
        return self.M

    def mat2vec(self):
        vec = q.R2Vector(self.M)

        return vec



        

    def __mul__(self, other):
        
      
        return SO3(self.M.dot(other.matrix()))


class so3():
 
    G1 = np.matrix([[0, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]])
    G2 = np.matrix([[0, 0, 1],
                    [0, 0, 0],
                    [-1, 0, 0]])
    G3 = np.matrix([[0, -1, 0],
                    [1, 0, 0],
                    [0, 0, 0]])

    def __init__(self, **kwargs):
     
        if "vector" in kwargs:
            self.w = kwargs["vector"]
        elif "matrix" in kwargs:
            m = kwargs["matrix"]
            self.w = np.array([0, 0, 0])
            self.w[0] = m[2, 1]
            self.w[1] = m[0, 2]
            self.w[2] = m[1, 0]
        else:
            raise TypeError("Argument must be matrix or vector")

    def add(self, other):

        R1 = self.exp()
        R2 = other.exp()
        R = R1 * R2
        print(R.log())
        return R.log()

    def magnitude(self):
 
        return np.linalg.norm(self.w)

    def exp(self):
        wx = self.matrix()
        theta = np.linalg.norm(self.w)
        cs = np.cos(theta)
        sn = np.sin(theta)
        I = np.eye(3)
        a = (sn / theta) if theta != 0 else 1
        b = ((1 - cs) / theta ** 2) if theta != 0 else 1 / 2.0
        R = I + a * wx + b * wx.dot(wx)
        return SO3(R)

    def vector(self):
        return self.w

    def matrix(self):
 
        return so3.G1 * self.w[0] + so3.G2 * self.w[1] + so3.G3 * self.w[2]


class se3():
    n = np.array([0, 0, 0, 1])
    def __init__(self, group, T):
        self.quat = group
        self.t = np.array([T])

    #四元数
    def quat2se3(self):
        R = q.Quat2R(self.quat)
        Ra = np.hstack((R, self.t.T))
        Ra = np.vstack((Ra, se3.n))
        Ra = np.mat(Ra)
        return Ra

    def mat2se3(self):
        ra = np.hstack((self.quat, self.t.T))
        ra = np.vstack((ra, se3.n))
        ra = np.mat(ra)
        return ra

    def se3toSE3(self):
        rv = quat2se3(self.quat)
        rv = rv[:3, :3]
        v = q.R2Vector(rv)
        SE3 = np.vstack((v, self.t))
        return SE3
        


class SE3():
    def __init__(self, quat):
        self.qua = quat

    def r_inv(self):
        rr = np.linalg.inv(self.qua)
        return rr
    def tov(self):
        r1 = self.qua[:3, :3]
        vec = self.qua[:3, 3]
        r2v = q.R2Vector(r1)
        vector = np.vstack((vec, r2v))
        vector = vector.T
        return vector
        
        
    
        
        
