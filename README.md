# NFL Play by Play Scraping Analysis
*by Ben Kearsley & Zayne Maughan*
## Project Description
This package is for performing analysis of plays from NFL games, and was inspired by ESPN's win prediction algorithm.  Getting granular with NFL data can be messy, and this package aims to clean up some of that mess. 

In this package you will find functions in three modules:

 
### 1. scraping_functions.py

This module contains functions used to scrape one or multiple games from the Pro Football Reference site.[^1]  Also, contains some functions to scrape a table containing drive data from the game.

### 2. cleaning_functions.py

This module contains functions to clean and organize the data scraped from the Pro Football Reference site.[^1]

### 3. predicting_functions.py

This module contains our attempt to forecast game win probability.  This module is subject to further iterations with improved accuracy.

### 4. loading_functions.py

This module contains functions to load the prescraped data in the package.

Contained in this package is also a prescraped set of game data from Week 1 of the 2023 NFL season.[^2]

## Documentation
Documentation for this package can be found [here](https://benkearsley.github.io/nfl_scraping_project/).

## Installation Instructions
To install this package, run the following command in your terminal:

    pip install git+https://github.com/benkearsley/nfl_scraping_project.git
    
## Usage Examples
Feel free to check out the demo.ipynb file for examples of how to use the package for scraping game data or predicting game outcome.

## Contribution Guidelines
If you wish to contribute, please fork the repository, create a new branch for your contributions, and submit a pull request with a detailed description of the changes. Additionally, please follow the established coding style, provide comprehensive test coverage, and be receptive to feedback for a collaborative and efficient contribution experience.

## Licensing Information
This project is licensed under the [GPL-3.0 License](https://github.com/benkearsley/nfl_scraping_project?tab=GPL-3.0-1-ov-file).

For details, see the [LICENSE](https://github.com/benkearsley/nfl_scraping_project/blob/main/LICENSE) file.

## Contact and Support Details
Feel free to contact me at [ben.kearsley@outlook.com](mailto:ben.kearsley@outlook.com)

[^1]: Pro Football Reference. https://www.pro-football-reference.com/. Accessed 12/14/2023
[^2]: Raw data files are not included in this package because they are scraped directly from the Pro Football Reference site. The game_links found in the [clean_data.py](https://github.com/benkearsley/nfl_scraping_project/blob/main/nflscraping/clean_data.py) file contain the 'raw' data and they are static and should not change with time.
