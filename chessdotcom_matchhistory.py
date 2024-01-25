#!/usr/bin/env python3
import requests
import os
import sys
import datetime

# ----------------------------------------------------------

# USAGE: python chessdotcom_matchhistory.py [year] [month]
#   no args ->  current year & month

user = 'magnuscarlsen'   # <- CHESS.COM USERNAME

# ----------------------------------------------------------

# month & year
current = datetime.datetime.now()
year_current = str(current.year)
month_current = str(current.month).zfill(2)
if len(sys.argv) == 1:      # No args       ->  use current month & year
    year = year_current
    month = month_current
elif len(sys.argv) == 3:    # With args     ->  use args
    year = sys.argv[1]
    month = sys.argv[2].zfill(2)
else:                       # Weird format  ->  show help
    print("USAGE: python chessdotcom_matchhistory.py [year] [month]")
    sys.exit(1)


def get_chess_games(year, month):
    url = f"https://api.chess.com/pub/player/{user}/games/{year}/{month}"

    headers = {'User-Agent': 'chessdotcom_matchhistory/1.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error HTTP: {response.status_code})")
        return []

    try:
        games = response.json().get('games', [])
    except ValueError:
        print("Error: invalid JSON")
        return []

    return games

def update_markdown_file(year, month, games):
    folder_path = f"{year}"
    file_path = f"{folder_path}/{month}.md"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    existing_games = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.count('\t') >= 4:
                    existing_games.append(line)

    with open(file_path, 'a') as file:
        for game in games:
            game_number = games.index(game) + 1
            timestamp = game['end_time']
            game_day = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M')
            color_emoji = '♔' if game['white']['username'].lower() == user.lower() else '♚'
            white_result = game['white']['result']
            black_result = game['black']['result']
            result = f"<!-- {white_result} -->" if color_emoji == '♔' else f"<!-- {black_result} -->"
            if 'win' in result or 'agreed' in result:
                result = result.replace('win', 'win\t').replace('agreed', 'agreed\t')
            opponent = f"vs {game['black']['username']}" if color_emoji == '♔' else f"vs {game['white']['username']}"

            game_line = f"{game_number}\t{game_day}\t{color_emoji}\t{result}\t{opponent}\n"
            if game_line not in existing_games:
                file.write(game_line)


games = get_chess_games(year, month)
update_markdown_file(year, month, games)
