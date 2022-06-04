import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from lib.bbox_helper import get_axis_aligned_bbox,cxy_wh_2_rect

def APCE(response_map):
    Fmax=np.max(response_map)
    Fmin=np.min(response_map)
    apce=(Fmax-Fmin)**2/(np.mean((response_map-Fmin)**2))
    return apce

def PSR(response):
    response_map=response.copy()
    max_loc=np.unravel_index(np.argmax(response_map, axis=None),response_map.shape)
    y,x=max_loc
    F_max = np.max(response_map)
    response_map[y-5:y+6,x-5:x+6]=0.
    mean=np.mean(response_map[response_map>0])
    std=np.std(response_map[response_map>0])
    psr=(F_max-mean)/std
    return psr

def to_color_map(score,sz):
    score = cv2.resize(score, sz)
    score -= score.min()
    score = score / score.max()
    score = (score * 255).astype(np.uint8)
    # score = 255 - score
    score = cv2.applyColorMap(score, cv2.COLORMAP_JET)
    return score

def calAUC(value_list):
    length=len(value_list)
    delta=1./(length-1)
    area=0.
    for i in range(1,length):
        area+=(delta*((value_list[i]+value_list[i-1])/2))
    return area


def cos_window(sz):
    """
    width, height = sz
    j = np.arange(0, width)
    i = np.arange(0, height)
    J, I = np.meshgrid(j, i)
    cos_window = np.sin(np.pi * J / width) * np.sin(np.pi * I / height)
    """

    cos_window = np.hanning(int(sz[1]))[:, np.newaxis].dot(np.hanning(int(sz[0]))[np.newaxis, :])
    return cos_window


def get_img_list(img_dir):
    frame_list = []
    for frame in sorted(os.listdir(img_dir)):
        if os.path.splitext(frame)[1] == '.jpg':
            frame_list.append(os.path.join(img_dir, frame))
    return frame_list

def get_states_data(states_dir):
    st_path = os.path.join(states_dir, 'camera_states.txt')
    st = np.loadtxt(st_path, delimiter=',').astype(np.float64)
    return st[:,4:7]

def get_ground_truthes(img_path):
    gt_path = os.path.join(img_path, 'groundtruth_rect.txt')
    gts=[]
    with open(gt_path, 'r') as f:
        while True:
            line = f.readline()
            if line=='':
                gts=np.array(gts,dtype=np.float32)

                #for i in range(4):  # x, y, width, height
                #    xp = range(0, gts.shape[0], 5)
                #    fp = gts[xp, i]
                #    x = range(gts.shape[0])
                #    gts[:, i] = pylab.interp(x, xp, fp)
                return gts
            if ',' in line:
                gt_pos = line.split(',')
            else:
                gt_pos=line.split()
            gt_pos_int=[(float(element)) for element in gt_pos]
            gts.append(gt_pos_int)

def get_ground_truthes_viot(img_path):
    gt_path = os.path.join(img_path, 'groundtruth.txt')
    gts=[]
    with open(gt_path, 'r') as f:
        while True:
            line = f.readline()
            if line=='':
                gts=np.array(gts,dtype=np.float32)

                #for i in range(4):  # x, y, width, height
                #    xp = range(0, gts.shape[0], 5)
                #    fp = gts[xp, i]
                #    x = range(gts.shape[0])
                #    gts[:, i] = pylab.interp(x, xp, fp)
                return gts
            if ',' in line:
                gt_pos = line.split(',')
            else:
                gt_pos=line.split()

            gt_pos_int=[(float(element)) for element in gt_pos]
            gt_pos_int = get_axis_aligned_bbox(np.array(gt_pos_int))
            target_pos = np.array([gt_pos_int[0], gt_pos_int[1]])
            target_sz = np.array([gt_pos_int[2], gt_pos_int[3]])
            location=cxy_wh_2_rect(target_pos,target_sz)
            gts.append(location)

def get_init_gt(img_path):
    gt_path = os.path.join(img_path, 'groundtruth_rect.txt')
    with open(gt_path, 'r') as f:
        line = f.readline()
        if ',' in line:
            gt_pos = line.split(',')
        else:
            gt_pos=line.split()
        gt_pos_int=[int(float(element)) for element in gt_pos]
    return tuple(gt_pos_int)

def gaussian2d_labels(sz,sigma):
    w,h=sz
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    center_x, center_y = w / 2, h / 2
    dist = ((xs - center_x) ** 2 + (ys - center_y) ** 2) / (sigma**2)
    labels = np.exp(-0.5*dist)
    return labels

"""
max val at the top left loc
"""
def gaussian2d_rolled_labels(sz,sigma):
    w,h=sz
    xs, ys = np.meshgrid(np.arange(w)-w//2, np.arange(h)-h//2)
    dist = (xs**2+ys**2) / (sigma**2)
    labels = np.exp(-0.5*dist)
    labels = np.roll(labels, -int(np.floor(sz[0] / 2)), axis=1)
    labels=np.roll(labels,-int(np.floor(sz[1]/2)),axis=0)
    return labels


def plot_precision(gts,preds,save_path):
    plt.figure(2)
    # x,y,w,h
    threshes,precisions=get_thresh_precision_pair(gts,preds)
    idx20 = [i for i, x in enumerate(threshes) if x == 20][0]
    plt.plot(threshes,precisions,label=str(precisions[idx20])[:5])
    plt.title('Precision Plots')
    plt.legend()
    plt.savefig(save_path)
    plt.show()

def get_thresh_precision_pair(gts,preds):
    length=min(len(gts),len(preds))
    gts=gts[:length,:]
    preds=preds[:length,:]
    gt_centers_x = (gts[:, 0]+gts[:,2]/2)
    gt_centers_y = (gts[:, 1]+gts[:,3]/2)
    preds_centers_x = (preds[:, 0]+preds[:,2]/2)
    preds_centers_y = (preds[:, 1]+preds[:,3]/2)
    dists = np.sqrt((gt_centers_x - preds_centers_x) ** 2 + (gt_centers_y - preds_centers_y) ** 2)
    threshes = []
    precisions = []
    for thresh in np.linspace(0, 50, 101):
        true_len = len(np.where(dists < thresh)[0])
        precision = true_len / len(dists)
        threshes.append(thresh)
        precisions.append(precision)
    return threshes,precisions


def plot_success(gts,preds,save_path):
    plt.figure(1)
    threshes, successes=get_thresh_success_pair(gts, preds)
    plt.plot(threshes,successes,label=str(calAUC(successes))[:5])
    plt.title('Success Plot')
    plt.legend()
    plt.savefig(save_path)
    plt.show()


def get_thresh_success_pair(gts, preds):
    length=min(len(gts),len(preds))
    gts=gts[:length,:]
    preds=preds[:length,:]
    intersect_tl_x = np.max((gts[:, 0], preds[:, 0]), axis=0)
    intersect_tl_y = np.max((gts[:, 1], preds[:, 1]), axis=0)
    intersect_br_x = np.min((gts[:, 0] + gts[:, 2], preds[:, 0] + preds[:, 2]), axis=0)
    intersect_br_y = np.min((gts[:, 1] + gts[:, 3], preds[:, 1] + preds[:, 3]), axis=0)
    intersect_w = intersect_br_x - intersect_tl_x
    intersect_w[intersect_w < 0] = 0
    intersect_h = intersect_br_y - intersect_tl_y
    intersect_h[intersect_h < 0] = 0
    intersect_areas = intersect_h * intersect_w
    ious = intersect_areas / (gts[:, 2] * gts[:, 3] + preds[:, 2] * preds[:, 3] - intersect_areas)
    threshes = []
    successes = []
    for thresh in np.linspace(0, 1, 101):
        success_len = len(np.where(ious > thresh)[0])
        success = success_len / len(ious)
        threshes.append(thresh)
        successes.append(success)
    return threshes,successes

def plot_kinematics(eul,inertia_dir,ax_3d,corners):

    tl, tr, bl, br = corners

    ax_3d.cla()
    ax_3d.plot([0,inertia_dir[0]],[0,inertia_dir[1]],[0,inertia_dir[2]], color='r')

    ax_3d.quiver(0, 0, 0, 1, 0, 0, length=1, linewidth=2, color='red')
    ax_3d.quiver(0, 0, 0, 0, 1, 0, length=1, linewidth=2, color='green')
    ax_3d.quiver(0, 0, 0, 0, 0, 1, length=1, linewidth=2, color='blue')

    ax_3d.text(tl[0], tl[1], tl[2]+0.1, "tl", color='black')
    ax_3d.text(tr[0], tr[1], tr[2]+0.1, "tr", color='black')
    ax_3d.text(bl[0], bl[1], bl[2]-0.1, "bl", color='black')
    ax_3d.text(br[0], br[1], br[2]-0.1, "br", color='black')

    ax_3d.plot([0,tl[0]],[0,tl[1]],[0,tl[2]], color='black')
    ax_3d.plot([0,tr[0]],[0,tr[1]],[0,tr[2]], color='black')
    ax_3d.plot([0,bl[0]],[0,bl[1]],[0,bl[2]], color='black')
    ax_3d.plot([0,br[0]],[0,br[1]],[0,br[2]], color='black')
    ax_3d.plot([tl[0],tr[0]],[tl[1],tr[1]],[tl[2],tr[2]], color='black')
    ax_3d.plot([tl[0],bl[0]],[tl[1],bl[1]],[tl[2],bl[2]], color='black')
    ax_3d.plot([tr[0],br[0]],[tr[1],br[1]],[tr[2],br[2]], color='black')
    ax_3d.plot([bl[0],br[0]],[bl[1],br[1]],[bl[2],br[2]], color='black')

    ax_3d.set_xlim([-1.5,1.5])
    ax_3d.set_ylim([-1.5,1.5])
    ax_3d.set_zlim([-1.5,1.5])

    ax_3d.set_xlabel('x')
    ax_3d.set_ylabel('y')
    ax_3d.set_zlabel('z')

    plt.pause(0.01)
