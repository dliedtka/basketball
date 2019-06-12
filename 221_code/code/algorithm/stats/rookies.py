import pickle
import sys
import os
#sys.path.append("../data_generation")
#import normalize_data
#sys.path.append("../evaluation")
#import rmse
import collections
import random


def create_neighborhood(data, player):
    relevant_stats = ['DRBPM', '2PP', 'FGPM', '3PP', 'DWSPM', 'TRBP', 'PER', 'FTPM', '3PAPM', 'DRBP', 'USGP', 'TSP', 'PFPM', 'eFGP', 'STLPM', 'DBPM', '3PPM', 'GSPG', 'FGP', 'PPM', 'FTAPM', 'OBPM', 'TOVP', 'WSP48', 'MP', 'FTP', 'GS', 'BLKPM', 'G', 'BPM', 'VORP', 'ORBPM', 'TRBPM', '3PAr', 'ASTP', '2PPM', 'MPG', 'FTr', 'ORBP', 'BLKP', '2PAPM', 'STLP', 'FGAPM', 'TOVPM', 'ASTPM', 'OWSPM', 'WSPM']
    relevant_college_stats = ["G", "FGP", "3PP", "FTP", "MP", "FGPM", "FGAPM", "3PPM", "3PAPM", "2PPM", "2PAPM", "FTPM", "FTAPM", "TRBPM", "ASTPM", "STLPM", "BLKPM", "TOVPM", "PPM", "MPG", "2PP"]

    neighborhood = {}
    neighborhood["x"] = collections.defaultdict(float)
    neighborhood["y"] = collections.defaultdict(float)
            
    neighborhood["x"]["drafted"] = data[player]["drafted"]
    neighborhood["x"]["height"] = data[player]["height"]
    neighborhood["x"]["weight"] = data[player]["weight"]
    neighborhood["x"]["hand"] = data[player]["hand"]
            
    # draft year binary
    draft_year_feature_name = "drafted" + str(data[player]["draft_year"])
    neighborhood["x"][draft_year_feature_name] = 1.

    # position binary
    positions = []
    for season in data[player]["professional"].keys():
        if data[player]["professional"][season]["num_seasons"] == -1.:
            positions = data[player]["professional"][season]["position"]
    num_positions = len(positions)
    for pos in positions:
        pos_feat_name = "playing" + str(pos)
        neighborhood["x"][pos_feat_name] = 1. / float(num_positions)

    # only applicable if attended college
    if "college" in data[player].keys():

        # college attended binary
        # reducing size because pull is too strong
        college_teams = []
        for season in data[player]["college"].keys():
            college_teams.append(data[player]["college"][season]["team"])
        for team in set(college_teams):
            counter = 0
            for colteam in college_teams:
                if colteam == team:
                    counter += 1
            college_feat_name = "went" + str(team)
            neighborhood["x"][college_feat_name] = (float(counter) / float(len(college_teams))) #/ 10. # reducing pull *** revisit?
            
        # add college stats to neighborhood
        # weigh each more recent season 2x as much as the last
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
                neighborhood["x"]["college" + stat] += season_weight[counter] * data[player]["college"][season][stat]
            counter += 1
                    
        last_season = sorted(data[player]["college"].keys())[-1]
        # college number of seasons played
        neighborhood["x"]["college_seasons"] = data[player]["college"][last_season]["num_seasons"]
    
        # college age
        neighborhood["x"]["draft_age"] = data[player]["college"][last_season]["age"]
    
    first_season = sorted(data[player]["professional"].keys())[0]
    neighborhood["x"]["rookie_age"] = data[player]["professional"][first_season]["age"]

    # add rookie stats to y component
    season = sorted(data[player]["professional"].keys())[0]
    for stat in relevant_stats:
        neighborhood["y"][stat] = data[player]["professional"][season][stat]

    return neighborhood


def compute_distance(address1, address2):
    distance_vector = []
    original_keys1 = address1.keys()
    original_keys2 = address2.keys()

    # subtraction
    for key in address1.keys():
        distance_vector.append(address1[key] - address2[key])
    for key in address2.keys():
        if key not in address1.keys():
            distance_vector.append(address1[key] - address2[key])
    
    # prevent overwhelming dict growth
    for key in address1.keys():
        if key not in original_keys1:
            del address1[key]
    for key in address2.keys():
        if key not in original_keys2:
            del address2[key]

    # square
    for i in range(len(distance_vector)):
        distance_vector[i] = distance_vector[i] ** 2.

    # sum
    total = sum(distance_vector)

    # root
    return total ** 0.5


def find_my_neighbors(data, player, neighborhood):
    neighbors = {}
    neighbors["neighborhood"] = create_neighborhood(data, player)
    neighbors["num_neighbors"] = 0
    neighbor_list = [0,1,2,3,4,5,6,7]
    for neighbor in neighbor_list:
        neighbors[neighbor] = {}

    # search neighborhood
    for other_player in neighborhood.keys():
        if neighbors["num_neighbors"] < 8:
            neighbors[neighbors["num_neighbors"]]["name"] = other_player
            neighbors[neighbors["num_neighbors"]]["distance"] = compute_distance(neighbors["neighborhood"]["x"], neighborhood[other_player]["x"])    
            neighbors["num_neighbors"] += 1
        else:
            distances = []
            for neighbor in neighbor_list:
                distances.append(neighbors[neighbor]["distance"])
            max_distance = max(distances)
            worst_neighbor = distances.index(max_distance)

            new_distance = compute_distance(neighbors["neighborhood"]["x"], neighborhood[other_player]["x"])    
            
            if max_distance > new_distance:
                neighbors[worst_neighbor]["distance"] = new_distance
                neighbors[worst_neighbor]["name"] = other_player

    return neighbors


def get_rookie_comparison(data_type=2, validation_trials=1):
        
    rookie_comparison = {}
    rookie_comparison["validation"] = {}
    rookie_comparison["test"] = {}
    rookie_comparison["validation"]["predicted"] = {}
    rookie_comparison["validation"]["true"] = {}
    rookie_comparison["test"]["predicted"] = {}
    rookie_comparison["test"]["true"] = {}

    relevant_stats = ['DRBPM', '2PP', 'FGPM', '3PP', 'DWSPM', 'TRBP', 'PER', 'FTPM', '3PAPM', 'DRBP', 'USGP', 'TSP', 'PFPM', 'eFGP', 'STLPM', 'DBPM', '3PPM', 'GSPG', 'FGP', 'PPM', 'FTAPM', 'OBPM', 'TOVP', 'WSP48', 'MP', 'FTP', 'GS', 'BLKPM', 'G', 'BPM', 'VORP', 'ORBPM', 'TRBPM', '3PAr', 'ASTP', '2PPM', 'MPG', 'FTr', 'ORBP', 'BLKP', '2PAPM', 'STLP', 'FGAPM', 'TOVPM', 'ASTPM', 'OWSPM', 'WSPM']

    fnames = ["data.pkl", "data_removeoutliers.pkl", "data_-1to1.pkl", "data_-1to1_removeoutliers.pkl", "data_0to1.pkl", "data_0to1_removeoutliers.pkl"]

    # intialize as empty lists
    for value in relevant_stats:
        rookie_comparison["validation"]["predicted"][value] = []
        rookie_comparison["validation"]["true"][value] = []
        rookie_comparison["test"]["predicted"][value] = []
        rookie_comparison["test"]["true"][value] = []
    
    
    # nearest neighbors for validation set
    # load validation data
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fnames[data_type][:-4] + "_validation.pkl", "rb")
    val_data = pickle.load(fin)
    fin.close()

    # new stuff starting here
    complete_neighborhood = {}
    for player in val_data.keys():
        complete_neighborhood[player] = create_neighborhood(val_data, player)

    for trial in range(validation_trials):
        #print trial

        neighborhood = {}
        val_players = []
        for player in val_data.keys():
            if random.randint(0,9) == 0:
                val_players.append(player)
            else:
                neighborhood[player] = complete_neighborhood[player]

        # find neighborhood for each player in validation set
        rookie_neighbors = {}
        for player in val_players:
            rookie_neighbors[player] = find_my_neighbors(val_data, player, neighborhood)

        # predict
        for player in rookie_neighbors.keys():
            #print player

            true_stats = rookie_neighbors[player]["neighborhood"]["y"]
            pred_stats = {}
            for stat in relevant_stats:
                pred_stats[stat] = 0.

            neighbor_factor = []
            for i in range(8):
                neighbor_factor.append(1/rookie_neighbors[player][i]["distance"])
            total = sum(neighbor_factor)
            for i in range(8):
                neighbor_factor[i] /= total
            for i in range(8):
                neighbor_name = rookie_neighbors[player][i]["name"]
                for stat in relevant_stats:
                    pred_stats[stat] += neighbor_factor[i] * neighborhood[neighbor_name]["y"][stat]

            # add to comparison
            for stat in relevant_stats:
                rookie_comparison["validation"]["predicted"][stat].append(pred_stats[stat])
                rookie_comparison["validation"]["true"][stat].append(true_stats[stat])

    '''
    neighborhood = {}
    for player in val_data.keys():
        # create a list of veteran neighbors
        if len(val_data[player]["professional"].keys()) != 1 or "2016-17" not in val_data[player]["professional"].keys():
            neighborhood[player] = create_neighborhood(val_data, player)

    # find nearest 8 neighbors for each rookie
    rookie_neighbors = {}
    for player in val_data.keys():
        if len(val_data[player]["professional"].keys()) == 1 and "2016-17" in val_data[player]["professional"].keys():
            rookie_neighbors[player] = find_my_neighbors(val_data, player, neighborhood)
            
    # predict
    # validation
    for player in rookie_neighbors.keys():
        #print player

        true_stats = rookie_neighbors[player]["neighborhood"]["y"]
        pred_stats = {}
        for stat in relevant_stats:
            pred_stats[stat] = 0.

        neighbor_factor = []
        for i in range(8):
            neighbor_factor.append(1/rookie_neighbors[player][i]["distance"])
        total = sum(neighbor_factor)
        for i in range(8):
            neighbor_factor[i] /= total
        for i in range(8):
            neighbor_name = rookie_neighbors[player][i]["name"]
            for stat in relevant_stats:
                pred_stats[stat] += neighbor_factor[i] * neighborhood[neighbor_name]["y"][stat]

        # add to comparison
        for stat in relevant_stats:
            rookie_comparison["validation"]["predicted"][stat].append(pred_stats[stat])
            rookie_comparison["validation"]["true"][stat].append(true_stats[stat])
    '''

    
    # nearest neighbors for test set
    # load test data
    fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/" + fnames[data_type], "rb")
    test_data = pickle.load(fin)
    fin.close()
    neighborhood = {}
    for player in test_data.keys():
        # create a list of veteran neighbors
        if len(test_data[player]["professional"].keys()) != 1 or "2017-18" not in test_data[player]["professional"].keys():
            neighborhood[player] = create_neighborhood(test_data, player)

    # find nearest 8 neighbors for each rookie
    rookie_neighbors = {}
    for player in test_data.keys():
        if len(test_data[player]["professional"].keys()) == 1 and "2017-18" in test_data[player]["professional"].keys():
            rookie_neighbors[player] = find_my_neighbors(test_data, player, neighborhood)

    # predict
    rookie_preds = {}
    for player in rookie_neighbors.keys():
        #print player
        rookie_preds[player] = {}

        true_stats = rookie_neighbors[player]["neighborhood"]["y"]
        pred_stats = {}
        for stat in relevant_stats:
            pred_stats[stat] = 0.

        neighbor_factor = []
        for i in range(8):
            neighbor_factor.append(1/rookie_neighbors[player][i]["distance"])
        total = sum(neighbor_factor)
        for i in range(8):
            neighbor_factor[i] /= total
        for i in range(8):
            neighbor_name = rookie_neighbors[player][i]["name"]
            for stat in relevant_stats:
                pred_stats[stat] += neighbor_factor[i] * neighborhood[neighbor_name]["y"][stat]

        # add to comparison
        for stat in relevant_stats:
            rookie_comparison["test"]["predicted"][stat].append(pred_stats[stat])
            rookie_comparison["test"]["true"][stat].append(true_stats[stat])
            rookie_preds[player][stat] = pred_stats[stat]

            
    fout = open("rookie_preds.pkl", "wb")
    pickle.dump(rookie_preds, fout)
    fout.close()
            
    return rookie_comparison


#print get_rookie_comparison()
