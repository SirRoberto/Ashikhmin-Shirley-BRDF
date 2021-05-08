from lights import PointLight

import numpy as np
from numpy.linalg import norm
from math import sin, cos, sqrt, pi, acos


class AshikhminShirleyModel():
    def __init__(self):
        self.epsilon = np.array([0.5, 1.0, 0.5])
        self.ambient = np.array([0.0, 0.0, 0.1])
        self.n_x = 10
        self.n_y = 100
        self.rd = np.array([0.0, 0.84, 1.0])
        self.rs = np.array([1.0, 0.0, 0.0])


    def render_pixel(self, pointLight:PointLight, normal_vec:np.array, viewer_vec:np.array):
        light_vec = pointLight.pos - normal_vec
        return self.reflect(light_vec, normal_vec, viewer_vec)


    def reflect(self, light_vec:np.array, normal_vec:np.array, viewer_vec:np.array):
        l = light_vec / norm(light_vec)
        n = normal_vec / norm(normal_vec)
        v = viewer_vec / norm(viewer_vec)
        h_vec = light_vec + viewer_vec
        h = h_vec / np.linalg.norm(h_vec)

        epsilon = np.array([-1,0.5,1]) 
        epsilon /= norm(epsilon)
        tangent = np.cross(n, epsilon)
        tangent /= norm(tangent)
        bitangent = np.cross(n, tangent)
        bitangent /= norm(bitangent)

        VdotN = v.dot(n)
        LdotN = l.dot(n)
        HdotN = h.dot(n)
        HdotL = h.dot(l)
        HdotT = h.dot(tangent)
        HdotB = h.dot(bitangent)

        Rd = np.array(self.rd)
        Rs = np.array(self.rs)

        n_u = self.n_x
        n_v = self.n_y

        fd = (28.0 * Rd) / (23.0 * pi)
        fd *= (np.array([1.0,1.0,1.0]) - Rs)
        fd *= (1.0 - pow(1.0 - 0.5 * LdotN, 5.0))
        fd *= (1.0 - pow(1.0 - 0.5 * VdotN, 5.0))


        p = n_u * HdotT * HdotT + n_v * HdotB * HdotB
        if (1.0 - HdotN * HdotN) < 1e-6:
            p /= 1e-6
        else:
            p /= (1.0 - HdotN * HdotN)

        fs_num = sqrt((n_u + 1) * (n_v + 1))
        fs_num *= pow(HdotN, p)

        fs_den = 8.0 * pi * HdotL
        fs_den *= max(LdotN, VdotN)

        fs = Rs * (fs_num / fs_den)
        fs *= self.fresnel(HdotL, Rs)

        fs[0] = fs[0] if fs[0] > 0 else 0
        fs[1] = fs[1] if fs[1] > 0 else 0
        fs[2] = fs[2] if fs[2] > 0 else 0

        fd[0] = fd[0] if fd[0] > 0 else 0
        fd[1] = fd[1] if fd[1] > 0 else 0
        fd[2] = fd[2] if fd[2] > 0 else 0

        return fd + fs + self.ambient


    def fresnel(self, cos_beta, rs):
        return rs + (1 - rs) * (1 - cos_beta)**5


    