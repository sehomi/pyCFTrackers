class VIOTDatasetConfig:

    fov={
        "cup_0.5HZ":55.0,
        "cup_0.9HZ":55.0,
        "cup_1.1HZ":55.0,
        "cup_1.5HZ":55.0,
        "cup_1.8HZ":55.0,
        "cup_2.1HZ":55.0,
        "cup_3.2HZ":55.0,
        "park_mavic_1":66.0,
        "park_mavic_2":66.0,
        "park_mavic_3":66.0,
        "park_mavic_4":66.0,
        "park_mavic_5":66.0,
        "park_mavic_6":66.0,
        "park_mavic_7":66.0,
        "soccerfield_mavic_3":66.0,
        "soccerfield_mavic_4":66.0
    }

    frames={
        # "cup_0.5HZ":[1,220],
        # "cup_0.9HZ":[1,760],
        # "cup_1.1HZ":[1,329],
        # "cup_1.5HZ":[1,312],
        # "cup_1.8HZ":[1,357],
        # "cup_2.1HZ":[1,465],
        # "cup_3.2HZ":[1,254],
        # "park_mavic_1":[1,1005],
        # "park_mavic_1":[1,630],
        # "park_mavic_2":[1,945],
        # "park_mavic_3":[1,2022],
        # "park_mavic_3":[710,1010],
        # "park_mavic_4":[1,1906],
        # "park_mavic_5":[840,1697],
        # "park_mavic_6":[1,1137],
        # "park_mavic_7":[1,915],
        "park_mavic_7":[1,360],
        "soccerfield_mavic_3":[1,1104],
        "soccerfield_mavic_4":[1,1297]
    }

    params={
        "MOSSE":None,
        "CSK":None,
        "CN":None,
        "DSST":None,
        "Staple":None,
        "Staple-CA":None,
        "KCF_CN":None,
        "KCF_GRAY":None,
        "KCF_HOG":{"cup_0.5HZ":[0.1, 1], "cup_0.9HZ":[0.1, 1], "cup_1.1HZ":[0.1, 1], \
                   "cup_1.5HZ":[0.1, 1], "cup_1.8HZ":[0.1, 1], "cup_2.1HZ":[0.1, 1], \
                   "cup_3.2HZ":[0.1, 1], "park_mavic_1":[0.1, 0.3], "park_mavic_2":[0.1, 0.3], \
                   "park_mavic_3":[0.1, 0.3], "park_mavic_4":[0.1, 0.3], "park_mavic_5":[0.1, 0.3], \
                   "park_mavic_6":[0.1, 0.3], "park_mavic_7":[0.1, 0.3], "soccerfield_mavic_3":[0.1, 0.3], \
                   "soccerfield_mavic_4":[0.1, 0.3]},
        "DCF_GRAY":None,
        "DCF_HOG":None,
        "DAT":None,
        "ECO-HC":None,
        "ECO":{"cup_0.5HZ":[0.5, 1], "cup_0.9HZ":[0.5, 1], "cup_1.1HZ":[0.5, 1], \
               "cup_1.5HZ":[0.5, 1], "cup_1.8HZ":[0.5, 1], "cup_2.1HZ":[0.5, 1], \
               "cup_3.2HZ":[0.5, 1], "park_mavic_1":[0.5, 0.3], "park_mavic_2":[0.5, 0.3], \
               "park_mavic_3":[0.5, 0.3], "park_mavic_4":[0.5, 0.3], "park_mavic_5":[0.5, 0.3], \
               "park_mavic_6":[0.5, 0.3], "park_mavic_7":[0.5, 0.3], "soccerfield_mavic_3":[0.5, 0.3], \
               "soccerfield_mavic_4":[0.5, 0.3]},
        "DIMP50":{"cup_0.5HZ":[0.3, 1], "cup_0.9HZ":[0.3, 1], "cup_1.1HZ":[0.3, 1], \
                  "cup_1.5HZ":[0.3, 1], "cup_1.8HZ":[0.3, 1], "cup_2.1HZ":[0.3, 1], \
                  "cup_3.2HZ":[0.3, 1], "park_mavic_1":[0.3, -50], "park_mavic_2":[0.3, 0], \
                  "park_mavic_3":[0.3, 0], "park_mavic_4":[0.3, 0], "park_mavic_5":[0.3, 0], \
                  "park_mavic_6":[0.3, -60], "park_mavic_7":[0.2, -80], "soccerfield_mavic_3":[0.3, 0], \
                  "soccerfield_mavic_4":[0.3, 0]},
        "PRDIMP50":{"cup_0.5HZ":[0.1, 1], "cup_0.9HZ":[0.1, 1], "cup_1.1HZ":[0.1, 1], \
                  "cup_1.5HZ":[0.1, 1], "cup_1.8HZ":[0.1, 1], "cup_2.1HZ":[0.1, 1], \
                  "cup_3.2HZ":[0.1, 1], "park_mavic_1":[0.1, -80], "park_mavic_2":[0.1, 0], \
                  "park_mavic_3":[0.1, 0], "park_mavic_4":[0.1, 0], "park_mavic_5":[0.1, 0], \
                  "park_mavic_6":[0.1, 0], "park_mavic_7":[0.2, -80], "soccerfield_mavic_3":[0.1, 0], \
                  "soccerfield_mavic_4":[0.1, 0]},
        "KYS":{"cup_0.5HZ":[0.2, 1], "cup_0.9HZ":[0.2, 1], "cup_1.1HZ":[0.2, 1], \
                  "cup_1.5HZ":[0.2, 1], "cup_1.8HZ":[0.2, 1], "cup_2.1HZ":[0.2, 1], \
                  "cup_3.2HZ":[0.2, 1], "park_mavic_1":[0.2, -90], "park_mavic_2":[0.2, 0], \
                  "park_mavic_3":[0.2, 0], "park_mavic_4":[0.2, 0], "park_mavic_5":[0.2, 0], \
                  "park_mavic_6":[0.2, 0], "park_mavic_7":[0.2, 0], "soccerfield_mavic_3":[0.2, 0], \
                  "soccerfield_mavic_4":[0.2, 0]},
        "TOMP":{"cup_0.5HZ":[0.2, 1], "cup_0.9HZ":[0.2, 1], "cup_1.1HZ":[0.2, 1], \
                  "cup_1.5HZ":[0.2, 1], "cup_1.8HZ":[0.2, 1], "cup_2.1HZ":[0.2, 1], \
                  "cup_3.2HZ":[0.2, 1], "park_mavic_1":[0.5, -50], "park_mavic_2":[0.2, 0], \
                  "park_mavic_3":[0.2, 0], "park_mavic_4":[0.2, 0], "park_mavic_5":[0.2, 0], \
                  "park_mavic_6":[0.2, 0], "park_mavic_7":[0.2, 0], "soccerfield_mavic_3":[0.2, 0], \
                  "soccerfield_mavic_4":[0.2, 0]},
        "BACF":None,
        "CSRDCF":{"cup_0.5HZ":[0.3, 1], "cup_0.9HZ":[0.3, 1], "cup_1.1HZ":[0.3, 1], \
                  "cup_1.5HZ":[0.3, 1], "cup_1.8HZ":[0.3, 1], "cup_2.1HZ":[0.3, 1], \
                  "cup_3.2HZ":[0.3, 1], "park_mavic_1":[0.3, 0.3], "park_mavic_2":[0.3, 0.3], \
                  "park_mavic_3":[0.3, 0.3], "park_mavic_4":[0.3, 0.3], "park_mavic_5":[0.3, 0.3], \
                  "park_mavic_6":[0.3, 0.3], "park_mavic_7":[0.3, 0.3], "soccerfield_mavic_3":[0.3, 0.3], \
                  "soccerfield_mavic_4":[0.3, 0.3]},
        "CSRDCF-LP":None,
        "SAMF":None,
        "LDES":{"cup_0.5HZ":[0.2, 1], "cup_0.9HZ":[0.2, 1], "cup_1.1HZ":[0.2, 1], \
                "cup_1.5HZ":[0.2, 1], "cup_1.8HZ":[0.2, 1], "cup_2.1HZ":[0.2, 1], \
                "cup_3.2HZ":[0.2, 1], "park_mavic_1":[0.2, 0.3], "park_mavic_2":[0.2, 0.3], \
                "park_mavic_3":[0.2, 0.3], "park_mavic_4":[0.2, 0.3], "park_mavic_5":[0.2, 0.3], \
                "park_mavic_6":[0.2, 0.3], "park_mavic_7":[0.2, 0.3], "soccerfield_mavic_3":[0.2, 0.3], \
                "soccerfield_mavic_4":[0.2, 0.3]},
        "DSST-LP":None,
        "MKCFup":None,
        "MKCFup-LP":None,
        "STRCF":{"cup_0.5HZ":[0.2, 1], "cup_0.9HZ":[0.2, 1], "cup_1.1HZ":[0.2, 1], \
                 "cup_1.5HZ":[0.2, 1], "cup_1.8HZ":[0.2, 1], "cup_2.1HZ":[0.2, 1], \
                 "cup_3.2HZ":[0.2, 1], "park_mavic_1":[0.2, 0.3], "park_mavic_2":[0.2, 0.3], \
                 "park_mavic_3":[0.2, 0.3], "park_mavic_4":[0.2, 0.3], "park_mavic_5":[0.2, 0.3], \
                 "park_mavic_6":[0.2, 0.3], "park_mavic_7":[0.2, 0.3], "soccerfield_mavic_3":[0.2, 0.3], \
                 "soccerfield_mavic_4":[0.2, 0.3]},
        "MCCTH-Staple":None,
        "MCCTH":None
    }
