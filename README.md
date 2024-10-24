# Search-Movie-Director

This repository contains a simple Flask web application that takes a movie title as input and returns the name of the director of the movie.

## Installation

To install the application, you will need to have Python installed on your machine. You can then install the required packages using pip:

`
pip install -r requirements.txt
`


## Usage

To run the application, navigate to the root of the repository and run:

`
python app.py
`

This will start the Flask development server, and you can access the application by navigating to `http://localhost:5000` in your web browser.

## API Endpoints

The application has two API endpoints:

* `/`: The home page of the application, which renders the `index.html` template.
* `/search`: A POST endpoint that takes a movie title as input and returns the name of the director of the movie.

## API Documentation

You can find more information about the API endpoints and how to use them in the `app.py` file.

## Templates

The application uses the following templates:

* `index.html`: The home page of the application, which contains a form to input a movie title.
* `results.html`: A template that displays the results of the movie search, including the director's name.

## Environment Variables

The application uses the following environment variables:

* `TMDB_API_KEY`: Your API key for The Movie Database (TMDB).
* `TMDB_BASE_URL`: The base URL for the TMDB API.

You can set these environment variables in a `.env` file in the root of your repository.

## Contributing

Pull requests are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

Note: You'll need to set up the environment variables in a `.env` file.