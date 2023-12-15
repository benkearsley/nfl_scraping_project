"""
Given a set of game links from pro-football-reference.com,this script imports the raw data, 
cleans it, and outputs the final dataset. Specifically, this current set of game links
exports all games played in week 1 of the 2023 NFL season. 

The function scrape_games() from the scraping_functions module contains function calls to 
other custom cleaning and scraping functions.  Documentation for all of these functions can be found at:
https://benkearsley.github.io/nfl_scraping_project/
"""


if __name__ == '__main__':
    import scraping_functions as sf

    game_links = [
    'https://www.pro-football-reference.com/boxscores/202309110nyj.htm',
    'https://www.pro-football-reference.com/boxscores/202309070kan.htm',
    'https://www.pro-football-reference.com/boxscores/202309100atl.htm',
    'https://www.pro-football-reference.com/boxscores/202309100chi.htm',
    'https://www.pro-football-reference.com/boxscores/202309100cle.htm',
    'https://www.pro-football-reference.com/boxscores/202309100clt.htm',
    'https://www.pro-football-reference.com/boxscores/202309100den.htm',
    'https://www.pro-football-reference.com/boxscores/202309100min.htm',
    'https://www.pro-football-reference.com/boxscores/202309100nor.htm',
    'https://www.pro-football-reference.com/boxscores/202309100nwe.htm',
    'https://www.pro-football-reference.com/boxscores/202309100nyg.htm',
    'https://www.pro-football-reference.com/boxscores/202309100pit.htm',
    'https://www.pro-football-reference.com/boxscores/202309100rav.htm',
    'https://www.pro-football-reference.com/boxscores/202309100sdg.htm',
    'https://www.pro-football-reference.com/boxscores/202309100sea.htm',
    'https://www.pro-football-reference.com/boxscores/202309100was.htm'    
    ]

    game_file_path ='../nfl_scraping_project/mypackage/data/week_1_2023_games.csv'
    data_file_path = '../nfl_scraping_project/mypackage/data/week_1_2023_plays.csv'

    sf.scrape_games(game_links, data_file_path, game_file_path)