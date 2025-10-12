import sys
import webbrowser
def read_light_novel():
    """Opens a web browser to search for a light novel."""
    if len(sys.argv) > 2:
        ln_title = ' '.join(sys.argv[2:])
        print(f"Searching for light novel '{ln_title}'...")
        query = f"{ln_title} light novel"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        print("Please provide a light novel title to read.")