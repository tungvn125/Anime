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

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from features.watch_list import get_watchlist, save_watchlist, add_to_watchlist_func
from features.watch_anime import watch_anime
from mal import AnimeSearch
from features.manga_manager import add_to_readlist, list_readlist, search_manga, recommend_manga
from features.genre_manager import add_genre, clear_genres, list_genres, remove_genre
from features.rcm_system import recommend_anime
from features.read_light_novel import read_light_novel
from features.search_anime import search_anime
from features.watch_list import list_watchlist, update_watchlist

# Define tool functions

get_user_like_genre_func = {
    "name": "get_user_like_genre",
    "description": "Get the anime genres the user likes.",
    "parameters": {
        "type": "object",
        "properties": {
            "genres": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of genres the user likes."
            }
        },
        "required": ["genres"]
    }
}

add_to_watchlist_declaration = {
    "name": "add_to_watchlist_func",
    "description": "Add an anime to the watchlist.",
    "parameters": {
        "type": "object",
        "properties": {
            "anime_title": {
                "type": "string",
                "description": "The title of the anime to add to the watchlist."
            }
        },
        "required": ["anime_title"]
    }
}
quit_func = {
    "name": "quit_chat",
    "description": "End the chat session with the anime assistant.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}
watch_anime_func = {
    "name": "watch_anime",
    "description": "Start watching an anime.",
    "parameters": {
        "type": "object",
        "properties": {
            "anime_title": {
                "type": "string",
                "description": "The title of the anime to watch."
            }
        },
        "required": ["anime_title"]
    }
}                
search_anime_declaration = {
    "name": "search_anime_feature",
    "description": "Search for an anime.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the anime to search for."
            }
        },
        "required": ["title"]
    }
}

read_light_novel_declaration = {
    "name": "read_light_novel_feature",
    "description": "Search for a light novel to read.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the light novel."
            }
        },
        "required": ["title"]
    }
}

list_genres_declaration = {
    "name": "list_genres",
    "description": "List the user's preferred anime genres.",
    "parameters": {"type": "object", "properties": {}}
}

remove_genre_declaration = {
    "name": "remove_genre",
    "description": "Remove a genre from the user's preferred anime genres.",
    "parameters": {"type": "object", "properties": {}}
}

add_genre_declaration = {
    "name": "add_genre",
    "description": "Add a genre to the user's preferred anime genres.",
    "parameters": {"type": "object", "properties": {}}
}

clear_genres_declaration = {
    "name": "clear_genres",
    "description": "Clear all of the user's preferred anime genres.",
    "parameters": {"type": "object", "properties": {}}
}

recommend_anime_declaration = {
    "name": "recommend_anime",
    "description": "Recommend anime to the user based on their preferences.",
    "parameters": {"type": "object", "properties": {}}
}

list_watchlist_declaration = {
    "name": "list_watchlist",
    "description": "List all anime in the user's watchlist.",
    "parameters": {"type": "object", "properties": {}}
}

update_watchlist_declaration = {
    "name": "update_watchlist",
    "description": "Update the number of episodes watched for an anime in the watchlist.",
    "parameters": {"type": "object", "properties": {}}
}

def search_anime_wrapper(title):
    import sys
    sys.argv = ["", ""] + title.split(" ")
    search_anime()
    return "Interactive anime search started."

def read_light_novel_wrapper(title):
    import sys
    sys.argv = ["", ""] + title.split(" ")
    read_light_novel()
    return f"Searching for light novel '{title}'."

def find_n_watch_anime(anime_title):
    """Find and open an anime to watch."""
    try:
        watch_anime(anime_title)
        return f"Opening anime '{anime_title}' to watch."
    except Exception as e:
        # If opening fails, try to search and fallback to the first result
        search = AnimeSearch(anime_title)
        if search.results:
            first_result = search.results[0]
            title = first_result.title
            print(f"Could not open '{anime_title}'. However, I found: {title}")
            watch_anime(title)
            return f"Opening anime '{title}' to watch."
        else:
            return f"Could not find anime '{anime_title}'."

        


def save_user_like_genre(genres):
    """Saves the user's liked genres to a JSON file."""
    
    # Load existing genres or create empty list
    try:
        with open("user_like_genre.json", 'r', encoding='utf-8') as f:
            existing_genres = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_genres = []

    # Convert new genres to strings and add only unique ones
    for g in genres:
        try:
            genre = str(g)
            if genre not in existing_genres:
                existing_genres.append(genre)
        except Exception:
            continue

    try:
        with open("user_like_genre.json", 'w', encoding='utf-8') as f:
            json.dump(existing_genres, f, indent=4, ensure_ascii=False)
        return "Your genre preferences have been saved."
    except Exception as e:
        print(f"Error saving genres: {e}")
        return f"Failed to save genre preferences: {e}"
def chat_with_bot(first_prompt: str = None):
    """Start a chat session with the anime assistant powered by Gemini."""
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Please create a .env file and add your GEMINI_API_KEY to it.")
            return

        genai.configure(api_key=api_key)

        # Define tools
        tools = [
            types.Tool(function_declarations=[get_user_like_genre_func]),
            types.Tool(function_declarations=[add_to_watchlist_declaration]),
            types.Tool(function_declarations=[quit_func]),
            types.Tool(function_declarations=[watch_anime_func])
        ]

        # Manga related function declarations for the model
        add_to_readlist_declaration = {
            "name": "add_to_readlist",
            "description": "Add a manga to the readlist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "manga_title": {"type": "string", "description": "Title of the manga to add."}
                },
                "required": ["manga_title"]
            }
        }
        list_readlist_declaration = {
            "name": "list_readlist",
            "description": "List items in the user's manga readlist.",
            "parameters": {"type": "object", "properties": {}}
        }
        search_manga_declaration = {
            "name": "search_manga",
            "description": "Search for a manga by title.",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        }
        recommend_manga_declaration = {
            "name": "recommend_manga",
            "description": "Recommend manga based on a keyword or preferences. ",
            "parameters": {"type": "object", "properties": {"keyword": {"type": "string"}}}
        }

        # add manga tools to toolset
        tools.extend([
            types.Tool(function_declarations=[add_to_readlist_declaration]),
            types.Tool(function_declarations=[list_readlist_declaration]),
            types.Tool(function_declarations=[search_manga_declaration]),
            types.Tool(function_declarations=[recommend_manga_declaration]),
            types.Tool(function_declarations=[search_anime_declaration]),
            types.Tool(function_declarations=[read_light_novel_declaration]),
            types.Tool(function_declarations=[list_genres_declaration]),
            types.Tool(function_declarations=[remove_genre_declaration]),
            types.Tool(function_declarations=[add_genre_declaration]),
            types.Tool(function_declarations=[clear_genres_declaration]),
            types.Tool(function_declarations=[recommend_anime_declaration]),
            types.Tool(function_declarations=[list_watchlist_declaration]),
            types.Tool(function_declarations=[update_watchlist_declaration]),
        ])

        # Initialize model
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite", tools=tools)

        # Open chat history file
        initial_history_from_file = []
        try:
            with open("history.json", 'r', encoding='utf-8') as f:
                loaded_history = json.load(f)
                # Convert loaded history to Message format
                for item in loaded_history:
                    role = item['role']
                    parts = []
                    for part_data in item['parts']:
                        if isinstance(part_data, str):
                            parts.append(part_data)
                        elif isinstance(part_data, dict):
                            if 'function_call' in part_data:
                                fc_data = part_data['function_call']
                                try:
                                    parts.append(types.FunctionCall(name=fc_data['name'], args=fc_data['args']))
                                except Exception as e:
                                    print(f"Error loading FunctionCall from history: {e}")
                                    continue
                            elif 'function_response' in part_data:
                                fr_data = part_data['function_response']
                                parts.append(types.FunctionResponse(name=fr_data['name'], response=fr_data['response']))
                    initial_history_from_file.append(types.Message(role=role, parts=parts))

        except (FileNotFoundError, json.JSONDecodeError):
            initial_history_from_file = []

        print("Anime assistant is ready. You can start chatting.")

        
        if not initial_history_from_file:
            initial_prompt = (
                "You are an anime assistant. You can help users with many things"
                "like adding anime to the watch list, searching and suggesting anime based on interests and automatically stop when user wants to quit. You can call functions to open an anime when the user requests it. " \
                "dont answer after calling a function, these functions will handle the user requests. "
                "To start, ask the user what types of anime they like?"
            )
            # Start chat without history, then send the initial prompt
            chat = model.start_chat()
            response = chat.send_message(initial_prompt)
            print(f"assistant: {response.text}")
            # first prompt handled here
            if first_prompt:
                response = chat.send_message(first_prompt)
                print(f"assistant: {response.text}")
            else:
                # No first prompt, continue as normal
                pass
            # Chat manages its own history
        else:
            # Start chat with loaded history
            chat = model.start_chat(history=initial_history_from_file)
            # If there is history, print the last message so the user knows the state
            if chat.history:
                last_message = chat.history[-1]
                if last_message.role == 'model' and last_message.parts:
                    print(f"assistant (continuing): {last_message.parts[0].text}")
                elif last_message.role == 'user' and last_message.parts:
                     # If the last message is from the user, wait for model response
                    response = chat.send_message("...") # Send an empty message to trigger a response
                    print(f"assistant (continuing): {response.text}")
            # handle first prompt if provided
            if first_prompt:
                response = chat.send_message(first_prompt)
                print(f"assistant: {response.text}")
            else:
                # No first prompt, continue as normal
                pass
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Ending the chat. Goodbye!")
                break

            response = chat.send_message(user_input)
            
            # Handle function calls if present
            try:
                # Check for function_call in response parts
                function_call_handled = False
                for part in response.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        function_name = fc.name
                        try:
                            function_args = dict(fc.args) # Convert args to dict
                        except Exception as e:
                            print(f"Error parsing function_call args: {e}")
                            break
                        if function_name == "get_user_like_genre":
                            genres = function_args.get("genres", [])
                            result = save_user_like_genre(genres)
                            print(f"assistant: {result}")
                            # Send function result back to the model
                            follow = chat.send_message([{"function_response": {"name": "get_user_like_genre", "response": {"result": result}}}])
                            # Print the model's follow-up response immediately if present
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "add_to_watchlist_func":
                            anime_title = function_args.get("anime_title", "")
                            result = add_to_watchlist_func(anime_title)
                            print(f"assistant: {result}")
                            # Send function result back to the model
                            follow = chat.send_message([{"function_response": {"name": "add_to_watchlist_func", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "quit_chat":
                            print("Assistant: Ending the chat per your request. Goodbye!")
                            chat.send_message([{"function_response": {"name": "quit_chat", "response": {"result": "Chat ended by user request."}}}])
                            function_call_handled = True
                            return
                        elif function_name == "watch_anime":
                            anime_title = function_args.get("anime_title", "")
                            result = find_n_watch_anime(anime_title)
                            print(f"assistant: {result}")
                            # Send function result back to the model
                            follow = chat.send_message([{"function_response": {"name": "watch_anime", "response": {"result": "Watch anime sucsesful"}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "add_to_readlist":
                            manga_title = function_args.get("manga_title", "")
                            result = add_to_readlist(manga_title)
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "add_to_readlist", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "list_readlist":
                            # Execute list and send an empty response back
                            list_readlist()
                            follow = chat.send_message([{"function_response": {"name": "list_readlist", "response": {"result": "Listed readlist."}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "search_manga":
                            query = function_args.get("query", "")
                            # search_manga interacts with user; if a query provided, run search flow
                            if query:
                                # We'll call the simple search flow by opening the interactive search
                                print("Running interactive manga search...")
                                search_manga()
                                follow = chat.send_message([{"function_response": {"name": "search_manga", "response": {"result": "Search completed."}}}])
                                if getattr(follow, 'text', None):
                                    print(f"assistant: {follow.text}")
                            else:
                                search_manga()
                            function_call_handled = True
                            break
                        elif function_name == "recommend_manga":
                            keyword = function_args.get("keyword", "")
                            if keyword:
                                print(f"Finding manga recommendations for: {keyword}")
                            recommend_manga()
                            follow = chat.send_message([{"function_response": {"name": "recommend_manga", "response": {"result": "Recommendations displayed."}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "search_anime_feature":
                            title = function_args.get("title", "")
                            result = search_anime_wrapper(title)
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "search_anime_feature", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "read_light_novel_feature":
                            title = function_args.get("title", "")
                            result = read_light_novel_wrapper(title)
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "read_light_novel_feature", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "list_genres":
                            list_genres()
                            result = "Listed user's preferred genres."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "list_genres", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "remove_genre":
                            remove_genre()
                            result = "Interactive genre removal started."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "remove_genre", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "add_genre":
                            add_genre()
                            result = "Interactive genre adding started."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "add_genre", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "clear_genres":
                            clear_genres()
                            result = "Cleared all preferred genres."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "clear_genres", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "recommend_anime":
                            recommend_anime()
                            result = "Anime recommendation process started."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "recommend_anime", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "list_watchlist":
                            list_watchlist()
                            result = "Listed anime in watchlist."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "list_watchlist", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        elif function_name == "update_watchlist":
                            update_watchlist()
                            result = "Interactive watchlist update process started."
                            print(f"assistant: {result}")
                            follow = chat.send_message([{"function_response": {"name": "update_watchlist", "response": {"result": result}}}])
                            if getattr(follow, 'text', None):
                                print(f"assistant: {follow.text}")
                            function_call_handled = True
                            break
                        else:
                            print(f"assistant called an unknown function: {function_name}")
                            function_call_handled = True
                            break

                # If no function call was handled and there is text, print assistant text
                if not function_call_handled and response.text:
                    print(f"assistant: {response.text}")

            except Exception as e:
                print(f"Error handling function_call or text response: {e}")
                if response.text: # Print text if there was an error in function_call handling
                    print(f"assistant: {response.text}")

        # Save full conversation history before exiting
        final_history = chat.history
        serialized_history = []
        for message in final_history:
            parts_list = []
            for part in message.parts:
                if isinstance(part, str):
                    parts_list.append(part)
                
                #elif isinstance(part, types.FunctionCalled):
                #    parts_list.append({"function_call": {"name": part.name, "args": dict(part.args)}})
                #
                #elif isinstance(part, types.FunctionResponse):
                #    parts_list.append({"function_response": {"name": part.name, "response": part.response}})
                else:
                    # Handle other part types if present
                    parts_list.append(str(part)) # Fallback to store as string
            serialized_history.append({"role": message.role, "parts": parts_list})

        with open("history.json", 'w', encoding='utf-8') as f:
            json.dump(serialized_history, f, ensure_ascii=False, indent=4)
            print("Chat history saved to 'history.json'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    chat_with_bot()