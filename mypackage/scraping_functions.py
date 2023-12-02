
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup, Comment
import re
import time
import cleaning_functions as cf

# functions
def get_drive_table(team, soup):
    """
    Extracts drive data from a BeautifulSoup object for a specific team.

    Parameters
    ----------
    team : str
        The team for which to extract drive data. Should be either 'home' or 'vis'.
    soup : BeautifulSoup
        A BeautifulSoup object containing the HTML content.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the drive data for the specified team.

    Notes
    -----
    The function looks for a specific div element with an 'id' attribute corresponding
    to the team's drives, then extracts drive data from the embedded table.

    Example
    -------
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> home_drives = get_drive_table('home', soup)
    >>> vis_drives = get_drive_table('vis', soup)
    """


    if team == 'home':
        ids = ['all_home_drives', 'home_drives']
    if team == 'vis':
        ids = ['all_vis_drives', 'vis_drives']
    drive_data = []
    parent = soup.find('div', {'id': ids[0]})
    team = parent.find('h2').get_text(strip=False)
    team = team.split()
    team = team[0]
    if parent:
        div = parent.find(string=lambda text: isinstance(text, Comment))
        if div:
            comment_soup = BeautifulSoup(str(div), 'html.parser')
            table = comment_soup.find('table', {'id': ids[1]})
            if table:
                cols = table.find('thead').find('tr')
                column_headers = [th.get_text(strip=True) for th in cols.find_all('th')]
                drives = table.find('tbody').find_all('tr')
                for drive in drives:
                    columns = drive.find_all(['th', 'td'])
                    row_data = [column.get_text(strip=False) for column in columns]
                    drive_data.append(row_data)
    drives_df = pd.DataFrame(columns = column_headers, data = drive_data)
    drives_df['team'] = team
    return drives_df


def scrape_pbp(game_page_soup):
    """
    Scrape play-by-play (PBP) data from a BeautifulSoup object representing a game page from the site `pro-football-reference.com _. Main function called in scrape_game_data() function.

    Parameters
    ----------
    game_page_soup : BeautifulSoup
        A BeautifulSoup object containing the HTML content of the game page.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing play-by-play data extracted from the specified game page.

    Notes
    -----
    This function specifically targets the 'div' element with class 'table_wrapper' and
    id 'all_pbp' to locate the play-by-play data. It extracts data from the embedded
    'table' with id 'pbp'.

    Example
    -------
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> pbp_data = scrape_pbp(soup)

    .. _https://www.pro-football-reference.com/
    """

    pbp_datas = []
    pbp_parent = game_page_soup.find('div', {'class': 'table_wrapper', 'id': 'all_pbp'})
    if pbp_parent:
        pbp_div = pbp_parent.find(string=lambda text: isinstance(text, Comment))
        if pbp_div:
            comment_soup = BeautifulSoup(str(pbp_div), 'html.parser')
            pbp_table = comment_soup.find('table', {'id': 'pbp'})
            if pbp_table:
                cols = pbp_table.find('thead').find('tr')
                column_headers = [th.get_text(strip=True) for th in cols.find_all('th')]
                plays = pbp_table.find('tbody').find_all('tr',{'class': ''})
                for play in plays:
                    columns = play.find_all(['th', 'td'])
                    play_data = [column.get_text(strip=False) for column in columns]
                    pbp_datas.append(play_data)
    pbp_datas = pd.DataFrame(columns = column_headers, data = pbp_datas)
    return pbp_datas


def scrape_game_data(game_url):
    """
    Scrape game data from the specified Pro Football Reference game URL.

    Parameters
    ----------
    game_url : str
        The URL of the Pro Football Reference game page to scrape.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing cleaned play-by-play (PBP) data for the game.

    Notes
    -----
    This function extracts drive data for the home and visiting teams, as well as play-by-play
    (PBP) data, from the specified game URL. It performs data cleaning and transformation,
    including handling time-related columns and determining possession.

    Parameters
    ----------
    game_url : str
        The URL of the Pro Football Reference game page to scrape.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing cleaned play-by-play (PBP) data for the game.

    Example
    -------
    >>> url = 'https://www.pro-football-reference.com/boxscores/202309070kan.htm'
    >>> game_data = scrape_game_data(url)
    """

    team_keys = {
        'DET': 'Lions',
        'KAN': 'Chiefs',
        'ATL': 'Falcons',
        'CAR': 'Panthers',
        'CLE': 'Browns', 
        'CIN': 'Bengals', 
        'IND': 'Colts', 
        'JAX': 'Jaguars',
        'MIN': 'Vikings', 
        'TAM': 'Buccaneers',
        'NOR': 'Saints', 
        'TEN': 'Titans',
        'PIT': 'Steelers', 
        'SFO': '49ers', 
        'BAL': 'Ravens',
        'HOU': 'Texans', 
        'WAS': 'Commanders',
        'ARI': 'Cardinals',
        'CHI': 'Bears', 
        'GNB': 'Packers',
        'DEN': 'Broncos', 
        'LVR': 'Raiders', 
        'NWE': 'Patriots', 
        'PHI': 'Eagles', 
        'LAC': 'Chargers', 
        'MIA': 'Dolphins',
        'SEA': 'Seahawks',
        'LAR': 'Rams',
        'NYG': 'Giants',
        'DAL': 'Cowboys',
        'NYJ': 'Jets', 
        'BUF': 'Bills'
    }
    pbp_data = []
    # game_url = 'https://www.pro-football-reference.com/boxscores/202309070kan.htm'
    r = requests.get(game_url)
    game_page_soup = BeautifulSoup(r.text, 'html.parser')
    # scraping drive data for home and away team
    home_drives = get_drive_table('home', game_page_soup)
    vis_drives = get_drive_table('vis', game_page_soup)
    # getting home and away team variables
    home_team = home_drives['team'][0]
    vis_team = vis_drives['team'][0]
    teams = [home_team, vis_team]
    drives = pd.concat([home_drives, vis_drives], axis=0)
    drives['Quarter'] = drives['Quarter'].astype(int)
    drives['minute'] = drives['Time'].str.extract(r'([0-9]+):').astype(int)
    drives['seconds'] = drives['Time'].str.extract(r'[0-9]+:([0-9]+)').astype(int)
    drives['seconds_ratio'] = (drives['seconds'] / 60).astype(float)
    drives['Numeric_time'] = drives['minute'] + drives['seconds_ratio']
    drives = drives.sort_values(by=['Quarter', 'Numeric_time'], ascending=[True, False]).reset_index()
    drives['drive_time'] = cf.elapsed_time(drives['Numeric_time'])
    drives['drive_start_time'] = cf.game_time(drives['drive_time'])
    drives = drives.drop(columns=['minute', 'seconds', 'seconds_ratio', 'index', '#', 'Numeric_time', 'drive_time'])
    # scraping pbp data
    pbp_data = scrape_pbp(game_page_soup)
    # Setting up receiving and kicking teams
    coin_toss = pbp_data.iloc[0]
    pbp_data = pbp_data.drop(0)
    coin_toss = coin_toss[7]
    teams = re.findall(r'\b[A-Z][a-zA-Z]*\b', coin_toss)
    match = re.search(r"(\w+)\s+to\s+receive\s+the\s+opening\s+kickoff", coin_toss)
    if match:
        receiving_team = match.group(1)
    # dropping timeouts
    pbp_data = pbp_data[pbp_data['Location'].str.strip() != '']
    pbp_data = pbp_data.dropna(subset=['Location'])
    print(f'{home_team} vs. {vis_team} \n total plays: {len(pbp_data)}')
    # General Cleaning
    pbp_data['Quarter'] = pbp_data['Quarter'].astype(int)
    pbp_data['field_side'] = pbp_data['Location'].str.extract(r'([A-Z]+)')
    pbp_data['yardline'] = pbp_data['Location'].str.extract(r'([0-9]+)')
    pbp_data['yardline'] = pbp_data['yardline'].astype(int)
    pbp_data['minute'] = pbp_data['Time'].str.extract(r'([0-9]+):').astype(int)
    pbp_data['seconds'] = pbp_data['Time'].str.extract(r'[0-9]+:([0-9]+)').astype(int)
    pbp_data['seconds_ratio'] = (pbp_data['seconds'] / 60).astype(float)
    pbp_data['Numeric_time'] = pbp_data['minute'] + pbp_data['seconds_ratio']
    pbp_data['play_time'] = cf.elapsed_time(pbp_data['Numeric_time'])
    pbp_data['play_start_time'] = cf.game_time(pbp_data['play_time'])
    pbp_data = pbp_data.drop(columns=['minute', 'seconds', 'seconds_ratio','Numeric_time', 'play_time'])
    pbp_data['Play_Type'] = pbp_data['Detail'].apply(cf.play_type)
    pbp_data['possession'] = pbp_data['play_start_time'].apply(lambda play_start: cf.determine_possession(play_start, drives))
    pbp_data['Yardage'] = pbp_data.apply(lambda row: cf.yardage_by_play(row['Detail'], row['Play_Type']), axis=1)
    pbp_data = pbp_data.rename(columns={pbp_data.columns[5]: team_keys[pbp_data.columns[5]], 
                                    pbp_data.columns[6]: team_keys[pbp_data.columns[6]]})
    
    return pbp_data


def scrape_games(game_links=[], data_file_path ='data.csv', game_file_path='games.csv'):
    """
    Scrape game data from a list of Pro Football Reference game URLs and save the results.

    Parameters
    ----------
    game_links : list of str, optional
        List of Pro Football Reference game URLs to scrape. Default is an empty list.
    data_file_extension : str, optional
        Extension for the data file CSV. Default is 'data'.
    game_file_extension : str, optional
        Extension for the game file CSV. Default is 'games'.

    Returns
    -------
    None

    Notes
    -----
    This function iterates through the provided list of game links, extracts game and play-by-play data
    using the `scrape_game_data` function, and saves the cleaned data in CSV files. It introduces a
    delay of 30 seconds between each scraping operation to avoid overloading the server.

    Example
    -------
    >>> game_urls = ['https://www.pro-football-reference.com/boxscores/202309070kan.htm', ...]
    >>> scrape_games(game_links=game_urls)
    """

    games = {
    'game_id': [], 
    'team1': [], 
    'team2': [],
    'link': []
    }

    data = pd.DataFrame({
        'Quarter': [], 
        'Time': [], 
        'Down': [], 
        'ToGo': [], 
        'Location': [], 
        'Lions': [], 
        'Chiefs': [], 
        'Detail': [], 
        'EPB': [],
        'EPA': [], 
        'field_side': [], 
        'yardline': [], 
        'play_start_time': [], 
        'Play_Type': [], 
        'posession': [], 
        'Yardage': []
                    })
    
    for link in game_links:
        game_data = scrape_game_data(link)
        game_data['game_id'] = id
        team1 = game_data.columns[5]
        team2 = game_data.columns[6]
        game_data = game_data.rename(columns={game_data.columns[5]: 'team1', 
                                    game_data.columns[6]: 'team2'})
        games['game_id'].append(id)
        games['team1'].append(team1)
        games['team2'].append(team2)
        games['link'].append(link)
        data = pd.concat([data, game_data], axis=0)
        id = id + 1
        time.sleep(30)
    games_df = pd.DataFrame(games)
    data.to_csv(data_file_path,index=False)
    games_df.to_csv(game_file_path, index=False)
    print('done')