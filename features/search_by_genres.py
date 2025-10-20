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

  return data["data"]["Page"]["media"]
def collect_genres_from_anime(anime=""):
    url = "https://graphql.anilist.co"

    query = """
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        genres
      }
    }
    """

    variables = {
        "search": anime
    }

    response = requests.post(url, json={"query": query, "variables": variables})
    data = response.json()

    if "data" in data and "Media" in data["data"]:
        genres = data["data"]["Media"]["genres"]
        return genres
    else:
        print(f"No genres found for anime: {anime}")
        return []