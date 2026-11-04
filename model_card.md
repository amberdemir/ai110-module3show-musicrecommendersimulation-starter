# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The catalog has only 10 songs, and only one of them is rock, so the "Deep Intense Rock" listener gets 3 weak matches in their top 5, songs that only share an energy level with what they asked for. Genres must match exactly, so a song labeled "indie pop" never counts as "pop", even though a pop fan would probably enjoy it. Because every song earns some points just for being close in energy, the top 5 is always full, even when few songs really fit. To make this honest instead of hidden, I added a warning when a user's genre or mood doesn't exist in the catalog at all (for example, no song has the mood "sad"), and a "Weak match: only energy lined up" label on any song that matched neither the genre nor the mood.

---

## 7. Evaluation  

### Profiles I tested

I ran the recommender for five listener profiles. Each profile has a favorite genre, a favorite mood, and a target energy level from 0 (very calm) to 1 (very intense).

| Profile | Genre | Mood | Energy | Why I picked it |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.9 | A typical upbeat pop fan |
| Chill Lofi | lofi | chill | 0.35 | A calm listener, the opposite of the pop fan |
| Deep Intense Rock | rock | intense | 0.95 | A genre with only one song in the catalog |
| Conflicted (High Energy + Sad) | pop | sad | 0.9 | Tricky: wants high energy but a sad mood, and no song is "sad" |
| Unknown Genre (K-Pop) | k-pop | happy | 0.7 | Tricky: asks for a genre that isn't in the catalog |

### What surprised me

- **Four of the five profiles got the same five songs, just in a different order.** Only five songs in the catalog have high energy (Sunrise City, Gym Hero, Storm Runner, Rooftop Lights, Night Drive Loop). Any profile that wants energetic music ends up choosing from that same small group. Only Chill Lofi got a different list.
- **"Gym Hero" keeps showing up for the happy pop listener.** It ranks #2 for High-Energy Pop even though its mood is "intense", not "happy". It gets 2 points for being pop, the biggest reward in the scoring, and its energy (0.93) is almost exactly the 0.9 the user asked for. Those two things together outweigh the 1 point it misses for mood. Only Sunrise City, which is pop *and* happy, beats it. In plain terms: the recommender cares more about genre than mood, so a pop workout song beats a happy song from another genre.
- **The tricky profiles still got a full top 5 without complaint**, until I added the warnings and weak-match labels described in Limitations and Bias.

### Comparing the profiles, pair by pair

- **High-Energy Pop vs. Chill Lofi:** The two lists share no songs. High-Energy Pop moves toward fast, energetic pop songs, while Chill Lofi moves toward slow, calm lofi songs. That makes sense because they want opposite genres *and* opposite energy levels.
- **High-Energy Pop vs. Deep Intense Rock:** The same five songs, reordered. Storm Runner jumps from #4 to #1 because it is the only rock song and its mood is "intense". Both listeners want high energy, so they draw from the same small group of energetic songs.
- **High-Energy Pop vs. Conflicted:** The same five songs, but Gym Hero moves up to #1 and Sunrise City drops to #2. No song is "sad", so nobody earns mood points, and the closest energy level decides. Gym Hero (0.93) is a little closer to 0.9 than Sunrise City (0.82). This shows the "sad" request was quietly ignored.
- **High-Energy Pop vs. Unknown Genre:** The same five songs, but Rooftop Lights moves up to #1 and Gym Hero falls to #5. No song is "k-pop", so nobody gets genre points. That leaves mood and energy: Rooftop Lights is happy and its energy (0.76) is close to the requested 0.7, while Gym Hero loses the genre points that were holding it up.
- **Chill Lofi vs. Deep Intense Rock:** No shared songs. They sit at opposite ends of the catalog: quiet, gentle lofi tracks versus loud, intense ones.
- **Chill Lofi vs. Conflicted:** No shared songs. Conflicted still asks for pop at 0.9 energy, so it pulls the same energetic songs as the pop listener, far from the calm lofi tracks.
- **Chill Lofi vs. Unknown Genre:** No shared songs. Unknown Genre wants happy songs at medium-high energy (0.7). The lofi songs are calm (energy around 0.35 to 0.42) and none of them is happy, so they score low.
- **Deep Intense Rock vs. Conflicted:** The same five songs. Storm Runner is #1 for the rock fan but only #3 for Conflicted, because it is rock, not pop. Gym Hero is #2 for the rock fan only because it is "intense" (a mood match), not because it is rock.
- **Deep Intense Rock vs. Unknown Genre:** The same five songs, ordered by different moods. The rock fan's "intense" mood lifts Gym Hero to #2, while the k-pop fan's "happy" mood puts Rooftop Lights and Sunrise City at the top.
- **Conflicted vs. Unknown Genre:** The same five songs. Each profile has one preference the catalog can't satisfy, so each falls back on its other two. Conflicted ranks by "is it pop?" plus energy, so the pop songs lead. Unknown Genre ranks by "is it happy?" plus energy, so the happy songs lead.

### Terminal output for each profile

These are the results of running `python -m src.main`.

**High-Energy Pop**

```
=== High-Energy Pop ===
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}

Top recommendations:

1. Sunrise City
   Score: 3.92
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.92)

2. Gym Hero
   Score: 2.97
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.97)

3. Rooftop Lights
   Score: 1.86
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.86)

4. Storm Runner
   Score: 0.99
   Reasons:
     - energy closeness (+0.99)
   Weak match: only energy lined up

5. Night Drive Loop
   Score: 0.85
   Reasons:
     - energy closeness (+0.85)
   Weak match: only energy lined up
```

**Chill Lofi**

```
=== Chill Lofi ===
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}

Top recommendations:

1. Library Rain
   Score: 4.00
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+1.00)

2. Midnight Coding
   Score: 3.93
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.93)

3. Focus Flow
   Score: 2.95
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.95)

4. Spacewalk Thoughts
   Score: 1.93
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.93)

5. Coffee Shop Stories
   Score: 0.98
   Reasons:
     - energy closeness (+0.98)
   Weak match: only energy lined up
```

**Deep Intense Rock**

```
=== Deep Intense Rock ===
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.95}

Top recommendations:

1. Storm Runner
   Score: 3.96
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.96)

2. Gym Hero
   Score: 1.98
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.98)

3. Sunrise City
   Score: 0.87
   Reasons:
     - energy closeness (+0.87)
   Weak match: only energy lined up

4. Rooftop Lights
   Score: 0.81
   Reasons:
     - energy closeness (+0.81)
   Weak match: only energy lined up

5. Night Drive Loop
   Score: 0.80
   Reasons:
     - energy closeness (+0.80)
   Weak match: only energy lined up
```

**Conflicted (High Energy + Sad)**

```
=== Conflicted (High Energy + Sad) ===
Preferences: {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}
Warning: no songs in the catalog have mood "sad".

Top recommendations:

1. Gym Hero
   Score: 2.97
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.97)

2. Sunrise City
   Score: 2.92
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.92)

3. Storm Runner
   Score: 0.99
   Reasons:
     - energy closeness (+0.99)
   Weak match: only energy lined up

4. Rooftop Lights
   Score: 0.86
   Reasons:
     - energy closeness (+0.86)
   Weak match: only energy lined up

5. Night Drive Loop
   Score: 0.85
   Reasons:
     - energy closeness (+0.85)
   Weak match: only energy lined up
```

**Unknown Genre (K-Pop)**

```
=== Unknown Genre (K-Pop) ===
Preferences: {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}
Warning: no songs in the catalog have genre "k-pop".

Top recommendations:

1. Rooftop Lights
   Score: 1.94
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.94)

2. Sunrise City
   Score: 1.88
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.88)

3. Night Drive Loop
   Score: 0.95
   Reasons:
     - energy closeness (+0.95)
   Weak match: only energy lined up

4. Storm Runner
   Score: 0.79
   Reasons:
     - energy closeness (+0.79)
   Weak match: only energy lined up

5. Gym Hero
   Score: 0.77
   Reasons:
     - energy closeness (+0.77)
   Weak match: only energy lined up
```

### Experiment: changing the weights

I tried a weight-shift experiment: I doubled the importance of energy (up to 2 points instead of 1) and halved the importance of genre (1 point instead of 2), leaving mood at 1 point. Then I ran all five profiles again.

**Result:** the top 5 stayed exactly the same, in the same order, for all five profiles. Only the scores changed, and the gaps between songs got smaller. For example, for Chill Lofi, Focus Flow had been ahead of Spacewalk Thoughts by about 1 point, and that lead shrank to just 0.04.

**Why:** in this small catalog, genre and energy line up. Pop songs here tend to be energetic and lofi songs tend to be calm, so rewarding energy more mostly rewards the same songs that genre was already favoring. With a bigger, more varied catalog, the change would likely start pushing songs from the wrong genre into the top 5.

**Decision:** I kept the original weights (genre +2.0, mood +1.0, energy up to +1.0). The experiment didn't improve any recommendation, and it made weak matches look closer to good ones.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
