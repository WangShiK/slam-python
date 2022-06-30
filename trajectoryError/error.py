import groudturetext as g
import estimatedtext as e
import numpy as np
import quaternion as q
import sophus as s



_,gt, gq, gc = g.g_t()
_, et, eq, ec = e.read_e()
rmse = 0
for i in range(gc):
    t1 = np.array(et[i]).astype(float)
    q1 = np.array(eq[i]).astype(float)
    t2 = np.array(gt[i]).astype(float)
    q2 = np.array(gq[i]).astype(float)

    r1 = s.se3(q1, t1)
    r2 = s.se3(q2, t2)
    r1 = r1.quat2se3()
    r2 = r2.quat2se3()

    S1 = s.SE3(r2)
    r2_inv = S1.r_inv()
    S2 = s.SE3(r2_inv * r1)
    v = S2.tov()
    
    
    error = np.linalg.norm(v)

    rmse += error * error
print(rmse)
rmse = np.sqrt(rmse / gc)
print("误差：", rmse)
