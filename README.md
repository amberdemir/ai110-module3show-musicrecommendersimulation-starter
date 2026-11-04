# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This is a content-based music recommender. It scores every song in a small CSV catalog against a user's favorite genre, mood, and target energy, then ranks the songs and explains each recommendation with the points behind it. It runs from the command line
---

## How The System Works


Platforms like Spotify and YouTube mix two approaches. Collaborative filtering uses other users' behavior (likes, skips, playlists) to find songs that people with similar taste enjoyed. Content-based filtering uses song attributes (genre, mood, energy, tempo) to find songs similar to what you already like. My version is content-based, since I only have a song catalog and one user profile

**Song features:** genre, mood, energy (0.0 to 1.0), tempo_bpm

**UserProfile features:** genre, mood, energy

**Algorithm Recipe (scoring one song):**
- +2.0 points if the song's genre matches the user's favorite genre
- +1.0 point if the song's mood matches the user's favorite mood
- Energy similarity: `1.0 - abs(song_energy - target_energy)`, so songs closer to the target earn more points (max 1.0)

**Ranking rule:** Score every song in the CSV, sort from highest to lowest, and return the top K.

**Expected biases:** Genre is worth the most points, so the system may over-prioritize genre and bury great songs that match the user's mood and energy but have a different genre. It can also create a filter bubble by recommending the same kind of song over and over.



## Algorithm Summary
The recommender is content-based. It scores every song in the catalog
against the user's taste profile. A genre match adds 2.0 points, a mood
match adds 1.0 point, and energy adds up to 1.0 point depending on how
close the song's energy is to the user's target (closer = more points).
Each song ends up with a total score and a list of reasons explaining
where the points came from. Songs are then sorted from highest to
lowest score, and the top 5 are shown to the user.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 10

Top recommendations:

1. Sunrise City
   Score: 3.98
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.98)

2. Gym Hero
   Score: 2.87
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.87)

3. Rooftop Lights
   Score: 1.96
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.96)

4. Night Drive Loop
   Score: 0.95
   Reasons:
     - energy closeness (+0.95)

5. Storm Runner
   Score: 0.89
   Reasons:
     - energy closeness (+0.89)
```

---

## Experiments You Tried

- **Five test profiles.** I ran the recommender for five listeners: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicted (pop, sad, energy 0.9), and Unknown Genre (k-pop). The last two were designed to trick the scoring.
- **Weight shift.** I halved the genre points (+2.0 to +1.0) and doubled the energy points (up to +2.0). The top 5 stayed exactly the same for every profile. Only the scores changed, and the gaps between songs got smaller. This happened because genre and energy line up in such a tiny catalog: the pop songs are energetic and the lofi songs are calm. I kept the original weights.
- **Honesty checks.** I added a warning when a user's genre or mood isn't in the catalog at all. I also added a "Weak match" label for songs that only matched on energy.

---

## Limitations and Risks

- The catalog has only 10 songs, and only one of them is rock.
- Genre must match exactly, so "indie pop" never counts as "pop".
- Every song earns some energy points, so the top 5 is always full, even when most picks are weak matches.
- It ignores lyrics, language, artist, and listening history.

---

## Reflection

This project showed me that a recommender turns data into a prediction by adding up points. Each song's score is just its genre points, plus its mood points, plus how close its energy is to what the user wants. The highest totals become the recommendations. Showing the reasons next to each song made this easy to see, because every point can be traced back to where it came from.

It also showed me where bias can sneak in. Genre is worth the most points, so a song in the "right" genre can beat a better-fitting song from a different genre. That can favor popular genres and bury good songs from others. A tiny catalog makes this worse: with only one rock song, a rock fan mostly gets songs that just happen to have the right energy. For more detail, see the [Model Card](model_card.md).
