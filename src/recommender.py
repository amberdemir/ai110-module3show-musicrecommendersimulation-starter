from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        self.songs = songs

    def _prefs(self, user: UserProfile) -> Dict:
        return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, vars(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(self._prefs(user), vars(song))
        return ", ".join(reasons) if reasons else "no strong match"

NUMERIC_COLUMNS = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting id and numeric columns to numbers."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for col in NUMERIC_COLUMNS:
                row[col] = float(row[col])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")
    energy_closeness = 1.0 - abs(song["energy"] - user_prefs["energy"])
    score += energy_closeness
    reasons.append(f"energy closeness (+{energy_closeness:.2f})")
    return score, reasons

def catalog_warnings(user_prefs: Dict, songs: List[Dict]) -> List[str]:
    """Return warnings for a preferred genre or mood that no song in the catalog has."""
    warnings = []
    for key in ("genre", "mood"):
        if not any(song[key] == user_prefs[key] for song in songs):
            warnings.append(f'Warning: no songs in the catalog have {key} "{user_prefs[key]}".')
    return warnings

def is_weak_match(user_prefs: Dict, song: Dict) -> bool:
    """Return True if a song matches neither the user's genre nor mood."""
    return song["genre"] != user_prefs["genre"] and song["mood"] != user_prefs["mood"]

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs and return the top k as (song, score, reasons) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
