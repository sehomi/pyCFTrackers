import os
import numpy as np
import matplotlib.pyplot as plt
from examples.pytracker import PyTracker
import json
from lib.utils import get_ground_truthes,get_ground_truthes_viot,get_thresh_success_pair,get_thresh_precision_pair,calAUC
from examples.otbdataset_config import OTBDatasetConfig
from examples.viotdataset_config import VIOTDatasetConfig

if __name__ == '__main__':
    # data_dir = '../dataset/OTB100'
    data_dir = '../dataset/VIOT'
    # data_names=sorted(os.listdir(data_dir)) ## OTB
    data_names=sorted([ name for name in os.listdir(data_dir) if \
                        os.path.isdir(os.path.join(data_dir, name)) ]) ## VIOT
    viot_results = {}

    # dataset_config=OTBDatasetConfig()
    dataset_config=VIOTDatasetConfig()

    for data_name in data_names:

        print('data name:', data_name)
        viot_results[data_name]={}
        data_path = os.path.join(data_dir, data_name)
        # img_dir = os.path.join(data_path,'img') ## OTB
        img_dir = data_path ## VIOT

        gts=get_ground_truthes_viot(data_path)
        if data_name in dataset_config.frames.keys():
            start_frame,end_frame=dataset_config.frames[data_name][:2]
            gts = gts[start_frame - 1:end_frame]
        else:
            continue

        viot_results[data_name]['gts']=[]
        for gt in gts:
            viot_results[data_name]['gts'].append(list(gt.astype(np.int)))


        # tracker_kcf_gray=PyTracker(img_dir, tracker_type='KCF_GRAY',dataset_config=dataset_config)
        tracker_kcf_hog=PyTracker(img_dir,tracker_type='KCF_HOG',dataset_config=dataset_config)
        # tracker_bacf=PyTracker(img_dir,tracker_type='BACF',dataset_config=dataset_config)
        tracker_ldes=PyTracker(img_dir,tracker_type='LDES',dataset_config=dataset_config)
        tracker_strcf=PyTracker(img_dir,tracker_type='STRCF',dataset_config=dataset_config)
        tracker_csrdcf=PyTracker(img_dir,tracker_type='CSRDCF',dataset_config=dataset_config)
        # tracker_mosse=PyTracker(img_dir,tracker_type='MOSSE',dataset_config=dataset_config)
        # tracker_csk=PyTracker(img_dir,tracker_type='CSK',dataset_config=dataset_config)
        # tracker_kcf_cn=PyTracker(img_dir,tracker_type='KCF_CN',dataset_config=dataset_config)
        tracker_eco=PyTracker(img_dir,tracker_type='ECO',dataset_config=dataset_config)
        tracker_prdimp50=PyTracker(img_dir,tracker_type='PRDIMP50',dataset_config=dataset_config)
        tracker_kys=PyTracker(img_dir,tracker_type='KYS',dataset_config=dataset_config)
        tracker_tomp=PyTracker(img_dir,tracker_type='TOMP',dataset_config=dataset_config)
        tracker_dimp50=PyTracker(img_dir,tracker_type='DIMP50',dataset_config=dataset_config)
        # tracker_eco_hc=PyTracker(img_dir,tracker_type='ECO-HC',dataset_config=dataset_config)
        # tracker_cn=PyTracker(img_dir,tracker_type='CN',dataset_config=dataset_config)

        # kcf_gray_preds=tracker_kcf_gray.tracking()
        # viot_results[data_name]['kcf_gray_preds']=[]
        # for kcf_gray_pred in kcf_gray_preds:
        #     viot_results[data_name]['kcf_gray_preds'].append(list(kcf_gray_pred.astype(np.int)))
        # print('kcf gray done!')

        dimp50_preds=tracker_dimp50.tracking()
        viot_results[data_name]['tracker_dimp50_preds'] = []
        for dimp50_pred in dimp50_preds:
            viot_results[data_name]['tracker_dimp50_preds'].append(list(dimp50_pred.astype(np.int)))
        print('dimp50 done!')

        kys_preds=tracker_kys.tracking()
        viot_results[data_name]['tracker_kys_preds'] = []
        for kys_pred in kys_preds:
            viot_results[data_name]['tracker_kys_preds'].append(list(kys_pred.astype(np.int)))
        print('kys done!')

        tomp_preds=tracker_tomp.tracking()
        viot_results[data_name]['tracker_tomp_preds'] = []
        for tomp_pred in tomp_preds:
            viot_results[data_name]['tracker_tomp_preds'].append(list(tomp_pred.astype(np.int)))
        print('tomp done!')

        prdimp50_preds=tracker_prdimp50.tracking()
        viot_results[data_name]['tracker_prdimp50_preds'] = []
        for prdimp50_pred in prdimp50_preds:
            viot_results[data_name]['tracker_prdimp50_preds'].append(list(prdimp50_pred.astype(np.int)))
        print('prdimp50 done!')

        eco_preds = tracker_eco.tracking()
        viot_results[data_name]['eco'] = []
        for eco_pred in eco_preds:
            viot_results[data_name]['eco'].append(list(eco_pred.astype(np.int)))
        print('eco done!')

        kcf_hog_preds=tracker_kcf_hog.tracking()
        viot_results[data_name]['kcf_hog_preds'] = []
        for kcf_hog_pred in kcf_hog_preds:
            viot_results[data_name]['kcf_hog_preds'].append(list(kcf_hog_pred.astype(np.int)))
        print('kcf hog done!')

        ldes_preds=tracker_ldes.tracking()
        viot_results[data_name]['ldes_preds'] = []
        for ldes_pred in ldes_preds:
            viot_results[data_name]['ldes_preds'].append(list(ldes_pred.astype(np.int)))
        print('ldes done!')

        csrdcf_preds=tracker_csrdcf.tracking()
        viot_results[data_name]['csrdcf_preds'] = []
        for csrdcf_pred in csrdcf_preds:
            viot_results[data_name]['csrdcf_preds'].append(list(csrdcf_pred.astype(np.int)))
        print('csrdcf done!')

        strcf_preds=tracker_strcf.tracking()
        viot_results[data_name]['strcf_preds'] = []
        for strcf_pred in strcf_preds:
            viot_results[data_name]['strcf_preds'].append(list(strcf_pred.astype(np.int)))
        print('strcf done!')

        # bacf_preds=tracker_bacf.tracking()
        # viot_results[data_name]['bacf_preds'] = []
        # for bacf_pred in bacf_preds:
        #     viot_results[data_name]['bacf_preds'].append(list(bacf_pred.astype(np.int)))
        # print('bacf done!')

        # mosse_preds=tracker_mosse.tracking()
        # viot_results[data_name]['mosse'] = []
        # for mosse_pred in mosse_preds:
        #     viot_results[data_name]['mosse'].append(list(mosse_pred.astype(np.int)))
        # print('mosse done!')
        #
        # csk_preds=tracker_csk.tracking()
        # viot_results[data_name]['csk'] = []
        # for csk_pred in csk_preds:
        #     viot_results[data_name]['csk'].append(list(csk_pred.astype(np.int)))
        # print('csk done!')

        # kcf_cn_preds=tracker_kcf_cn.tracking()
        # viot_results[data_name]['kcf_cn']=[]
        # for kcf_cn_pred in kcf_cn_preds:
        #     viot_results[data_name]['kcf_cn'].append(list(kcf_cn_pred.astype(np.int)))
        # print('kcf_cn done!')

        # eco_hc_preds=tracker_eco_hc.tracking()
        # viot_results[data_name]['eco_hc']=[]
        # for eco_hc_pred in eco_hc_preds:
        #     viot_results[data_name]['eco_hc'].append(list(eco_hc_pred.astype(np.int)))
        # print('eco_hc done!')
        #
        # cn_preds=tracker_cn.tracking()
        # viot_results[data_name]['cn']=[]
        # for cn_pred in cn_preds:
        #     viot_results[data_name]['cn'].append(list(cn_pred.astype(np.int)))
        # print('cn done!')

        # threshes,precisions_kcf_gray=get_thresh_precision_pair(gts,kcf_gray_preds)
        threshes,precisions_kcf_hog=get_thresh_precision_pair(gts,kcf_hog_preds)
        # _,precisions_bacf=get_thresh_precision_pair(gts,bacf_preds)
        _,precisions_ldes=get_thresh_precision_pair(gts,ldes_preds)
        _,precisions_strcf=get_thresh_precision_pair(gts,strcf_preds)
        _,precisions_csrdcf=get_thresh_precision_pair(gts,csrdcf_preds)
        # _,precisions_mosse=get_thresh_precision_pair(gts,mosse_preds)
        # _,precisions_csk=get_thresh_precision_pair(gts,csk_preds)
        # _,precisions_kcf_cn=get_thresh_precision_pair(gts,kcf_cn_preds)
        _,precisions_eco=get_thresh_precision_pair(gts,eco_preds)
        _,precisions_dimp50=get_thresh_precision_pair(gts,dimp50_preds)
        _,precisions_prdimp50=get_thresh_precision_pair(gts,prdimp50_preds)
        _,precisions_kys=get_thresh_precision_pair(gts,kys_preds)
        _,precisions_tomp=get_thresh_precision_pair(gts,tomp_preds)
        # _,precisions_eco_hc=get_thresh_precision_pair(gts,eco_hc_preds)
        # _,precisions_cn=get_thresh_precision_pair(gts,cn_preds)
        idx20=[i for i, x in enumerate(threshes) if x==20][0]
        #
        # plt.plot(threshes, precisions_kcf_gray, label='KCF_GRAY '+str(precisions_kcf_gray[idx20])[:5])
        plt.plot(threshes,precisions_kcf_hog,label='KCF_HOG '+str(precisions_kcf_hog[idx20])[:5])
        # plt.plot(threshes,precisions_bacf,label='BACF '+str(precisions_bacf[idx20])[:5])
        plt.plot(threshes,precisions_ldes,label='LDES '+str(precisions_ldes[idx20])[:5])
        plt.plot(threshes,precisions_strcf,label='STRCF '+str(precisions_strcf[idx20])[:5])
        plt.plot(threshes,precisions_csrdcf,label='CSRDCF '+str(precisions_csrdcf[idx20])[:5])
        # plt.plot(threshes,precisions_mosse,label='MOSSE '+str(precisions_mosse[idx20])[:5])
        # plt.plot(threshes,precisions_csk,label='CSK '+str(precisions_csk[idx20])[:5])
        # plt.plot(threshes,precisions_kcf_cn,label='KCF_CN '+str(precisions_kcf_cn[idx20])[:5])
        plt.plot(threshes,precisions_eco,label='ECO '+str(precisions_eco[idx20])[:5])
        plt.plot(threshes,precisions_dimp50,label='DIMP50 '+str(precisions_dimp50[idx20])[:5])
        plt.plot(threshes,precisions_prdimp50,label='PRDIMP50 '+str(precisions_prdimp50[idx20])[:5])
        plt.plot(threshes,precisions_kys,label='KYS '+str(precisions_kys[idx20])[:5])
        plt.plot(threshes,precisions_tomp,label='TOMP '+str(precisions_tomp[idx20])[:5])
        # plt.plot(threshes,precisions_eco_hc,label='ECO-HC '+str(precisions_eco_hc[idx20])[:5])
        # plt.plot(threshes,precisions_cn,label='CN '+str(precisions_cn[idx20])[:5])
        plt.title(data_name+' Precision')
        plt.xlabel('thresh')
        plt.ylabel('precision')
        plt.legend()
        # # plt.savefig('../results/OTB100_cftrackers/'+data_name+'_precision.jpg')
        plt.savefig('../results/VIOT/'+data_name+'_precision.jpg')
        plt.clf()
        #
        #
        # threshes,successes_kcf_gray=get_thresh_success_pair(gts, kcf_gray_preds)
        threshes,successes_kcf_hog=get_thresh_success_pair(gts,kcf_hog_preds)
        # _,successes_bacf=get_thresh_success_pair(gts,bacf_preds)
        _,successes_ldes=get_thresh_success_pair(gts,ldes_preds)
        _,successes_strcf=get_thresh_success_pair(gts,strcf_preds)
        _,successes_csrdcf=get_thresh_success_pair(gts,csrdcf_preds)
        # _,successes_mosse=get_thresh_success_pair(gts,mosse_preds)
        # _,successes_csk=get_thresh_success_pair(gts,csk_preds)
        # _,successes_kcf_cn=get_thresh_success_pair(gts,kcf_cn_preds)
        _,successes_eco=get_thresh_success_pair(gts,eco_preds)
        _,successes_dimp50=get_thresh_success_pair(gts,dimp50_preds)
        _,successes_prdimp50=get_thresh_success_pair(gts,prdimp50_preds)
        _,successes_kys=get_thresh_success_pair(gts,kys_preds)
        _,successes_tomp=get_thresh_success_pair(gts,tomp_preds)
        # _,successes_eco_hc=get_thresh_success_pair(gts,eco_hc_preds)
        # _,successes_cn=get_thresh_success_pair(gts,cn_preds)
        # plt.plot(threshes,successes_kcf_cn,label='KCF_CN '+str(calAUC(successes_kcf_cn))[:5])
        plt.plot(threshes,successes_eco,label='ECO '+str(calAUC(successes_eco))[:5])
        plt.plot(threshes,successes_dimp50,label='DIMP50 '+str(calAUC(successes_dimp50))[:5])
        plt.plot(threshes,successes_prdimp50,label='PRDIMP50 '+str(calAUC(successes_prdimp50))[:5])
        plt.plot(threshes,successes_kys,label='KYS '+str(calAUC(successes_kys))[:5])
        plt.plot(threshes,successes_tomp,label='TOMP '+str(calAUC(successes_tomp))[:5])
        # plt.plot(threshes,successes_kcf_gray, label='KCF_GRAY '+str(calAUC(successes_kcf_gray))[:5])
        plt.plot(threshes,successes_kcf_hog,label='KCF_HOG '+str(calAUC(successes_kcf_hog))[:5])
        # plt.plot(threshes,successes_bacf,label='BACF '+str(calAUC(successes_bacf))[:5])
        plt.plot(threshes,successes_ldes,label='LDES '+str(calAUC(successes_ldes))[:5])
        plt.plot(threshes,successes_strcf,label='STRCF '+str(calAUC(successes_strcf))[:5])
        plt.plot(threshes,successes_csrdcf,label='CSRDCF '+str(calAUC(successes_csrdcf))[:5])
        # plt.plot(threshes,successes_mosse,label='MOSSE '+str(calAUC(successes_mosse))[:5])
        # plt.plot(threshes,successes_csk,label='CSK '+str(calAUC(successes_csk))[:5])
        # plt.plot(threshes,successes_eco_hc,label='ECO-HC '+str(calAUC(successes_eco_hc))[:5])
        # plt.plot(threshes,successes_cn,label='CN '+str(calAUC(successes_cn))[:5])
        #
        plt.title(data_name+' Success')
        plt.xlabel('thresh')
        plt.ylabel('success')
        plt.legend()
        # # plt.savefig('../results/OTB100_cftrackers/'+data_name+'_success.jpg')
        plt.savefig('../results/VIOT/'+data_name+'_success.jpg')
        plt.clf()

    json_content = json.dumps(viot_results, default=str)
    f = open('viot_results.json', 'w')
    f.write(json_content)
    f.close()
