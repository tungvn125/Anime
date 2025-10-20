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
from features.search_by_genres import fetch_anime_by_genres, collect_genres_from_anime

def recommend_anime():
    """Helps users find anime recommendations based on their genre preferences and watchlist."""
    
    def load_user_genres():
        try:
            with open("user_like_genre.json", 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_watchlist():
        try:
            with open("watchlist.json", 'r') as f:
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
    watchlist = load_watchlist()
    if "watchlist" in watchlist and isinstance(watchlist["watchlist"], list):
        watchlist = [anime["title"] for anime in watchlist["watchlist"]]
        print(f"DEBUG: Watchlist loaded successfully.{watchlist}")
        watchlist_genres = set()
        for anime_name in watchlist:
            print("DEBUG: Collecting genres for anime:", anime_name)
            genres = collect_genres_from_anime(anime_name)
            if genres:
                watchlist_genres.update(genres)
        print("DEBUG: Collected genres from watchlist:", watchlist_genres)
        watchlist = list(watchlist_genres)
    else:
        watchlist = []
        print("DEBUG: No watchlist found or invalid format.")


    # Check if we have any data to work with
    if not selected_genres and not watchlist:
        print("\nNo preferences found. Please use the chat feature to set genre preferences or add anime to your watchlist.")
        return

    # Display current preferences
    print("\nCurrent Preferences:")
    print(f"Genres: {', '.join(selected_genres) if selected_genres else 'None'}")
    print(f"Watchlist items: {len(watchlist)}")
    
    # Setup recommendation options
    options = ["Recommend by genres", "Recommend by watchlist", "Combined recommendations", "Exit"]
    choice = options[TerminalMenu(options).show()]
    
    if choice == "Exit":
        return

    recommendations = []
    
    # Get genre-based recommendations
    if choice in ["Recommend by genres", "Combined recommendations"] and selected_genres:
        genre_recs = get_recommendations(selected_genres, False)
        if genre_recs:
            print(f"\n------Anime Recommendations for your liked genres({genres})------")
            for anime in genre_recs:
                print(f"{anime['title']['romaji']} ({anime['title']['english']})")
                print(f"  + Genres: {', '.join(anime['genres'])}")
                print(f"  + Score: {anime['averageScore']}\n")
            recommendations.append(genre_recs)

    # Get watchlist-based recommendations
    if choice in ["Recommend by watchlist", "Combined recommendations"] and watchlist:
        if watchlist_genres:
            watchlist_recs = get_recommendations(list(watchlist_genres), False)
            if watchlist_recs:
                print(f"\n------Anime Recommendations based on your Watchlist------")
                for anime in watchlist_recs:
                    print(f"{anime['title']['romaji']} ({anime['title']['english']})")
                    print(f"  + Genres: {', '.join(anime['genres'])}")
                    print(f"  + Score: {anime['averageScore']}\n")
                recommendations.append(watchlist_recs)

    # Handle recommendations output
    if recommendations:
        save_option = TerminalMenu(["Yes", "No"], title="Save recommendations to 'recommendations.txt'?").show()
        if save_option == 0:
            save_recommendations(choice, selected_genres, recommendations)
            print("\nRecommendations saved successfully to recommendations.txt")
    else:
        print("\nNo recommendations could be generated. Try different preferences or add more items to your watchlist.")
