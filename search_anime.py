import sys
import time
import webbrowser
from mal import AnimeSearch
from simple_term_menu import TerminalMenu
from watch_anime import watch_anime


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
        options = []
        if search.results:
            print(f"Search results for \"{anime_title}\":")
            for result in search.results:
                #print(f"{c}. {result.title} (Score: {result.score})")
                options.append(f"{result.title} (Score: {result.score})")
                c += 1
                if c >= 5:
                    break
            options.append("(exit)")
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            print(f"You selected: {options[menu_entry_index]}")
            if options[menu_entry_index] != "(exit)":
                choice = ["watch", "view on web"]
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
            else:
                pass
            #print("(exit)")
            
        else:
            print(f"No results found for \"{anime_title}\".")

    except Exception as e:
        print(f"An error occurred: {e}")
