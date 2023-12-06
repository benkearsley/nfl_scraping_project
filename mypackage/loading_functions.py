import pandas as pd

def load_data(name = 'games'):
    if name == 'games':
        path = '../data/week_10_2023_games.csv'
    elif name == 'plays':
        path = '../data/week_10_2023_plays.csv'
    else:
        raise NameError(f"{name}-is-not-recognized. -The-only-names-are-'games'-and-'data'.")
    
    return pd.read_csv(path)