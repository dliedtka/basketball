import pickle
import os
import util
import collections


def algorithm_feature_extractor(data, player, season_number, relevant_stats, relevant_college_stats, normalization_type=None):
    fv = collections.defaultdict(float)
    #fv = {}
        
    fv["drafted"] = data[player]["drafted"]
    fv["height"] = data[player]["height"]
    fv["weight"] = data[player]["weight"]
    fv["hand"] = data[player]["hand"]

    # draft year binary
    draft_year_feature_name = "drafted" + str(data[player]["draft_year"])
    fv[draft_year_feature_name] = 1.

    # position binary
    positions = []
    current_season = sorted(data[player]["professional"].keys())[season_number]
    positions = data[player]["professional"][current_season]["position"]
    num_positions = len(positions)
    for pos in positions:
        pos_feat_name = "playing" + str(pos)
        fv[pos_feat_name] = 1. / float(num_positions)

    # team binary
    teams = []
    teams = data[player]["professional"][current_season]["team"]
    num_teams = len(teams)
    for tm in teams:
        team_feat_name = "team" + str(tm)
        fv[team_feat_name] = 1. / float(num_teams)

    # college attended binary
    if "college" in data[player].keys():
        college_teams = []
        for season in data[player]["college"].keys():
            college_teams.append(data[player]["college"][season]["team"])
        for team in set(college_teams):
            counter = 0
            for colteam in college_teams:
                if colteam == team:
                    counter += 1
            college_feat_name = "went" + str(team)
            fv[college_feat_name] = (float(counter) / float(len(college_teams)))
        
    # *** experiment with and without this
    # add college stats to fv
    # weigh each more recent season 2x as much as the last
    '''
    if "college" in data[player].keys():
        # experiment with combined seasons, just last season?
        
        last_season = sorted(data[player]["college"].keys())[-1]
        for stat in relevant_college_stats:
            fv["last_college" + stat] = data[player]["college"][last_season][stat]
        
        season_weight = []
        counter = 1.
        for season in data[player]["college"].keys():
            season_weight.append(counter)
            counter *= 2
        total = sum(season_weight)
        for i in range(len(season_weight)):
            season_weight[i] = season_weight[i] / float(total)

        counter = 0
        for season in sorted(data[player]["college"].keys()):
            for stat in relevant_college_stats:
                fv["combined_college" + stat] += season_weight[counter] * data[player]["college"][season][stat]
            counter += 1
    '''   
    # current season age
    fv["current_age"] = data[player]["professional"][current_season]["age"]
    # current season number of nba seasons
    fv["current_num_seasons"] = data[player]["professional"][current_season]["num_seasons"]
    
    # add past NBA season stats
    # *** experiment with combining all previous seasons, just last season, both
    # just last season
    last_season = sorted(data[player]["professional"].keys())[season_number-1]
    '''
    for stat in relevant_stats:
        fv["last" + stat] = data[player]["professional"][last_season][stat]
    '''
    # combine seasons, more recent season worth twice as much as previous
    season_weight = []
    counter = 1
    for season in sorted(data[player]["professional"].keys()):
        season_weight.append(counter)
        counter *= 2
        if season == last_season:
            break
    total = sum(season_weight)
    for i in range(len(season_weight)):
        season_weight[i] = season_weight[i] / float(total)
    
    counter = 0
    for season in sorted(data[player]["professional"].keys()):
        for stat in relevant_stats:
            fv["combined" + stat] += season_weight[counter] * data[player]["professional"][season][stat]
        counter += 1
        if season == last_season:
            break
     
    # number of college seasons played
    if "college" in data[player].keys():
        num_seasons = float(len(data[player]["college"].keys()))
    else:
        num_seasons = 0.
    if normalization_type is None:
        fv["college_years"] = num_seasons
    elif normalization_type == "-1to1":
        fv["college_years"] = (num_seasons / 2.5) - 1
    elif normalization_type == "0to1":
        fv["college_years"] = num_seasons / 5.
    else:
        raise("ERROR")
        
    return fv


def get_veteran_comparison(data_type=2):

    veteran_comparison = {}
    veteran_comparison["training"] = {}
    veteran_comparison["validation"] = {}
    veteran_comparison["test"] = {}
    veteran_comparison["training"]["predicted"] = {}
    veteran_comparison["training"]["true"] = {}
    veteran_comparison["validation"]["predicted"] = {}
    veteran_comparison["validation"]["true"] = {}
    veteran_comparison["test"]["predicted"] = {}
    veteran_comparison["test"]["true"] = {}

    relevant_stats = ['DRBPM', '2PP', 'FGPM', '3PP', 'DWSPM', 'TRBP', 'PER', 'FTPM', '3PAPM', 'DRBP', 'USGP', 'TSP', 'PFPM', 'eFGP', 'STLPM', 'DBPM', '3PPM', 'GSPG', 'FGP', 'PPM', 'FTAPM', 'OBPM', 'TOVP', 'WSP48', 'MP', 'FTP', 'GS', 'BLKPM', 'G', 'BPM', 'VORP', 'ORBPM', 'TRBPM', '3PAr', 'ASTP', '2PPM', 'MPG', 'FTr', 'ORBP', 'BLKP', '2PAPM', 'STLP', 'FGAPM', 'TOVPM', 'ASTPM', 'OWSPM', 'WSPM']
    relevant_college_stats = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP"]

    fnames = ["data.pkl", "data_removeoutliers.pkl", "data_-1to1.pkl", "data_-1to1_removeoutliers.pkl", "data_0to1.pkl", "data_0to1_removeoutliers.pkl"]

    if data_type == 0 or data_type == 1:
        normalization_type = None
    elif data_type == 2 or data_type == 3:
        normalization_type = "-1to1"
    elif data_type == 4 or data_type == 5:
        normalization_type = "0to1"
    else:
        raise("ERROR")

    # intialize as empty lists
    for value in relevant_stats:
        veteran_comparison["training"]["predicted"][value] = []
        veteran_comparison["training"]["true"][value] = []
        veteran_comparison["validation"]["predicted"][value] = []
        veteran_comparison["validation"]["true"][value] = []
        veteran_comparison["test"]["predicted"][value] = []
        veteran_comparison["test"]["true"][value] = []

    # build a model for each stat based on validation data
    weights = {}
    for stat in relevant_stats:
        weights[stat] = collections.defaultdict(float)
        #weights[stat] = {}
    # eta, try 0.01?
    eta = 0.0033
    # computed by trial and error
    reg_lambda_mapping = {}
    for stat in relevant_stats:
        if stat in ["BPM", "FTAPM", "FTr", "MP", "MPG", "OWSPM", "PFPM", "TOVPM", "VORP", "WSPM"]:
            reg_lambda = 1.
        elif stat in ["GS"]:
            reg_lambda = 0.5
        elif stat in ["3PAPM", "DWSPM", "FTPM", "G", "GSPG"]:
            reg_lambda = 0.333
        elif stat in ["3PAr", "ASTPM"]:
            reg_lambda = 0.1
        elif stat in ["ASTP", "DRBP"]:
            reg_lamba = 0.0333
        elif stat in ["3PPM", "USGP"]:
            reg_lambda = 0.01
        elif stat in ["FGAPM"]:
            reg_lambda = 0.000333
        elif stat in ["2PAPM", "2PP", "2PPM", "3PP", "BLKP", "BLKPM", "DBPM", "DRBPM", "FGP", "FGPM", "FTP", "OBPM", "ORBP", "ORBPM", "PER", "PPM", "STLP", "STLPM", "TOVP", "TRBP", "TRBPM", "TSP", "WSP48", "eFGP"]:
            reg_lambda = 0.
        else:
            raise("ERROR")
        
    # load validation data
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fnames[data_type][:-4] + "_validation.pkl", "rb")
    val_data = pickle.load(fin)
    fin.close()

    # iterate through each player, training the model on 2nd to last seasons for each stat (stochastic gradient descent using least squares regression)
    for player in val_data.keys():
        # skip rookies
        if len(val_data[player]["professional"].keys()) == 1:
            continue
        #print player
        # use previous seasons as features, current season as y
        for season_idx in range(1, len(sorted(val_data[player]["professional"].keys()))):
            predicting_season = sorted(val_data[player]["professional"].keys())[season_idx]
            prior_season = sorted(val_data[player]["professional"].keys())[season_idx - 1]
            if predicting_season == "2016-17":
                continue

            fv = algorithm_feature_extractor(val_data, player, season_idx, relevant_stats, relevant_college_stats, normalization_type)
            for stat in relevant_stats:
                #print fv["lastDRBPM"]
                y = val_data[player]["professional"][predicting_season][stat]
                #print y
                # predict
                #pred = util.dotProduct(fv, weights[stat])
                # *** try making prediction last years stats plus inference
                pred = val_data[player]["professional"][prior_season][stat]  + util.dotProduct(fv, weights[stat])
                #print pred
                # gradient
                scale = -eta * 2. * (pred - y)
                #print scale
                #print weights[stat]["lastDRBPM"]
                # update
                # now with regularization
                util.increment(weights[stat], -eta * reg_lambda, weights[stat])
                util.increment(weights[stat], scale, fv)
                #print weights[stat]["lastDRBPM"]

                
    # iterate through each player, predicting on training data (all season prior to 2016-17)
    for player in val_data.keys():
        # skip players that only played in 2016-17
        if len(val_data[player]["professional"].keys()) == 1 and "2016-17" in val_data[player]["professional"].keys():
            continue
        #print player

        season_list = sorted(val_data[player]["professional"].keys())
        for season_idx in range(len(season_list)):
            season = season_list[season_idx]
            # skip rookie year
            if season == season_list[0]:
                continue
            prior_season = season_list[season_idx - 1]
            season_number = season_idx
            fv = algorithm_feature_extractor(val_data, player, season_number, relevant_stats, relevant_college_stats, normalization_type)
            for stat in relevant_stats:
                # predict
                pred_val = val_data[player]["professional"][prior_season][stat] + util.dotProduct(fv, weights[stat])
                true_val = val_data[player]["professional"][season][stat]
                # append
                veteran_comparison["training"]["predicted"][stat].append(pred_val)
                veteran_comparison["training"]["true"][stat].append(true_val)


    # iterate through each player, making predictions for 2016-17
    for player in val_data.keys():
        # skip rookies, players who didn't play this year
        if len(val_data[player]["professional"].keys()) == 1 or "2016-17" not in val_data[player]["professional"].keys():
            continue
        #print player

        # use previous seasons as features, 2016-17 as y
        season = "2016-17"
        prior_season = sorted(val_data[player]["professional"].keys())[-2]
        season_number = len(val_data[player]["professional"].keys()) - 1 # 2016-17 is last season
        fv = algorithm_feature_extractor(val_data, player, season_number, relevant_stats, relevant_college_stats, normalization_type)
        for stat in relevant_stats:
            # predict
            pred_val = val_data[player]["professional"][prior_season][stat] + util.dotProduct(fv, weights[stat])
            true_val = val_data[player]["professional"][season][stat]
            # append
            veteran_comparison["validation"]["predicted"][stat].append(pred_val)
            veteran_comparison["validation"]["true"][stat].append(true_val)

    
    # iterate through each player, making predictions for 2017-18
    # load test data
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fnames[data_type], "rb")
    test_data = pickle.load(fin)
    fin.close()
    veteran_preds = {}
    for player in test_data.keys():
        # skip rookies, players who didn't play this year
        if len(test_data[player]["professional"].keys()) == 1 or "2017-18" not in test_data[player]["professional"].keys():
            continue
        #print player
        veteran_preds[player] = {}

        # use previous seasons as features, 2016-17 as y
        season = "2017-18"
        prior_season = sorted(test_data[player]["professional"].keys())[-2]
        season_number = len(test_data[player]["professional"].keys()) - 1 # 2016-17 is last season
        fv = algorithm_feature_extractor(test_data, player, season_number, relevant_stats, relevant_college_stats, normalization_type)
        for stat in relevant_stats:
            # predict
            pred_val = test_data[player]["professional"][prior_season][stat] + util.dotProduct(fv, weights[stat])
            true_val = test_data[player]["professional"][season][stat]
            # append
            veteran_comparison["test"]["predicted"][stat].append(pred_val)
            veteran_comparison["test"]["true"][stat].append(true_val)
            veteran_preds[player][stat] = pred_val


    fout = open("veteran_preds.pkl", "wb")
    pickle.dump(veteran_preds, fout)
    fout.close()
    
    return veteran_comparison
            

#get_veteran_comparison()

