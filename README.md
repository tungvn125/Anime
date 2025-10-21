# Anime CLI

*For when you've finished Netflix and reality is just not cutting it.*

## Overview

Tired of endlessly scrolling for your next anime fix? Do you have more tabs open than you have friends? Let our Python-powered, AI-driven, coffee-brewing (okay, maybe not the coffee part... yet) toolkit do the heavy lifting. 

It's like having a personal anime butler, but without the fancy uniform and the risk of them judging your questionable life choices.

## Features

- **AI Chat Assistant**: Chat with our resident AI otaku. It's trained in the ancient art of recommending anime and might even develop a personality. It can add anime to your watchlist, find something to watch, or just keep you company on a lonely night. It's a better listener than your cat.
- **Anime Search**: Can't remember that one anime with the blue-haired guy who screams a lot? Our search is probably better than your memory.
- **Watch Anime**: Stream anime faster than you can say "Nani?!". Requires `ani-cli`, so don't forget to install it, or things will get awkward.
- **Watchlist Management(beta)**: A watchlist that's easier to manage than your real-life responsibilities. Add, list, and update with minimal effort.
- **Genre Management**: Tell us you like "Slice of Life" and "Mecha". We won't judge. Much. This helps the AI give you recommendations that are *chef's kiss*.
- **Anime Recommendations**: Our recommendation system is so good, you'll wonder if it's reading your mind. (It's not. Probably.)
- **Light Novel Search**: For when you want to be *that person* who says, "The book was better."
 - **Manga Manager**: New feature — search for manga, get simple recommendations, maintain a readlist (add/list).

## Installation

Ready to join the elite? Of course you are. Just follow these sacred instructions. It's less painful than a filler arc, we promise.

- **Requires**: Python 3.13, [ani-cli](https://github.com/pystardust/ani-cli)

```bash
# Clone this repository
git clone https://github.com/tungvn125/Anime.git

# Go into the project folder
cd Anime

# Install some packages
pip install -r requirements.txt
```

## Usage

Using this is easier than understanding the plot of *Evangelion*. Just tell the script what you want.

To see all the available command, run:
```bash
python main.py --help
```

Interactive TUI
-----------------

Run the program without arguments to open the interactive terminal UI inspired by gemini-cli. It includes shortcuts to all features (Chat, Search, Recommend, Watch, Read LN, Genre Manager, Watchlist, Manga Manager).

Example: run the TUI

```bash
python main.py
```

Manga Manager
-----------------

The new Manga Manager is accessible via the TUI. It provides:
- Search Manga: interactive search and quick actions (view on MAL, add to readlist)
- Recommend Manga: simple recommendations based on a keyword
- List Readlist: show items saved in `readlist.json`
- Add to Readlist: add a manga title directly

Chat Function Calls
---------------------

The AI chat assistant can now call functions for manga actions (add to readlist, list readlist, search, recommend). When the model requests a function call, the CLI executes it and sends the function result back to the model; the model's follow-up message is displayed immediately in the same request cycle.

## Commands

just run:
```bash
python main.py
```


## Contributing

Got ideas? Found a bug that's more annoying than an endless tutorial level? Don't just stand there, open a pull request! We welcome contributions more than a shonen protagonist welcomes a power-up.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the boring details.

## Links

- [Issues](https://github.com/tungvn125/Anime/issues) (Where dreams go to be debugged)

