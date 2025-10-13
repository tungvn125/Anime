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
from watch_list import get_watchlist, save_watchlist

# Định nghĩa các hàm công cụ

get_user_like_genre_func = {
    "name": "get_user_like_genre",
    "description": "Lấy thể loại anime mà người dùng thích.",
    "parameters": {
        "type": "object",
        "properties": {
            "genres": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Danh sách thể loại mà người dùng thích."
            }
        },
        "required": ["genres"]
    }
}

add_to_watchlist_declaration = {
    "name": "add_to_watchlist_func",
    "description": "Thêm một anime vào danh sách xem.",
    "parameters": {
        "type": "object",
        "properties": {
            "anime_title": {
                "type": "string",
                "description": "Tiêu đề của anime cần thêm vào danh sách xem."
            }
        },
        "required": ["anime_title"]
    }
}

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
    """Bắt đầu một phiên trò chuyện với trợ lý anime được hỗ trợ bởi Gemini."""
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Hãy tạo một tệp .env và thêm GEMINI_API_KEY của cậu vào đó nhé.")
            return

        genai.configure(api_key=api_key)

        # Định nghĩa các công cụ
        tools = [
            types.Tool(function_declarations=[get_user_like_genre_func]),
            types.Tool(function_declarations=[add_to_watchlist_declaration])
        ]

        # Khởi tạo mô hình
        model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite", tools=tools)

        # Mở "cuốn nhật ký hành trình" (lịch sử trò chuyện)
        initial_history_from_file = []
        try:
            with open("history.json", 'r', encoding='utf-8') as f:
                loaded_history = json.load(f)
                # Chuyển đổi lịch sử đã tải về sang định dạng Message
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

        print("Trợ lý anime đã sẵn sàng. Cậu có thể bắt đầu trò chuyện (gõ 'quit' để kết thúc).")

        # Lời chào đầu tiên nếu là một cuộc hành trình mới
        if not initial_history_from_file:
            initial_prompt = (
                "Bạn là một trợ lý anime. Bạn có thể giúp user nhiều việc "
                "như thêm anime vào danh sách xem, tìm kiếm và gợi ý anime dựa trên sở thích. "
                "Để bắt đầu, hãy hỏi user thích những thể loại anime nào không?"
            )
            # Khởi tạo chat mà không có lịch sử, sau đó gửi prompt ban đầu
            chat = model.start_chat()
            response = chat.send_message(initial_prompt)
            print(f"Trợ lý: {response.text}")
            # Lịch sử được chat quản lý tự động
        else:
            # Khởi tạo chat với lịch sử đã tải
            chat = model.start_chat(history=initial_history_from_file)
            # Nếu có lịch sử, in ra tin nhắn cuối cùng để người dùng biết đã đến đâu
            if chat.history:
                last_message = chat.history[-1]
                if last_message.role == 'model' and last_message.parts:
                    print(f"Trợ lý (tiếp tục): {last_message.parts[0].text}")
                elif last_message.role == 'user' and last_message.parts:
                     # Nếu tin nhắn cuối cùng là của người dùng, đợi mô hình phản hồi
                    response = chat.send_message("...") # Gửi một tin nhắn trống để kích hoạt phản hồi
                    print(f"Trợ lý (tiếp tục): {response.text}")


        while True:
            user_input = input("Bạn: ")
            if user_input.lower() == 'quit':
                print("Kết thúc cuộc trò chuyện. Hẹn gặp lại!")
                break

            response = chat.send_message(user_input)
            
            # Xử lý các lệnh gọi hàm nếu có
            try:
                # Kiểm tra function_call trong các phần của phản hồi
                function_call_handled = False
                for part in response.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        function_name = fc.name
                        try:
                            function_args = dict(fc.args) # Chuyển đổi args thành dict
                        except Exception as e:
                            print(f"Lỗi khi phân tích cú pháp args của function_call: {e}")
                            break
                        if function_name == "get_user_like_genre":
                            genres = function_args.get("genres", [])
                            result = save_user_like_genre(genres)
                            print(f"Trợ lý: {result}")
                            # Gửi kết quả của hàm trở lại mô hình
                            chat.send_message([{"function_response": {"name": "get_user_like_genre", "response": {"result": result}}}])
                            function_call_handled = True
                            # Sau khi gửi FunctionResponse, mô hình sẽ phản hồi lại, không in văn bản ngay lập tức
                            # Chúng ta sẽ chờ vòng lặp tiếp theo để mô hình phản hồi
                            break # Đã xử lý function_call, thoát vòng lặp parts
                        elif function_name == "add_to_watchlist_func":
                            anime_title = function_args.get("anime_title", "")
                            result = add_to_watchlist_func(anime_title)
                            print(f"Trợ lý: {result}")
                            # Gửi kết quả của hàm trở lại mô hình
                            chat.send_message(
                                types.FunctionResponse(name="add_to_watchlist_func", response={"result": result})
                            )
                            function_call_handled = True
                            break # Đã xử lý function_call, thoát vòng lặp parts
                        else:
                            print(f"Trợ lý đã gọi một hàm không xác định: {function_name}")
                            function_call_handled = True
                            break # Đã xử lý function_call, thoát vòng lặp parts

                # Nếu không có function_call nào được xử lý và có văn bản, in văn bản phản hồi của trợ lý
                if not function_call_handled and response.text:
                    print(f"Trợ lý: {response.text}")

            except Exception as e:
                print(f"Lỗi khi xử lý function_call hoặc phản hồi văn bản: {e}")
                if response.text: # In văn bản nếu có lỗi trong function_call
                    print(f"Trợ lý: {response.text}")

        # Ghi lại toàn bộ cuộc hành trình vào nhật ký trước khi tạm biệt
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
                    # Xử lý các loại phần khác nếu có
                    parts_list.append(str(part)) # Fallback để lưu trữ dưới dạng chuỗi
            serialized_history.append({"role": message.role, "parts": parts_list})

        with open("history.json", 'w', encoding='utf-8') as f:
            json.dump(serialized_history, f, ensure_ascii=False, indent=4)
            print("Lịch sử trò chuyện đã được lưu lại trong 'history.json'.")
    except Exception as e:
        print(f"Ôi, có một sự cố ma thuật đã xảy ra: {e}")

if __name__ == "__main__":
    chat_with_bot()