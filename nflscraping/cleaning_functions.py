import re
import pandas as pd
import numpy as np


def elapsed_time(time_list):
    """
    Calculate elapsed time between consecutive elements in a list of plays from an nfl game.

    Parameters
    ----------
    time_list : list-like
        A list or array-like object containing game times.

    Returns
    -------
    elapsed_times : list
        A list containing elapsed times between consecutive elements in `time_list`.

    Notes
    -----
    This function calculates the elapsed time between plays in an nfl game based off of `time_list`.
    It considers scenarios where the times may wrap around from the end of one quarter to the
    beginning of the next quarter.

    Examples
    --------
    >>> game_times = [720, 700, 400, 300, 100]
    >>> elapsed_times = elapsed_time(game_times)
    >>> print(elapsed_times)
    [20, 300, 100, 200]
    """

    time_list = time_list.tolist()
    elapsed_times = []
    length = len(time_list)
    for i in range(0,length-1):
        time1 = time_list[i]
        time2 = time_list[i+1]
        if time1 > time2:
            elapsed = time1 - time2
            elapsed_times.append(elapsed)
        elif time1 == time2:
            elapsed = 0
            elapsed_times.append(elapsed)
        else:
            elapsed = (time1) + (15-time2)
            elapsed_times.append(elapsed)
    elapsed_times.append(time_list[length-1])
    return elapsed_times


def game_time(elapsed_time):
    """
    Calculate the cumulative real game time based on a list of elapsed times.

    Parameters
    ----------
    elapsed_time : list-like
        A list or array-like object containing elapsed times between consecutive game events.

    Returns
    -------
    real_game_time: list
        A list containing the cumulative real game time at each event based on the provided elapsed times.

    Notes
    -----
    This function computes the cumulative real game time at each event based on a list of elapsed times.
    It starts with an initial time of 0 and adds the elapsed times sequentially.

    Examples
    --------
    >>> elapsed_times = [20, 300, 100, 200, 100]
    >>> real_game_times = game_time(elapsed_times)
    >>> print(real_game_times)
    [0, 20, 320, 420, 620, 720]
    """

    elapsed_time = elapsed_time.tolist()
    real_game_time = []
    real_game_time.append(0)
    for i in range(0,len(elapsed_time)-1):
        time = real_game_time[i] + elapsed_time[i]
        real_game_time.append(time)
    return real_game_time


def play_type(play_description):
    """
    Determine the type of play based on the play description.

    Parameters
    ----------
    play_description : str
        The description of the play.

    Returns
    -------
    str
        The type of play, which can be 'Pass', 'Special Teams', or 'Run'.

    Notes
    -----
    This function analyzes the play description to categorize the type of play. It considers
    keywords such as 'pass' or 'scrambles' for passing plays, and 'kicks' or 'punts' for special
    teams plays. If none of these conditions are met, it assumes a running play.

    Examples
    --------
    >>> play_type('Pass completed to wide receiver')
    'Pass'

    >>> play_type('Punt for 40 yards')
    'Special Teams'

    >>> play_type('Run up the middle')
    'Run'
    """

    if 'pass' in play_description.lower() or 'scrambles' in play_description.lower():
        return 'Pass'
    elif 'kicks' in play_description.lower() or 'punts' in play_description.lower():
        return "Special Teams"
    else: 
            return "Run"
        

def determine_possession(play_start, drives):
    """
    Determine which team possesses the ball at the start of a given play.

    Parameters
    ----------
    play_start : int
        The start time of the play in seconds.
    drives : pandas.DataFrame
        A DataFrame containing drive information, including start times and teams.

    Returns
    -------
    closest_drive_team : str or None
        The team that possesses the ball at the start of the play. Returns None if possession cannot be determined.

    Notes
    -----
    This function determines the possession of the ball at the start of a given play based on the provided
    play start time and information about the drives. It iterates through the drives to find the closest drive
    that started before or at the same time as the play. If found, it returns the corresponding team; otherwise, it
    returns None.

    Examples
    --------
    >>> drives_data = pd.DataFrame({
    ...     'drive_start_time': [0, 180, 400],
    ...     'team': ['TeamA', 'TeamB', 'TeamA']
    ... })
    >>> determine_possession(200, drives_data)
    'TeamB'

    >>> determine_possession(50, drives_data)
    'TeamA'

    >>> determine_possession(600, drives_data)
    None
    """
    
    team_data = ['MIA', 'BUF', 'NYJ', 'NWE', 'PHI', 'DAL', 'NYG', 'WAS', 'BAL', 'PIT', 'CLE', 'CIN', 'DET', 'MIN', 'GNB', 'CHI', 'JAX', 'IND', 'HOU',
                    'TEN', 'ATL','NOR', 'TAM', 'CAR', 'KAN', 'DEN', 'LVR', 'LAC', 'SFO', 'SEA', 'LAR', 'ARI']
    mascot_data = ['Dolphins', 'Bills', 'Jets', 'Patriots', 'Eagles', 'Cowboys', 'Giants', 'Commanders', 'Ravens', 'Steelers', 'Browns', 'Bengals', 'Lions', 'Vikings', 'Packers', 'Bears',
                    'Jaguars', 'Colts', 'Texans', 'Titans', 'Falcons', 'Saints', 'Buccaneers', 'Panthers', 'Chiefs', 'Broncos', 'Raiders', 'Chargers', '49ers', 'Seahawks', 'Rams',
                    'Cardinals']

    teams = pd.DataFrame({'Team' : team_data, 'Mascot' : mascot_data})

    closest_drive_team = None

    for drive_start, drive_team in zip(drives['drive_start_time'], drives['team']):
            if drive_start <= play_start:
                closest_drive_team = drive_team
            else:
                break

    for i, mascot in enumerate(teams['Mascot']):
        if closest_drive_team == mascot :
            possession = teams['Team'][i]
            break
    return possession


def calculate_yardage(current_yardline, next_yardline):
    """
    Calculate the yardage gained or lost between two yardlines.

    Parameters
    ----------
    current_yardline : int
        The starting yardline.
    next_yardline : int
        The ending yardline.

    Returns
    -------
    int
        The yardage gained (positive) or lost (negative) between the two yardlines.
    """
    return next_yardline - current_yardline


def yards_gained(plays):
    """
    Calculate the yardage gained or lost for each play in a given set of plays.

    Parameters
    ----------
    plays : pandas.DataFrame
        A DataFrame containing information about each play, including columns:
        - 'Play_Type': str, the type of play ('Run', 'Pass', etc.).
        - 'possession': str, the team in possession of the ball.
        - 'field_side': str, the side of the field where the play occurs.
        - 'yardline': int, the yardline where the play starts.

    Returns
    -------
    yardage_gained_list : list of int
        A list containing the yardage gained (positive) or lost (negative) for each play.
    """
    plays = pd.DataFrame(plays).reset_index(drop = True)
    
    # If the team with the ball is on the opposite side, subtract the yardline from 100
    plays['yardline'] = np.where(plays['possession'] != plays['field_side'], 100 - plays['yardline'], plays['yardline'])

    yardage_gained_list = []

    for index, row in plays.iterrows():
        # Check if the play type is 'Run' or 'Pass'
        if row['Play_Type'] in ['Run', 'Pass']:
            if row['possession'] != plays['possession'].shift(-1).iloc[index]:
                # Check if the current and next plays are on the same side of the field
                if row['field_side'] == plays['field_side'].shift(-1).iloc[index]:
                    # Update current play's yardline to 100 - yardline
                    yardline = 100 - row['yardline']
                else:
                        yardline = row['yardline']
            else:
                yardline = row['yardline']

            yardage_gained = calculate_yardage(yardline, plays['yardline'].shift(-1).iloc[index])
        else: 
            yardage_gained = 0.0
        # Append the calculated yardage gained to the list
        yardage_gained_list.append(yardage_gained)
    return yardage_gained_list


def seconds_left(plays):
    """
    Calculate the remaining seconds until the specified play start time.

    Parameters
    ----------
    plays : pandas.DataFrame
        A DataFrame containing information about plays, including the 'play_start_time' column.

    Returns
    -------
    seconds_left : int
        The number of seconds remaining until the specified play start time.

    Notes
    -----
    This function assumes that the 'play_start_time' column in the 'plays' DataFrame represents
    the time in minutes, and it calculates the remaining seconds until 60 minutes from the start time.

    Examples
    --------
    >>> import pandas as pd
    >>> plays_data = {'play_start_time': [45, 50, 55]}
    >>> plays_df = pd.DataFrame(plays_data)
    >>> seconds_left(plays_df)
    900  # 15 minutes (900 seconds) remaining until the specified play start time.
    """
    seconds_left = abs(plays['play_start_time'] - 60) * 60
    return seconds_left


def score_diff(plays):
    """
    Calculate the score difference between two columns in a plays DataFrame.

    Parameters
    ----------
    plays : pandas.DataFrame
        A DataFrame containing information about plays, with columns representing scores.

    Returns
    -------
    pandas.Series
        A Series containing the calculated score differences.

    Notes
    -----
    This function assumes that the input DataFrame 'plays' has columns at index 5 and index 6
    representing numeric scores. It calculates the score difference as the difference between
    the values in these two columns, converting them to float.

    Examples
    --------
    >>> import pandas as pd
    >>> plays_data = {'Score_A': [20, 25, 30], 'Score_B': [15, 22, 28]}
    >>> plays_df = pd.DataFrame(plays_data)
    >>> score_diff(plays_df)
    0    5.0
    1    3.0
    2    2.0
    dtype: float64
    """
    return plays.iloc[:,5].astype(float) - plays.iloc[:,6].astype(float)


def adjusted_score_calc(plays):
    """
    Calculate adjusted scores based on the score difference and remaining time.

    Parameters
    ----------
    plays : pandas.DataFrame
        A DataFrame containing information about plays, including 'score_diff' and 'seconds_left' columns.

    Returns
    -------
    adjusted_score : pandas.Series
        A Series containing the calculated adjusted scores.

    Notes
    -----
    This function calculates adjusted scores using the formula:
        adjusted_score = score_diff / ((seconds_left) + 1) ** gamma

    where 'score_diff' is the difference between two scores, 'seconds_left' is the time remaining,
    and 'gamma' is a constant (default value: 0.5).

    Examples
    --------
    >>> import pandas as pd
    >>> plays_data = {'score_diff': [5, 3, 2], 'seconds_left': [900, 1200, 600]}
    >>> plays_df = pd.DataFrame(plays_data)
    >>> adjusted_score_calc(plays_df)
    0    0.01111
    1    0.00083
    2    0.02857
    dtype: float64
    """
    gamma = .5

    adjusted_score = plays['score_diff'] / ((plays['seconds_left']) + 1) ** gamma

    return adjusted_score


def win(plays):
    """
    Determine the winning team at the end of plays and create a binary list indicating possession.

    Parameters
    ----------
    plays : pandas.DataFrame
        A DataFrame containing information about plays, including team possession.

    Returns
    -------
    Y : list
        A binary list indicating possession at the end of each play (1 for the winning team, 0 otherwise).

    Notes
    -----
    This function determines the winning team based on the scores at the end of the plays. It creates
    a binary list where each element represents possession at the end of a play (1 for the winning team,
    0 for the other team).

    Examples
    --------
    >>> import pandas as pd
    >>> plays_data = {'home_team_score': [20, 25, 30], 'visiting_team_score': [15, 22, 28], 'possession': ['Home', 'Visiting', 'Home']}
    >>> plays_df = pd.DataFrame(plays_data)
    >>> win(plays_df)
    [1, 0, 1]
    """
    #plays = pd.DataFrame(plays)
    winning_team = None

    # Get the column names dynamically
    home_team = plays.columns[6]
    vis_team = plays.columns[5]

    Y = []

    # Compare who is the winning team
    if plays.iloc[-1, 5] >= plays.iloc[-1, 6]:
        winning_team = vis_team
    else:
        winning_team = home_team
        

    # Figure out who is winning at the end
    for _, play in plays.iterrows():
        if play['possession'] == winning_team:
            Y.append(1)
        else:
            Y.append(0)
        
    
    return Y

