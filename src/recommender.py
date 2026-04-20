from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Scoring weights — Experiment: Weight Shift
#
# Original recipe:
#   genre=2.0, mood=1.0, energy=1.0  → max score 4.0
#
# Shifted recipe (active):
#   genre halved, energy doubled — tests sensitivity to over-prioritising genre
#   genre=1.0, mood=1.0, energy=2.0  → max score 4.0 (unchanged)
#
# Math check:
#   max = WEIGHTS["genre"]*1 + WEIGHTS["mood"]*1 + WEIGHTS["energy"]*1.0
#       = 1.0 + 1.0 + 2.0 = 4.0  ✓
WEIGHTS: Dict[str, float] = {
    "genre":  1.0,   # halved from 2.0
    "mood":   1.0,   # unchanged
    "energy": 2.0,   # doubled from 1.0
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialise the recommender with a catalog of Song objects."""
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Return a weighted score (0.0–4.0) for how well a song matches the user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += WEIGHTS["genre"]
        if song.mood == user.favorite_mood:
            score += WEIGHTS["mood"]
        score += (1.0 - abs(song.energy - user.target_energy)) * WEIGHTS["energy"]
        return round(score, 4)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song in the catalog and return the top k matches for the user."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended to the user."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches ({song.genre}) +{WEIGHTS['genre']:.1f}")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches ({song.mood}) +{WEIGHTS['mood']:.1f}")
        energy_pts = (1.0 - abs(song.energy - user.target_energy)) * WEIGHTS["energy"]
        reasons.append(f"energy {song.energy} vs target {user.target_energy} (+{energy_pts:.2f})")
        return " | ".join(reasons)

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song dict against user preferences and return (score, explanation)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += WEIGHTS["genre"]
        reasons.append(f"genre matches ({song['genre']}) +{WEIGHTS['genre']:.1f}")

    if song["mood"] == user_prefs["mood"]:
        score += WEIGHTS["mood"]
        reasons.append(f"mood matches ({song['mood']}) +{WEIGHTS['mood']:.1f}")

    energy_pts = (1.0 - abs(song["energy"] - user_prefs["energy"])) * WEIGHTS["energy"]
    score += energy_pts
    reasons.append(f"energy {song['energy']} vs target {user_prefs['energy']} (+{energy_pts:.2f})")

    return round(score, 4), " | ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with all numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
