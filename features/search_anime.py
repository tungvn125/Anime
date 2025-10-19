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


import sys
import time
import webbrowser
from mal import AnimeSearch
from simple_term_menu import TerminalMenu
from features.watch_anime import watch_anime
from features.chat import add_to_watchlist_func


def search_anime():
    """
    This function takes an anime title as a command-line argument, searches for it using the MyAnimeList API,
    and displays the search results.
    """
    try:
        # Get the anime title from the command-line arguments
        if len(sys.argv) > 2:
            anime_title = ' '.join(sys.argv[2:])
        else:
            print("Please provide an anime title to search.")
            return

        # Search for the anime
        search = AnimeSearch(anime_title)

        # Display the search results
        c = 0
        try:
            max_results = int(input("Enter the number of results to display: "))
        except ValueError:
            print("Invalid input. Displaying 10 results by default.")
            max_results = 10
        options = []
        if search.results:
            print(f"Search results for \"{anime_title}\":")
            for result in search.results:
                #print(f"{c}. {result.title} (Score: {result.score})")
                options.append(f"{result.title} (Score: {result.score})")
                c += 1
                if c >= max_results:
                    break
            options.append("(exit)")
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            print(f"You selected: {options[menu_entry_index]}")
            if options[menu_entry_index] != "(exit)":
                choice = ["watch", "view on web", "add to watchlist", "(exit)"]
                terminal_menu = TerminalMenu(choice)
                choice_index = terminal_menu.show()
                print(f"You selected: {choice[choice_index]}")
                if choice[choice_index] == "view on web":
                    query = options[menu_entry_index].split(" (Score:")[0]
                    url = f"https://myanimelist.net/anime.php?q={query.replace(' ', '+')}"
                    webbrowser.open(url)
                elif choice[choice_index] == "watch":
                    print("enjoy your anime!")
                    time.sleep(1)
                    watch_anime(options[menu_entry_index].split(" (Score:")[0])
                elif choice[choice_index] == "add to watchlist":
                    add_to_watchlist_func(options[menu_entry_index].split(" (Score:")[0])
                elif choice[choice_index] == "(exit)":
                    pass
            else:
                pass
            #print("(exit)")
            
        else:
            print(f"No results found for \"{anime_title}\".")

    except Exception as e:
        print(f"An error occurred: {e}")
