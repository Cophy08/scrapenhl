import scrapenhl_globals

def get_url(season, game):
    """
    Returns the NHL API url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        URL to scrape, http://statsapi.web.nhl.com/api/v1/game/[season]0[game]/feed/live
    """
    return 'http://statsapi.web.nhl.com/api/v1/game/{0:d}0{1:d}/feed/live'.format(season, game)

def get_shift_url(season, game):
    """
    Returns the NHL API shifts url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId=[season]0[game]
    """
    return 'http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId={0:d}0{1:d}'.format(season, game)

def get_json_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the json accessed online.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game.zlib
    """
    return '{0:s}{1:d}/{2:d}.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def get_shift_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the shift json accessed online.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game_shifts.zlib
    """
    return '{0:s}{1:d}/{2:d}_shifts.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def get_parsed_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the parsed pbp file.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game_parsed.zlib
    """
    return '{0:s}{1:d}/{2:d}_parsed.zlib'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def get_parsed_shifts_save_filename(season, game):
    """
    Returns the algorithm-determined save file name of the parsed toi file.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    str
        file name, SAVE_FOLDER/Season/Game_shifts_parsed.zlib
    """
    return '{0:s}/{1:d}/{2:d}_shifts_parsed.hdf5'.format(scrapenhl_globals.SAVE_FOLDER, season, game)

def scrape_game(season, game, force_overwrite = False):
    """
    Scrapes and saves game files in compressed (zlib) format

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.

    Returns
    -------
    bool
        A boolean indicating whether the NHL API was queried.
    """
    query = False

    import os.path
    url = get_url(season, game)
    filename = get_json_save_filename(season, game)
    if force_overwrite or not os.path.exists(filename):
        import urllib.request
        try:
            query = True
            with urllib.request.urlopen(url) as reader:
                page = reader.read()
        except Exception as e:
            if game < 30111:
                print('Error reading pbp url for', season, game, e, e.args)
                page = bytes('', encoding = 'latin-1')
        if game < 30111:
            import zlib
            page2 = zlib.compress(page, level=9)
            w = open(filename, 'wb')
            w.write(page2)
            w.close()

    url = get_shift_url(season, game)
    filename = get_shift_save_filename(season, game)
    if force_overwrite or not os.path.exists(filename):
        import urllib.request
        try:
            query = True
            with urllib.request.urlopen(url) as reader:
                page = reader.read()
        except Exception as e:
            if game < 30111:
                print('Error reading shift url for', season, game, e, e.args)
                page = bytes('', encoding='latin-1')
        if game < 30111:
            import zlib
            page2 = zlib.compress(page, level=9)
            w = open(filename, 'wb')
            w.write(page2)
            w.close()

    return query

def parse_game(season, game, force_overwrite = False):
    """
    Reads this game's zlib file from disk and parses into a friendlier format, then saves again to disk in zlib.

    This method also updates the global player id and game log files, and writes any updates to disk.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    force_overwrite : bool
        If True, will overwrite previously raw html files. If False, will not scrape if files already found.
    """
    import os.path
    import zlib
    import json
    import pandas as pd
    filename = get_parsed_save_filename(season, game)
    if (force_overwrite or not os.path.exists(filename)):
        r = open(get_json_save_filename(season, game), 'rb')
        page = r.read()
        r.close()

        page = zlib.decompress(page)
        data = json.loads(page.decode('latin-1'))

        teamdata = data['liveData']['boxscore']['teams']

        update_team_ids_from_json(teamdata)
        update_player_ids_from_json(teamdata)
        update_quick_gamelog_from_json(data)

        events = read_events_from_json(data['liveData']['plays']['allPlays'])

        #pbp_compressed = zlib.compress(bytes(events, encoding = 'latin-1'), level=9)
        #w = open(filename, 'wb')
        #w.write(pbp_compressed)
        #w.close()

    filename = get_parsed_shifts_save_filename(season, game)
    if (force_overwrite or not os.path.exists(filename)):
        r = open(get_shift_save_filename(season, game), 'rb')
        page = r.read()
        r.close()

        page = zlib.decompress(page)
        data = json.loads(page.decode('latin-1'))

        try:
            thisgamedata = scrapenhl_globals.BASIC_GAMELOG.query('Season == {0:d} & Game == {1:d}'.format(season, game))
            rname = thisgamedata['Away'].iloc[0]
            hname = thisgamedata['Home'].iloc[0]
        except Exception as e:
            hname = None
            rname = None

        shifts = read_shifts_from_json(data['data'], hname, rname)

        if shifts is not None:
            #shifts = ''
            #shifts_compressed = zlib.compress(shifts, level=9)
            #w = open(filename, 'wb')
            #w.write(shifts_compressed)
            #w.close()
            shifts.to_hdf(filename, key = 'Game{0:d}0{1:d}'.format(season, game), mode = 'w',
                          complevel = 9, complib = 'zlib')

def read_shifts_from_json(data, homename = None, roadname = None):

    if len(data) == 0:
        return
    ids = ['' for i in range(len(data))]
    periods = [0 for i in range(len(data))]
    starts = ['0:00' for i in range(len(data))]
    ends = ['0:00' for i in range(len(data))]
    teams = ['' for i in range(len(data))]
    durations = [0 for i in range(len(data))]

    for i, dct in enumerate(data):
        ids[i] = dct['playerId']
        periods[i] = dct['period']
        starts[i] = dct['startTime']
        ends[i] = dct['endTime']
        durations[i] = dct['duration']
        teams[i] = dct['teamAbbrev']

    ### Seems like home players come first
    if homename is None:
        homename = teams[0]
        for i in range(len(teams) - 1, 0, -1):
            if not teams[i] == homename:
                roadname = teams[i]
                break

    startmin = [x[:x.index(':')] for x in starts]
    startsec = [x[x.index(':') + 1:] for x in starts]
    starttimes = [1200 * (p-1) + 60 * int(m) + int(s) for p, m, s in zip(periods, startmin, startsec)]
    endmin = [x[:x.index(':')] for x in ends]
    endsec = [x[x.index(':') + 1:] for x in ends]
    ### There is an extra -1 in endtimes to avoid overlapping start/end
    endtimes = [1200 * (p - 1) + 60 * int(m) + int(s) - 1 for p, m, s in zip(periods, endmin, endsec)]

    durationtime = [e - s for s, e in zip(starttimes, endtimes)]

    import pandas as pd
    df = pd.DataFrame({'PlayerID': ids, 'Period': periods, 'Start': starttimes, 'End': endtimes,
                       'Team': teams, 'Duration': durationtime})
    ### TODO: fill in code here for goalies who can have a shift start and shift end in different periods
    ### All I need to do is see whether I subtract 1200 from start or add 1200 to end
    tempdf = df[['PlayerID', 'Start', 'End', 'Team', 'Duration']]
    tempdf = tempdf.assign(Time = tempdf.Start)
    #print(tempdf.head(20))

    toi = pd.DataFrame({'Time': [i for i in range(0, max(df.End) + 1)]})

    toidfs = []
    while len(tempdf.index) > 0:
        temptoi = toi.merge(tempdf, how = 'inner', on = 'Time')
        toidfs.append(temptoi)

        tempdf = tempdf.assign(Time = tempdf.Time + 1)
        tempdf = tempdf.query('Time <= End')

    tempdf = pd.concat(toidfs)
    tempdf = tempdf.sort_values(by = 'Time')

    ### Append team name to start of columns by team
    hdf = tempdf.query('Team == "' + homename + '"')
    hdf2 = hdf.groupby('Time').rank()
    hdf2 = hdf2.rename(columns = {'PlayerID': 'rank'})
    hdf2['rank'] = hdf2['rank'].apply(lambda x: int(x))
    hdf['rank'] = homename + hdf2['rank'].astype('str')

    rdf = tempdf.query('Team == "' + roadname + '"')
    rdf2 = rdf.groupby('Time').rank()
    rdf2 = rdf2.rename(columns={'PlayerID': 'rank'})
    rdf2['rank'] = rdf2['rank'].apply(lambda x: int(x))
    rdf['rank'] = roadname + rdf2['rank'].astype('str')

    ### Occasionally bad entries make duplicates on time and rank. Take one with longer duration

    tokeep = hdf.sort_values(by = 'Duration', ascending = False)
    tokeep = tokeep.groupby(['Time', 'PlayerID']).first()
    tokeep.reset_index(inplace = True)
    hdf = hdf.merge(tokeep, how = 'inner', on = ['Time', 'PlayerID', 'Start', 'End', 'Team', 'rank'])

    tokeep = rdf.sort_values(by='Duration', ascending=False)
    tokeep = tokeep.groupby(['Time', 'PlayerID']).first()
    tokeep.reset_index(inplace=True)
    rdf = rdf.merge(tokeep, how='inner', on=['Time', 'PlayerID', 'Start', 'End', 'Team', 'rank'])

    ### Remove values above 6--looking like there won't be many
    hdf = hdf.pivot(index = 'Time', columns = 'rank', values = 'PlayerID').iloc[:, 1:6]
    hdf.reset_index(inplace = True) #get time back as a column
    rdf = rdf.pivot(index='Time', columns='rank', values='PlayerID').iloc[:, 1:6]
    rdf.reset_index(inplace = True)

    toi = toi.merge(hdf, how = 'left', on = 'Time').merge(rdf, how = 'left', on = 'Time')

    return(toi)

def update_team_ids_from_json(teamdata):

    hid = teamdata['home']['team']['id']
    if hid not in scrapenhl_globals.TEAM_IDS:
        import urllib.request
        import json
        import pandas as pd
        url = 'https://statsapi.web.nhl.com{0:s}'.format(teamdata['home']['team']['link'])
        with urllib.request.urlopen(url) as reader:
            page = reader.read()
        teaminfo = json.loads(page.decode('latin-1'))
        hid = teaminfo['teams'][0]['id']
        habbrev = teaminfo['teams'][0]['abbreviation']
        hname = teaminfo['teams'][0]['name']

        df = pd.DataFrame({'ID': [hid], 'Abbreviation': [habbrev], 'Name': [hname]})
        scrapenhl_globals.TEAM_IDS = pd.concat([scrapenhl_globals.TEAM_IDS, df])
        scrapenhl_globals.write_team_id_file()

    rid = teamdata['away']['team']['id']
    if rid not in scrapenhl_globals.TEAM_IDS:
        import urllib.request
        import json
        url = 'https://statsapi.web.nhl.com{0:s}'.format(teamdata['away']['team']['link'])
        with urllib.request.urlopen(url) as reader:
            page = reader.read()
        teaminfo = json.loads(page.decode('latin-1'))
        rid = teaminfo['teams'][0]['id']
        rabbrev = teaminfo['teams'][0]['abbreviation']
        rname = teaminfo['teams'][0]['name']

        df = pd.DataFrame({'ID': [rid], 'Abbreviation': [rabbrev], 'Name': [rname]})
        scrapenhl_globals.TEAM_IDS = pd.concat([scrapenhl_globals.TEAM_IDS, df])
        scrapenhl_globals.write_team_id_file()

def update_player_ids_from_json(teamdata):
    """
    Creates a data frame of player data from current game's json[liveData][boxscore] to update global PLAYER_IDS.

    This method reads player ids, names, handedness, team, position, and number, and full joins to PLAYER_IDS.
    If there are any changes to PLAYER_IDS, the dataframe gets written to disk again.

    Parameters
    -----------
    teamdata : dict
        A json dict that is the result of api_page['liveData']['boxscore']['teams']
    """
    rteam = scrapenhl_globals.TEAM_IDS.query('ID == ' + str(teamdata['away']['team']['id']))
    rabbrev = rteam['Abbreviation'].iloc[0]
    hteam = scrapenhl_globals.TEAM_IDS.query('ID == ' + str(teamdata['home']['team']['id']))
    habbrev = hteam['Abbreviation'].iloc[0]

    awayplayers = teamdata['away']['players']
    homeplayers = teamdata['home']['players']

    numplayers = len(awayplayers) + len(homeplayers)
    ids = ['' for i in range(numplayers)]
    names = ['' for i in range(numplayers)]
    teams = ['' for i in range(numplayers)]
    positions = ['' for i in range(numplayers)]
    nums = [-1 for i in range(numplayers)]
    handedness = ['' for i in range(numplayers)]

    for i, (pid, pdata) in enumerate(awayplayers.items()):
        idnum = pid[2:]
        name = pdata['person']['fullName']
        try:
            hand = pdata['person']['shootsCatches']
        except KeyError:
            hand = 'N/A'
        try:
            num = pdata['jerseyNumber']
            if num == '':
                raise KeyError
        except KeyError:
            num = -1
        pos = pdata['position']['code']

        ids[i] = idnum
        names[i] = name
        teams[i] = rabbrev
        positions[i] = pos
        nums[i] = num
        handedness[i] = hand

    for i, (pid, pdata) in enumerate(homeplayers.items()):
        idnum = pid[2:]
        name = pdata['person']['fullName']
        try:
            hand = pdata['person']['shootsCatches']
        except KeyError:
            hand = 'N/A'
        try:
            num = pdata['jerseyNumber']
            if num == '':
                raise KeyError
        except KeyError:
            num = -1
        pos = pdata['position']['code']

        ids[i + len(awayplayers)] = idnum
        names[i + len(awayplayers)] = name
        teams[i + len(awayplayers)] = habbrev
        positions[i + len(awayplayers)] = pos
        nums[i + len(awayplayers)] = num
        handedness[i + len(awayplayers)] = hand

    import pandas as pd
    gamedf = pd.DataFrame({'ID': ids,
                           'Name': names,
                           'Team': teams,
                           'Pos': positions,
                           '#': nums,
                           'Hand': handedness})
    ### Find change in length and join
    oldlength = len(scrapenhl_globals.PLAYER_IDS)
    if(oldlength == 0):
        scrapenhl_globals.PLAYER_IDS = gamedf
    else:
        scrapenhl_globals.PLAYER_IDS = scrapenhl_globals.PLAYER_IDS.merge(
            gamedf, how = 'outer', on = ['ID', 'Name', 'Team', 'Pos', '#', 'Hand'])
    newlength = len(scrapenhl_globals.PLAYER_IDS)

    ### Write to disk again immediately in case an error later crashes script
    ### This is in feather format for quick read/write
    if newlength > oldlength:
        scrapenhl_globals.write_player_id_file()

def update_quick_gamelog_from_json(data):
    """
    Creates a data frame of basic game data from current game's json to update global BASIC_GAMELOG.

    This method reads the season, game, date and time, venue, and team names, coaches, anc scores, joining to
    BASIC_GAMELOG.
    If there are any changes to BASIC_GAMELOG, the dataframe gets written to disk again.

    Parameters
    -----------
    data : dict
        The full json dict from the api_page
    """
    season = int(str(data['gameData']['game']['pk'])[:4])
    game = int(str(data['gameData']['game']['pk'])[4:])
    datetime = data['gameData']['datetime']['dateTime']
    try:
        venue = data['gameData']['venue']['name']
    except KeyError:
        venue = 'N/A'
    hname = scrapenhl_globals.TEAM_IDS.query('ID == ' + str(data['gameData']['teams']['home']['id']))
    hname = hname['Abbreviation'].iloc[0]
    rname = scrapenhl_globals.TEAM_IDS.query('ID == ' + str(data['gameData']['teams']['away']['id']))
    rname = rname['Abbreviation'].iloc[0]
    try:
        hcoach = data['liveData']['boxscore']['teams']['home']['coaches'][0]['person']['fullName']
    except IndexError:
        hcoach = 'N/A'
    try:
        rcoach = data['liveData']['boxscore']['teams']['away']['coaches'][0]['person']['fullName']
    except IndexError:
        rcoach = 'N/A'
    hscore = data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
    rscore = data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']

    import pandas as pd
    gamedf = pd.DataFrame({'Season': [season], 'Game': [game], 'Datetime': [datetime], 'Venue': [venue],
                           'Home': [hname], 'HomeCoach': [hcoach], 'HomeScore': [hscore],
                           'Away': [rname], 'AwayCoach': [rcoach], 'AwayScore': [rscore]})
    oldlength = len(scrapenhl_globals.BASIC_GAMELOG)
    scrapenhl_globals.BASIC_GAMELOG = scrapenhl_globals.BASIC_GAMELOG.merge(
        gamedf, how='outer', on = ['Season', 'Game', 'Datetime', 'Venue', 'Home', 'HomeCoach', 'HomeScore',
                                   'Away', 'AwayCoach', 'AwayScore'])
    newlength = len(scrapenhl_globals.BASIC_GAMELOG)
    if newlength > oldlength:
        scrapenhl_globals.write_quick_gamelog_file()

def read_events_from_json(pbp):
    """
    Returns the NHL API url to scrape.

    Parameters
    -----------
    season : int
        The season of the game. 2007-08 would be 2007.
    game : int
        The game id. This can range from 20001 to 21230 for regular season, and 30111 to 30417 for playoffs.
        The preseason, all-star game, Olympics, and World Cup also have game IDs that can be provided.
    Returns
    --------
    pandas df
        Dataframe of the game's play by play data
    """
    ### TODO fill this out
    pass