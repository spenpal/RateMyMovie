import csv
import os

import requests
from dotenv import load_dotenv


def get_movie_info(detail, data):
    match detail:
        case "year":
            year = data.get("Year", "")
            return year if year != "N/A" else ""
        case "certificate":
            certificate = data.get("Rated", "")
            return certificate if certificate != "N/A" else ""
        case "runtime":
            runtime = data.get("Runtime", "")
            return runtime if runtime != "N/A" else ""
        case "genre":
            genres = data.get("Genre", "")
            return genres if genres != "N/A" else ""
        case "director":
            directors = data.get("Director", "")
            return directors if directors != "N/A" else ""
        case "star":
            stars = data.get("Actors", "")
            return stars if stars != "N/A" else ""
        case "rating":
            rating = data.get("imdbRating", "")
            return rating if rating != "N/A" else ""


# Get API key
load_dotenv("../.env")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Open the input CSV file
with open("../datasets/filtered_action_movie_data.csv", "r") as input_file:
    # Open the output CSV file
    with open(
        "../datasets/filled_action_movie_data.csv", "w", newline=""
    ) as output_file:
        reader = csv.reader(input_file)  # Create a CSV reader object
        header = next(reader)  # Read the header row
        header_dict = {k: v for v, k in enumerate(header)}
        writer = csv.writer(output_file)  # Create a CSV writer object
        writer.writerow(header)  # Write the header row

        # Loop through the rows in the input file
        for i, row in enumerate(reader, start=1):
            imdb_id = row[header_dict["movie_id"]]  # Get the IMDb ID from the row

            response = requests.get(
                f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
            )
            data = response.json()

            if data["Response"] == "False":
                print(f"Skipped Row #{i}. No movie found.")
                continue
            if "English" not in data["Language"]:
                print(
                    f"Skipped Row #{i}. Not an English movie. [Language(s): {data['Language']}] | IMDB id: {imdb_id}"
                )
                continue

            # Check for missing values in the row
            missing_vals_idx = [idx for idx, val in enumerate(row) if not val]
            if missing_vals_idx:
                for missing_val_idx in missing_vals_idx:
                    row[missing_val_idx] = get_movie_info(header[missing_val_idx], data)
                writer.writerow(row)  # Write the row to the output file
                print(f"Filled in Row #{i}!")
            else:
                writer.writerow(row)  # Write the row to the output file
                print(f"Skipped Row #{i}. No missing values. :)")
