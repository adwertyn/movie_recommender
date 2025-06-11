# movie_api.py

import requests
import random
from config import TMDB_API_KEY

main_url = "https://api.themoviedb.org/3"

genre_map = {
    'action': 28,
    'comedy': 35,
    'drama': 18,
    'history': 36,
    'horror': 27,
    'romance': 10749,
    'sci-fi': 878,
}

def get_movie_recommendation(genre: str):
    genre_id = genre_map.get(genre.lower())
    if not genre_id:
        return None, None

    url = f"{main_url}/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}"
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get('results', [])
        if movies:
            movie = random.choice(movies)
            title = movie.get('title', 'Unknown Title')
            rating = movie.get('vote_average', 'N/A')
            overview = movie.get('overview', 'No description available.')
            poster_path = movie.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            text = (
                f"🎬 *{title}*\n"
                f"⭐ Rating: {rating}\n\n"
                f"📝 {overview}"
            )
            return text, poster_url
        else:
            return "No movies found for this genre.", None
    else:
        return "Failed to get data from the movie API.", None
