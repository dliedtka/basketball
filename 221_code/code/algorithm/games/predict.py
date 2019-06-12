import os
import pickle
import random
import collections
import util
import numpy as np
#from sklearn.feature_selection import RFE


fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/data.pkl", "rb")
data = pickle.load(fin)
fin.close()

fin = open(os.path.dirname("/Users/dliedtka/Documents/stanford/cs221/project/files/data_generation/") + "/schedule.pkl", "rb")
schedule = pickle.load(fin)
fin.close()

# store which teams played on what days
calendar = {}
for year in schedule.keys():
    calendar[year] = collections.defaultdict(float)
    for game in schedule[year]:
        calendar[year][game[0]] = []
    for game in schedule[year]:
        calendar[year][game[0]].append(game[1])
        calendar[year][game[0]].append(game[2])

all_training = []

for year in schedule.keys():
    if year == "1718" or year == "1314":
        continue
    else:
        for game in schedule[year]:
            all_training.append([year, int(game[0]), game[1], game[2], int(game[3])])

# create training and validation set (10%)
train_set = []
val_set = []
for game in all_training:
    if random.randint(0,9) == 0:
        val_set.append(game)
    else:
        train_set.append(game)

# create test set
test_set = []
for game in schedule["1718"]:
    test_set.append(["1718", int(game[0]), game[1], game[2], int(game[3])])


# year, date, visitor, home, home_win?



def pick_random(train_set, val_set, test_set):
    # pick randomly
    # training accuracy
    correct = 0.
    total = 0.
    for game in train_set:
        if (random.randint(0,1) == 1 and game[4] == 1) or (random.randint(0,1) == 0 and game[4] == -1):
            correct += 1.
        total += 1.
    train_acc = correct / total
    # validation
    correct = 0.
    total = 0.
    for game in val_set:
        if (random.randint(0,1) == 1 and game[4] == 1) or (random.randint(0,1) == 0 and game[4] == -1):
            correct += 1.
        total += 1.
    val_acc = correct / total
    # test
    correct = 0.
    total = 0.
    for game in test_set:
        if (random.randint(0,1) == 1 and game[4] == 1) or (random.randint(0,1) == 0 and game[4] == -1):
            correct += 1.
        total += 1.
    test_acc = correct / total
    
    #fout = open("random.csv", "a")
    #fout.write(str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    #fout.close()
    #print "random"
    #print (str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    return (train_acc, val_acc, test_acc)


def pick_home(train_set, val_set, test_set):
    # pick home
    # training accuracy
    correct = 0.
    total = 0.
    for game in train_set:
        if game[4] == 1:
            correct += 1.
        total += 1.
    train_acc = correct / total
    # validation
    correct = 0.
    total = 0.
    for game in val_set:
        if game[4] == 1:
            correct += 1.
        total += 1.
    val_acc = correct / total
    # test
    correct = 0.
    total = 0.
    for game in test_set:
        if game[4] == 1:
            correct += 1.
        total += 1.
    test_acc = correct / total

    #fout = open("home.csv", "a")
    #fout.write(str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    #fout.close()
    #print "home"
    #print (str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    return (train_acc, val_acc, test_acc)


def hinge_no_players(train_set, val_set, test_set, calendar):
    # hinge loss with no player features

    def feature_extractor(game, calendar):
        fv = collections.defaultdict(float)

        day = game[1]
        home = game[3]
        away = game[2]

        fv["home" + home] = 1.
        fv["away" + away] = 1.
        fv["date"] = float(day - 105) / float(88)

        # check for back to back
        year = game[0]
        if calendar[year][day-1] != 0 and home in calendar[day-1]:
            fv["back_to_back_home"] = 1
        if calendar[year][day-1] != 0 and away in calendar[day-1]:
            fv["back_to_back_away"] = 1

        # check for three in four
        home_counter = 0
        away_counter = 0
        for new_day in [day-1, day-2, day-3]:
            if calendar[year][new_day] != 0 and home in calendar[new_day]:
                home_counter += 1
            if calendar[year][new_day] != 0 and away in calendar[new_day]:
                away_counter += 1
        if home_counter > 1:
            fv["three_in_four_home"] = 1
        if away_counter > 1:
            fv["three_in_four_away"] = 1

        return fv


    # training
    weights = collections.defaultdict(float)
    eta = 0.11 # 0.1?
    reg_lambda = 0.11 # revisit values 0.11: 56,55,51
    for game in train_set:
        
        y = game[4]
        fv = feature_extractor(game, calendar)

        hinge_loss = max(0, 1 - (util.dotProduct(weights, fv) * y))
        for key in fv:
            if hinge_loss == 0:
                fv[key] = 0
            else:
                fv[key] *= (-1 * y)
        #util.increment(weights, (eta * -1), fv)
        # now using regularization
        util.increment(fv, reg_lambda, weights)
        util.increment(weights, (eta * -1), fv)


    # prediction
    # training
    right_count = 0.
    total_count = 0.
    for game in train_set:

        y = game[4]
        fv = feature_extractor(game, calendar)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    train_acc = float(right_count) / float(total_count)

    # validation
    right_count = 0.
    total_count = 0.
    for game in val_set:

        y = game[4]
        fv = feature_extractor(game, calendar)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    val_acc = float(right_count) / float(total_count)

    # test
    right_count = 0.
    total_count = 0.
    for game in test_set:

        y = game[4]
        fv = feature_extractor(game, calendar)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    test_acc = float(right_count) / float(total_count)
    
    #fout = open("hinge_no_player.csv", "a")
    #fout.write(str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    #fout.close()
    #print "hinge no player"
    #print (str(train_acc)+", "+str(val_acc)+", "+str(test_acc)+", \n")
    return (train_acc, val_acc, test_acc)
    

def get_last_years_stats(data, current_season):
    if current_season == "1718":
        current_season = "2017-18"
        last_season = "2016-17"
    elif current_season == "1617":
        current_season = "2016-17"
        last_season = "2015-16"
    elif current_season == "1516":
        current_season = "2015-16"
        last_season = "2014-15"
    elif current_season == "1415":
        current_season = "2014-15"
        last_season = "2013-14"
    else:
        raise("ERROR")

    # create a mapping of each player who played on each team this year
    teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", 
             "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
    team_player_map = {}
    for team in teams:
        team_player_map[team] = []
    # iterate through all players, adding to appropriate teams
    for player in data.keys():
        if current_season in data[player]["professional"].keys():
            for season_team in data[player]["professional"][current_season]["team"]:
                team_player_map[season_team].append(player)

    # create mapping of last years statistics averaged out by position for each team
    stat_map = {}
    for team in teams:
        stat_map[team] = collections.defaultdict(float)
    positions = ["PG", "SG", "SF", "PF", "C"]
    # measurables: height, weight
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if last_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][last_season]["position"]:

                    stat_map[team][position + "_height"] += float(data[player]["height"]) * float(data[player]["professional"][last_season]["MP"])
                    stat_map[team][position + "_weight"] += float(data[player]["weight"]) * float(data[player]["professional"][last_season]["MP"])
                    minutes_total += float(data[player]["professional"][last_season]["MP"])

            if minutes_total == 0.:
                minutes_total = 1.
            stat_map[team][position + "_height"] /= minutes_total
            stat_map[team][position + "_weight"] /= minutes_total

    # stats
    feature_stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if last_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][last_season]["position"]:

                    for stat in feature_stats:
                        stat_map[team][position + "_" + stat] += float(data[player]["professional"][last_season][stat]) * float(data[player]["professional"][last_season]["MP"])
                    
                    minutes_total += float(data[player]["professional"][last_season]["MP"])

            for stat in feature_stats:
                if minutes_total == 0.:
                    minutes_total = 1
                stat_map[team][position + "_" + stat] /= minutes_total
    
    return stat_map


def get_current_years_stats(data, current_season):
    if current_season == "1718":
        current_season = "2017-18"
        last_season = "2017-18"
    elif current_season == "1617":
        current_season = "2016-17"
        last_season = "2016-17"
    elif current_season == "1516":
        current_season = "2015-16"
        last_season = "2015-16"
    elif current_season == "1415":
        current_season = "2014-15"
        last_season = "2014-15"
    else:
        raise("ERROR")

    # create a mapping of each player who played on each team this year
    teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", 
             "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
    team_player_map = {}
    for team in teams:
        team_player_map[team] = []
    # iterate through all players, adding to appropriate teams
    for player in data.keys():
        if current_season in data[player]["professional"].keys():
            for season_team in data[player]["professional"][current_season]["team"]:
                team_player_map[season_team].append(player)

    # create mapping of last years statistics averaged out by position for each team
    stat_map = {}
    for team in teams:
        stat_map[team] = collections.defaultdict(float)
    positions = ["PG", "SG", "SF", "PF", "C"]
    # measurables: height, weight
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if last_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][last_season]["position"]:

                    stat_map[team][position + "_height"] += float(data[player]["height"]) * float(data[player]["professional"][last_season]["MP"])
                    stat_map[team][position + "_weight"] += float(data[player]["weight"]) * float(data[player]["professional"][last_season]["MP"])
                    minutes_total += float(data[player]["professional"][last_season]["MP"])

            if minutes_total == 0.:
                minutes_total = 1.
            stat_map[team][position + "_height"] /= minutes_total
            stat_map[team][position + "_weight"] /= minutes_total

    # stats
    feature_stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if last_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][last_season]["position"]:

                    for stat in feature_stats:
                        stat_map[team][position + "_" + stat] += float(data[player]["professional"][last_season][stat]) * float(data[player]["professional"][last_season]["MP"])
                    
                    minutes_total += float(data[player]["professional"][last_season]["MP"])

            for stat in feature_stats:
                if minutes_total == 0.:
                    minutes_total = 1
                stat_map[team][position + "_" + stat] /= minutes_total
    
    return stat_map


def get_projected_years_stats(data, current_season):
    assert current_season == "1718"
    current_season = "2017-18"

    # load player stats
    fin = open("../stats/rookie_preds.pkl", "rb")
    rookie_stats = pickle.load(fin)
    fin.close()
    fin = open("../stats/veteran_preds.pkl", "rb")
    veteran_stats = pickle.load(fin)
    fin.close()
    player_stats = {}
    for player in veteran_stats.keys():
        player_stats[player] = veteran_stats[player]
    for player in rookie_stats.keys():
        player_stats[player] = rookie_stats[player]

    # create a mapping of each player who played on each team this year
    teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", 
             "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
    team_player_map = {}
    for team in teams:
        team_player_map[team] = []
    # iterate through all players, adding to appropriate teams
    for player in data.keys():
        if current_season in data[player]["professional"].keys():
            for season_team in data[player]["professional"][current_season]["team"]:
                team_player_map[season_team].append(player)

    # create mapping of last years statistics averaged out by position for each team
    stat_map = {}
    for team in teams:
        stat_map[team] = collections.defaultdict(float)
    positions = ["PG", "SG", "SF", "PF", "C"]
    # measurables: height, weight
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if current_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][current_season]["position"]:

                    stat_map[team][position + "_height"] += float(data[player]["height"]) * float(data[player]["professional"][current_season]["MP"])
                    stat_map[team][position + "_weight"] += float(data[player]["weight"]) * float(data[player]["professional"][current_season]["MP"])
                    minutes_total += float(data[player]["professional"][current_season]["MP"])

            if minutes_total == 0.:
                minutes_total = 1.
            stat_map[team][position + "_height"] /= minutes_total
            stat_map[team][position + "_weight"] /= minutes_total

    # stats
    feature_stats = ['2PAPM', '2PP', '2PPM', '3PAPM', '3PAr', '3PP', '3PPM', 'ASTP', 'ASTPM', 'BLKP', 'BLKPM', 'BPM', 'DBPM', 'DRBP', 'DRBPM', 'DWSPM', 'FGAPM', 'FGP', 'FGPM', 'FTAPM', 'FTP', 'FTPM', 'FTr', 'OBPM', 'ORBP', 'ORBPM', 'OWSPM', 'PER', 'PFPM', 'PPM', 'STLP', 'STLPM', 'TOVP', 'TOVPM', 'TRBP', 'TRBPM', 'TSP', 'USGP', 'VORP', 'WSP48', 'WSPM', 'eFGP']
    for team in teams:
        for position in positions:

            minutes_total = 0.
            for player in team_player_map[team]:
                if current_season not in data[player]["professional"].keys():
                    continue
                if position in data[player]["professional"][current_season]["position"]:

                    for stat in feature_stats:
                        stat_map[team][position + "_" + stat] += float(player_stats[player][stat]) * float(player_stats[player]["MP"])
                    
                    minutes_total += float(player_stats[player]["MP"])

            for stat in feature_stats:
                if minutes_total == 0.:
                    minutes_total = 1
                stat_map[team][position + "_" + stat] /= minutes_total
    
    return stat_map



def hinge_last_years_players(train_set, val_set, test_set, calendar, data):
    # hinge loss with last years player features

    ly_stat_map = {}
    ly_stat_map["1718"] = get_last_years_stats(data, "1718")
    ly_stat_map["1617"] = get_last_years_stats(data, "1617")
    ly_stat_map["1516"] = get_last_years_stats(data, "1516")
    ly_stat_map["1415"] = get_last_years_stats(data, "1415")
    

    def feature_extractor(game, calendar, stat_map):
        fv = collections.defaultdict(float)

        day = game[1]
        home = game[3]
        away = game[2]

        fv["home" + home] = 1.
        fv["away" + away] = 1.
        fv["date"] = float(day - 105) / float(88)

        # check for back to back
        year = game[0]
        if calendar[year][day-1] != 0 and home in calendar[day-1]:
            fv["back_to_back_home"] = 1
        if calendar[year][day-1] != 0 and away in calendar[day-1]:
            fv["back_to_back_away"] = 1

        # check for three in four
        home_counter = 0
        away_counter = 0
        for new_day in [day-1, day-2, day-3]:
            if calendar[year][new_day] != 0 and home in calendar[new_day]:
                home_counter += 1
            if calendar[year][new_day] != 0 and away in calendar[new_day]:
                away_counter += 1
        if home_counter > 1:
            fv["three_in_four_home"] = 1
        if away_counter > 1:
            fv["three_in_four_away"] = 1

        # use stat map
        for feat in stat_map[year][home].keys():
            if "WS" in feat or "VORP" in feat:
                fv["home_" + feat] = stat_map[year][home][feat]
            #fv["home_" + feat] = stat_map[year][home][feat]
        for feat in stat_map[year][away].keys():
            if "WS" in feat or "VORP" in feat:
                fv["away_" + feat] = stat_map[year][away][feat]
            #fv["away_" + feat] = stat_map[year][away][feat]

        return fv


    # training
    weights = collections.defaultdict(float)
    eta = 0.11 # 0.1?
    reg_lambda = 0.11 # experiment with vals
    for game in train_set:
        
        y = game[4]
        fv = feature_extractor(game, calendar, ly_stat_map)

        hinge_loss = max(0, 1 - (util.dotProduct(weights, fv) * y))
        for key in fv:
            if hinge_loss == 0:
                fv[key] = 0
            else:
                fv[key] *= (-1 * y)
        #util.increment(weights, (eta * -1), fv)
        # now using regularization
        util.increment(fv, reg_lambda, weights)
        util.increment(weights, (eta * -1), fv)
    

    # prediction
    # training
    right_count = 0.
    total_count = 0.
    for game in train_set:

        y = game[4]
        fv = feature_extractor(game, calendar, ly_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    training_accuracy = float(right_count) / float(total_count)


    # validation
    right_count = 0.
    total_count = 0.
    for game in val_set:

        y = game[4]
        fv = feature_extractor(game, calendar, ly_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    validation_accuracy = float(right_count) / float(total_count)

    # test
    right_count = 0.
    total_count = 0.
    for game in test_set:

        y = game[4]
        fv = feature_extractor(game, calendar, ly_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    test_accuracy = float(right_count) / float(total_count)

    #fout = open("hinge_player.csv", "a")
    #fout.write(str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    #fout.close()
    #print "hinge player"
    #print (str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    return (training_accuracy, validation_accuracy, test_accuracy)


def hinge_current_years_players(train_set, val_set, test_set, calendar, data):
    # hinge loss with current years player features

    cy_stat_map = {}
    cy_stat_map["1718"] = get_current_years_stats(data, "1718")
    cy_stat_map["1617"] = get_current_years_stats(data, "1617")
    cy_stat_map["1516"] = get_current_years_stats(data, "1516")
    cy_stat_map["1415"] = get_current_years_stats(data, "1415")
    

    def feature_extractor(game, calendar, stat_map):
        fv = collections.defaultdict(float)

        day = game[1]
        home = game[3]
        away = game[2]

        fv["home" + home] = 1.
        fv["away" + away] = 1.
        fv["date"] = float(day - 105) / float(88)

        # check for back to back
        year = game[0]
        if calendar[year][day-1] != 0 and home in calendar[day-1]:
            fv["back_to_back_home"] = 1
        if calendar[year][day-1] != 0 and away in calendar[day-1]:
            fv["back_to_back_away"] = 1

        # check for three in four
        home_counter = 0
        away_counter = 0
        for new_day in [day-1, day-2, day-3]:
            if calendar[year][new_day] != 0 and home in calendar[new_day]:
                home_counter += 1
            if calendar[year][new_day] != 0 and away in calendar[new_day]:
                away_counter += 1
        if home_counter > 1:
            fv["three_in_four_home"] = 1
        if away_counter > 1:
            fv["three_in_four_away"] = 1

        # use stat map
        for feat in stat_map[year][home].keys():
            if "WS" in feat or "VORP" in feat:
                fv["home_" + feat] = stat_map[year][home][feat]
            #fv["home_" + feat] = stat_map[year][home][feat]
        for feat in stat_map[year][away].keys():
            if "WS" in feat or "VORP" in feat:
                fv["away_" + feat] = stat_map[year][away][feat]
            #fv["away_" + feat] = stat_map[year][away][feat]

        return fv


    # training
    weights = collections.defaultdict(float)
    eta = 0.11 # 0.1?
    reg_lambda = 0.11 # experiment with vals
    for game in train_set:
        
        y = game[4]
        fv = feature_extractor(game, calendar, cy_stat_map)

        hinge_loss = max(0, 1 - (util.dotProduct(weights, fv) * y))
        for key in fv:
            if hinge_loss == 0:
                fv[key] = 0
            else:
                fv[key] *= (-1 * y)
        #util.increment(weights, (eta * -1), fv)
        # now using regularization
        util.increment(fv, reg_lambda, weights)
        util.increment(weights, (eta * -1), fv)
    

    # prediction
    # training
    right_count = 0.
    total_count = 0.
    for game in train_set:

        y = game[4]
        fv = feature_extractor(game, calendar, cy_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    training_accuracy = float(right_count) / float(total_count)


    # validation
    right_count = 0.
    total_count = 0.
    for game in val_set:

        y = game[4]
        fv = feature_extractor(game, calendar, cy_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    validation_accuracy = float(right_count) / float(total_count)

    # test
    right_count = 0.
    total_count = 0.
    for game in test_set:

        y = game[4]
        fv = feature_extractor(game, calendar, cy_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    test_accuracy = float(right_count) / float(total_count)

    #fout = open("hinge_player.csv", "a")
    #fout.write(str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    #fout.close()
    #print "hinge player"
    #print (str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    return (training_accuracy, validation_accuracy, test_accuracy)


def hinge_projected_years_players(train_set, val_set, test_set, calendar, data):
    # hinge loss with current years player features

    py_stat_map = {}
    py_stat_map["1718"] = get_projected_years_stats(data, "1718")
    py_stat_map["1617"] = get_current_years_stats(data, "1617")
    py_stat_map["1516"] = get_current_years_stats(data, "1516")
    py_stat_map["1415"] = get_current_years_stats(data, "1415")
    

    def feature_extractor(game, calendar, stat_map):
        fv = collections.defaultdict(float)

        day = game[1]
        home = game[3]
        away = game[2]

        fv["home" + home] = 1.
        fv["away" + away] = 1.
        fv["date"] = float(day - 105) / float(88)

        # check for back to back
        year = game[0]
        if calendar[year][day-1] != 0 and home in calendar[day-1]:
            fv["back_to_back_home"] = 1
        if calendar[year][day-1] != 0 and away in calendar[day-1]:
            fv["back_to_back_away"] = 1

        # check for three in four
        home_counter = 0
        away_counter = 0
        for new_day in [day-1, day-2, day-3]:
            if calendar[year][new_day] != 0 and home in calendar[new_day]:
                home_counter += 1
            if calendar[year][new_day] != 0 and away in calendar[new_day]:
                away_counter += 1
        if home_counter > 1:
            fv["three_in_four_home"] = 1
        if away_counter > 1:
            fv["three_in_four_away"] = 1

        # use stat map
        for feat in stat_map[year][home].keys():
            #if "WS" in feat or "VORP" in feat:
            if "VORP" in feat:    
                fv["home_" + feat] = stat_map[year][home][feat]
            #fv["home_" + feat] = stat_map[year][home][feat]
        for feat in stat_map[year][away].keys():
            #if "WS" in feat or "VORP" in feat:
            if "VORP" in feat:
                fv["away_" + feat] = stat_map[year][away][feat]
            #fv["away_" + feat] = stat_map[year][away][feat]

        return fv


    # training
    weights = collections.defaultdict(float)
    eta = 0.11 # 0.1?
    reg_lambda = 0.11 # experiment with vals
    for game in train_set:
        
        y = game[4]
        fv = feature_extractor(game, calendar, py_stat_map)

        hinge_loss = max(0, 1 - (util.dotProduct(weights, fv) * y))
        for key in fv:
            if hinge_loss == 0:
                fv[key] = 0
            else:
                fv[key] *= (-1 * y)
        #util.increment(weights, (eta * -1), fv)
        # now using regularization
        util.increment(fv, reg_lambda, weights)
        util.increment(weights, (eta * -1), fv)
    

    # prediction
    # training
    right_count = 0.
    total_count = 0.
    for game in train_set:

        y = game[4]
        fv = feature_extractor(game, calendar, py_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    training_accuracy = float(right_count) / float(total_count)


    # validation
    right_count = 0.
    total_count = 0.
    for game in val_set:

        y = game[4]
        fv = feature_extractor(game, calendar, py_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    validation_accuracy = float(right_count) / float(total_count)

    # test
    right_count = 0.
    total_count = 0.
    for game in test_set:

        y = game[4]
        fv = feature_extractor(game, calendar, py_stat_map)
        pred = util.dotProduct(weights, fv)

        if pred >= 0 and y > 0 or pred < 0 and y < 0:
            #print y, pred, "RIGHT"
            right_count += 1
        elif pred >= 0 and y < 0 or pred < 0 and y > 0:
            #print y, pred, "WRONG"
            pass
        else:
            print pred, y
            raise("ERROR")

        total_count += 1

    test_accuracy = float(right_count) / float(total_count)

    #fout = open("hinge_player.csv", "a")
    #fout.write(str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    #fout.close()
    #print "hinge player"
    #print (str(training_accuracy)+", "+str(validation_accuracy)+", "+str(test_accuracy)+", \n")
    return (training_accuracy, validation_accuracy, test_accuracy)
    

# run 100 trials
random_vals = [0., 0., 0.]
home_vals = [0., 0., 0.]
hinge_np_vals = [0., 0., 0.]
hinge_lyp_vals = [0., 0., 0.]
hinge_cyp_vals = [0., 0., 0.]
hinge_pyp_vals = [0., 0., 0.]
for i in range(100):#(100):
    print i

    new_random = pick_random(train_set, val_set, test_set)
    new_home = pick_home(train_set, val_set, test_set)
    new_hinge_np = hinge_no_players(train_set, val_set, test_set, calendar)
    new_hinge_lyp = hinge_last_years_players(train_set, val_set, test_set, calendar, data)
    new_hinge_cyp = hinge_current_years_players(train_set, val_set, test_set, calendar, data)
    new_hinge_pyp = hinge_projected_years_players(train_set, val_set, test_set, calendar, data)

    for val in range(3):
        random_vals[val] += new_random[val]
        home_vals[val] += new_home[val]
        hinge_np_vals[val] += new_hinge_np[val]
        hinge_lyp_vals[val] += new_hinge_lyp[val]
        hinge_cyp_vals[val] += new_hinge_cyp[val]
        hinge_pyp_vals[val] += new_hinge_pyp[val]

for val in range(3):
    random_vals[val] /= 100. #100.
    home_vals[val] /= 100.
    hinge_np_vals[val] /= 100.
    hinge_lyp_vals[val] /= 100.
    hinge_cyp_vals[val] /= 100.
    hinge_pyp_vals[val] /= 100.

# print results
print "random"
print (str(random_vals[0])+", "+str(random_vals[1])+", "+str(random_vals[2])+", \n")
print "home"
print (str(home_vals[0])+", "+str(home_vals[1])+", "+str(home_vals[2])+", \n")
print "hinge_np"
print (str(hinge_np_vals[0])+", "+str(hinge_np_vals[1])+", "+str(hinge_np_vals[2])+", \n")
print "hinge_lyp"
print (str(hinge_lyp_vals[0])+", "+str(hinge_lyp_vals[1])+", "+str(hinge_lyp_vals[2])+", \n")
print "hinge_cyp"
print (str(hinge_cyp_vals[0])+", "+str(hinge_cyp_vals[1])+", "+str(hinge_cyp_vals[2])+", \n")
print "hinge_pyp"
print (str(hinge_pyp_vals[0])+", "+str(hinge_pyp_vals[1])+", "+str(hinge_pyp_vals[2])+", \n")
