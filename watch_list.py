"""Copyright 2025 Trần Phan Thanh Tùng

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
Tùng
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import json
import sys
import os
WATCHLIST_FILE = "watchlist.json"
def get_watchlist():
    """Reads the watchlist from the JSON file."""
    try:
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"watchlist": []}

def save_watchlist(watchlist):
    """Saves the watchlist to the JSON file."""
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f, indent=4)

# error. fix later
def update_watchlist():
    """Updates the number of episodes watched for an anime."""
    if len(sys.argv) > 3:
        anime_title = sys.argv[2]
        try:
            episodes = int(sys.argv[3])
            watchlist = get_watchlist()
            for anime in watchlist["watchlist"]:
                if anime["title"].lower() == anime_title.lower():
                    anime["episodes_watched"] = episodes
                    save_watchlist(watchlist)
                    print(f"Updated '{anime_title}' to {episodes} episodes watched.")
                    return
            print(f"'{anime_title}' not found in your watchlist.")
        except ValueError:
            print("Please provide a valid number for episodes watched.")
    else:
        print("Please provide an anime title and the number of episodes watched.")

def list_watchlist():
    """Lists all the anime in the watchlist."""
    watchlist = get_watchlist()
    if watchlist["watchlist"]:
        print("Your watchlist:")
        for anime in watchlist["watchlist"]:
            print(f"- {anime['title']} (Episodes watched: {anime['episodes_watched']})")
    else:
        print("Your watchlist is empty.")