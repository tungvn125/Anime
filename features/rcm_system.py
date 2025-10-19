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
from mal import AnimeSearch
from simple_term_menu import TerminalMenu
from features.search_by_genres import fetch_anime_by_genres
def recommend_anime():
    """Helps users find anime recommendations based on their genre preferences."""
    
    def load_user_genres():
        try:
            with open("user_like_genre.json", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_recommendations(genres, is_single_genre=True):
        try:
            search = fetch_anime_by_genres(genres=genres, max_results=5)
            if not search:
                genre_str = genres[0] if is_single_genre else ", ".join(genres)
                print(f"No recommendations found for {genre_str}.")
            return search
        except Exception as e:
            print(f"An error occurred while searching: {e}")
            return None

    def save_recommendations(choice, selected_genres, recommendations):
        with open("recommendations.txt", 'w') as f:
            f.write(f"Anime recommendations for genres: {', '.join(selected_genres)}\n\n")
            for rec in recommendations:
                if rec:
                    for anime in rec:
                        f.write(f"{anime['title']['romaji']} ({anime['title']['english']})\n")
                        f.write(f"  + Genres: {', '.join(anime['genres'])}\n")
                        f.write(f"  + Score: {anime['averageScore']}\n\n")

    # Main execution
    selected_genres = load_user_genres()
    if not selected_genres:
        print("\nPlease chat with the bot first to save your genre preferences.")
        return

    print("\nYour preferred genres:", ", ".join(selected_genres))
    
    options = ["Each genre separately", "All genres combined", "Both", "Exit"]
    menu = TerminalMenu(options)
    choice = options[menu.show()]
    
    if choice == "Exit":
        return

    recommendations = []
    
    if choice in ["Each genre separately", "Both"]:
        for genre in selected_genres:
            recommendations.append(get_recommendations([genre]))

    if choice in ["All genres combined", "Both"]:
        recommendations.append(get_recommendations(selected_genres, False))

    # Ask to save recommendations
    print("\nSave result to 'recommendations.txt' ?:")
    if TerminalMenu(["Yes", "No"]).show() == 0:
        save_recommendations(choice, selected_genres, recommendations)
        print("Recommendations saved to recommendations.txt")
