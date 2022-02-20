#!/usr/bin/env python

import time
import numpy as np
from scipy.spatial.transform import Rotation as R

class CameraKinematics:

    def __init__(self, cx, cy, f=None, w=None, h=None, hfov=None):

        self._cx = cx
        self._cy = cy

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



    def body_to_inertia(self, body_vec, eul):

        if body_vec is None:
            return None

        ## calculate a "DCM" using euler angles of camera body, to convert vector
        ## from body to inertial coordinates
        r = R.from_euler('zyx', eul, degrees=False)

        ## return the vector in inertial coordinates
        return np.matmul(r.as_matrix(), body_vec)


    def inertia_to_body(self, in_vec, eul):

        ## calculate a transformation using euler angles
        r = R.from_euler('zyx', eul, degrees=False)

        ## calculate a DCM and find transpose that takes inertial to body
        DCM_bi = r.as_matrix().T

        ## return vector in body coordinates
        return np.matmul(DCM_bi, in_vec)



    def cam_to_body(self, rect, beta=0):

        if rect is None:
            return None

        ## converting 2d rectangle to a 3d vector in camera coordinates
        vec = self.to_direction_vector(rect, self._cx, self._cy, self._f)

        ## for MAVIC Mini logs, no conversion is needed since we have gimbal orientation
        return vec

        # r1 = R.from_euler('xyz', [beta-90, 0, -90], degrees=True)
        # dcm_cam_to_body = r1.as_matrix()
        # vec = self.to_direction_vector(rect, 487.4 *float(640)/960, 363.1 *float(480)/720, 929)
        # return np.matmul(dcm_cam_to_body, vec)




    def to_direction_vector(self, rect, cx, cy, f):

        ## find center point of target
        center = np.array([rect[0]+rect[2]/2, rect[1]+rect[3]/2])

        ## project 2d point from image plane to 3d space using a simple pinhole
        ## camera model
        w = np.array( [ -(center[0] - cx) , -(center[1] - cy), f] )
        return w/np.linalg.norm(w)

    def from_direction_vector(self, dir, cx, cy, f):

        ## avoid division by zero
        if dir[2] < 0.01:
            dir[2] = 0.01

        ## calculate reprojection of direction vectors to image plane using a
        ## simple pinhole camera model
        X = cx - (dir[0] / dir[2]) * f
        Y = cy - (dir[1] / dir[2]) * f

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
            if inertia_dir is not None:
                ## find the difference between new observation (inertia_dir) and last
                ## known direction (self._inertia_dir_before)
                diff = inertia_dir - self._inertia_dir_before

                ## make the differences smooth overtime. this add a dynamic to target
                ## direction vector.
                self._diff = 0.5*self._diff + 0.5*diff

            ## calculate new estimate for target's direction vector
            self._inertia_dir_after = self._inertia_dir_before + self._diff

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

        ## convert new estimate of target direction vector to body coordinates
        body_dir_est = self.inertia_to_body(self._inertia_dir_after, imu_meas)

        ## reproject to image plane
        center_est = self.from_direction_vector(body_dir_est, self._cx, self._cy, self._f)

        ## estimated rectangle
        rect_est = (int(center_est[0]-self._last_rect[2]/2), \
                    int(center_est[1]-self._last_rect[3]/2),
                    self._last_rect[2], self._last_rect[3])

        return rect_est
