import json
from mal import AnimeSearch
from simple_term_menu import TerminalMenu
def recommend_anime():
    """
    This function helps the user find anime recommendations based on their genre preferences.
    """
    print("Let's find some anime recommendations for you!")

    try:
        with open("user_like_genre.json", 'r') as f:
            selected_genres = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_genres = []

    if not selected_genres:
        print("\nPlease chat with the bot first to save your genre preferences.")
        return

    print("\nBased on your preferences, you like the following genres:")
    for genre in selected_genres:
        print(f"- {genre}")
    print("\nHow would you like to receive your recommendations?")
    choice = ["Each genre separately", "All genres combined", "Both", "Exit"]
    terminal_menu = TerminalMenu(choice)
    choice_index = terminal_menu.show()
    print(f"You selected: {choice[choice_index]}")
    if choice[choice_index] == "Exit":
        return
    if choice[choice_index] == "Each genre separately":
        print("\nHere are some recommendations for you:")
        for genre in selected_genres:
            try:
                print(f"\n--- Recommendations for {genre} ---")
                search = AnimeSearch(genre)
                if search.results:
                    # Limit the number of recommendations to 5 for each genre
                    for i, result in enumerate(search.results):
                        if i >= 5:
                            break
                        print(f"- {result.title} (Score: {result.score})")
                else:
                    print(f"No recommendations found for {genre}.")
            except Exception as e:
                print(f"An error occurred while searching for {genre}: {e}")
    # recommendations for all genres
    elif choice[choice_index] == "All genres combined":
        print("\nHere are some recommendations for you:")
        try:
            print(f"\n--- Recommendations for all your preferred genres ---")
            combined_genres = ' '.join(selected_genres)
            search = AnimeSearch(combined_genres)
            if search.results:
                for i, result in enumerate(search.results):
                    if i >= 5:
                        break
                    print(f"- {result.title} (Score: {result.score})")
            else:
                print("No recommendations found for your combined genres.")
        except Exception as e:
            print(f"An error occurred while searching for combined genres: {e}")
    elif choice[choice_index] == "Both":
        print("\nHere are some recommendations for you:")
        for genre in selected_genres:
            try:
                print(f"\n--- Recommendations for {genre} ---")
                search = AnimeSearch(genre)
                if search.results:
                    # Limit the number of recommendations to 5 for each genre
                    for i, result in enumerate(search.results):
                        if i >= 5:
                            break
                        print(f"- {result.title} (Score: {result.score})")
                else:
                    print(f"No recommendations found for {genre}.")
            except Exception as e:
                print(f"An error occurred while searching for {genre}: {e}")
        try:
            print(f"\n--- Recommendations for all your preferred genres ---")
            combined_genres = ' '.join(selected_genres)
            search = AnimeSearch(combined_genres)
            if search.results:
                for i, result in enumerate(search.results):
                    if i >= 5:
                        break
                    print(f"- {result.title} (Score: {result.score})")
            else:
                print("No recommendations found for your combined genres.")
        except Exception as e:
            print(f"An error occurred while searching for combined genres: {e}")
