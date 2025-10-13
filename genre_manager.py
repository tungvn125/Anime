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


from simple_term_menu import TerminalMenu
import json
from mal import AnimeSearch
def list_genres():
    """
    This function lists the user's preferred genres stored in 'user_like_genre.json'.
    """
    try:
        with open("user_like_genre.json", 'r') as f:
            selected_genres = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_genres = []

    if selected_genres:
        print("Your preferred genres are:")
        for genre in selected_genres:
            print(f"- {genre}")
    else:
        print("You have no preferred genres saved.")
def remove_genre():
    list_genres()
    genre_to_remove = input("Enter the genre you want to remove: ").strip()
    if not genre_to_remove:
        print("No genre entered. Operation cancelled.")
        return
    """
    This function removes a genre from the user's preferred genres list stored in 'user_like_genre.json'.
    """
    try:
        with open("user_like_genre.json", 'r') as f:
            selected_genres = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_genres = []

    if genre_to_remove in selected_genres:
        selected_genres.remove(genre_to_remove)
        with open("user_like_genre.json", 'w') as f:
            json.dump(selected_genres, f)
        print(f"Removed genre: {genre_to_remove}")
    else:
        print(f"Genre '{genre_to_remove}' not found in your preferences.")
def add_genre():
    list_genres()
    genre_to_add = input("Enter the genre you want to add: ").strip()
    if not genre_to_add:
        print("No genre entered. Operation cancelled.")
        return
    """
    This function adds a genre to the user's preferred genres list stored in 'user_like_genre.json'.
    """
    try:
        with open("user_like_genre.json", 'r') as f:
            selected_genres = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_genres = []

    if genre_to_add not in selected_genres:
        selected_genres.append(genre_to_add)
        with open("user_like_genre.json", 'w') as f:
            json.dump(selected_genres, f)
        print(f"Added genre: {genre_to_add}")
    else:
        print(f"Genre '{genre_to_add}' is already in your preferences.")

def clear_genres():
    """
    This function clears all genres from the user's preferred genres list stored in 'user_like_genre.json'.
    """
    with open("user_like_genre.json", 'w') as f:
        json.dump([], f)
    print("Cleared all preferred genres.")