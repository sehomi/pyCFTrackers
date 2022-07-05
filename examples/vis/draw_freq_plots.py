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

import json
import numpy as np
import matplotlib.pyplot as plt
from examples.vis.VIOT_info import VIOT, FREQS, FREQ_DATAS
from lib.utils import get_thresh_precision_pair,get_thresh_success_pair,calAUC

def get_preds_by_name(preds_dict,key):
    valid_keys=['gts','kcf_gray_preds','kcf_hog_preds','dcf_gray_preds',
                'dcf_hog_preds','mosse','csk','eco_hc','kcf_cn','kcf_pyECO_cn',
                'kcf_pyECO_hog','cn','DSST','DAT','Staple', 'ldes_preds',
                'strcf_preds', 'csrdcf_preds', 'tracker_dimp50_preds', 'tracker_kys_preds',
                'tracker_tomp_preds','tracker_prdimp50_preds']
    assert key in valid_keys
    str_preds=preds_dict[key]
    np_preds=[]
    for bbox in str_preds:
        bbox=[int(a) for a in bbox]
        np_preds.append(bbox)
    np_preds=np.array(np_preds)
    return np_preds

def draw_plot(datalist,dataset_name):
    f = open('../all_results.json', 'r')
    results = json.load(f)

    successes_kcf_gray_all = np.zeros((101,))
    successes_kcf_hog_all = np.zeros_like(successes_kcf_gray_all)
    successes_ldes_all = np.zeros_like(successes_kcf_gray_all)
    successes_strcf_all = np.zeros_like(successes_kcf_gray_all)
    successes_csrdcf_all = np.zeros_like(successes_kcf_gray_all)
    successes_dimp50_all = np.zeros_like(successes_kcf_gray_all)
    successes_prdimp50_all = np.zeros_like(successes_kcf_gray_all)
    successes_tomp_all = np.zeros_like(successes_kcf_gray_all)
    successes_kys_all = np.zeros_like(successes_kcf_gray_all)

    success_kcf_hog_all = []
    success_ldes_all = []
    success_strcf_all = []
    success_csrdcf_all = []
    success_dimp50_all = []
    success_prdimp50_all = []
    success_kys_all = []
    success_tomp_all = []

    results_list = []
    for data_name in results.keys():
        if data_name not in datalist:
            print("ignoring ", data_name)
            continue
        else:
            print("plotting ", data_name)
            results_list.append(data_name)

    num_videos=0
    for data_name in results_list:

        num_videos+=1
        data_all = results[data_name]
        gts = get_preds_by_name(data_all, 'gts')
        kcf_hog_preds = get_preds_by_name(data_all, 'kcf_hog_preds')
        ldes_preds = get_preds_by_name(data_all, 'ldes_preds')
        strcf_preds = get_preds_by_name(data_all, 'strcf_preds')
        csrdcf_preds = get_preds_by_name(data_all, 'csrdcf_preds')
        dimp50_preds = get_preds_by_name(data_all, 'tracker_dimp50_preds')
        prdimp50_preds = get_preds_by_name(data_all, 'tracker_prdimp50_preds')
        tomp_preds = get_preds_by_name(data_all, 'tracker_tomp_preds')
        kys_preds = get_preds_by_name(data_all, 'tracker_kys_preds')

        success_kcf_hog_all.append( calAUC( np.array(get_thresh_success_pair(gts, kcf_hog_preds)[1]) ) )
        success_ldes_all.append( calAUC( np.array(get_thresh_success_pair(gts, ldes_preds)[1]) ) )
        success_strcf_all.append( calAUC( np.array(get_thresh_success_pair(gts, strcf_preds)[1]) ) )
        success_csrdcf_all.append( calAUC( np.array(get_thresh_success_pair(gts, csrdcf_preds)[1]) ) )
        success_dimp50_all.append(calAUC( np.array(get_thresh_success_pair(gts, dimp50_preds)[1]) ) )
        success_prdimp50_all.append( calAUC( np.array(get_thresh_success_pair(gts, prdimp50_preds)[1]) ) )
        success_kys_all.append( calAUC( np.array(get_thresh_success_pair(gts, kys_preds)[1]) ) )
        success_tomp_all.append( calAUC( np.array(get_thresh_success_pair(gts, tomp_preds)[1]) ) )

    idxs = []
    for j in  range(len(FREQS)):
        freq = FREQS[j]
        freq_str = str(freq)

        for i in  range(len(results_list)):
            key = results_list[i]
            if freq_str in key:
                idxs.append(i)
    
    print(idxs)
    print(list(np.array(results_list)[idxs]))
    success_kcf_hog_all = np.array( success_kcf_hog_all )[idxs]
    success_ldes_all = np.array( success_ldes_all )[idxs] 
    success_strcf_all = np.array( success_strcf_all )[idxs] 
    success_csrdcf_all = np.array( success_csrdcf_all )[idxs] 
    success_dimp50_all = np.array( success_dimp50_all )[idxs] 
    success_prdimp50_all = np.array( success_prdimp50_all )[idxs] 
    success_kys_all = np.array( success_kys_all )[idxs] 
    success_tomp_all = np.array( success_tomp_all )[idxs] 


    plt.plot(FREQS, success_kcf_hog_all, ':', color='blue', label='KCF_HOG ')
    plt.plot(FREQS, success_ldes_all, ':', color='orange', label='LDES ')
    plt.plot(FREQS, success_strcf_all, ':', color='green', label='STRCF ')
    plt.plot(FREQS, success_csrdcf_all, ':', color='red', label='CSRDCF ')
    # plt.plot(FREQS, success_dimp50_all, '--', label='DiMP50 ')
    # plt.plot(FREQS, success_prdimp50_all, '--', label='PrDiMP50 ')
    # plt.plot(FREQS, success_kys_all, '--', label='KYS ')
    # plt.plot(FREQS, success_tomp_all, '--', label='ToMP ')
    # plt.title(dataset_name + '')

    f = open('../all_results_viot.json', 'r')
    results = json.load(f)

    successes_kcf_gray_all = np.zeros((101,))
    successes_kcf_hog_all = np.zeros_like(successes_kcf_gray_all)
    successes_ldes_all = np.zeros_like(successes_kcf_gray_all)
    successes_strcf_all = np.zeros_like(successes_kcf_gray_all)
    successes_csrdcf_all = np.zeros_like(successes_kcf_gray_all)
    successes_dimp50_all = np.zeros_like(successes_kcf_gray_all)
    successes_prdimp50_all = np.zeros_like(successes_kcf_gray_all)
    successes_tomp_all = np.zeros_like(successes_kcf_gray_all)
    successes_kys_all = np.zeros_like(successes_kcf_gray_all)

    success_kcf_hog_all = []
    success_ldes_all = []
    success_strcf_all = []
    success_csrdcf_all = []
    success_dimp50_all = []
    success_prdimp50_all = []
    success_kys_all = []
    success_tomp_all = []

    results_list = []
    for data_name in results.keys():
        if data_name not in datalist:
            print("ignoring ", data_name)
            continue
        else:
            print("plotting ", data_name)
            results_list.append(data_name)

    num_videos=0
    for data_name in results_list:

        num_videos+=1
        data_all = results[data_name]
        gts = get_preds_by_name(data_all, 'gts')
        kcf_hog_preds = get_preds_by_name(data_all, 'kcf_hog_preds')
        ldes_preds = get_preds_by_name(data_all, 'ldes_preds')
        strcf_preds = get_preds_by_name(data_all, 'strcf_preds')
        csrdcf_preds = get_preds_by_name(data_all, 'csrdcf_preds')
        dimp50_preds = get_preds_by_name(data_all, 'tracker_dimp50_preds')
        prdimp50_preds = get_preds_by_name(data_all, 'tracker_prdimp50_preds')
        tomp_preds = get_preds_by_name(data_all, 'tracker_tomp_preds')
        kys_preds = get_preds_by_name(data_all, 'tracker_kys_preds')

        success_kcf_hog_all.append( calAUC( np.array(get_thresh_success_pair(gts, kcf_hog_preds)[1]) ) )
        success_ldes_all.append( calAUC( np.array(get_thresh_success_pair(gts, ldes_preds)[1]) ) )
        success_strcf_all.append( calAUC( np.array(get_thresh_success_pair(gts, strcf_preds)[1]) ) )
        success_csrdcf_all.append( calAUC( np.array(get_thresh_success_pair(gts, csrdcf_preds)[1]) ) )
        success_dimp50_all.append( calAUC( np.array(get_thresh_success_pair(gts, dimp50_preds)[1]) ) )
        success_prdimp50_all.append( calAUC( np.array(get_thresh_success_pair(gts, prdimp50_preds)[1]) ) )
        success_kys_all.append( calAUC( np.array(get_thresh_success_pair(gts, kys_preds)[1]) ) )
        success_tomp_all.append( calAUC( np.array(get_thresh_success_pair(gts, tomp_preds)[1]) ) )

    idxs = []
    for j in  range(len(FREQS)):
        freq = FREQS[j]
        freq_str = str(freq)

        for i in  range(len(results_list)):
            key = results_list[i]
            if freq_str in key:
                idxs.append(i)

    success_kcf_hog_all = np.array( success_kcf_hog_all )[idxs]
    success_ldes_all = np.array( success_ldes_all )[idxs] 
    success_strcf_all = np.array( success_strcf_all )[idxs] 
    success_csrdcf_all = np.array( success_csrdcf_all )[idxs] 
    success_dimp50_all = np.array( success_dimp50_all )[idxs] 
    success_prdimp50_all = np.array( success_prdimp50_all )[idxs] 
    success_kys_all = np.array( success_kys_all )[idxs] 
    success_tomp_all = np.array( success_tomp_all )[idxs] 

    plt.plot(FREQS, success_kcf_hog_all, color='blue', label='KCF_HOG_VIOT ')
    plt.plot(FREQS, success_ldes_all, color='orange', label='LDES_VIOT ')
    plt.plot(FREQS, success_strcf_all, color='green', label='STRCF_VIOT ')
    plt.plot(FREQS, success_csrdcf_all, color='red', label='CSRDCF_VIOT ')
    # plt.plot(FREQS, success_dimp50_all, label='DiMP50_VIOT ')
    # plt.plot(FREQS, success_prdimp50_all, label='PrDiMP50_VIOT ')
    # plt.plot(FREQS, success_kys_all, label='KYS_VIOT ')
    # plt.plot(FREQS, success_tomp_all, label='ToMP_VIOT ')
    # plt.title(dataset_name + '')
    plt.xlabel('Camera Motion Frequencies (Hz)')
    plt.ylabel('Success Rate (%)')
    plt.legend()
    plt.grid()
    plt.xticks(FREQS, FREQS)
    plt.savefig(dataset_name + '_freq.pdf', format="pdf")


if __name__=='__main__':

    draw_plot(FREQ_DATAS,'VIOT')