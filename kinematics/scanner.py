#!/usr/bin/env python

import numpy as np
from scipy.spatial.transform import Rotation as R
from skimage.draw import polygon

class Scanner:

    def __init__(self, f, cx, cy, res, max_dist=300):

        self._f = f
        self._cx = cx
        self._cy = cy

        self._map_size = int(50/res)
        self._res = res
        self._max_dist = max_dist

        self.RAD = np.pi/180.0

        self._mapp = 80*np.ones((2*self._map_size+1, 2*self._map_size+1), 'int8')


    def cam_to_map_motion(self, vectors, beta, quat, pos):

        r1 = R.from_euler('xyz', [90+beta, 0, 90], degrees=True)
        dcm_cam_to_body = r1.as_matrix()

        r2 = R.from_quat(quat)
        dcm_body_to_inertia = r2.as_matrix()

        ps1_ws, ps2_ws = self.to_direction_vector_motion([vec[0] for vec in vectors], [vec[1] for vec in vectors])

        ps1_vs    = [np.matmul(dcm_body_to_inertia,np.matmul(dcm_cam_to_body,w)) for w in ps1_ws]
        ps2_vs = [np.matmul(dcm_body_to_inertia,np.matmul(dcm_cam_to_body,w)) for w in ps2_ws]

        scaled_ps1_vs    = [self.scale_vector2(v, pos[2]) for v in ps1_vs]
        scaled_ps2_vs = [self.scale_vector2(v, pos[2]) for v in ps2_vs]

        ps1_pos = []
        for v in scaled_ps1_vs:
            if v is not None:
                ps1_pos.append([v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]])
            else:
                ps1_pos.append(None)

        ps2_pos = []
        for v in scaled_ps2_vs:
            if v is not None:
                ps2_pos.append([v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]])
            else:
                ps2_pos.append(None)

        return ps1_pos, ps2_pos

    def cam_to_map(self, cars, persons, beta, quat, pos):

        r1 = R.from_euler('xyz', [90+beta, 0, 90], degrees=True)
        dcm_cam_to_body = r1.as_matrix()

        r2 = R.from_quat(quat)
        dcm_body_to_inertia = r2.as_matrix()

        # print(r2.as_euler('zyx')/self.RAD)
        # dcm_cam_to_body = self.calc_dcm((-90-beta)*RAD, 0, -90*RAD)
        # dcm_body_to_inertia = self.calc_dcm(euler[0], euler[1], euler[2])

        car_ws, person_ws = self.to_direction_vector(cars, persons)

        car_vs    = [np.matmul(dcm_body_to_inertia,np.matmul(dcm_cam_to_body,w)) for w in car_ws]
        person_vs = [np.matmul(dcm_body_to_inertia,np.matmul(dcm_cam_to_body,w)) for w in person_ws]

        scaled_car_vs    = [self.scale_vector2(v, pos[2]) for v in car_vs]
        scaled_person_vs = [self.scale_vector2(v, pos[2]) for v in person_vs]

        car_pos = []
        for v in scaled_car_vs:
            if v is not None:
                car_pos.append([v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]])
            else:
                car_pos.append(None)

        person_pos = []
        for v in scaled_person_vs:
            if v is not None:
                person_pos.append([v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]])
            else:
                person_pos.append(None)

        return car_pos, person_pos

    def fov_on_map(self, w, h, beta, quat, pos):

        r1 = R.from_euler('xyz', [90+beta, 0, 90], degrees=True)
        dcm_cam_to_body = r1.as_matrix()

        r2 = R.from_quat(quat)
        dcm_body_to_inertia = r2.as_matrix()

        # print(r2.as_euler('zyx')/self.RAD)
        # dcm_cam_to_body = self.calc_dcm((-90-beta)*RAD, 0, -90*RAD)
        # dcm_body_to_inertia = self.calc_dcm(euler[0], euler[1], euler[2])

        points = [[0,0], [0,h], [w,h], [w,0]]
        ws = [np.array( [ -(p[0] - self._cx) , -(p[1] - self._cy), self._f] ) for p in points]
        ws = [w/np.linalg.norm(w) for w in ws]
        vs    = [np.matmul(dcm_body_to_inertia,np.matmul(dcm_cam_to_body,w)) for w in ws]
        scaled_vs    = [self.scale_vector1(v, pos[2]) for v in vs]
        poses = [[v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]] for v in scaled_vs]

        arrows = [[pos, [v[0]+pos[0], v[1]+pos[1], v[2]+pos[2]]] for v in scaled_vs]
        arrows.append([arrows[0][1], arrows[1][1]])
        arrows.append([arrows[1][1], arrows[2][1]])
        arrows.append([arrows[2][1], arrows[3][1]])
        arrows.append([arrows[3][1], arrows[0][1]])

        max_pos = np.abs(np.array(poses)).max() / self._res
        if max_pos > self._map_size:
            self.expand_map(max_pos)
        poly = np.rint(np.array(poses)/self._res+self._map_size)
        rr, cc = polygon(poly[:,1], poly[:,0], self._mapp.shape)
        self._mapp[self._mapp==1] = 50
        self._mapp[rr,cc] = 1

        return self._mapp, arrows


    def expand_map(self, new_size):

        diff = int(new_size - self._map_size + 1)
        addition = 80*np.ones((2*self._map_size+1, diff), 'int8')
        # print(self._mapp.shape, addition.shape)
        temp = np.hstack((self._mapp, addition))
        temp = np.hstack((addition, temp))
        addition = 80*np.ones((diff, 2*self._map_size+1+2*diff), 'int8')
        temp = np.vstack((temp, addition))
        temp = np.vstack((addition, temp))

        self._map_size = int(temp.shape[0]/2)

        self._mapp = temp


    def scale_vector1(self, v, z):

        if v[2] < 0:
            factor = np.abs(z) / np.abs(v[2])
            if np.linalg.norm(factor*v) < self._max_dist:
                return factor*v
            else:
                return self._max_dist*v
        elif v[2] >= 0:
            return self._max_dist*v

    def scale_vector2(self, v, z):

        if v[2] < 0:
            factor = np.abs(z) / np.abs(v[2])
            return factor*v
        else:
            return None

    def to_direction_vector(self, cars, persons):

        car_ws = []
        person_ws = []

        for car in cars:
            center = self.center_of_rect(car)
            w = np.array( [ -(center[0] - self._cx) , -(center[1] - self._cy), self._f] )
            car_ws.append(w/np.linalg.norm(w))

        for person in persons:
            center = self.center_of_rect(person)
            w = np.array( [ -(center[0] - self._cx) , -(center[1] - self._cy), self._f] )
            person_ws.append(w/np.linalg.norm(w))

        return car_ws, person_ws

    def to_direction_vector_motion(self, ps1, ps2):

        ps1_ws = []
        ps2_ws = []

        for p in ps1:
            center = p
            w = np.array( [ -(center[0] - self._cx) , -(center[1] - self._cy), self._f] )
            ps1_ws.append(w/np.linalg.norm(w))

        for p in ps2:
            center = p
            w = np.array( [ -(center[0] - self._cx) , -(center[1] - self._cy), self._f] )
            ps2_ws.append(w/np.linalg.norm(w))

        return ps1_ws, ps2_ws

    def calc_dcm(self, phi, theta, psi):

         dcm = np.zeros((3,3), dtype=np.float32)

         dcm[0,0] = np.cos(theta)*np.cos(psi)
         dcm[0,1] = np.cos(theta)*np.sin(psi)
         dcm[0,2] = -np.sin(theta)
         dcm[1,0] = np.sin(phi)*np.sin(theta)*np.cos(psi) - np.cos(phi)*np.sin(psi)
         dcm[1,1] = np.sin(phi)*np.sin(theta)*np.sin(psi) + np.cos(phi)*np.cos(psi)
         dcm[1,2] = np.sin(phi)*np.cos(theta)
         dcm[2,0] = np.cos(phi)*np.sin(theta)*np.cos(psi) + np.sin(phi)*np.sin(psi)
         dcm[2,1] = np.cos(phi)*np.sin(theta)*np.sin(psi) - np.sin(phi)*np.cos(psi)
         dcm[2,2] = np.cos(phi)*np.cos(theta)

         return dcm

    def center_of_rect(self, rect):
        return (rect[0]+int(rect[2]/2), rect[1]+int(rect[3]/2))
