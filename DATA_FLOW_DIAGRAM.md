# Data Flow Diagram — Music Recommender Simulation

Visualizes how a single song moves from the CSV file to the final ranked list.

```mermaid
flowchart TD
    A([songs.csv]) -->|load_songs| B[List of 18 Song Dicts]
    C([user_prefs: genre=pop mood=happy energy=0.85]) --> D

    B -->|for each song| D[score_song]

    D --> E{genre match?}
    E -->|yes| F[score plus 1.0]
    E -->|no| G[score plus 0.0]

    D --> H{mood match?}
    H -->|yes| I[score plus 1.0]
    H -->|no| J[score plus 0.0]

    D --> K[energy similarity]
    K --> L[1 minus abs diff = 0.0 to 2.0]

    F --> M([total score 0.0 to 4.0])
    G --> M
    I --> M
    J --> M
    L --> M

    M --> N[scored list: song + score + explanation]
    N -->|repeat x18| N
    N -->|sort descending| O[Ranked List]
    O -->|slice top k| P([Top 5 Recommendations])
```

## Step-by-Step Breakdown

| Step | What Happens | Code Location |
|---|---|---|
| 1 | `load_songs()` reads all 18 rows from `songs.csv`, casts types | `recommender.py:106` |
| 2 | `recommend_songs()` loops over every song | `recommender.py:137` |
| 3 | `score_song()` checks genre match → +2.0 or +0.0 | `recommender.py:91` |
| 4 | `score_song()` checks mood match → +1.0 or +0.0 | `recommender.py:95` |
| 5 | `score_song()` computes energy similarity → +0.0 to +1.0 | `recommender.py:99` |
| 6 | Score + explanation appended to `scored` list | `recommender.py:138` |
| 7 | `scored.sort()` ranks all songs highest to lowest | `recommender.py:141` |
| 8 | Top `k` sliced and returned | `recommender.py:142` |
| 9 | Title, score, and explanation printed | `main.py:35` |

## Max Possible Score: 4.0

```
genre match   +2.0
mood match    +1.0
energy sim    +1.0  (when song.energy == user target exactly)
              ────
total          4.0
```
