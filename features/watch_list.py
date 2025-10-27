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
from simple_term_menu import TerminalMenu
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
    try:
        watchlist = get_watchlist()
        ter_menu = TerminalMenu([anime["title"] for anime in watchlist["watchlist"]])
        menu_entry_index = ter_menu.show()
        print(f"You selected: {watchlist['watchlist'][menu_entry_index]['title']}")
        anime_title = watchlist["watchlist"][menu_entry_index]["title"]                 
        for anime in watchlist["watchlist"]:
            if anime["title"].lower() == anime_title.lower():
                episodes = int(input(f"Enter the number of episodes watched for '{anime_title}': "))
                anime["episodes_watched"] = episodes
                save_watchlist(watchlist)
                print(f"Updated '{anime_title}' to {episodes} episodes watched.")
                return
        print(f"'{anime_title}' not found in your watchlist.")
    except ValueError:
        print("Please provide a valid number for episodes watched.")


def list_watchlist():
    """Lists all the anime in the watchlist."""
    watchlist = get_watchlist()
    if watchlist["watchlist"]:
        print("Your watchlist:")
        for anime in watchlist["watchlist"]:
            print(f"- {anime['title']} (Episodes watched: {anime['episodes_watched']})")
    else:
        print("Your watchlist is empty.")

def add_to_watchlist_func(anime_title):
    """Adds an anime to the watchlist."""
    # Validate input
    if not isinstance(anime_title, str):
        try:
            anime_title = str(anime_title)
        except Exception:
            return "Invalid anime title."

    title = anime_title.strip()
    if not title:
        return "Anime title is empty."

    # Load or initialize watchlist structure
    watchlist = get_watchlist() or {"watchlist": []}
    if not isinstance(watchlist, dict):
        watchlist = {"watchlist": []}
    if "watchlist" not in watchlist or not isinstance(watchlist["watchlist"], list):
        watchlist["watchlist"] = []

    # Check for duplicates (case-insensitive, trimmed)
    for anime in watchlist["watchlist"]:
        existing_title = ""
        if isinstance(anime, dict):
            existing_title = str(anime.get("title", "")).strip()
        else:
            existing_title = str(anime).strip()
        if existing_title.lower() == title.lower():
            return f"'{title}' is already in your watchlist."

    # Append and save
    watchlist["watchlist"].append({"title": title, "episodes_watched": 0})
    try:
        save_watchlist(watchlist)
    except Exception as e:
        return f"Failed to save watchlist: {e}"

    return f"Added '{title}' to your watchlist."
