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
ylimitations under the License."""

from ranimegen.animegen import RandomAnime
import json
import time
generator = RandomAnime()


async def search_anime(genres: list):
    """Search for an anime by list.

    Args:
        name (str): The name of the anime to search for."""
    all_genre = generator.genres
    print(all_genre)
    #await time.sleep(4)
    for n in genres:
        n = n.lower()
        ##n = n.replace(" ", "_")
        print(n)
        if n not in all_genre:
            print(f"Genre '{n}' not found. Available genres: {', '.join(all_genre)}")
            raise ValueError(f"Genre '{n}' not found. Available genres: {', '.join(all_genre)}")
        else:
            genres = "".join(n)
            print(genres)
    myinfo = await generator.suggestanime(genre=genres)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(myinfo, f, ensure_ascii=False, indent=4)
    return myinfo
#test
#import asyncio
#if __name__ == "__main__":
#    genres = ["Demons", "Magic", "Romance"]
#    result = asyncio.run(search_anime(genres))
#    print(result)