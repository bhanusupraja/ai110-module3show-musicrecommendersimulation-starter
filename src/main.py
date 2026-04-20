"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Alex's taste profile: energetic, feel-good, non-acoustic
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "acousticness": 0.10,
        "tempo_bpm": 120,
        "valence": 0.80,
        "danceability": 0.85,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  >>  Top 5 Recommendations for Alex")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"     Score: {score:.2f} / 4.00")
        print(f"     Why:   {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
