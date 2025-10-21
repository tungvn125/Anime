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
import os
import subprocess
from simple_term_menu import TerminalMenu
from features.chat import chat_with_bot
from features.search_anime import search_anime
from features.rcm_system import recommend_anime
from features.watch_list import update_watchlist, list_watchlist
from features.watch_anime import watch_anime
from features.read_light_novel import read_light_novel
from features.chat import add_to_watchlist_func
from features.genre_manager import add_genre, remove_genre, list_genres, clear_genres
from features.manga_manager import search_manga, recommend_manga, list_readlist, add_to_readlist




def main():
    """
    Main function to handle command-line arguments.
    """

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "-s" or command == "--search":
            search_anime()
        elif command == "-rcm" or command == "--recommend":
            recommend_anime()
        elif command == "-a" or command == "--add":
            if len(sys.argv) > 2:
                anime_title = ' '.join(sys.argv[2:])
                print(add_to_watchlist_func(anime_title))
            else:
                print("Please provide an anime title to add.")
        elif command == "-u" or command == "--update":
            update_watchlist()
        elif command == "-l" or command == "--list" or command == "-ls":
            list_watchlist()
        elif command == "-c" or command == "--chat":
            chat_with_bot()
        elif command == "-w" or command == "--watch":
            # Ani-cli package check
            try:
                subprocess.run(["ani-cli", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Error: 'ani-cli' is not installed or not found in PATH. Please install it from:  https://github.com/pystardust/ani-cli")
            if len(sys.argv) > 2:
                watch_anime(' '.join(sys.argv[2:]))
            else:
                print("Please provide an anime title to watch.")
        elif command == "-r" or command == "--read":
            read_light_novel()
        elif command == "-g" or command == "--genre":
            choice = ["Add Genre", "Remove Genre", "List Genres", "Clear All Genres", "Exit"]
            terminal_menu = TerminalMenu(choice)
            choice_index = terminal_menu.show()
            print(f"You selected: {choice[choice_index]}")
            if choice[choice_index] == "Add Genre":
                add_genre()
            elif choice[choice_index] == "Remove Genre":
                remove_genre()
            elif choice[choice_index] == "List Genres":
                list_genres()
            elif choice[choice_index] == "Clear All Genres":
                run = True
                while run:
                    confirm_choice = input("Are you sure you want to clear all genres? (Y/n): ").strip().lower()
                    if confirm_choice == 'y' or confirm_choice == '':
                        clear_genres()
                        run = False
                    elif confirm_choice == 'n' or confirm_choice == 'no':
                        run = False
                    else:
                        print("Operation cancelled.")
                        
            elif choice[choice_index] == "Exit":
                return
        elif command == "-h" or command == "--help":
            print("usage: python main.py [command]")
            print("operations:")
            print("       -s, --search <anime>       Search for an anime")
            print("       -rcm, --recommend <anime>  Get anime recommendations")
            print("       -a, --add <anime>          Add an anime to your watchlist")
            print("       -u, --update <anime>       Update your watchlist(not working yet)")
            print("       -l, --list, -ls            List your watchlist")    
            print("       -c, --chat                 Chat with the bot")
            print("       -w, --watch <anime>        Watch an anime")
            print("       -r, --read <light novel>   Read a light novel")
            print("       -h, --help                 Show this help message\n")
            print("Example: python main.py -s Silent Witch")

        else:
            print(f"Unknown command: {command}")
    else:
        # Launch interactive TUI similar to gemini-cli
        menu_items = [
            "Chat with AI",
            "Search Anime",
            "Recommend Anime",
            "Watch Anime",
            "Read Light Novel",
            "Manage Genres",
            "Watchlist",
            "Manga Manager",
            "Exit"
        ]
        terminal_menu = TerminalMenu(menu_items, title="Anime CLI - TUI")
        while True:
            idx = terminal_menu.show()
            choice = menu_items[idx]
            if choice == "Chat with AI":
                chat_with_bot()
            elif choice == "Search Anime":
                search_anime()
            elif choice == "Recommend Anime":
                recommend_anime()
            elif choice == "Watch Anime":
                name = input("Enter anime title to watch: ")
                if name.strip():
                    watch_anime(name)
            elif choice == "Read Light Novel":
                read_light_novel()
            elif choice == "Manage Genres":
                g_choice = ["Add Genre", "Remove Genre", "List Genres", "Clear All Genres", "Back"]
                gmenu = TerminalMenu(g_choice)
                gi = gmenu.show()
                if g_choice[gi] == "Add Genre":
                    add_genre()
                elif g_choice[gi] == "Remove Genre":
                    remove_genre()
                elif g_choice[gi] == "List Genres":
                    list_genres()
                elif g_choice[gi] == "Clear All Genres":
                    confirm = input("Are you sure? (Y/n): ").strip().lower()
                    if confirm == 'y' or confirm == '':
                        clear_genres()
            elif choice == "Watchlist":
                wl_choice = ["List Watchlist", "Update Watchlist", "Back"]
                wlmenu = TerminalMenu(wl_choice)
                wi = wlmenu.show()
                if wl_choice[wi] == "List Watchlist":
                    list_watchlist()
                elif wl_choice[wi] == "Update Watchlist":
                    update_watchlist()
            elif choice == "Manga Manager":
                m_choice = ["Search Manga", "Recommend Manga", "List Readlist", "Add to Readlist", "Back"]
                mmenu = TerminalMenu(m_choice)
                mi = mmenu.show()
                if m_choice[mi] == "Search Manga":
                    search_manga()
                elif m_choice[mi] == "Recommend Manga":
                    recommend_manga()
                elif m_choice[mi] == "List Readlist":
                    list_readlist()
                elif m_choice[mi] == "Add to Readlist":
                    title = input("Enter manga title to add: ")
                    if title.strip():
                        print(add_to_readlist(title))
            elif choice == "Exit":
                print("Goodbye!")
                return

if __name__ == "__main__":
    main()
