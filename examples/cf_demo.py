import os
from examples.pytracker import PyTracker
from lib.utils import get_ground_truthes,get_ground_truthes_viot,get_ground_truthes,plot_precision,plot_success
from examples.otbdataset_config import OTBDatasetConfig
from examples.viotdataset_config import VIOTDatasetConfig

if __name__ == '__main__':
    data_dir='../dataset/VIOT'
    # data_names=sorted(os.listdir(data_dir)) ## OTB
    data_names=sorted([ name for name in os.listdir(data_dir) if \
                        os.path.isdir(os.path.join(data_dir, name)) ]) ## VIOT

    # dataset_config=OTBDatasetConfig()
    dataset_config=VIOTDatasetConfig() ## VIOT

    for data_name in data_names:
        data_path=os.path.join(data_dir,data_name)
        gts = get_ground_truthes_viot(data_path)
        if data_name in dataset_config.frames.keys():
            start_frame,end_frame=dataset_config.frames[data_name][:2]
            gts=gts[start_frame-1:end_frame]

        # img_dir = os.path.join(data_path,'img') ## OTB
        img_dir = data_path ## VIOT
        tracker = PyTracker(img_dir,tracker_type='ECO',dataset_config=dataset_config)
        poses=tracker.tracking(verbose=True,video_path=os.path.join('../results/CF',data_name+'_vis.avi'))
        plot_success(gts,poses,os.path.join('../results/CF',data_name+'_success.jpg'))
        plot_precision(gts,poses,os.path.join('../results/CF',data_name+'_precision.jpg'))
