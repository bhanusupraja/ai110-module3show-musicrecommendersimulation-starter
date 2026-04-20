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

### The Big Picture

Real-world platforms like Spotify don't just look at what you like — they look at what millions of people with similar taste like, and combine that with the actual sound of a song (its tempo, energy, mood) to make a prediction. It's crowd wisdom plus audio science working together.

This version keeps it simpler: it takes what a user tells us they prefer — their favorite genre, mood, and energy level — and finds songs from the catalog that best match those preferences. Every recommendation comes with a plain-English reason so you can see exactly why it was picked.

---

### Step 1 — The Songs

Each song in `data/songs.csv` is described by these features:

- **genre** and **mood** — what kind of song it is (e.g. pop, happy)
- **energy** — how intense it feels, from 0.0 (very calm) to 1.0 (very intense)
- **tempo_bpm** — speed in beats per minute
- **valence** — how positive or joyful it sounds (0.0 = sad, 1.0 = happy)
- **danceability** and **acousticness** — rhythm strength and acoustic vs. electronic texture
- **title**, **artist**, **id** — display only, not used for scoring

---

### Step 2 — The User Profile

The user (Alex) tells the system what they like:

- **favorite_genre** = `"pop"` — the genre they want
- **favorite_mood** = `"happy"` — the mood they want
- **target_energy** = `0.85` — they like high-energy music

---

### Step 3 — Scoring Every Song

For each of the 18 songs, the system awards points based on how well it matches Alex:

| Rule | Points |
|---|---|
| Genre matches (`"pop"`) | +2.0 |
| Mood matches (`"happy"`) | +1.0 |
| Energy is close to 0.85 | +0.0 to +1.0 |
| **Max possible score** | **4.0** |

The closer a song's energy is to the target, the more points it earns. An exact match gives the full +1.0.

---

### Step 4 — Ranking and Output

Once every song has a score, the system sorts them from highest to lowest and returns the top 5. Each result is printed with its score and a reason:

```
Sunrise City - Score: 3.97
Because: genre matches (pop) +2.0 | mood matches (happy) +1.0 | energy 0.82 vs target 0.85 (+0.97)
```

Songs that match genre AND mood AND energy float to the top. Songs that miss on all three sink to the bottom.

---

## Algorithm Recipe

This is the exact rule the system uses to score every song:

```
1. Start with score = 0.0

2. If the song's genre matches the user's favorite genre:
       score += 2.0

3. If the song's mood matches the user's favorite mood:
       score += 1.0

4. Calculate how close the song's energy is to the user's target:
       score += 1.0 - abs(song.energy - target_energy)
       (a perfect energy match adds 1.0, a total mismatch adds 0.0)

5. The final score is a number between 0.0 and 4.0.
   Higher = better match.

6. Sort all 18 songs by score, highest first.
   Return the top 5.
```

**Why these weights?**
Genre gets the most points (2.0) because it is the strongest signal of who you are as a listener. Mood gets the second most (1.0) because it matters but changes with context. Energy is a continuous measure — it rewards songs that are close, not just exact matches.

---

## Potential Biases

| Bias | Why it happens | Example |
|---|---|---|
| **Genre over-prioritization** | Genre is worth 2.0 points — double any other signal. A perfect mood + energy match (2.0 pts max) still loses to any genre match. | `Island Drift` (reggae, happy, energy=0.61) scores lower than `Gym Hero` (pop, intense, energy=0.93) for a pop/happy user, even though Island Drift matches mood. |
| **Wrong-genre penalty is invisible** | All non-matching genres score 0 — there is no difference between "close genre" (indie pop) and "completely unrelated" (classical). | `Rooftop Lights` (indie pop) and `Moonlit Waltz` (classical) both get 0 genre points, despite indie pop being far closer to pop. |
| **Energy bias toward active users** | Energy similarity rewards songs near the user's target. A user who prefers calm music (energy=0.2) will rarely see high-energy songs — even if they occasionally want something upbeat. | A chill user will never get `Gym Hero` in their top 5, even on days they want something energetic. |
| **Mood is binary** | A song either matches the mood exactly or gets nothing. There is no partial credit for related moods. | `"uplifting"` and `"happy"` feel similar but the system treats them as completely different. |
| **Small catalog bias** | With only 18 songs, some genres and moods have just one representative. The system has no choice but to recommend it regardless of quality. | There is only one classical song — `Moonlit Waltz` will always be last for high-energy users, and first for classical users with no alternatives. |

---

## Data Flow Diagram

```mermaid
flowchart TD
    A([songs.csv]) -->|load_songs| B[List of 18 Song Dicts]
    C([user_prefs\ngenre=pop, mood=happy\nenergy=0.85]) --> D

    B -->|for each song| D[score_song\nuser_prefs, song]

    D --> E{genre match?}
    E -->|yes| F[+2.0]
    E -->|no|  G[+0.0]

    D --> H{mood match?}
    H -->|yes| I[+1.0]
    H -->|no|  J[+0.0]

    D --> K[1 - abs\nsong.energy - 0.85]
    K --> L[+0.0 to +1.0]

    F & G --> M([score])
    I & J --> M
    L     --> M

    M --> N[scored list\nsong, score, explanation]

    N -->|repeat x18| N
    N -->|sort descending| O[Ranked List]
    O -->|slice top k| P([Top 5 Recommendations\nprinted in main.py])
```

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

