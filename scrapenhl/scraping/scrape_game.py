from scrapenhl_globals import SAVE_FOLDER

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
        URL to scrape
    """
    return 'http://statsapi.web.nhl.com/api/v1/game/{0:d}0{1:d}/feed/live'.format(season, game)

def get_json_save_filename(season, game):
    return '{0:s}/{1:d}/{2:d}.json'.format(SAVE_FOLDER, season, game)

def get_parsed_save_filename(season, game):
    pass

def scrape_game(season, game, force_overwrite = False):
    """
        Scrapes and saves game files in compressed (.pkl) format

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
    url = get_url(season, game)
    filename = get_json_save_filename(season, game)
    if force_overwrite or not os.path.exists(filename):
        import urllib.request
        with urllib.request.urlopen(url) as reader:
            try:
                page = reader.read().decode('latin-1')
            except Exception as e:
                print('Error with', season, game, e, e.args)
                page = ''
        import pickle
        w = open(filename, 'wb')
        pickle.dump(page, w)

scrape_game(2007, 20001, True)