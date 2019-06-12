import urllib2
import re


def get_html(url):
    try:
        response = urllib2.urlopen(url)
        return response.read()
    except:
        return "ERROR"


######################################################################################################
#
# JOB #1: Generate list of URLs for each player in last 5 seasons
#
######################################################################################################

def player_list():

    base_url_start = "https://www.basketball-reference.com/teams/"
    #base_url_end = "/2018.html"
    years = ["2018", "2017", "2016", "2015", "2014"]

    #test_html = get_html(base_url_start + "ATL" + base_url_end)
    
    teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", 
             "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
    
    player_urls = []

    for year in years:
        print year
        for team in teams:
            if team == "CHO" and year == "2014":
                team = "CHA"
            print team

            team_html = get_html(base_url_start + team + "/" + year + ".html")

            # pull out player table
            searchObj = re.search( r'<table class="sortable stats_table" id="roster" data-cols-to-freeze=2><caption>Roster Table<\/caption>(.|[\n\s])*?<\/table>', team_html)
            player_table = searchObj.group()
            # pull out table body
            searchObj = re.search( r'<tbody>(.|[\n\s])*?<\/tbody>', player_table)
            player_table = searchObj.group()
            # separate by players
            player_entries = player_table.split("<tr ")
            for entry in player_entries[1:]:
                # extract url
                searchObj = re.search( r'href="(.|[\n\s])*?"', entry)
                #print entry
                player_url = searchObj.group()[6:-1]
                if "http://www.basketball-reference.com" + player_url + "\n" not in player_urls:
                    player_urls.append("http://www.basketball-reference.com" + player_url + "\n")

    return player_urls



######################################################################################################
#
# JOB #2: Generate a CSV with stats for each player
#
######################################################################################################

def generate_dataset():

    # testing, replace with file call
    #test_url = "http://www.basketball-reference.com/players/b/bazemke01.html"
    #test_url_euro = "http://www.basketball-reference.com/players/b/belinma01.html"
    #test_url_allstar = "https://www.basketball-reference.com/players/e/embiijo01.html"
    #player_urls = [test_url, test_url_euro, test_url_allstar]

    player_urls = player_list()
    
    fout = open("dataset.csv", 'w')

    for player_url in player_urls:

        player_html = get_html(player_url)

        # get name, shooting hand, height, weight, stats from "totals", stats from "advanced", stats for "college"
        # put each in try-except?
        measurables = get_measurables(player_html)
        totals = get_totals(player_html) # need rookie handling, other league handling
        advanced = get_advanced(player_html) # rookie handling, other league handling
        college = get_college(player_html) # no college handling

        # track progress
        print measurables[0]

        # file I/O
        fout.write("PLAYER\n")
        for entry in measurables:
            fout.write(str(entry) + ", ")
        fout.write("\n")
        fout.write("PROFESSIONAL\n")
        for season in range(len(totals)):
            for entry in totals[season]:
                fout.write(str(entry) + ", ")
            for entry in advanced[season]:
                fout.write(str(entry) + ", ")
            fout.write("\n")
        if college == "NO_COLLEGE":
            pass
        else:
            fout.write("COLLEGE\n")
            for season in college:
                for entry in season:
                    fout.write(str(entry) + ", ")
                fout.write("\n")

    fout.close()
   

def get_measurables(player_html):
    
    row = []

    # get name
    searchObj = re.search( r'<h1 itemprop="name">.*<\/h1>', player_html)
    name = '_'.join(searchObj.group()[20:-5].split())
    row.append(name)

    # get shooting hand
    searchObj = re.search( r'<strong>[\n\s]*Shoots:[\n\s]*<\/strong>[\n\s]*\w*', player_html)
    if "Left" in searchObj.group():
        shooting_hand = "left"
    else:
        shooting_hand = "right"
    row.append(shooting_hand)

    # get height
    searchObj = re.search( r'<span itemprop="height">.*?</span>', player_html)
    searchObj = re.search( r'\d+-\d+', searchObj.group())
    # find dash index
    height_string = searchObj.group()
    separator = height_string.find('-')
    height = float(height_string[:separator]) * 12. + float(height_string[separator+1:])
    row.append(height)

    # get weight
    searchObj = re.search( r'<span itemprop="weight">\d+lb', player_html)
    weight = float(searchObj.group()[24:-2])
    row.append(weight)

    # get draft position, year
    searchObj = re.search( r'<p>[\n\s]*<strong>[\n\s]*Draft:(.|[\n\s])*?<\/p>', player_html)
    if searchObj is None:
        row.append("u")
        searchObj = re.search( r'<strong>NBA\sDebut:(.|[\n\s])*?\s\d\d\d\d', player_html)
        draft_year = searchObj.group()[-4:]
        row.append(draft_year)
    else:
        draft_text = searchObj.group()
        searchObj = re.search( r'\d+\w\w\soverall', draft_text)
        draft_pos = float(searchObj.group()[:-10])
        searchObj = re.search( r'\d\d\d\d\sNBA', draft_text)
        draft_year = searchObj.group()[:-4]
        row.append(draft_pos)
        row.append(draft_year)

    return row


# get stats from "totals" table
# Season, Age, Tm, Lg, Pos, G, GS, MP, FG, FGA, FG%, 3P, 3PA, 3P%, 2P, 2PA, 2P%, eFG%, FT, FTA, FT%, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS
# add number of seasons in NBA as a feature after Pos
def get_totals(player_html):
    
    # extract totals table
    searchObj = re.search( r'<table class="row_summable sortable stats_table" id="totals" data-cols-to-freeze=1><caption>Totals Table<\/caption>(.|[\n\s])*?<\/table>', player_html)
    totals_table = searchObj.group()
    # extract table body
    searchObj = re.search( r'<tbody>(.|[\n\s])*?<\/tbody>', totals_table)
    totals_table = searchObj.group()

    # break table body into individual seasons
    totals_season_list = totals_table.split("<tr ")

    # extract stats from each season
    season_by_season_stats = []
    counter = 0 # keep track of seasons played
    last_season = None # don't increment for trades (2 teams in one season)
    for entry in totals_season_list[1:]:

        # try-except for errors here to skip row? (think d-league, DNP, etc.), could use continue/break combination depending on issue

        # extract season
        searchObj = re.search( r'>\d+-\d+<\/a>(<span class="sr_star"><\/span>)?<\/th>', entry)
        season = searchObj.group()[1:8]
        # check for 2018-19, if so break
        if season == "2018-19":
                break
        if season != last_season:
            counter += 1
        last_season = season

        # get age, team, league, position
        stat_entries = entry.split("<td ")
        # get age
        searchObj = re.search( r'>\d+<\/td>', stat_entries[1])
        age = float(searchObj.group()[1:-5])
        # get team
        searchObj = re.search( r'>\w+<\/a><\/td>', stat_entries[2])
        if searchObj is None:
            team = "TOT" # trade occurred
        else:
            team = searchObj.group()[1:-9]
        # get league
        # might need to check this? if not NBA: continue?
        searchObj = re.search( r'>\w+<\/a><\/td>', stat_entries[3])
        league = searchObj.group()[1:-9]
        # get position
        searchObj = re.search( r'>(\w|-)+<\/td>', stat_entries[4])
        position = searchObj.group()[1:-5]
        row = [season, age, team, league, position, float(counter)]

        # get statistics
        for stat_entry in stat_entries[5:]:
            searchObj = re.search( r'>.*<\/td>', stat_entry)
            stat_string = searchObj.group()[1:-5]
            # how to deal with blanks? check for empty string/blank here, account for None when printing
            if stat_string == '':
                stat = None
            elif "<strong>" in stat_string:
                stat = float(stat_string[8:-9])
            else:
                stat = float(stat_string)
            row.append(stat)

        season_by_season_stats.append(row)

    return season_by_season_stats


# get stats from "advanced" table
# PER, TS%, 3PAr, FTr, ORB%, DRB%, TRB%, AST%, STL%, BLK%, TOV%, USG%, OWS, DWS, WS, WS/48, OBPM, DBPM, BPM, VORP
def get_advanced(player_html):
    
    # extract advanced table
    searchObj = re.search( r'<table class="row_summable sortable stats_table" id="advanced" data-cols-to-freeze=1><caption>Advanced Table</caption>(.|[\n\s])*?<\/table>', player_html)
    advanced_table = searchObj.group()
    # extract table body
    searchObj = re.search( r'<tbody>(.|[\n\s])*?<\/tbody>', advanced_table)
    advanced_table = searchObj.group()

    # break table body into individual seasons
    advanced_season_list = advanced_table.split("<tr ")

    # extract stats from each season
    season_by_season_stats = []
    for entry in advanced_season_list[1:]:

        # try-except for errors here to skip row? (think d-league, DNP, etc.), could use continue/break combination depending on issue

        # check season
        searchObj = re.search( r'>\d+-\d+<\/a>(<span class="sr_star"><\/span>)?<\/th>', entry)
        season = searchObj.group()[1:8]
        # check for 2018-19, if so break
        if season == "2018-19":
                break

        # break season into stats
        stat_entries = entry.split("<td ")
        
        
        # might need this? if not NBA: continue?
        # check league
        #searchObj = re.search( r'>\w+<\/a><\/td>', stat_entries[3])
        #league = searchObj.group()[1:-9]

        # get statistics
        row = []
        counter = 7
        for stat_entry in stat_entries[7:]:
            # take into account empty cells between USG%/OWS and WS48/OBPM
            if counter == 19 or counter == 24:
                counter += 1
                continue
            searchObj = re.search( r'>.*<\/td>', stat_entry)
            stat_string = searchObj.group()[1:-5]
            # how to deal with blanks? check for empty string/blank here, account for None when printing
            if stat_string == '':
                stat = None
            elif "<strong>" in stat_string:
                stat = float(stat_string[8:-9])
            else:
                stat = float(stat_string)
            row.append(stat)
            counter += 1

        season_by_season_stats.append(row)

    return season_by_season_stats


# get college stats
# G, MP, FG, FGA, 3P, 3PA, FT, FTA, ORB, TRB, AST, STL, BLK, TOV, PF, PTS, FG%, 3P%, FT%, MP, PTS, TRB, AST
def get_college(player_html):
    
    # track players that did not go to college
    try:
        # extract totals table
        searchObj = re.search( r'<table class="sortable stats_table" id="all_college_stats" data-cols-to-freeze=1><caption>College Table</caption>(.|[\n\s])*?<\/table>', player_html)
        college_table = searchObj.group()
    except:
        return "NO_COLLEGE"
    # extract table body
    searchObj = re.search( r'<tbody>(.|[\n\s])*?<\/tbody>', college_table)
    college_table = searchObj.group()

    # break table body into individual seasons
    college_season_list = college_table.split("<tr ")

    # extract stats from each season
    season_by_season_stats = []
    for entry in college_season_list[1:]:

        # try-except for errors here to skip row? (think d-league, DNP, etc.), could use continue/break combination depending on issue

        # extract season
        searchObj = re.search( r'>\d+-\d+<\/th>', entry)
        season = searchObj.group()[1:8]

        # get age, team
        stat_entries = entry.split("<td ")
        # get age
        searchObj = re.search( r'>\d+<\/td>', stat_entries[1])
        age = float(searchObj.group()[1:-5])
        # get team
        searchObj = re.search( r'>\w+<\/a><\/td>', stat_entries[2])
        team = searchObj.group()[1:-9]

        row = [season, age, team]

        # get statistics
        for stat_entry in stat_entries[3:]:
            searchObj = re.search( r'>.*<\/td>', stat_entry)
            stat_string = searchObj.group()[1:-5]
            # how to deal with blanks? check for empty string/blank here, account for None when printing
            if stat_string == '':
                stat = None
            elif "<strong>" in stat_string:
                stat = float(stat_string[8:-9])
            else:
                stat = float(stat_string)
            row.append(stat)

        season_by_season_stats.append(row)

    return season_by_season_stats


######################################################################################################
#
# JOB #3: Generate 2016-2017, 2017-2018 Schedules
#
######################################################################################################

def generate_schedule():

    schedule = []
    # respective months:
    # 1 Oct
    # 2 Nov
    # 3 Dec
    # 4 Jan
    # 5 Feb
    # 6 Mar
    # 7 Apr

    #base_url_start = "https://www.basketball-reference.com/leagues/NBA_2018_games-"
    base_url_start = "https://www.basketball-reference.com/leagues/NBA_20"
    base_url_end = ".html"
    months = ["october", "november", "december", "january", "february", "march", "april"]
    month_binding = {"october" : 0, "november": 31, "december" : 61, "january" : 92, "february" : 123, "march" : 151, "april" : 182}
    years = ["1314", "1415", "1516", "1617", "1718"]

    teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", 
             "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

    for year in years:
        for month in months:
            schedule_html = get_html(base_url_start + year[-2:] + "_games-" + month + base_url_end)
        
            # extract table
            searchObj = re.search( r'<table class="suppress_glossary sortable stats_table" id="schedule" data-cols-to-freeze=1><caption>\w+ Schedule Table<\/caption>(.|[\n\s])*?<\/table>', schedule_html)
            schedule_table = searchObj.group()
            # extract tbody
            if month != "april":
                searchObj = re.search( r'<tbody>(.|[\n\s])*?<\/tbody>', schedule_table)
                schedule_table = searchObj.group()
            # if april, break before playoffs
            else:
                searchObj = re.search( r'<tbody>(.|[\n\s])*?Playoffs<\/th><\/tr>', schedule_table)
                schedule_table = searchObj.group()

            # break into individual games
            games = schedule_table.split("<tr >")[1:]
            if month != "april":
                games[-1] = games[-1][:-9]
            else:
                games[-1] = games[-1][:-53]

            # process game
            for game in games:
                # month, day, visitor, home, homewin?
                # get day
                searchObj = re.search( r';day=\d+', game)
                day = int(searchObj.group()[5:])

                # visitor
                searchObj = re.search( r'csk="\w\w\w\.', game)
                visitor = searchObj.group()[-4:-1]

                # home
                searchObj = re.search( r'csk="\w\w\w\.\d+\w\w\w', game)
                home = searchObj.group()[-3:]

                # home win
                searchObj = re.search( r'visitor_pts"\s>\d+', game)
                visitor_points = int(searchObj.group()[14:])
                searchObj = re.search( r'home_pts"\s>\d+', game)
                home_points = int(searchObj.group()[11:])
                #print home_points, visitor_points
                if home_points > visitor_points:
                    #print "home"
                    home_win = 1
                else:
                    #print "away"
                    home_win = -1

                # account for hornets 2014 name change
                if home == "CHA":
                    home = "CHO"
                if visitor == "CHA":
                    visitor = "CHO"

                schedule.append([ year, month_binding[month] + day, visitor, home, home_win ])

    fout = open("schedule.csv", "w")    
    for game in schedule:
        for spec in game:
            fout.write(str(spec) + ", ")
        fout.write("\n")
    fout.close()


def generate_data():
    generate_dataset()
    generate_schedule()

generate_data()
