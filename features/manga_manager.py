"""Manga manager feature: search, recommend, readlist management."""
import json
import webbrowser
from simple_term_menu import TerminalMenu
from mal import AnimeSearch

READLIST_FILE = "readlist.json"


def load_readlist():
    try:
        with open(READLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"readlist": []}


def save_readlist(readlist):
    with open(READLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(readlist, f, indent=4, ensure_ascii=False)


def list_readlist():
    readlist = load_readlist()
    if readlist.get("readlist"):
        print("Your manga readlist:")
        for item in readlist["readlist"]:
            print(f"- {item.get('title')} (Progress: {item.get('progress', '')})")
    else:
        print("Your readlist is empty.")


def add_to_readlist(manga_title):
    if not manga_title or not isinstance(manga_title, str):
        return "Invalid manga title."

    title = manga_title.strip()
    if not title:
        return "Manga title is empty."

    readlist = load_readlist()
    if "readlist" not in readlist or not isinstance(readlist["readlist"], list):
        readlist["readlist"] = []

    for item in readlist["readlist"]:
        existing = item.get("title", "")
        if existing.strip().lower() == title.lower():
            return f"'{title}' is already in your readlist."

    readlist["readlist"].append({"title": title, "progress": "0"})
    try:
        save_readlist(readlist)
    except Exception as e:
        return f"Failed to save readlist: {e}"

    return f"Added '{title}' to your readlist."


def search_manga():
    try:
        query = input("Enter manga title to search: ").strip()
        if not query:
            print("No query provided.")
            return

        # Reuse AnimeSearch for basic title search (works for manga in MAL wrapper)
        search = AnimeSearch(query)
        if not search.results:
            print(f"No results found for '{query}'.")
            return

        options = [f"{r.title} (Score: {getattr(r, 'score', 'N/A')})" for r in search.results]
        options.append("(exit)")
        menu = TerminalMenu(options)
        idx = menu.show()
        if options[idx] == "(exit)":
            return

        chosen = options[idx]
        choice = ["view on web", "add to readlist", "(exit)"]
        cmenu = TerminalMenu(choice)
        ci = cmenu.show()
        if choice[ci] == "view on web":
            title = chosen.split(" (Score:")[0]
            url = f"https://myanimelist.net/manga.php?q={title.replace(' ', '+')}"
            webbrowser.open(url)
        elif choice[ci] == "add to readlist":
            title = chosen.split(" (Score:")[0]
            print(add_to_readlist(title))
        else:
            return

    except Exception as e:
        print(f"An error occurred: {e}")


def recommend_manga():
    # Very simple recommend: suggest from user's readlist genres is not available, so suggest top results for 'manga'
    try:
        query = input("Enter a keyword or leave blank for popular manga: ").strip()
        search = AnimeSearch(query or "manga")
        if not search.results:
            print("No recommendations found.")
            return

        print("Recommendations:")
        for r in search.results[:10]:
            print(f"- {r.title} (Score: {getattr(r, 'score', 'N/A')})")

    except Exception as e:
        print(f"An error occurred while recommending manga: {e}")
