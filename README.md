# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Platforms like Spotify and YouTube mix two approaches. Collaborative filtering uses other users' behavior (likes, skips, playlists) to find songs that people with similar taste enjoyed. Content-based filtering uses song attributes (genre, mood, energy, tempo) to find songs similar to what you already like. My version is content-based, since I only have a song catalog and one user profile

**Song features:** genre, mood, energy (0.0 to 1.0), tempo_bpm

**UserProfile features:** favorite_genre, favorite_mood, target_energy

**Algorithm Recipe (scoring one song):**
- +2.0 points if the song's genre matches the user's favorite genre
- +1.0 point if the song's mood matches the user's favorite mood
- Energy similarity: `1.0 - abs(song_energy - target_energy)`, so songs closer to the target earn more points (max 1.0)

**Ranking rule:** Score every song in the CSV, sort from highest to lowest, and return the top K.

**Expected biases:** Genre is worth the most points, so the system may over-prioritize genre and bury great songs that match the user's mood and energy but have a different genre. It can also create a filter bubble by recommending the same kind of song over and over.
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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



