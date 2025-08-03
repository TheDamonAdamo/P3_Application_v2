# Starter code - OpenClassrooms WPS | P3

This repository contains the work that has been done so far on the chess tournament program.

### Data files

There are data files provided:
- JSON files for the chess clubs of Springfield and Cornville
- JSON files for two tournaments: one completed, and one in progress

### Models

This package contains the models already defined by the application:
* `Player` is a class that represents a chess player
* `Club` is a class that represents a chess club (including `Player`s)
* `ClubManager` is a manager class that allows to manage all clubs (and create new ones)
* `match.py` is a class that returns the match results
* `player_directory.py` is a class that creates a dictionary of all players and clubs for quick searching
* `round` is a class that contains the matches and checks for completion to go the next round or complete the tournament

### Screens

This package contains classes that are used by the application to display information from the models on the screen.
Each screen returns a Command instance (= the action to be carried out).
There are 3 sub-packages contained in screens along with the base screen and main menu, The 3 packages are for clubs, players, and tournaments.

### Commands

This package contains "commands" - instances of classes that are used to perform operations from the program.
Commands follow a *template pattern*. They **must** define the `execute` method.
When executed, a command returns a context.
In addition to the existing commands a command for tournaments and create_tournaments were added to facilitate the tournament functions

### Main application

The main application is controlled by `main.py`. it has it's own menu to access manage_clubs.py and manage_tournaments.py'. To keep the two functionalities separate and modular.

The main application is an infinite loop and stops when a context has the attribute `run` set to False.

## Instructions for Setup and Installation

## Chess Tournament Manager

This is an offline console application to manage chess clubs and run chess tournaments from start to finish.

## Requirements

- Python 3.10 or higher (tested with 3.13)
- Works offline (no internet connection required)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TheDamonAdamo/P3_Application_v2.git
   cd P3_Application_v2

2. ** Create a Virutal Environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate    

3. Install Dependencies
    pip install -r requirements.txt

4. Run the Application
    python main.py

## Running flake8 and Generating Reports

1. Install Linting Tools
    pip install flake8 flake8-html

2. Generate HTML Report
    flake8 . --format=html --htmldir=flake8_report

3. Open the Report
    Open flake8_report/index.html in a browser.
