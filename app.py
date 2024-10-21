"""
find_director_webapp

A Flask web application that takes a movie title as input and returns the
name of the director of the movie.

"""

import os
from functools import wraps

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_api_key_here")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def handle_api_errors(f):
    """Handle API errors for the decorated function.

    The function will catch any `requests.exceptions.RequestException` and return
    a JSON response with an appropriate error message and status code.

    If the exception has a response object, it will extract the status code
    and return a JSON response with a matching error message. The status code
    is used to determine the error message to return.

    If the exception does not have a response object, it will return a JSON
    response with a generic error message and a 503 status code.

    Args:
        f: The function to be decorated

    Returns:
        A decorated function that handles API errors
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            if not hasattr(e, "response") or e.response is None:
                return jsonify({"error": "Failed to fetch data from TMDB API"}), 503
            elif e.response.status_code == 401:
                return jsonify({"error": "Invalid API key"}), 401
            elif e.response.status_code == 429:
                return jsonify({"error": "Too many requests"}), 429
            else:
                return jsonify({"error": "Failed to fetch data from TMDB API"}), 503

    return decorated_function


@app.route("/")
def home():
    """
    The home page of the application.

    This route renders the "index.html" template, which contains the
    HTML structure and styles for the home page of the application.

    :return: The rendered "index.html" template
    """
    return render_template("index.html")


@app.route("/search", methods=["POST"])
@handle_api_errors
def search_movie():
    """
    Search for a movie by its name and return the director's information.

    This route handles POST requests to search for a movie by its name using
    The Movie Database (TMDB) API. It retrieves the director's information
    for the first movie found in the search results.

    The function expects a form data with the key "movie_name". If the movie
    name is not provided or if no movie is found, it returns an appropriate
    error message and status code. If the director information is not found
    for the movie, it also returns an error message.

    :return: A JSON response containing the movie's title, director's name,
             release date, and poster path if successful. Otherwise, a JSON
             response with an error message and status code.
    """
    movie_name = request.form.get("movie_name")
    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400

    # Search for the movie
    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_name, "language": "en-US"}

    response = requests.get(search_url, params=params, timeout=10)
    data = response.json()

    if not data.get("results"):
        return jsonify({"error": "No movies found"}), 404

    # Get first movie's details
    movie_id = data["results"][0]["id"]
    movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
    params = {
        "api_key": TMDB_API_KEY,
    }

    response = requests.get(movie_url, params=params, timeout=10)
    credits_data = response.json()

    # Find director
    director = next(
        (
            crew_member
            for crew_member in credits_data.get("crew", [])
            if crew_member["job"] == "Director"
        ),
        None,
    )

    if not director:
        return jsonify({"error": "Director information not found"}), 404

    return jsonify(
        {
            "movie_title": data["results"][0]["title"],
            "director_name": director["name"],
            "release_date": data["results"][0]["release_date"],
            "poster_path": f"https://image.tmdb.org/t/p/w500{data['results'][0]['poster_path']}",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
