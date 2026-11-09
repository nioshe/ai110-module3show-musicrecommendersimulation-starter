"""CLI runner for the Music Recommender Simulation. Run: python -m src.main"""
from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "High-Energy Pop": {"genre": "pop", "mood": "euphoric", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial / edge cases
    "Conflict: sad but energy 0.9": {"genre": "blues", "mood": "sad", "energy": 0.9},
    "Unknown genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}


def show(name: str, prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    print(f"\n=== {name}: {prefs} ===")
    for i, (song, score, why) in enumerate(recommend_songs(prefs, songs, k, weights), 1):
        print(f"{i}. {song['title']} by {song['artist']} [{song['genre']}/{song['mood']}] - {score:.2f}")
        print(f"   Because: {why}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        show(name, prefs, songs)
    # Experiment: double energy, halve genre
    print("\n##### EXPERIMENT: energy x2, genre x0.5 #####")
    exp = {"genre": 1.0, "mood": 1.0, "energy": 2.0}
    for name in ("Default Pop/Happy", "Conflict: sad but energy 0.9"):
        show(name, PROFILES[name], songs, weights=exp)


if __name__ == "__main__":
    main()
