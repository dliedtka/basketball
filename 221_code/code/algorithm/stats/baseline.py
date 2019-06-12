import os
import pickle

def compute_baseline():
    
    stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'G', 'GS', 'GSPG', 'MP', 'MPG', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']

    baseline = {}
    baseline["rookies"] = {}
    baseline["veterans"] = {}
    baseline["rookies"]["predicted"] = {}
    baseline["rookies"]["true"] = {}
    baseline["veterans"]["predicted"] = {}
    baseline["veterans"]["true"] = {}

    fname = "data_-1to1.pkl"
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fname, "rb")
    data = pickle.load(fin)
    fin.close()

    # veterans
    # predict using 2017-18
    for stat in stats:
        pred_vals = []
        true_vals = []

        for player in data.keys():
            if "2016-17" not in data[player]["professional"].keys() or "2017-18" not in data[player]["professional"].keys():
                continue
            else:
                pred_vals.append(data[player]["professional"]["2016-17"][stat])
                true_vals.append(data[player]["professional"]["2017-18"][stat])

        baseline["veterans"]["predicted"][stat] = pred_vals
        baseline["veterans"]["true"][stat] = true_vals


    # rookies

    # average all rookie seasons to get rookie numbers
    rookie_averages = {}
    for stat in stats:
        rookie_averages[stat] = []

    for player in data.keys():
        for season in data[player]["professional"].keys():
            if data[player]["professional"][season]["num_seasons"] == -1.:
                for stat in stats:
                    rookie_averages[stat].append(data[player]["professional"][season][stat])

    for stat in stats:
        rookie_averages[stat] = sum(rookie_averages[stat]) / len(rookie_averages[stat])

    # predict using averages
    for stat in stats:
        pred_vals = []
        true_vals = []

        for player in data.keys():
            if len(data[player]["professional"].keys()) == 1 and "2017-18" in data[player]["professional"].keys():
                pred_vals.append(rookie_averages[stat])
                true_vals.append(data[player]["professional"]["2017-18"][stat])
            else:
                continue

        baseline["rookies"]["predicted"][stat] = pred_vals
        baseline["rookies"]["true"][stat] = true_vals

    return baseline
