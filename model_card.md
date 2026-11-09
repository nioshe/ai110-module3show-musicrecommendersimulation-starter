# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
**VibeFinder 1.0**

## 2. Intended Use
Suggests the top 5 songs from a small catalog for one user taste profile (favorite genre, mood, target energy). It is for classroom exploration, not real users or real music apps. It assumes the user can name one genre, one mood, and one energy level.

**Not intended for:** real product recommendations, judging artists, or any decision that affects people.

## 3. How the Model Works
Every song gets points. A genre match gives 2 points. A mood match gives 1 point. Energy gives up to 1 point, more the closer the song is to what the user wants. The points are added up and the songs with the most points are shown, each with a short reason like "genre match (+2.0)". The scoring step judges one song; the ranking step sorts all songs by that score.

## 4. Data
20 songs in `data/songs.csv`: the 10 starter songs plus 10 I added (r&b, hip hop, country, metal, edm, classical, reggae, folk, blues). Each has genre, mood, energy, tempo, valence, danceability, acousticness. Missing: lyrics, language, era, popularity, and any real listener data. Most genres appear only once.

## 5. Strengths
Works well when the user's taste matches a well-covered group: Chill Lofi and Deep Intense Rock got exactly the songs I expected at #1. Reasons are easy to read, so it is clear why each song ranked where it did.

## 6. Limitations and Bias
The system over-values genre. In the Pop/Happy test, "Gym Hero" (pop, intense) ranked #2 only because it is pop and high energy, even though it is not happy. A genre match outweighs a mood match, so a great "happy" song from another genre can lose. "Indie pop" gets no credit for a "pop" fan, and with 20 songs most genres have one entry, so fans of rarer genres see the same few songs. A genre missing from the catalog (k-pop) earns no genre points at all.

## 7. Evaluation
Profiles tested: Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock, plus two edge cases (sad blues with energy 0.9, and unknown genre k-pop). Outputs are pasted in the README.

Comparisons:
- **Pop/Happy vs. High-Energy Pop:** both put pop songs on top, but High-Energy Pop pulls in the two EDM "euphoric" songs and a rock song, because it asks for 0.9 energy and a different mood.
- **Chill Lofi vs. Deep Intense Rock:** opposite ends. Lofi returns quiet songs (energy 0.28-0.42); rock returns loud ones (0.90+). That makes sense because the energy score pushes in opposite directions.
- **Pop/Happy vs. Chill Lofi:** almost no overlap, so the profile really changes the output.
- **Conflict (sad + 0.9 energy) vs. Deep Intense Rock:** the conflict profile gets one blues song at #1 (genre and mood match, wrong energy), then the same loud songs the rock fan gets. No "sad but loud" song exists in the catalog.
- **Unknown genre vs. Pop/Happy:** with no genre points, the k-pop user gets mood/energy matches only, so "indie pop" tops the list.

Surprise: "Gym Hero" keeps showing up for people who just want happy pop. In plain words: it is a pop song with very high energy, and every pop fan gets 2 free points for the label "pop" no matter how intense the song feels.

Experiment: doubling energy and halving genre pushed "Gym Hero" down and moved the indie-pop happy song up, which felt more accurate.

## 8. Future Work
- Treat related genres as partial matches ("indie pop" is close to "pop").
- Add valence, tempo and acousticness to the score, and allow several favorite moods.
- Add a diversity rule so the top 5 are not all one genre or artist.

## 9. Personal Reflection
(Draft written by the AI assistant; replace with your own words before submitting.)

Biggest learning moment: the weights are opinions. Changing genre from 2.0 to 1.0 changed who the system "thinks" the user is. AI tools helped draft the scoring rule and code quickly, but the math (max score stays 4.0 after the weight change) and the results still needed checking by running the profiles. What surprised me is that adding three numbers already feels like a real recommendation, especially with reasons attached. Next I would try collaborative signals, like what similar users skipped.
