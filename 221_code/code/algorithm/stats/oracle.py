import os
import pickle
import collections
import util

def compute_oracle():
    
    stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'G', 'GS', 'GSPG', 'MP', 'MPG', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']

    comparison = {}
    comparison["rookies"] = {}
    comparison["veterans"] = {}
    comparison["rookies"]["predicted"] = {}
    comparison["rookies"]["true"] = {}
    comparison["veterans"]["predicted"] = {}
    comparison["veterans"]["true"] = {}

    for stat in stats:
        comparison["rookies"]["predicted"][stat] = []
        comparison["rookies"]["true"][stat] = []
        comparison["veterans"]["predicted"][stat] = []
        comparison["veterans"]["true"][stat] = []
        

    fname = "data_-1to1.pkl"
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fname, "rb")
    data = pickle.load(fin)
    fin.close()

    # do veterans and rookies the same

    # build a model for each stat
    weights = {}
    for stat in stats:
        weights[stat] = collections.defaultdict(float)
        #weights[stat] = {}
    # eta, try 0.01?
    eta = 0.01

    def oracle_feature_extractor(x, stat):
        fv = collections.defaultdict(float)
        #fv = {}
        for feature in x.keys():
            if feature != stat and feature not in ["team", "position", "year"]: 
                fv[feature] = x[feature]
        return fv

    # iterate through each player, training the model for each stat (stochastic gradient descent using least squares regression)
    for player in data.keys():
        #print player
        for season in data[player]["professional"].keys():
            # don't train on what oracle will predict
            if season != "2017-18":
                for stat in stats:
                    y = data[player]["professional"][season][stat]
                    fv = oracle_feature_extractor(data[player]["professional"][season], stat)
                    # compute
                    pred = util.dotProduct(fv, weights[stat])
                    #print pred
                    # compute gradient
                    scale = -eta * 2. * (pred - y)
                    #print scale
                    #print weights[stat]
                    # add gradient to weights
                    util.increment(weights[stat], scale, fv)
                    #print weights[stat]

    #print weights

    # iterate through each player, making a prediction and storing the true value in comparison dict
    for player in data.keys():
        #print player

        if "2017-18" not in data[player]["professional"].keys():
            continue

        # veteran
        if len(data[player]["professional"].keys()) != 1:
            for value in stats:
                # predict based on weights
                fv = oracle_feature_extractor(data[player]["professional"]["2017-18"], value)
                pred = util.dotProduct(fv, weights[value])
                comparison["veterans"]["predicted"][value].append(pred)
                # retrieve true value
                comparison["veterans"]["true"][value].append(data[player]["professional"]["2017-18"][value])
        # rookie
        else:
            for value in stats:
                # predict based on weights
                fv = oracle_feature_extractor(data[player]["professional"]["2017-18"], value)
                pred = util.dotProduct(fv, weights[value])
                comparison["rookies"]["predicted"][value].append(pred)
                # retrieve true value
                comparison["rookies"]["true"][value].append(data[player]["professional"]["2017-18"][value])


    return comparison
