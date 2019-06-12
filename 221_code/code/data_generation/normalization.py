def get_max_values(data):

    max_values = {}
    # initialize to 0
    values = ["height", "weight"]
    for value in values:
        max_values[value] = -float("inf")
    values = ["G", "GS", "FGP", "3PP", "2PP", "eFGP", "FTP", "PER", "TSP", "3PAr", "FTr", "ORBP", "DRBP", "TRBP", "ASTP", "STLP", "BLKP", "TOVP", "USGP", "OWSPM", "DWSPM", "WSPM", "WSP48", "OBPM", "DBPM", "BPM", "VORP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "ORBPM", "DRBPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PFPM", "PPM", "MPG", "GSPG", "age", "num_seasons"]
    for value in values:
        max_values[value] = -float("inf")
    values = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP", "age", "num_seasons"]
    for i in range(len(values)):
        values[i] = "college_" + values[i]
    for value in values:
        max_values[value] = -float("inf")

    for player in data.keys():

        # measurables to find max values for
        values = ["height", "weight"]
        # find max
        for value in values:
            max_values[value] = max(max_values[value], data[player][value])

        # professional stats to find max values for
        values = ["G", "GS", "FGP", "3PP", "2PP", "eFGP", "FTP", "PER", "TSP", "3PAr", "FTr", "ORBP", "DRBP", "TRBP", "ASTP", "STLP", "BLKP", "TOVP", "USGP", "OWSPM", "DWSPM", "WSPM", "WSP48", "OBPM", "DBPM", "BPM", "VORP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "ORBPM", "DRBPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PFPM", "PPM", "MPG", "GSPG", "age", "num_seasons"]
        # find max
        for value in values:
            for season in data[player]["professional"].keys():
                max_values[value] = max(max_values[value], data[player]["professional"][season][value])            

        if "college" in data[player].keys():
            # college stats to find max values for
            values = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP", "age", "num_seasons"]
            for i in range(len(values)):
                values[i] = "college_" + values[i]
            # find max
            for value in values:
                for season in data[player]["college"].keys():
                    max_values[value] = max(max_values[value], data[player]["college"][season][value[8:]])    

    return max_values


def get_max_values_stored_with_outliers():
    return {'DRBPM': 1.0, '2PP': 1.0, 'college_FGPM': 0.3844889033435565, 'college_FTP': 1.0, 'FGPM': 1.0, 'college_ASTPM': 0.29520605550883094, 'weight': 360.0, 'college_STLPM': 0.16666666666666666, '3PP': 1.0, 'DWSPM': 0.004347826086956522, 'college_MPG': 39.94285714285714, 'TRBP': 62.8, 'college_MP': 1543.0, 'PER': 133.8, 'height': 89.0, 'college_FTAPM': 0.4444444444444444, '3PAPM': 1.0, 'PPM': 3.0, 'college_TOVPM': 0.21568627450980393, 'college_2PP': 3.0, 'DRBP': 100.0, 'USGP': 47.8, 'TSP': 1.5, 'PFPM': 1.0, 'eFGP': 1.5, 'STLPM': 0.25, 'DBPM': 17.1, '3PPM': 1.0, 'GSPG': 1.0, 'college_BLKPM': 0.25, 'FGP': 1.0, 'ORBPM': 1.0, 'FTAPM': 0.6666666666666666, 'college_age': 26.0, 'OBPM': 68.6, 'num_seasons': 21.0, 'ASTP': 78.5, 'TOVP': 100.0, 'college_3PPM': 0.1607992625507439, 'WSP48': 2.712, 'college_G': 41.0, 'college_FGP': 0.833, 'college_2PAPM': 0.5128192697564264, 'MP': 3401.0, 'FTP': 1.0, 'GS': 82.0, 'BLKPM': 0.3333333333333333, 'G': 83.0, 'college_2PPM': 0.3230278518797166, 'BPM': 54.4, 'VORP': 12.4, 'college_TRBPM': 1.0, '2PPM': 1.0, 'TRBPM': 1.0, '3PAr': 1.0, 'college_FTPM': 0.4444444444444444, 'college_num_seasons': 5, 'FTPM': 0.4444444444444444, 'college_FGAPM': 0.77831309720742, 'MPG': 42.54430379746835, 'college_3PP': 1.0, 'FTr': 6.0, 'college_PPM': 1.02365020734918, 'college_3PAPM': 0.42857142857142855, 'ORBP': 100.0, 'age': 41.0, 'BLKP': 26.3, '2PAPM': 1.0, 'STLP': 12.5, 'FGAPM': 1.0, 'TOVPM': 0.6666666666666666, 'ASTPM': 0.36363636363636365, 'OWSPM': 0.1, 'WSPM': 0.1}


def get_max_values_stored_no_outliers():
    return {'DRBPM': 0.391304347826087, '2PP': 1.0, 'college_FGPM': 0.3844889033435565, 'college_FTP': 1.0, 'FGPM': 0.35, 'college_ASTPM': 0.29520605550883094, 'weight': 360.0, 'college_STLPM': 0.16666666666666666, '3PP': 1.0, 'DWSPM': 0.004347826086956522, 'college_MPG': 39.94285714285714, 'TRBP': 30.3, 'college_MP': 1543.0, 'PER': 35.3, 'height': 89.0, 'college_FTAPM': 0.3454206380719684, '3PAPM': 0.45454545454545453, 'PPM': 0.9130434782608695, 'college_TOVPM': 0.21568627450980393, 'college_2PP': 3.0, 'DRBP': 45.1, 'USGP': 41.7, 'TSP': 0.931, 'PFPM': 0.38461538461538464, 'eFGP': 1.0, 'STLPM': 0.2, 'DBPM': 7.7, '3PPM': 0.16, 'GSPG': 1.0, 'college_BLKPM': 0.25, 'FGP': 1.0, 'ORBPM': 0.3333333333333333, 'FTAPM': 0.391304347826087, 'college_age': 26.0, 'OBPM': 12.4, 'num_seasons': 21.0, 'ASTP': 57.3, 'TOVP': 100.0, 'college_3PPM': 0.1607992625507439, 'WSP48': 0.386, 'college_G': 41.0, 'college_FGP': 0.833, 'college_2PAPM': 0.5128192697564264, 'MP': 3401.0, 'FTP': 1.0, 'GS': 82.0, 'BLKPM': 0.21428571428571427, 'G': 83.0, 'college_2PPM': 0.3230278518797166, 'BPM': 15.6, 'VORP': 12.4, 'college_TRBPM': 0.5145576401623805, '2PPM': 0.2865013774104683, 'TRBPM': 0.5588235294117647, '3PAr': 1.0, 'college_FTPM': 0.2785354747317729, 'college_num_seasons': 5, 'FTPM': 0.391304347826087, 'college_FGAPM': 0.77831309720742, 'MPG': 42.54430379746835, 'college_3PP': 1.0, 'FTr': 6.0, 'college_PPM': 1.02365020734918, 'college_3PAPM': 0.42857142857142855, 'ORBP': 39.2, 'age': 41.0, 'BLKP': 17.3, '2PAPM': 0.5661764705882353, 'STLP': 10.3, 'FGAPM': 0.6927194860813705, 'TOVPM': 0.23076923076923078, 'ASTPM': 0.36363636363636365, 'OWSPM': 0.0058823529411764705, 'WSPM': 0.008695652173913044}


def get_min_values(data):

    min_values = {}
    # initialize
    values = ["height", "weight"]
    for value in values:
        min_values[value] = float("inf")
    values = ["G", "GS", "FGP", "3PP", "2PP", "eFGP", "FTP", "PER", "TSP", "3PAr", "FTr", "ORBP", "DRBP", "TRBP", "ASTP", "STLP", "BLKP", "TOVP", "USGP", "OWSPM", "DWSPM", "WSPM", "WSP48", "OBPM", "DBPM", "BPM", "VORP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "ORBPM", "DRBPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PFPM", "PPM", "MPG", "GSPG", "age", "num_seasons"]
    for value in values:
        min_values[value] = float("inf")
    values = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP", "age", "num_seasons"]
    for i in range(len(values)):
        values[i] = "college_" + values[i]
    for value in values:
        min_values[value] = float("inf")

    for player in data.keys():

        # measurables to find min values for
        values = ["height", "weight"]
        # find min
        for value in values:
            min_values[value] = min(min_values[value], data[player][value])

        # professional stats to find min values for
        values = ["G", "GS", "FGP", "3PP", "2PP", "eFGP", "FTP", "PER", "TSP", "3PAr", "FTr", "ORBP", "DRBP", "TRBP", "ASTP", "STLP", "BLKP", "TOVP", "USGP", "OWSPM", "DWSPM", "WSPM", "WSP48", "OBPM", "DBPM", "BPM", "VORP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "ORBPM", "DRBPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PFPM", "PPM", "MPG", "GSPG", "age", "num_seasons"]
        # find min
        for value in values:
            for season in data[player]["professional"].keys():
                min_values[value] = min(min_values[value], data[player]["professional"][season][value])            

        if "college" in data[player].keys():
            # college stats to find min values for
            values = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP", "age", "num_seasons"]
            for i in range(len(values)):
                values[i] = "college_" + values[i]
            # find min
            for value in values:
                for season in data[player]["college"].keys():
                    min_values[value] = min(min_values[value], data[player]["college"][season][value[8:]])    

    return min_values


def get_min_values_stored_with_outliers():
    return {'DRBPM': 0.0, '2PP': 0.0, 'college_FGPM': 0.0, 'college_FTP': 0.0, 'FGPM': 0.0, 'college_ASTPM': 0.0, 'weight': 150.0, 'college_STLPM': 0.0, '3PP': 0.0, 'DWSPM': -0.0003360215053763441, 'college_MPG': 0.0, 'TRBP': 0.0, 'college_MP': 0.0, 'PER': -54.4, 'height': 69.0, 'college_FTAPM': 0.0, '3PAPM': 0.0, 'PPM': 0.0, 'college_TOVPM': 0.0, 'college_2PP': 0.0, 'DRBP': 0.0, 'USGP': 0.0, 'TSP': 0.0, 'PFPM': 0.0, 'eFGP': 0.0, 'STLPM': 0.0, 'DBPM': -23.1, '3PPM': 0.0, 'GSPG': 0.0, 'college_BLKPM': 0.0, 'FGP': 0.0, 'ORBPM': 0.0, 'FTAPM': 0.0, 'college_age': 17.0, 'OBPM': -43.9, 'num_seasons': 1.0, 'ASTP': 0.0, 'TOVP': 0.0, 'college_3PPM': 0.0, 'WSP48': -1.312, 'college_G': 1.0, 'college_FGP': 0.0, 'college_2PAPM': 0.0, 'MP': 1.0, 'FTP': 0.0, 'GS': 0.0, 'BLKPM': 0.0, 'G': 1.0, 'college_2PPM': 0.0, 'BPM': -59.0, 'VORP': -1.6, 'college_TRBPM': 0.02143990167343252, '2PPM': 0.0, 'TRBPM': 0.0, '3PAr': 0.0, 'college_FTPM': 0.0, 'college_num_seasons': 1, 'FTPM': 0.0, 'college_FGAPM': 0.0, 'MPG': 0.5, 'college_3PP': 0.0, 'FTr': 0.0, 'college_PPM': 0.0, 'college_3PAPM': 0.0, 'ORBP': 0.0, 'age': 18.0, 'BLKP': 0.0, '2PAPM': 0.0, 'STLP': 0.0, 'FGAPM': 0.0, 'TOVPM': 0.0, 'ASTPM': 0.0, 'OWSPM': -0.03333333333333333, 'WSPM': -0.03333333333333333}


def get_min_values_stored_no_outliers():
    return {'DRBPM': 0.0, '2PP': 0.0, 'college_FGPM': 0.0, 'college_FTP': 0.0, 'FGPM': 0.0, 'college_ASTPM': 0.0, 'weight': 150.0, 'college_STLPM': 0.0, '3PP': 0.0, 'DWSPM': -0.0003360215053763441, 'college_MPG': 0.0, 'TRBP': 0.0, 'college_MP': 0.0, 'PER': -23.0, 'height': 69.0, 'college_FTAPM': 0.0, '3PAPM': 0.0, 'PPM': 0.0, 'college_TOVPM': 0.0, 'college_2PP': 0.0, 'DRBP': 0.0, 'USGP': 0.0, 'TSP': 0.0, 'PFPM': 0.0, 'eFGP': 0.0, 'STLPM': 0.0, 'DBPM': -12.5, '3PPM': 0.0, 'GSPG': 0.0, 'college_BLKPM': 0.0, 'FGP': 0.0, 'ORBPM': 0.0, 'FTAPM': 0.0, 'college_age': 17.0, 'OBPM': -22.4, 'num_seasons': 1.0, 'ASTP': 0.0, 'TOVP': 0.0, 'college_3PPM': 0.0, 'WSP48': -0.661, 'college_G': 0.0, 'college_FGP': 0.0, 'college_2PAPM': 0.0, 'MP': 0.0, 'FTP': 0.0, 'GS': 0.0, 'BLKPM': 0.0, 'G': 0.0, 'college_2PPM': 0.0, 'BPM': -29.9, 'VORP': -1.6, 'college_TRBPM': 0.0, '2PPM': 0.0, 'TRBPM': 0.0, '3PAr': 0.0, 'college_FTPM': 0.0, 'college_num_seasons': 1, 'FTPM': 0.0, 'college_FGAPM': 0.0, 'MPG': 0.0, 'college_3PP': 0.0, 'FTr': 0.0, 'college_PPM': 0.0, 'college_3PAPM': 0.0, 'ORBP': 0.0, 'age': 18.0, 'BLKP': 0.0, '2PAPM': 0.0, 'STLP': 0.0, 'FGAPM': 0.0, 'TOVPM': 0.0, 'ASTPM': 0.0, 'OWSPM': -0.013333333333333334, 'WSPM': -0.013333333333333334}


# set any season a player played in 10 minutes or less to 0s
def remove_outliers(data):
    for player in data.keys():
        # pro stats
        for season in data[player]["professional"].keys():
            if data[player]["professional"][season]["MPG"] * data[player]["professional"][season]["G"] <= 10:
                for stat in data[player]["professional"][season].keys():
                    if stat not in ["year", "team", "age", "num_seasons", "position"]:
                        data[player]["professional"][season][stat] = 0.

        # college stats
        if "college" in data[player].keys():
            for season in data[player]["college"].keys():
                if data[player]["college"][season]["MPG"] * data[player]["college"][season]["G"] <= 10:
                    for stat in data[player]["college"][season].keys():
                        if stat not in ["year", "team", "age", "num_seasons", "position"]:
                            data[player]["college"][season][stat] = 0.

    return data


# scale data from negative one to one
def normalize_neg1_to_1(value, minimum, maximum):
    # scale 0-2 then subtract 1
    minmax_range = maximum - minimum
    scaled = value - minimum
    scaled = scaled / (minmax_range / 2.)
    scaled -= 1.
    return scaled


# scale data roughly from 0 to 1
# 0 will be zero, max will be one (negative values possible for some advanced metrics)
def normalize_approx0_to_1(value, minimum, maximum):
    return value / maximum


# possibly normalize where mean is 0?


def normalize(data, check_outliers=False, type=None):

    if check_outliers:
        data = remove_outliers(data)
        max_values = get_max_values_stored_no_outliers()
        min_values = get_min_values_stored_no_outliers()
    else:
        max_values = get_max_values_stored_with_outliers()
        min_values = get_min_values_stored_with_outliers()

    if type is None:
        return data
    elif type == "-1to1":
        pass
    elif type == "0to1":
        pass
    else:
        raise("ERROR")
    

    for player in data.keys():
        print player
        
        # measurables to normalize
        # hand: left 0 right 1? # -1, 1?
        if data[player]["hand"] == "left":
            data[player]["hand"] = -1
        else:
            data[player]["hand"] = 1
        # drafted 1 overall becomes 1.0, 61st (undrafted equivalent) becomes -1.0
        if data[player]["drafted"] == "u":
            if type == "-1to1":
                data[player]["drafted"] = -1.0
            else:
                data[player]["drafted"] = 0
        else:
            if type == "-1to1":
                data[player]["drafted"] = (31.0 - float(data[player]["drafted"])) / 30.
            else:
                data[player]["drafted"] = (61.0 - float(data[player]["drafted"])) / 60.
        values = ["height", "weight"]
        # normalize
        for value in values:
            if type == "-1to1":
                data[player][value] = normalize_neg1_to_1(data[player][value], min_values[value], max_values[value])
            else:
                data[player][value] = normalize_approx0_to_1(data[player][value], min_values[value], max_values[value])

        # professional stats to normalize
        values = ["G", "GS", "FGP", "3PP", "2PP", "eFGP", "FTP", "PER", "TSP", "3PAr", "FTr", "ORBP", "DRBP", "TRBP", "ASTP", "STLP", "BLKP", "TOVP", "USGP", "OWSPM", "DWSPM", "WSPM", "WSP48", "OBPM", "DBPM", "BPM", "VORP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "ORBPM", "DRBPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PFPM", "PPM", "MPG", "GSPG", "age", "num_seasons"]
        # normalize
        for value in values:
            for season in data[player]["professional"].keys():
                if type == "-1to1":
                    data[player]["professional"][season][value] = normalize_neg1_to_1(data[player]["professional"][season][value], min_values[value], max_values[value])
                else:
                    data[player]["professional"][season][value] = normalize_approx0_to_1(data[player]["professional"][season][value], min_values[value], max_values[value])

        if "college" in data[player].keys():
            # college stats to normalize
            values = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP", "age", "num_seasons"]
            for i in range(len(values)):
                values[i] = "college_" + values[i]
            # normalize
            for value in values:
                for season in data[player]["college"].keys():
                    if type == "-1to1":
                        data[player]["college"][season][value[8:]] = normalize_neg1_to_1(data[player]["college"][season][value[8:]], min_values[value], max_values[value])
                    else:
                        data[player]["college"][season][value[8:]] = normalize_approx0_to_1(data[player]["college"][season][value[8:]], min_values[value], max_values[value])

    return data


def unnormalize(results, outliers_removed, normalization, baseline=False, training=False):
    
    if baseline:
        return unnormalize_baseline(results, outliers_removed, normalization)

    stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'G', 'GS', 'GSPG', 'MP', 'MPG', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']
    assert set(stats) == set(results["validation"]["true"].keys()) 
    assert set(stats) == set(results["validation"]["predicted"].keys()) 
    assert set(stats) == set(results["test"]["true"].keys())
    assert set(stats) == set(results["test"]["predicted"].keys())
    if training:
        assert set(stats) == set(results["training"]["true"].keys())
        assert set(stats) == set(results["training"]["predicted"].keys())

    if outliers_removed:
        max_values = get_max_values_stored_no_outliers()
        min_values = get_min_values_stored_no_outliers()
    else:
        max_values = get_max_values_stored_with_outliers()
        min_values = get_min_values_stored_with_outliers()

    for stat in stats:
    
        set_types = ["validation", "test"]
        if training:
            set_types.append("training")
        for set_name in set_types:

            for val_type in ["true", "predicted"]:

                for i in range(len(results[set_name][val_type][stat])):

                    value = results[set_name][val_type][stat][i]

                    if normalization == "-1to1":
                        minmax_range = max_values[stat] - min_values[stat]
                        value += 1.
                        value *= (minmax_range / 2.)
                        value += min_values[stat]

                    elif normalization == "0to1":
                        value *= max_values[stat]

                    else:
                        raise("ERROR")

                    results[set_name][val_type][stat][i] = value

    return results


def unnormalize_baseline(results, outliers_removed, normalization):
    
    stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'G', 'GS', 'GSPG', 'MP', 'MPG', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']
    assert set(stats) == set(results["true"].keys()) 
    assert set(stats) == set(results["predicted"].keys()) 

    if outliers_removed:
        max_values = get_max_values_stored_no_outliers()
        min_values = get_min_values_stored_no_outliers()
    else:
        max_values = get_max_values_stored_with_outliers()
        min_values = get_min_values_stored_with_outliers()

    for stat in stats:

        for val_type in ["true", "predicted"]:

            for i in range(len(results[val_type][stat])):

                value = results[val_type][stat][i]

                if normalization == "-1to1":
                    minmax_range = max_values[stat] - min_values[stat]
                    value += 1.
                    value *= (minmax_range / 2.)
                    value += min_values[stat]

                elif normalization == "0to1":
                    value *= max_values[stat]

                else:
                    raise("ERROR")
                
                results[val_type][stat][i] = value

    return results
