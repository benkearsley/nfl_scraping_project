import re


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

    closest_drive_team = None
    for drive_start, drive_team in zip(drives['drive_start_time'], drives['team']):
            if drive_start <= play_start:
                closest_drive_team = drive_team
            else:
                break
    return closest_drive_team


def yardage_by_play(play_detail, play_type):
    """
    Calculate yardage gained or lost on a play based on play details and type.

    Parameters
    ----------
    play_detail : str
        The detailed description of the play.
    play_type : str
        The type of play, which can be 'Run' or 'Pass'.

    Returns
    -------
    yardage : float
        The yardage gained or lost on the play. Returns 0 if yardage cannot be determined.

    Notes
    -----
    This function calculates the yardage gained or lost on a play based on the provided play details
    and play type. For 'Run' or 'Pass' plays, it uses a regular expression pattern to find and sum up
    yardage values from the play details. If no yardage values are found or the play type is not 'Run'
    or 'Pass', it returns 0.

    Examples
    --------
    >>> yardage_by_play('Run for 5 yards', 'Run')
    5.0

    >>> yardage_by_play('Pass complete for 12 yards', 'Pass')
    12.0

    >>> yardage_by_play('Incomplete pass', 'Pass')
    0.0
    """

    yardage = 0
    
    if play_type in ['Run', 'Pass']:
        # Define a regular expression pattern to find yardage in play_detail
        pattern = r'(-?\d+\.\d+|-?\d+)'
        # Use re.findall to find all yardage values that match the pattern
        yards = re.findall(pattern, play_detail)
        # If we found yardage values, sum them up
        if yards:
            yardage = sum(map(float, yards))
    return yardage