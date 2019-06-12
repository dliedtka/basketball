import pickle
import normalization

######################################################################################################
#
# JOB #1: Process Schedule
#
######################################################################################################

def process_schedule():
    fin = open("schedule.csv", 'r')

    schedule = {}
    schedule["1314"] = []
    schedule["1415"] = []
    schedule["1516"] = []
    schedule["1617"] = []
    schedule["1718"] = []

    for line_raw in fin.readlines():
        line = line_raw.strip()
        game_info = line[:-1].split(", ")
        
        year = game_info[0]
        date = game_info[1]
        visitor = game_info[2]
        home = game_info[3]
        home_win = game_info[4]

        schedule[year].append([date, visitor, home, home_win])

    fin.close()

    fout = open("schedule.pkl", "wb")
    pickle.dump(schedule, fout)
    fout.close()



######################################################################################################
#
# JOB #2: Process Dataset
#
######################################################################################################


######################################################################################################
# PROCESSING FUNCTIONS
######################################################################################################

# function to fill in some missing college data with calculated college averages
def college_relevant_averages():
    counters = []
    aggregates = []
    for i in range(26):
        counters.append(0.)
        aggregates.append(0.)

    fopen = open("dataset.csv", 'r')

    college = False
    for line_raw in fopen.readlines():
        line = line_raw.strip()

        if line == "COLLEGE":
            college = True

        elif line == "PLAYER":
            college = False

        elif college:
            line = line[:-1]
            info = line.split(", ")
        
            for i in range(3,26):
                if info[i] != "None":
                    counters[i] += 1.0
                    aggregates[i] += float(info[i])

    fopen.close()

    averages = []
    for i in range(26):
        if counters[i] == 0.:
            averages.append(0.)
        else:
            averages.append(aggregates[i] / counters[i])

    relevant_averages = {}
    relevant_averages["MPG"] = averages[4] / averages[3]
    relevant_averages["TOPM"] = averages[16] / averages[4]

    return relevant_averages


def process_measurables(player, info):
    # track progress
    print info[0]

    player["name"] = info[0]
    player["hand"] = info[1]
    player["height"] = float(info[2])
    player["weight"] = float(info[3])
    # ignore below normalization, done in normalization file
    player["drafted"] = info[4]
    # *** normalize draft position -1 to 1
    #if info[4] == "u":
    #    player["drafted"] = -1.0
    #else:
    #    # drafted 1 overall becomes 1.0, 61st (undrafted equivalent) becomes -1.0
    #    player["drafted"] = (31.0 - float(info[4])) / 30
    # *** string for draft year because we don't want this to become quantitative feature
    player["draft_year"] = info[5][:-1] # remove comma

    return player


# G- games played, GS- games started, FGP- field goal percentage, 3PP- 3 point percentage, 2PP- 2 point percentage, eFGP- effective field goal percentage, FTP- free throw percentage, PER- player efficiency rating, TSP- true shooting percentage, 3PAr- 3 point attempt rate, FTr- free throw rate, ORBP- offensive rebound percentage, DRBP- defensive rebound percentage, TRBP- total rebound percentage, ASTP- assist percentage, STLP- steal percentage, BLKP- block percentage, TOVP- turnover percentage, USGP- usage percentage, OWSPM- offensive win shares per minute, DWSPM- defensive win shares per minute, WSPM- win shares per minute, WSP48- win shares per 48 minutes, OBMP- offensive box plus minus, DBPM- defensive box plus minus, BPM- box plus minus, VORP- value over replacement player, MP- minutes played, FGPM- field goals per minutes, FGAPM- field goals attempted per minute, 3PPM- 3 pointers per minute, 3PAPM- 3 pointers attempted per minute, 2PPM- 2 pointers per minute, 2PAPM- 2 pointers attempted per minute, FTPM- free throws per minutes, FTAPM- free throws attempted per minute, ORBPM- offensive rebounds per minute, DRBPM- defensive rebounds per minute, TRBPM- total rebounds per minute, ASTPM- assists per minute, STLPM- steals per minute, BLKPM- blocks per minute, TOVPM- turnovers per minute, PFPM- personal fouls per minute, PPM- points per minute, MPG- minutes per game, GSPG- games started per game (proportion of games started)
def process_professional(player, info):
    for i in range(len(info)):
        if info[i] == "None":
            info[i] = 0.

    season = {}
    year = info[0]

    # identifying info
    # *** string for year because we don't want this to become quantitative feature (think "was2010-11" binary feature)
    season["year"] = info[0]
    season["age"] = float(info[1])
    if info[2] == "TOT":
        season["team"] = [] # empty list because trade occurred
    else:
        season["team"] = [info[2]] # list in case of trade
    if info[3] != "NBA":
        raise("Non NBA season in player data")
    # check for multiple positions
    # *** list in case of multiple positions, will probably have to normalize this (two positions will lead to double gains?)
    if '-' in info[4]:
        season["position"] = info[4].split('-')
    else:
        season["position"] = [info[4]]
    season["num_seasons"] = float(info[5])

    # stats not normalized
    season["G"] = float(info[6])
    season["GS"] = float(info[7])
    season["FGP"] = float(info[11])
    season["3PP"] = float(info[14])
    season["2PP"] = float(info[17])
    season["eFGP"] = float(info[18])
    season["FTP"] = float(info[21])
    season["PER"] = float(info[31])
    season["TSP"] = float(info[32])
    season["3PAr"] = float(info[33])
    season["FTr"] = float(info[34])
    season["ORBP"] = float(info[35])
    season["DRBP"] = float(info[36])
    season["TRBP"] = float(info[37])
    season["ASTP"] = float(info[38])
    season["STLP"] = float(info[39])
    season["BLKP"] = float(info[40])
    season["TOVP"] = float(info[41])
    season["USGP"] = float(info[42])
    season["WSP48"] = float(info[46])
    season["OBPM"] = float(info[47])
    season["DBPM"] = float(info[48])
    season["BPM"] = float(info[49])
    season["VORP"] = float(info[50][:-1]) # get rid of final comma in row

    # stats normalized by minutes played
    minutes = float(info[8])
    temp_minutes = False
    if minutes == 0:
        temp_minutes = True
        minutes = 1
    season["MP"] = minutes
    season["FGPM"] = float(info[9]) / minutes
    season["FGAPM"] = float(info[10]) / minutes
    season["3PPM"] = float(info[12]) / minutes
    season["3PAPM"] = float(info[13]) / minutes
    season["2PPM"] = float(info[15]) / minutes
    season["2PAPM"] = float(info[16]) / minutes
    season["FTPM"] = float(info[19]) / minutes
    season["FTAPM"] = float(info[20]) / minutes
    season["ORBPM"] = float(info[22]) / minutes
    season["DRBPM"] = float(info[23]) / minutes
    season["TRBPM"] = float(info[24]) / minutes
    season["ASTPM"] = float(info[25]) / minutes
    season["STLPM"] = float(info[26]) / minutes
    season["BLKPM"] = float(info[27]) / minutes
    season["TOVPM"] = float(info[28]) / minutes
    season["PFPM"] = float(info[29]) / minutes
    season["PPM"] = float(info[30]) / minutes
    season["OWSPM"] = float(info[43]) / minutes
    season["DWSPM"] = float(info[44]) / minutes
    season["WSPM"] = float(info[45]) / minutes
    if temp_minutes:
        minutes = 0

    # miscellaneous stats
    season["MPG"] = season["MP"] / season["G"] # *** not sure if we will trust dividing projected minutes by projected games, analyze this in results
    season["GSPG"] = season["GS"] / season["G"] # *** proportion of games started, might be useful in stat bumps?

    player["professional"][year] = season
    return player


# G- games played, FGP- field goal percentage, 3PP- 3 point percentage, FTP- free throw percentage, MP- minutes played, FGPM- field goals per minute, FGAPM- field goal attempts per minute, 3PPM- 3 pointers per minute, 3PAPM- 3 pointer attempts per minute, 2PPM- 2 pointers per minute, 2PAPM- 2 pointer attempts per minute, FTPM- free throws per minute, FTAPM- free throw attempts per minute, TRBPM- total rebounds per minute, ASTPM- assists per minute, STLPM- steals per minute, BLKPM- blocks per minutes, TOVPM- turnovers per minute, PPM- points per minute, MPG- minutes per game, 2PP- 2 point percentage
def process_college(player, info, year_num):
    # fill in college stats
    average_stats = college_relevant_averages()
    
    for i in range(len(info)):
        if info[i] == "None" and i != 4 and i != 16:
            info[i] = 0.

    season = {}

    year = info[0]
    season["year"] = info[0]
    season["age"] = float(info[1])
    season["team"] = info[2]
    season["num_seasons"] = year_num

    # stats not normalized
    games = float(info[3])
    season["G"] = games
    if info[19] == "None":
        if info[6] == "None" or float(info[6]) == 0.:
            season["FGP"] = 0.
        else:
            season["FGP"] = float(info[5]) / float(info[6])
    else:
        season["FGP"] = float(info[19])
    if info[20] == "None":
        if info[8] == "None" or float(info[8]) == 0.:
            season["3PP"] = 0.
        else:
            season["3PP"] = float(info[7]) / float(info[8])
    else:
        season["3PP"] = float(info[20])
    if info[21] == "None":
        if info[10] == "None" or float(info[10]) == 0. or info[10]:
            season["FTP"] = 0.
        else:
            season["FTP"] = float(info[9]) / float(info[10])
    else:
        season["FTP"] = float(info[21])
        
    # stats normalized by minutes played
    if info[4] == "None":
        minutes_played = average_stats["MPG"] * games
    else:
        minutes_played = float(info[4])
    season["MP"] = minutes_played
    # edge case for < 30 seconds played in a season (avoid divide by zero)
    if minutes_played == 0:
        fix_later = True
        minutes_played = 1
    else:
        fix_later = False
    season["FGPM"] = float(info[5]) / minutes_played
    season["FGAPM"] = float(info[6]) / minutes_played
    season["3PPM"] = float(info[7]) / minutes_played
    season["3PAPM"] = float(info[8]) / minutes_played
    season["2PPM"] = season["FGPM"] - season["3PPM"]
    season["2PAPM"] = season["FGAPM"] - season["3PAPM"]
    season["FTPM"] = float(info[9]) / minutes_played
    season["FTAPM"] = float(info[10]) / minutes_played
    season["TRBPM"] = float(info[12]) / minutes_played
    season["ASTPM"] = float(info[13]) / minutes_played
    if info[14] == "None":
        season["STLPM"] = 0.
    else:
        season["STLPM"] = float(info[14]) / minutes_played
    if info[15] == "None":
        season["BLKPM"] = 0.
    else:
        season["BLKPM"] = float(info[15]) / minutes_played
    if info[16] == "None":
        season["TOVPM"] = average_stats["TOPM"]
    else:
        season["TOVPM"] = float(info[16]) / minutes_played
    season["PPM"] = float(info[18]) / minutes_played
    if fix_later:
        minutes_played = 0

    # miscellaneous stats
    season["MPG"] = minutes_played / games
    if season["2PAPM"] == 0.:
        season["2PP"] = 0.
    else:
        season["2PP"] = season["2PPM"] / season["2PAPM"]

    player["college"][year] = season
    return player


######################################################################################################
# CREATE DATA STRUCTURE
######################################################################################################

def generate_data_structure(normalization_type=None, filter_outliers=False):
    
    fin = open("dataset.csv", 'r')

    data = {}
    player = {}
    name = ""
    professional = college = measurables = False

    for line_raw in fin.readlines():
        line = line_raw.strip()

        # add player to data, reset player variable, prepare to process measurables
        if line == "PLAYER":
            if player != {}:
                data[name] = player
            player = {}
            name = ""
            professional = False
            college = False
            measurables = True

        # prepare to process professional statistics
        elif line == "PROFESSIONAL":
            professional = True
            player["professional"] = {}

        # prepare to process college statistics
        elif line == "COLLEGE":
            college = True
            professional = False
            player["college"] = {}

        # process measurable data
        elif measurables:
            info = line.split(", ")
            name = info[0]
            player = process_measurables(player, info)
            measurables = False

    # process professional data
        elif professional:
            info = line.split(", ")
            year = info[0]
            # if season already in player, need to add instead of creating new season
            if year in player["professional"].keys():
                player["professional"][year]["team"].append(info[2])
            else:
                player = process_professional(player, info)

        # process college data
        elif college:
            info = line.split(", ")
            year = len(player["college"].keys()) + 1
            player = process_college(player, info, year)

        # should not get here
        else:
            raise Exception("Error in data processing")


    data[name] = player

    fin.close()

    # normalize
    data = normalization.normalize(data, filter_outliers, normalization_type)

    # output to file to avoid computing everytime
    fname = "data"
    if normalization_type is not None:
        fname += "_" + normalization_type
    if filter_outliers:
        fname += "_removeoutliers"
    fname += ".pkl"
    import pickle
    outfile = open(fname, "wb")
    pickle.dump(data, outfile)
    outfile.close()

generate_data_structure()
generate_data_structure(filter_outliers=True)
generate_data_structure(normalization_type="-1to1")
generate_data_structure(normalization_type="-1to1", filter_outliers=True)
generate_data_structure(normalization_type="0to1")
generate_data_structure(normalization_type="0to1", filter_outliers=True)
