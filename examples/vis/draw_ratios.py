import sys
try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

if IN_COLAB:
    print("**** in colab ****")
    if "/content/pyCFTrackers" not in sys.path:
        print("**** path not set ****")
        sys.path.insert(0, "/content/pyCFTrackers")
        print(sys.path)

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from lib.utils import get_ground_truthes_viot

gts=get_ground_truthes_viot('/content/pyCFTrackers/dataset/VIOT/park_mavic_1')[109:190]

occ = np.loadtxt('/content/pyCFTrackers/results/occ_park_mavic_1.txt')
kcf_hog = np.loadtxt('/content/pyCFTrackers/results/kcf_park_mavic_1.txt')
ldes = np.loadtxt('/content/pyCFTrackers/results/ldes_park_mavic_1.txt')
csrdcf = np.loadtxt('/content/pyCFTrackers/results/csrdcf_park_mavic_1.txt')
strcf = np.loadtxt('/content/pyCFTrackers/results/strcf_park_mavic_1.txt')
dimp50 = np.loadtxt('/content/pyCFTrackers/results/dimp50_park_mavic_1.txt')
kys = np.loadtxt('/content/pyCFTrackers/results/kys_park_mavic_1.txt')
tomp = np.loadtxt('/content/pyCFTrackers/results/tomp_park_mavic_1.txt')
prdimp50 = np.loadtxt('/content/pyCFTrackers/results/prdimp50_park_mavic_1.txt')

print('score_kcf ', 1 - np.mean( np.abs(1-occ - kcf_hog) ) )
print('score_ldes ', 1 - np.mean( np.abs(1-occ - ldes) ) )
print('score_csrdcf ', 1 - np.mean( np.abs(1-occ - csrdcf) ) )
print('score_strcf ', 1 - np.mean( np.abs(1-occ - strcf) ) )
print('score_dimp50 ', 1 - np.mean( np.abs(1-occ - dimp50) ) )
print('score_kys ', 1 - np.mean( np.abs(1-occ - kys) ) )
print('score_tomp ', 1 - np.mean( np.abs(1-occ - tomp) ) )
print('score_prdimp50 ', 1 - np.mean( np.abs(1-occ - prdimp50) ) )

plt.rcParams["figure.figsize"] = (20,6)
plt.rcParams.update({'font.size': 14})

fig, ax = plt.subplots()

ax.plot(1-occ, color='black', linewidth=2, label='Target \n Visibility')
# ax.plot(kcf_hog, linewidth=2, label='KCF_HOG')
# ax.plot(ldes, linewidth=2, label='LDES')
# ax.plot(csrdcf, linewidth=2, label='CSRDCF')
# ax.plot(strcf, linewidth=2, label='STRCF')
ax.plot(dimp50, linewidth=2, label='DiMP50')
ax.plot(prdimp50, linewidth=2, label='PrDiMP50')
ax.plot(kys, linewidth=2, label='KYS')
ax.plot(tomp, linewidth=2, label='ToMP')

for i in range(0, 81, 10):

    ax.axvline(x=i, ymin=0.0, ymax=1.0, color='gray', linewidth=1, linestyle='--')
    img = cv.imread('/content/pyCFTrackers/dataset/VIOT/park_mavic_1/{:08}.jpg'.format(i+110))
    
    x_min = int( np.max([gts[i, 0] - gts[i, 2], 0]) )
    x_max = int( np.min([gts[i, 0] + 2*gts[i, 2], img.shape[1]-1]) )
    y_min = int( np.max([gts[i, 1] - gts[i, 3], 0]) )
    y_max = int( np.min([gts[i, 1] + 2*gts[i, 3], img.shape[0]-1]) )

    img = img[y_min:y_max, x_min:x_max, :]
    img = cv.resize(img, (70,140))
    # cv.rectangle(img, gts[i], (0,255,255), 2)
    # binImg = cv.cvtColor(binImg, cv.COLOR_GRAY2BGR)
    img = img.astype(np.float32) / 255.0
    imagebox = OffsetImage(img, zoom=1)
    ab = AnnotationBbox(imagebox, (i, -0.9))
    ax.add_artist(ab)


# plt.title(dataset_name + '')
plt.xlabel('Image Number')
ax.set_ylim(-1.8, 1.5)
ax.set_xlim(-5, 95)
plt.ylabel('psr/psr0')
plt.legend()
plt.grid()
plt.savefig('VIOT_ratios.pdf', format="pdf")