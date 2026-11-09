import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Algorithm Recipe: points available per feature.
DEFAULT_WEIGHTS: Dict[str, float] = {"genre": 2.0, "mood": 1.0, "energy": 1.0}


@dataclass
class Song:
    """A song and its catalog attributes."""
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
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file, converting numeric columns to int/float."""
    int_cols, float_cols = {"id"}, {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for c in int_cols:
                row[c] = int(row[c])
            for c in float_cols:
                row[c] = float(row[c])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, human-readable reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score, reasons = 0.0, []
    if song["genre"].lower() == str(user_prefs.get("genre", "")).lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")
    if song["mood"].lower() == str(user_prefs.get("mood", "")).lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")
    if "energy" in user_prefs:
        # Closeness, not "higher is better": 1.0 at an exact match, 0.0 at the max gap.
        pts = w["energy"] * (1.0 - abs(song["energy"] - user_prefs["energy"]))
        score += pts
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{pts:.2f})")
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    weights: Optional[Dict[str, float]] = None) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves `songs` untouched (list.sort() would mutate in place).
    return sorted(scored, key=lambda t: t[1], reverse=True)[:k]


class Recommender:
    """OOP wrapper around the same scoring logic, using Song/UserProfile objects."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score, reasons = score_song(self._prefs(user), song.__dict__)
        acoustic = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness
        score += 0.5 * acoustic
        reasons.append(f"acoustic fit (+{0.5 * acoustic:.2f})")
        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, best first."""
        return sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one line why a song scored the way it did."""
        score, reasons = self._score(user, song)
        return f"{song.title}: {score:.2f} total ({'; '.join(reasons)})"
