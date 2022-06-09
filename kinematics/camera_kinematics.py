#!/usr/bin/env python

import time
import numpy as np
from scipy.spatial.transform import Rotation as R
from lib.utils import plot_kinematics
import matplotlib.pyplot as plt

class CameraKinematics:

    def __init__(self, factor, cx, cy, f=None, w=None, h=None, hfov=None, vis=True):

        self._cx = cx
        self._cy = cy
        self._hfov = hfov
        self._w = w
        self._h = h

        if f is not None:
            self._f = f
        elif f is None and (hfov is not None and w is not None and \
                            h is not None):
            self._f = (0.5 * w * (1.0 / np.tan((hfov/2.0)*np.pi/180)));
        else:
            raise ValueError('At least one of arguments "f" or "hfov" must have value.')

        self._init = False

        self._diff = np.array( [0,0,0] )
        self._inertia_dir_before = np.array( [0,0,0] )
        self._inertia_dir_after = np.array( [0,0,0] )
        self._last_rect = (0,0,0,0)
        self._interp_factor=factor

        self._vis=vis
        if vis:
            self._fig_3d=plt.figure(0)
            self._ax_3d=plt.axes(projection ='3d')
            self._ax_3d.set_title('Kinematics Plot')
            # self._ax_3d.view_init(elev=-45, azim=45)


    def body_to_inertia(self, body_vec, eul):

        if body_vec is None:
            return None

        ## calculate a DCM and find transpose that takes body to inertial
        DCM_ib = self.make_DCM(eul).T

        ## return vector in inertial coordinates
        return np.matmul(DCM_ib, body_vec)


    def inertia_to_body(self, in_vec, eul):

        ## calculate a "DCM" using euler angles of camera body, to convert vector
        ## from inertial to body coordinates
        DCM_bi = self.make_DCM(eul)

        ## return the vector in body coordinates
        return np.matmul(DCM_bi, in_vec)


    def cam_to_body(self, rect):

        if rect is None:
            return None

        ## converting 2d rectangle to a 3d vector in camera coordinates
        vec = self.to_direction_vector(rect, self._cx, self._cy, self._f)

        ## for MAVIC Mini camera, the body axis can be converted to camera
        ## axis by a 90 deg yaw and a 90 deg roll consecutively. then we transpose
        ## it to get camera to body
        DCM_bc = self.make_DCM([90*np.pi/180, 0, 90*np.pi/180]).T

        return np.matmul(DCM_bc, vec)

    def body_to_cam(self, vec):

        ## for MAVIC Mini camera, the body axis can be converted to camera
        ## axis by a 90 deg yaw and a 90 deg roll consecutively.
        DCM_cb = self.make_DCM([90*np.pi/180, 0, 90*np.pi/180])

        return np.matmul(DCM_cb, vec)


    def to_direction_vector(self, rect, cx, cy, f):

        ## find center point of target
        center = np.array([rect[0]+rect[2]/2, rect[1]+rect[3]/2])

        ## project 2d point from image plane to 3d space using a simple pinhole
        ## camera model
        w = np.array( [ (center[0] - cx) , (center[1] - cy), f] )
        return w/np.linalg.norm(w)

    def from_direction_vector(self, dir, cx, cy, f):

        ## avoid division by zero
        if dir[2] < 0.01:
            dir[2] = 0.01

        ## calculate reprojection of direction vectors to image plane using a
        ## simple pinhole camera model
        X = cx + (dir[0] / dir[2]) * f
        Y = cy + (dir[1] / dir[2]) * f

        return (int(X),int(Y))


    def updateRect(self, imu_meas, rect=None):

        if rect is not None:
            self._last_rect = rect

        ## convert target from a rect in "image coordinates" to a vector
        ## in "camera body coordinates"
        body_dir = self.cam_to_body(rect)

        ## convert target from a vector in "camera body coordinates" to a vector
        ## in "inertial coordinates"
        inertia_dir = self.body_to_inertia(body_dir, imu_meas)

        if self._init:
            ## update difference vector only in case of new observation
            ## otherwise continue changing direction vector with last know
            ## speed
            diff=np.array([0.0,0.0,0.0])
            if inertia_dir is not None:
                ## find the difference between new observation (inertia_dir) and last
                ## known direction (self._inertia_dir_before)
                diff = inertia_dir - self._inertia_dir_before

                ## make the differences smooth overtime. this add a dynamic to target
                ## direction vector.
                self._diff = self._interp_factor*self._diff + (1-self._interp_factor)*diff

            ## calculate new estimate for target's direction vector
            self._inertia_dir_after = self._inertia_dir_before + self._diff
            print("diff ", self._diff)

            ## ensure direction vector always has a length of 1
            self._inertia_dir_after = self._inertia_dir_after/np.linalg.norm(self._inertia_dir_after)

            ## save this new estimate as last known direction in the memory
            self._inertia_dir_before = self._inertia_dir_after

        else:

            if inertia_dir is not None:
                ## initialize with first observation
                self._inertia_dir_before = inertia_dir
                self._inertia_dir_after = inertia_dir
                self._diff = np.array([0.0,0.0,0.0])

                self._init = True
            else:
                return None

        if self._vis:
            ## expressing camera frame by for vectors of its image corners in inertial
            ## frame
            corners = self.get_camera_frame_vecs(imu_meas,self._w,self._h)
            plot_kinematics(imu_meas,self._inertia_dir_after,self._ax_3d,corners)

        ## convert new estimate of target direction vector to body coordinates
        body_dir_est = self.inertia_to_body(self._inertia_dir_after,imu_meas)

        ## convert body to cam coordinates
        cam_dir_est = self.body_to_cam(body_dir_est)

        ## reproject to image plane
        center_est = self.from_direction_vector(cam_dir_est, self._cx, self._cy, self._f)

        ## estimated rectangle
        rect_est = (int(center_est[0]-self._last_rect[2]/2), \
                    int(center_est[1]-self._last_rect[3]/2),
                    self._last_rect[2], self._last_rect[3])

        return rect_est


    def get_camera_frame_vecs(self, eul, w, h):

        ## convert image corners from a point in "image coordinates" to a vector
        ## in "camera body coordinates"
        top_left = self.cam_to_body([-1,-1,2,2])
        top_right = self.cam_to_body([w-1,-1,2,2])
        bottom_left = self.cam_to_body([-1,h-1,2,2])
        bottom_right = self.cam_to_body([w-1,h-1,2,2])

        ## convert image corners from a vector in "camera body coordinates" to
        ## a vector in "inertial coordinates"
        top_left_inertia_dir = self.body_to_inertia(top_left, eul)
        top_right_inertia_dir = self.body_to_inertia(top_right, eul)
        bottom_left_inertia_dir = self.body_to_inertia(bottom_left, eul)
        bottom_right_inertia_dir = self.body_to_inertia(bottom_right, eul)


        return (top_left_inertia_dir,top_right_inertia_dir,\
                bottom_left_inertia_dir,bottom_right_inertia_dir)

    def make_DCM(self, eul):

        phi = eul[0]
        theta = eul[1]
        psi = eul[2]

        DCM = np.zeros((3,3))
        DCM[0,0] = np.cos(psi)*np.cos(theta)
        DCM[0,1] = np.sin(psi)*np.cos(theta)
        DCM[0,2] = -np.sin(theta)
        DCM[1,0] = np.cos(psi)*np.sin(theta)*np.sin(phi)-np.sin(psi)*np.cos(phi)
        DCM[1,1] = np.sin(psi)*np.sin(theta)*np.sin(phi)+np.cos(psi)*np.cos(phi)
        DCM[1,2] = np.cos(theta)*np.sin(phi)
        DCM[2,0] = np.cos(psi)*np.sin(theta)*np.cos(phi)+np.sin(psi)*np.sin(phi)
        DCM[2,1] = np.sin(psi)*np.sin(theta)*np.cos(phi)-np.cos(psi)*np.sin(phi)
        DCM[2,2] = np.cos(theta)*np.cos(phi)

        return DCM
