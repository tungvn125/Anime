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
from features.watch_list import get_watchlist, save_watchlist
from features.watch_anime import watch_anime
from mal import AnimeSearch

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

        
def add_to_watchlist_func(anime_title):
    """Adds an anime to the watchlist."""
    # Validate input
    if not isinstance(anime_title, str):
        try:
            anime_title = str(anime_title)
        except Exception:
            return "Invalid anime title."

    title = anime_title.strip()
    if not title:
        return "Anime title is empty."

    # Load or initialize watchlist structure
    watchlist = get_watchlist() or {"watchlist": []}
    if not isinstance(watchlist, dict):
        watchlist = {"watchlist": []}
    if "watchlist" not in watchlist or not isinstance(watchlist["watchlist"], list):
        watchlist["watchlist"] = []

    # Check for duplicates (case-insensitive, trimmed)
    for anime in watchlist["watchlist"]:
        existing_title = ""
        if isinstance(anime, dict):
            existing_title = str(anime.get("title", "")).strip()
        else:
            existing_title = str(anime).strip()
        if existing_title.lower() == title.lower():
            return f"'{title}' is already in your watchlist."

    # Append and save
    watchlist["watchlist"].append({"title": title, "episodes_watched": 0})
    try:
        save_watchlist(watchlist)
    except Exception as e:
        return f"Failed to save watchlist: {e}"

    return f"Added '{title}' to your watchlist."

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
def chat_with_bot():
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
                "like adding anime to the watch list, searching and suggesting anime based on interests and automatically stop when user wants to quit. You can call functions to open an anime when the user requests it. "
                "To start, ask the user what types of anime they like?"
            )
            # Start chat without history, then send the initial prompt
            chat = model.start_chat()
            response = chat.send_message(initial_prompt)
            print(f"assistant: {response.text}")
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
                            chat.send_message([{"function_response": {"name": "get_user_like_genre", "response": {"result": result}}}])
                            function_call_handled = True
                            # After sending FunctionResponse, the model will respond; wait for next loop
                            break
                        elif function_name == "add_to_watchlist_func":
                            anime_title = function_args.get("anime_title", "")
                            result = add_to_watchlist_func(anime_title)
                            print(f"assistant: {result}")
                            # Send function result back to the model
                            chat.send_message([{"function_response": {"name": "add_to_watchlist_func", "response": {"result": result}}}])
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
                            chat.send_message([{"function_response": {"name": "watch_anime", "response": {"result": result}}}])
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