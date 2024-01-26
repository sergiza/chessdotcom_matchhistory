#!/usr/bin/env python3
import sys
import datetime
import os

# ----------------------------------------------------------

# USAGE: python winrate.py [nº games] [year] [month]
#   no  args    ->  ALL games + current year & month
#   1   arg     ->  nº games + current year & month

# ----------------------------------------------------------

def calculate_win_ratio(file_path, num_games=None):
    total_games = 0
    wins = 0

    with open(file_path, 'r') as file:
        for line in reversed(list(file)):   # Read lines from the end
            if line.count('\t') >= 4:       # Count only game lines
                total_games += 1
                if 'win:' in line:
                    wins += 1
                if any(draw in line for draw in ['repetition:', 'agreed:', 'insufficient:', 'stalemate:']):
                    total_games -= 1        # Don't count draws in total games
                if num_games is not None and total_games >= num_games:
                    break

    if total_games == 0:
        return 0
    else:
        return wins / total_games

# Current year and month
current = datetime.datetime.now()
year_current = str(current.year)
month_current = str(current.month).zfill(2)

# args handling
if len(sys.argv) == 4:
    # Year and month provided
    num_games = int(sys.argv[1])
    year = sys.argv[2]
    month = sys.argv[3].zfill(2)
elif len(sys.argv) == 2:
    # Only number of games provided
    num_games = int(sys.argv[1])
    year = year_current
    month = month_current
elif len(sys.argv) == 1:
    # No arguments provided
    num_games = None
    year = year_current
    month = month_current
else:
    print("USAGE: python winrate.py [nº games] [year] [month]")
    sys.exit(1)

# Path
folder_path = f"{year}"
file_path = f"{folder_path}/{month}.md"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

win_ratio = calculate_win_ratio(file_path, num_games)
print(f"Win Ratio: {win_ratio:.2%}")
