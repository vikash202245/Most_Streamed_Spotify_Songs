import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Load the dataset
file_path = 'spotify-2023.csv'  # Replace with the actual path to your CSV file
spotify_data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Set up Spotify API credentials
client_id = '7dd243918eaa41fe82b0b2043ac90a6c'  # Replace with your actual Client ID
client_secret = '24a6675479f84885ba031447c1cd1134'  # Replace with your actual Client Secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover URL
def get_album_cover_url(track_name, artist_name):
    try:
        query = f'track:{track_name} artist:{artist_name}'
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            return tracks[0]['album']['images'][0]['url']
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {track_name} by {artist_name}: {e}")
        return None

# Add a new column for the URLs
spotify_data['cover_url'] = spotify_data.apply(lambda row: get_album_cover_url(row['track_name'], row['artist(s)_name']), axis=1)

# Save the modified DataFrame back to a CSV file
output_file_path = 'spotify-2023-with-urls.csv'  # Replace with the desired output path
spotify_data.to_csv(output_file_path, index=False)

print("URLs added and saved to new CSV file.")
