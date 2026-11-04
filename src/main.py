"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, catalog_warnings, is_weak_match


PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    # Edge case: high energy but a sad mood, which pull in opposite directions
    "Conflicted (High Energy + Sad)": {"genre": "pop", "mood": "sad", "energy": 0.9},
    # Edge case: a genre that doesn't exist in songs.csv
    "Unknown Genre (K-Pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        print(f"\n=== {profile_name} ===")
        print(f"Preferences: {user_prefs}")
        for warning in catalog_warnings(user_prefs, songs):
            print(warning)

        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\nTop recommendations:\n")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"     - {reason}")
            if is_weak_match(user_prefs, song):
                print("   Weak match: only energy lined up")
            print()

if __name__ == "__main__":
    main()
