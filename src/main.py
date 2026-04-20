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


# ---------------------------------------------------------------------------
# Standard profiles
# ---------------------------------------------------------------------------

PROFILES = {
    # Profile 1: High-Energy Pop
    # Expects: Sunrise City, Gym Hero at the top
    "High-Energy Pop (Alex)": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
    },

    # Profile 2: Chill Lofi
    # Expects: Midnight Coding, Library Rain, Focus Flow at the top
    "Chill Lofi (Sam)": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
    },

    # Profile 3: Deep Intense Rock
    # Expects: Storm Runner first, then high-energy songs
    "Deep Intense Rock (Jordan)": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.91,
    },
}

# ---------------------------------------------------------------------------
# Adversarial / edge case profiles — designed to stress-test scoring logic
# ---------------------------------------------------------------------------

EDGE_CASES = {
    # Edge case 1: Conflicting preferences
    # High energy (0.9) but sad mood — tests whether energy and mood
    # can independently pull the score in different directions.
    # Reveals: system can recommend an "angry" high-energy song to a "sad" user.
    "Conflicting (high energy + melancholic)": {
        "genre": "blues",
        "mood": "melancholic",
        "energy": 0.9,
    },

    # Edge case 2: Genre that does not exist in the catalog
    # No song has genre="metal" — genre match never fires.
    # Reveals: scoring falls back entirely on mood + energy proximity.
    "Unknown Genre (metal)": {
        "genre": "metal",
        "mood": "intense",
        "energy": 0.95,
    },

    # Edge case 3: Perfectly average user
    # All values sit in the middle — no song will score badly or brilliantly.
    # Reveals: ties broken arbitrarily; ranking may feel random.
    "Average Everything": {
        "genre": "pop",
        "mood": "chill",
        "energy": 0.5,
    },

    # Edge case 4: Extreme energy mismatch
    # Wants classical/dreamy but with maximum energy.
    # Reveals: genre+mood match can still win even with terrible energy score.
    "Dreamy but max energy": {
        "genre": "classical",
        "mood": "dreamy",
        "energy": 1.0,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    """Print top 5 recommendations for a given profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("\n" + "=" * 55)
    print(f"  >>  {label}")
    print(f"       genre={user_prefs['genre']}  mood={user_prefs['mood']}  energy={user_prefs['energy']}")
    print("=" * 55)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  --  {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"     Score: {score:.2f} / 4.00")
        print(f"     Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n\n*** STANDARD PROFILES ***")
    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs)

    print("\n\n*** EDGE CASES & ADVERSARIAL PROFILES ***")
    for label, prefs in EDGE_CASES.items():
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()
