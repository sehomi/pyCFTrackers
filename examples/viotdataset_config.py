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
        "cup_0.5HZ":[1,2],
        # "cup_0.9HZ":[1,760],
        "cup_0.9HZ":[1,2],
        # "cup_1.1HZ":[1,329],
        "cup_1.1HZ":[1,2],
        # "cup_1.5HZ":[1,312],
        "cup_1.5HZ":[1,2],
        # "cup_1.8HZ":[1,357],
        "cup_1.8HZ":[1,2],
        # "cup_2.1HZ":[1,465],
        "cup_2.1HZ":[1,2],
        # "cup_3.2HZ":[1,254],
        "cup_3.2HZ":[1,2],
        "park_mavic_1":[1,1005],
        "park_mavic_2":[400,825],
        "park_mavic_3":[400,825],
        "park_mavic_4":[400,825],
        "park_mavic_5":[400,825],
        "park_mavic_6":[400,825],
        "park_mavic_7":[400,825],
        "soccerfield_mavic_3":[400,825],
        "soccerfield_mavic_4":[400,825]
    }

    params={
        "MOSSE":[],
        "CSK":[400,825],
        "CN":[400,825],
        "DSST":[400,825],
        "Staple":[400,825],
        "Staple-CA":[400,825],
        "KCF_CN":[400,825],
        "KCF_GRAY":[400,825],
        "KCF_HOG":{"cup_0.5HZ":[0.1, 1], "cup_0.9HZ":[0.1, 1], "cup_1.1HZ":[0.1, 1], \
                   "cup_1.5HZ":[0.1, 1], "cup_1.8HZ":[0.1, 1], "cup_2.1HZ":[0.1, 1], \
                   "cup_3.2HZ":[0.1, 1]},
        "DCF_GRAY":[400,825],
        "DCF_HOG":[400,825],
        "DAT":[400,825],
        "ECO-HC":[400,825],
        "ECO":[400,825],
        "BACF":[400,825],
        "CSRDCF":[400,825],
        "CSRDCF-LP":[400,825],
        "SAMF":[400,825],
        "LDES":[400,825],
        "DSST-LP":[400,825],
        "MKCFup":[400,825],
        "MKCFup-LP":[400,825],
        "STRCF":[400,825],
        "MCCTH-Staple":[400,825],
        "MCCTH":[400,825]
    }
