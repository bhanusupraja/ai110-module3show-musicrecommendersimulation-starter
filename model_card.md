# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

A simple content-based music recommender built for classroom exploration. It matches songs to a user based on genre, mood, and energy level.

---

## 2. Goal / Task

VibeFinder tries to answer one question: *"Given what a user tells us they like, which songs in our catalog best match them?"*

It does not learn from feedback. It does not track listening history. It just takes three inputs — favorite genre, favorite mood, and target energy level — and returns the 5 best-matching songs with a plain-English reason for each pick.

---

## 3. Data Used

- **Catalog size:** 18 songs in `data/songs.csv`
- **Expanded from:** 10 starter songs — 8 new songs added to cover missing genres and moods
- **Features per song:** genre, mood, energy (0–1), tempo BPM, valence, danceability, acousticness

**Genre spread:**

| Genre | Songs | Genre | Songs |
|---|---|---|---|
| lofi | 3 | pop | 2 |
| indie pop | 2 | rock | 1 |
| jazz | 1 | ambient | 1 |
| synthwave | 1 | hip-hop | 1 |
| blues | 1 | country | 1 |
| electronic | 1 | classical | 1 |
| reggae | 1 | folk | 1 |

**Key limit:** 12 out of 14 genres have only 1 song. This means most users will get just one genre-matched result and four filler songs.

**Energy spread:** 7 high-energy (>0.7), 5 mid-energy (0.4–0.7), 6 low-energy (<0.4).

**What is missing:** No songs about specific activities (e.g. running, sleeping). No language or lyric data. No popularity or play-count signals.

---

## 4. Algorithm Summary

Here is how the system scores each song in plain language:

1. **Does the genre match?** If yes, add 1.0 point. If no, add nothing.
2. **Does the mood match?** If yes, add 1.0 point. If no, add nothing.
3. **How close is the energy?** Subtract the difference between the song's energy and the user's target from 1.0. A perfect match gives 1.0 point. A song that is 0.5 away gives 0.5 points. A song that is 1.0 away gives 0.0 points. Multiply that by 2.0 (energy is currently weighted double).
4. Add up all the points. The highest possible score is 4.0.
5. Sort all 18 songs from highest to lowest score. Return the top 5.

Every result includes a reason like: *"genre matches (pop) +1.0 | mood matches (happy) +1.0 | energy 0.82 vs target 0.85 (+1.94)"*

**Current weights:** genre=1.0, mood=1.0, energy=2.0 (shifted from original genre=2.0 after experiments showed genre was too dominant).

---

## 5. Observed Behavior / Biases

**`Gym Hero` appears everywhere.**
This one song showed up in 5 out of 7 tested profiles. It has high energy (0.93), an "intense" mood, and a "pop" genre — which means it scores points for rock fans (intense mood), pop fans (genre match), and anyone wanting high energy. In a real app, this would need a diversity filter to stop it from dominating unrelated playlists.

**Genre singleton bias.**
Most genres have only one song. Once that one song is recommended, positions #2–5 are filled by whatever is closest in energy — regardless of feel or mood. A rock fan gets one great rock match and then a pop workout song, a hip-hop song, and an electronic track. That is not a rock playlist.

**The energy gap filter bubble.**
Only 5 songs sit in the medium energy range (0.4–0.6). A user targeting energy 0.5 will always see roughly the same 5 songs, spread across completely unrelated genres. There is no escape from this pool unless the catalog grows.

**Mood is binary — no partial credit.**
"Uplifting" and "happy" feel almost the same in real life. To the system they are completely different and score zero overlap. A user wanting "romantic" songs only gets a mood match from one song in the whole catalog (`Golden Hour`).

**Conflicting preferences are silently broken.**
A user who asks for blues/melancholic but with high energy=0.90 gets a quiet, slow blues song as #1. Genre and mood together (2.0 points) easily outweigh a bad energy score (0.54 points). The system picks the low-energy song and never explains the conflict.

---

## 6. Evaluation Process

Seven profiles were tested — three normal, four edge cases:

| Profile | Genre | Mood | Energy | What it tests |
|---|---|---|---|---|
| High-Energy Pop (Alex) | pop | happy | 0.85 | Normal happy pop listener |
| Chill Lofi (Sam) | lofi | chill | 0.38 | Study music listener |
| Deep Intense Rock (Jordan) | rock | intense | 0.91 | Heavy music fan |
| Conflicting preferences | blues | melancholic | 0.90 | Sad mood + high energy — does it break? |
| Unknown genre | metal | intense | 0.95 | Genre not in catalog — does it crash? |
| Average everything | pop | chill | 0.50 | Contradictory preferences, mid energy |
| Dreamy but max energy | classical | dreamy | 1.00 | Genre/mood match vs. energy mismatch |

**What worked:** Chill Lofi gave the most satisfying results — all 3 lofi songs ranked in the right order, and a jazz song appeared at #5 which actually makes sense. High-Energy Pop also worked cleanly.

**What failed:** Deep Intense Rock exposed the catalog problem. `Storm Runner` scored 4.00/4.00 — perfect. But #2–5 were pop, hip-hop, electronic, and pop again. A real rock fan would stop after song #1.

**The key experiment:** Weights were shifted — genre halved from 2.0 to 1.0, energy doubled from 1.0 to 2.0. `Rooftop Lights` jumped from score 1.91 to 2.82 in Alex's list. The recommendations felt more musically varied with just that one change. This showed that the original genre weight was too powerful.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom demonstration of how content-based filtering works
- Learning exercise for understanding scoring, ranking, and bias in recommendation systems
- Testing how small changes in weights change the output

**Not intended for:**
- Real music discovery (catalog too small, no learning from feedback)
- Production apps or actual user-facing products
- Representing any user with complex or evolving taste
- Any genre or mood not present in the 18-song catalog

---

## 8. Ideas for Improvement

**1. Add a diversity filter.**
After scoring, reject any song that shares a genre with a song already chosen for the top 5. This alone would fix the `Gym Hero` problem and force the system to surface more variety.

**2. Replace binary mood matching with a similarity table.**
Create a lookup like: "uplifting" is 80% similar to "happy", "moody" is 70% similar to "melancholic". Award partial mood points instead of all-or-nothing. This would make the system feel much more natural.

**3. Expand the catalog to at least 5 songs per genre.**
Most improvements to the algorithm will not matter until there are enough songs to choose from. A rock fan needs at least 5 rock songs before a "top 5 rock" recommendation makes any sense.

---

## 9. Personal Reflection

**Biggest learning moment:**
The most important thing I learned is that the data matters more than the algorithm. The scoring logic was mathematically correct from the start — but the results still felt wrong because 12 out of 14 genres had only one song. No amount of weight tuning fixes a catalog that is too small. Real systems like Spotify have millions of songs precisely so the algorithm has enough material to work with.

**How AI tools helped — and when I had to double-check:**
AI tools were useful for generating the initial dataset, suggesting weight strategies, and explaining concepts like collaborative vs. content-based filtering. But I had to manually verify the math on every scoring change. When weights were shifted, I ran the program myself to confirm the max score still equaled 4.0 and that the rankings changed in the expected direction. The AI explained *what* to do but I had to check *whether it worked*.

**What surprised me about simple algorithms:**
It surprised me that three rules — genre match, mood match, energy closeness — could produce results that genuinely feel like recommendations. When `Coffee Shop Stories` (jazz) appeared at #5 for the chill lofi user, it felt right even though the algorithm had no idea jazz and lofi are related. It got there purely because the energy numbers were close. Simple math accidentally captured a real musical relationship.

**What I would try next:**
I would add user feedback — a simple thumbs up / thumbs down on each recommendation — and use that to adjust the weights automatically over time. If a user keeps skipping jazz songs, lower the weight of energy proximity for that user. That would turn VibeFinder from a static formula into something that actually learns, which is the core difference between a toy system and a real one.
