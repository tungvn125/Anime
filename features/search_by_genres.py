import requests

def fetch_anime_by_genres(genres=[], max_results=10):
  url = "https://graphql.anilist.co"

  # GraphQL query: search anime by multiple genres
  query = """
  query ($genres: [String], $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
      media(genre_in: $genres, type: ANIME, sort: POPULARITY_DESC) {
        id
        title {
          romaji
          english
        }
        genres
        averageScore
      }
    }
  }
  """

  # Variables for the query
  variables = {
      "genres": genres,  # You can add more genres here
      "page": 1,
      "perPage": max_results
  }

  # Send request
  response = requests.post(url, json={"query": query, "variables": variables})
  data = response.json()

  # Print results
  print(f"\n------Anime Recommendations for {genres}------")
  for anime in data["data"]["Page"]["media"]:
      print(f"{anime['title']['romaji']} ({anime['title']['english']})")
      print(f"  + Genres: {', '.join(anime['genres'])}")
      print(f"  + Score: {anime['averageScore']}\n")
  return data["data"]["Page"]["media"]