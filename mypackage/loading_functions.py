import pandas as pd

def load_data(name = 'games'):
    """
    Load data from a CSV file.

    Parameters
    ----------
    name : str, optional
        Specifies the type of data to load. Default is 'games'.
        If 'games', the function loads game data.
        If 'plays', the function loads play data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the loaded data.

    Raises
    ------
    NameError
        If the provided `name` is not recognized. The only valid names
        are 'games' and 'plays'.

    Example
    -------
    >>> games_data = load_data()  # Load game data by default
    >>> plays_data = load_data(name='plays')  # Load play data explicitly
    """
    if name == 'games':
        path = '../data/week_1_2023_games.csv'
    elif name == 'plays':
        path = '../data/week_1_2023_plays.csv'
    else:
        raise NameError(f"{name}-is-not-recognized. -The-only-names-are-'games'-and-'data'.")
    
    return pd.read_csv(path)