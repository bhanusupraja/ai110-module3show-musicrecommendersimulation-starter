# Designing Your Scoring Rule: A Math-Based Prompt Guide

## The Core Question You're Solving

**How do we convert user preferences and song attributes into a single number (0–1 or 0–100) that tells us "How much will this user love this song?"**

This is the central challenge of recommendation systems.

---

## Part 1: Scoring Numerical Features

### The Problem: Rewarding Closeness vs. Extremes

When a user likes songs with **energy = 0.80**, how should we score songs with different energy levels?

#### ❌ Wrong Approach 1: Direct Value
```
score = song_energy

Problem: A song with energy 0.95 gets 0.95 points
         A song with energy 0.10 gets 0.10 points
         
But what if the user only likes medium-high energy?
A song with 0.95 energy might be TOO intense (bad score)
but this approach gives it a high score anyway.
```

#### ❌ Wrong Approach 2: Majority Wins
```
score = 1 if song_energy > 0.75 else 0

Problem: A song with 0.79 energy gets 1 point
         A song with 0.75 energy gets 0 points
         
This is a cliff effect—no gradual transitions.
Very unnatural for recommendations.
```

#### ✅ Right Approach: Distance-Based Scoring

The key insight: **Reward closeness, penalize distance**

```
score = 1 - |user_preference - song_value|
        ↑                      ↑
        perfect match        absolute difference

Example:
User prefers energy 0.80

Song with 0.80 energy: score = 1 - |0.80 - 0.80| = 1 - 0 = 1.0 ✓ Perfect
Song with 0.78 energy: score = 1 - |0.80 - 0.78| = 1 - 0.02 = 0.98 ✓ Great
Song with 0.75 energy: score = 1 - |0.80 - 0.75| = 1 - 0.05 = 0.95 ✓ Good
Song with 0.70 energy: score = 1 - |0.80 - 0.70| = 1 - 0.10 = 0.90 ✓ OK
Song with 0.50 energy: score = 1 - |0.80 - 0.50| = 1 - 0.30 = 0.70 ~ Getting worse
Song with 0.20 energy: score = 1 - |0.80 - 0.20| = 1 - 0.60 = 0.40 ✗ Bad match
Song with 0.00 energy: score = 1 - |0.80 - 0.00| = 1 - 0.80 = 0.20 ✗ Terrible
```

### Why This Works

This approach **naturally rewards the sweet spot**:
- Perfect match gets 1.0
- Small deviations (±0.05) are still great (0.95+)
- Medium deviations (±0.20) are acceptable (0.80)
- Large deviations are bad, but gracefully so

---

## Part 2: Handling Multiple Features

Once you have individual feature scores, you need to **combine them**.

### Three Ways to Combine Scores

#### Option A: Simple Average (Treats all equally)
```
final_score = (energy_score + valence_score + genre_score) / 3

Problem: If genre is 0 but energy/valence are 0.95 each:
         final_score = (0.95 + 0.95 + 0) / 3 = 0.63
         
This says one wrong genre ruins three good features.
Is that fair?
```

#### Option B: Weighted Average (Features matter differently) ⭐ RECOMMENDED
```
final_score = w₁ × energy_score + w₂ × valence_score + w₃ × genre_score

where w₁ + w₂ + w₃ = 1.0

Example weights:
w₁ = 0.35 (energy)
w₂ = 0.35 (valence)
w₃ = 0.30 (genre)

With same scenario:
final_score = 0.35×0.95 + 0.35×0.95 + 0.30×0 = 0.665

Still penalizes genre mismatch but doesn't destroy the score.
```

#### Option C: Multiplicative (One failure kills everything)
```
final_score = energy_score × valence_score × genre_match

Problem: If any score is 0, final_score = 0
         This is too harsh.
         
Use only if you want STRICT filtering:
"I ONLY want pop songs, no negotiations"
```

---

## Part 3: The Weights Question: Genre vs. Mood

### The Strategic Decision

**Should a matching genre be worth more points than matching mood?**

The answer depends on **your recommendation philosophy**:

### Philosophy 1: "Keep Users in Familiar Territory"
```
Weights:
  Genre:  0.50 (HIGH - anchor the recommendation)
  Energy: 0.25 (Medium - some flexibility)
  Valence: 0.25 (Medium)

Outcome: Users mostly get recommendations from their favorite genre.
         Will feel "safe" and familiar.
         Less chance of discovery.

Example:
User loves pop music → mostly pop recommendations
Even if a rock song perfectly matches their energy/mood preferences,
the genre mismatch pulls the score down significantly.

Best for: Casual listeners, conservative users, niche genre fans.
```

### Philosophy 2: "Discover New Genres with Old Preferences"
```
Weights:
  Genre:  0.20 (LOW - less important)
  Energy: 0.40 (HIGH - prioritize vibe)
  Valence: 0.40 (HIGH - prioritize emotion)

Outcome: Users will discover music across genres if it matches their vibe.
         High chance of serendipity.
         Risk: Might feel jarring.

Example:
User loves pop music with 0.85 energy and 0.80 happiness.
A synthwave song with 0.83 energy and 0.82 happiness gets:
score = 0.20×(genre mismatch) + 0.40×0.98 + 0.40×0.96
      = (low penalty) + 0.392 + 0.384 = 0.776 ✓ Still recommended

Best for: Explorers, music aficionados, playlist curators.
```

### Philosophy 3: "Vibe First, Genre Second" (BALANCED) ⭐ RECOMMENDED
```
Weights:
  Genre:  0.30 (Moderate - matters but not dominant)
  Energy: 0.35 (Slightly higher - core vibe)
  Valence: 0.35 (Slightly higher - emotional resonance)

Outcome: Most recommendations stay in user's comfort zone (genre matters)
         but will occasionally suggest cross-genre matches (if vibe is perfect)
         Best balance of familiarity + discovery.

Example:
User loves pop with 0.85 energy and 0.80 valence.

Pop song (0.83 energy, 0.82 valence):
score = 0.30×1.0 + 0.35×0.98 + 0.35×0.98 = 0.993 ✓✓✓ Top recommendation

Synthwave song (0.83 energy, 0.82 valence):
score = 0.30×0.5 + 0.35×0.98 + 0.35×0.98 = 0.833 ✓ Still good, but rated lower

Best for: Most users, moving beyond beginner recommenders.
```

---

## Part 4: Real-World Examples with Different Weights

### Test Case: User Profile
```
Preferences:
  favorite_genre: "pop"
  target_energy: 0.82
  preferred_valence: 0.80
```

### Test Case: Five Songs to Rank

```
Song A: Sunrise City
  genre: pop, energy: 0.82, valence: 0.84
  → Should rank HIGH (matches everything perfectly)

Song B: Rooftop Lights
  genre: indie pop, energy: 0.76, valence: 0.81
  → Should rank HIGH (close matches, slight genre difference)

Song C: Storm Runner
  genre: rock, energy: 0.91, valence: 0.48
  → Should rank MEDIUM/LOW (high energy, wrong valence, different genre)

Song D: Midnight Coding
  genre: lofi, energy: 0.42, valence: 0.56
  → Should rank LOW (too chill, wrong genre)

Song E: Gym Hero
  genre: pop, energy: 0.93, valence: 0.77
  → Should rank HIGH (same genre, close valence, slightly higher energy)
```

### Scenario 1: Genre-Heavy Weights (0.50 / 0.25 / 0.25)
```
w_genre = 0.50, w_energy = 0.25, w_valence = 0.25

Song A (pop, 0.82, 0.84):
  genre_match = 1.0 → contributes 0.50
  energy = 1 - 0 = 1.0 → contributes 0.25
  valence = 1 - 0.04 = 0.96 → contributes 0.24
  TOTAL = 0.99 ✓✓✓

Song B (indie pop, 0.76, 0.81):
  genre_match = 0.5 (indie pop ≠ pop exactly) → contributes 0.25
  energy = 1 - 0.06 = 0.94 → contributes 0.235
  valence = 1 - 0.01 = 0.99 → contributes 0.2475
  TOTAL = 0.7325 ⚠️ (genre mismatch hurts badly)

Song C (rock, 0.91, 0.48):
  genre_match = 0.5 → contributes 0.25
  energy = 1 - 0.09 = 0.91 → contributes 0.2275
  valence = 1 - 0.32 = 0.68 → contributes 0.17
  TOTAL = 0.6475 ✗ (wrong mood + wrong genre)

Song E (pop, 0.93, 0.77):
  genre_match = 1.0 → contributes 0.50
  energy = 1 - 0.11 = 0.89 → contributes 0.2225
  valence = 1 - 0.03 = 0.97 → contributes 0.2425
  TOTAL = 0.965 ✓✓

RANKING: A (0.99) > E (0.965) > B (0.733) > C (0.648) > D
INTERPRETATION: Strong preference for pop, high penalty for cross-genre
```

### Scenario 2: Vibe-Heavy Weights (0.20 / 0.40 / 0.40)
```
w_genre = 0.20, w_energy = 0.40, w_valence = 0.40

Song A (pop, 0.82, 0.84):
  genre_match = 1.0 → contributes 0.20
  energy = 1.0 → contributes 0.40
  valence = 0.96 → contributes 0.384
  TOTAL = 0.984 ✓✓✓

Song B (indie pop, 0.76, 0.81):
  genre_match = 0.5 → contributes 0.10
  energy = 0.94 → contributes 0.376
  valence = 0.99 → contributes 0.396
  TOTAL = 0.872 ✓✓ (genre penalty is lighter)

Song C (rock, 0.91, 0.48):
  genre_match = 0.5 → contributes 0.10
  energy = 0.91 → contributes 0.364
  valence = 0.68 → contributes 0.272
  TOTAL = 0.736 ⚠️ (mood mismatch still matters)

Song E (pop, 0.93, 0.77):
  genre_match = 1.0 → contributes 0.20
  energy = 0.89 → contributes 0.356
  valence = 0.97 → contributes 0.388
  TOTAL = 0.944 ✓✓

RANKING: A (0.984) > E (0.944) > B (0.872) > C (0.736) > D
INTERPRETATION: Genre matters less, vibe matters more
               All songs with good energy/valence get chances
               Even indie pop breaks into top recommendations
```

### Scenario 3: Balanced Weights (0.30 / 0.35 / 0.35) ⭐ RECOMMENDED
```
w_genre = 0.30, w_energy = 0.35, w_valence = 0.35

Song A (pop, 0.82, 0.84):
  TOTAL = 0.30×1.0 + 0.35×1.0 + 0.35×0.96 = 0.986 ✓✓✓

Song B (indie pop, 0.76, 0.81):
  TOTAL = 0.30×0.5 + 0.35×0.94 + 0.35×0.99 = 0.827 ✓✓

Song E (pop, 0.93, 0.77):
  TOTAL = 0.30×1.0 + 0.35×0.89 + 0.35×0.97 = 0.948 ✓✓

RANKING: A (0.986) > E (0.948) > B (0.827) > C > D
INTERPRETATION: Balanced approach
               Same genre gets boost but isn't mandatory
               Cross-genre recommendations possible if vibes match perfectly
               Best of both worlds
```

---

## Part 5: The Prompt Framework

### How to Think Through Your Scoring Rule

Use this **prompt structure** with yourself (or an AI):

---

### 📋 **The Scoring Rule Design Prompt**

```
GOAL: Design a scoring rule that calculates how much [USER_NAME] will love [SONG_NAME].

STEP 1: FEATURE SELECTION
├─ Question: Which song features matter most?
├─ Your answer: [genre, energy, valence, danceability, acousticness, ...]
├─ Why: [These best describe what makes a song appealing]
└─ Mathematical form: Each feature will be a value between 0 and 1

STEP 2: INDIVIDUAL FEATURE SCORING
├─ Question: How do I score each feature individually?
├─ Formula for numeric features:
│  └─ score_feature = 1 - |user_preference - song_value|
│     Why: Rewards closeness, not extremes
│
├─ Formula for categorical features (like genre):
│  └─ score_genre = 1.0 if (song_genre == user_genre) else 0.5
│     Why: Exact match is best, similar is acceptable
│
└─ Test it:
   └─ If user prefers energy 0.80:
      - Song with 0.80 energy → score 1.0 ✓
      - Song with 0.70 energy → score 0.9 ✓
      - Song with 0.50 energy → score 0.7 ~

STEP 3: COMBINING FEATURES (THE WEIGHTS DECISION)
├─ Question: Should all features matter equally?
├─ No! Decide your philosophy:
│
│  Philosophy A: Genre is anchor (0.50 weight)
│  └─ Use if: Need familiar recommendations
│  └─ Weights: genre=0.50, energy=0.25, valence=0.25
│
│  Philosophy B: Vibe over genre (0.20 weight for genre)
│  └─ Use if: Want cross-genre discovery
│  └─ Weights: genre=0.20, energy=0.40, valence=0.40
│
│  Philosophy C: Balanced (0.30 weight) ⭐ DEFAULT
│  └─ Use if: Want both familiarity + discovery
│  └─ Weights: genre=0.30, energy=0.35, valence=0.35
│
└─ Choose: [Philosophy A / B / C] because [REASONING]

STEP 4: THE FORMULA
├─ Write the formula:
└─ final_score = w₁×score_feature₁ + w₂×score_feature₂ + ... + wₙ×score_featureₙ
   
   Example (Balanced philosophy):
   final_score = 0.30 × score_genre + 
                 0.35 × score_energy + 
                 0.35 × score_valence

STEP 5: TEST & VALIDATE
├─ Test on real songs:
│  User loves: [SONG_BASELINE]
│  
│  Test Song 1: [VERY_SIMILAR_SONG]
│  → Expected: High score (0.9+)
│  → Actual: [CALCULATED_SCORE]
│  → Match? YES/NO
│
│  Test Song 2: [VERY_DIFFERENT_SONG]
│  → Expected: Low score (0.3 or less)
│  → Actual: [CALCULATED_SCORE]
│  → Match? YES/NO
│
└─ Adjust weights if tests fail

STEP 6: EXPLAIN YOUR CHOICE
├─ Why this combination of features?
├─ Why these specific weights?
├─ What philosophy guided your decisions?
└─ How does it differ from other approaches?
```

---

## Part 6: Worked Example Using the Prompt

### 📝 Filling Out the Prompt

```
GOAL: Design a scoring rule for what music I enjoy during morning workouts.

STEP 1: FEATURE SELECTION
Features that matter:
  ✓ Energy (primary - need high intensity)
  ✓ Valence (secondary - upbeat helps motivation)
  ✓ Genre (I like pop/electronic for workouts)
  ✓ Danceability (helps with rhythm adherence)
  ✗ Acousticness (not important during workouts)
  ✗ Mood (captured by valence already)

STEP 2: INDIVIDUAL FEATURE SCORING
- Energy: score = 1 - |0.85 - song.energy|
  Test: Song with 0.85 → score 1.0 ✓
        Song with 0.75 → score 0.9 ✓
        Song with 0.50 → score 0.65 ~ (too chill for gym)

- Valence: score = 1 - |0.75 - song.valence|
  Test: Song with 0.75 → score 1.0 ✓
        Song with 0.65 → score 0.9 ✓

- Genre: score = 1.0 if pop or electronic, else 0.6
  Test: Pop → 1.0 ✓
        Electronic → 1.0 ✓
        Rock → 0.6 ~ (possible but lower)

- Danceability: score = song.danceability directly (0-1)
  Test: High (0.85+) → boost the recommendation
        Low (0.40) → acceptable but not ideal

STEP 3: COMBINING FEATURES
Philosophy: "Vibe-forward with genre consideration"
Reasoning: For workout playlists, the FEELING (energy + valence) matters more
           than staying in one genre. But I do have genre preferences.

Chosen weights:
  Energy = 0.40 (primary driver)
  Valence = 0.30 (secondary but important)
  Genre = 0.20 (context matters but vibe trumps it)
  Danceability = 0.10 (nice-to-have)

STEP 4: THE FORMULA
final_score = 0.40 × score_energy + 
              0.30 × score_valence + 
              0.20 × score_genre + 
              0.10 × song.danceability

STEP 5: TEST & VALIDATE
User baseline: "Gym Hero" (pop, 0.93 energy, 0.77 valence, 0.88 danceability)

Test Song 1: "Rooftop Lights" (indie pop, 0.76 energy, 0.81 valence, 0.82 danceability)
  Expected: High (similar vibe, slight genre difference) → 0.85+
  Calculated:
    energy_score = 1 - |0.85 - 0.76| = 0.91
    valence_score = 1 - |0.75 - 0.81| = 0.94
    genre_score = 0.6 (indie ≠ pop exactly)
    final = 0.40×0.91 + 0.30×0.94 + 0.20×0.6 + 0.10×0.82
          = 0.364 + 0.282 + 0.12 + 0.082
          = 0.848 ✓ Matches expectation!

Test Song 2: "Midnight Coding" (lofi, 0.42 energy, 0.56 valence, 0.62 danceability)
  Expected: Low (too chill for workout) → 0.40 or less
  Calculated:
    energy_score = 1 - |0.85 - 0.42| = 0.57
    valence_score = 1 - |0.75 - 0.56| = 0.81
    genre_score = 0.6 (lofi not pop/electronic)
    final = 0.40×0.57 + 0.30×0.81 + 0.20×0.6 + 0.10×0.62
          = 0.228 + 0.243 + 0.12 + 0.062
          = 0.653 ⚠️ HIGHER than expected!

Adjustment: Energy weight too low? Let me try w_energy = 0.50 instead.
  new_final = 0.50×0.57 + 0.25×0.81 + 0.15×0.6 + 0.10×0.62
           = 0.285 + 0.2025 + 0.09 + 0.062
           = 0.6395

Still too high. Actually, I realize: lofi with good valence might work during
cool-down phase of workout. So 0.64 might be reasonable. I'll accept this.

STEP 6: EXPLAIN
This formula prioritizes the energetic "pump" (0.50 weight) because that's what
makes music work during intense exercise. Valence (positivity) is secondary (0.25)
because upbeat helps but high energy alone can drive motivation. Genre gets 0.15
because I have preferences but will listen to non-pop if the vibe is right.
Cross-genre tracks get 0.6 genre score, allowing them to score well if their
energy/valence perfectly match my preferences.
```

---

## Part 7: Making Your Decision

### Genre vs. Mood Weight: The Summary

| Scenario | Genre Weight | Energy Weight | Valence Weight | Best For |
|----------|---|---|---|---|
| **Genre-obsessed** | 0.50 | 0.25 | 0.25 | People who ONLY listen to one genre |
| **Vibe-first** | 0.20 | 0.40 | 0.40 | Music explorers, DJs |
| **Balanced** (⭐ Recommended) | 0.30 | 0.35 | 0.35 | Most people, most playlists |
| **Context-specific** | Varies | Varies | Varies | Advanced (different weights by context) |

### Quick Decision Framework

**Ask yourself:**

1. **"If my favorite artist released a song in a different genre, would I listen to it?"**
   - YES → Lower genre weight (0.20–0.30)
   - NO → Higher genre weight (0.40–0.50)

2. **"Am I picking music based on HOW it FEELS or WHAT it is?"**
   - HOW it feels (energy, mood, vibe) → Lower genre weight
   - WHAT it is (genre label) → Higher genre weight

3. **"Do I want serendipitous discoveries?"**
   - YES → Lower genre weight (allow cross-genre recommendations)
   - NO → Higher genre weight (stay in familiar territory)

---

## Your Next Steps

### Implementation Checklist

```
□ Step 1: Read through all 7 sections of this guide
   └─ Understanding WHY we use distance-based scoring is crucial

□ Step 2: Choose your philosophy (Genre-heavy / Vibe-first / Balanced)
   └─ Start with Balanced (0.30/0.35/0.35) if unsure

□ Step 3: Fill out the Scoring Rule Design Prompt
   └─ Use the prompt template in Part 5
   └─ Write it down, share it if getting feedback

□ Step 4: Implement the formula in Python
   └─ See the code example below

□ Step 5: Test on your 10 songs
   └─ Recommendation should make intuitive sense
   └─ Songs similar to user baseline should rank high

□ Step 6: Iterate based on test results
   └─ If wrong songs ranking high, adjust weights
   └─ Document why you made each change
```

### Python Template

```python
def calculate_song_score(user_profile, song, w_genre=0.30, w_energy=0.35, w_valence=0.35):
    """
    Calculate recommendation score using your chosen weights.
    
    Args:
        user_profile: dict with 'favorite_genre', 'target_energy', 'preferred_valence'
        song: dict with 'genre', 'energy', 'valence'
        w_genre: weight for genre (0-1)
        w_energy: weight for energy (0-1)
        w_valence: weight for valence (0-1)
    
    Returns:
        score: float between 0 and 1
    """
    # Individual feature scores
    genre_score = 1.0 if song['genre'] == user_profile['favorite_genre'] else 0.5
    energy_score = 1.0 - abs(user_profile['target_energy'] - song['energy'])
    valence_score = 1.0 - abs(user_profile['preferred_valence'] - song['valence'])
    
    # Combine weighted
    final_score = (w_genre * genre_score + 
                   w_energy * energy_score + 
                   w_valence * valence_score)
    
    return final_score

# Test it
user = {
    'favorite_genre': 'pop',
    'target_energy': 0.82,
    'preferred_valence': 0.84
}

song_a = {
    'genre': 'pop',
    'energy': 0.82,
    'valence': 0.84
}

score = calculate_song_score(user, song_a)
print(f"Score: {score:.2%}")  # Should be ~98%
```

---

## Summary

**The Core Formulas You Need:**

1. **Individual Feature Score (for numeric features):**
   ```
   score = 1 - |user_preference - song_value|
   ```

2. **Combined Score (weighted average):**
   ```
   final_score = w₁ × score₁ + w₂ × score₂ + ... + wₙ × scoreₙ
   ```

3. **Answering "Genre vs. Mood" Question:**
   ```
   If you want discovery: genre 0.20, energy 0.40, valence 0.40
   If you want familiarity: genre 0.50, energy 0.25, valence 0.25
   If you want balance: genre 0.30, energy 0.35, valence 0.35 ⭐
   ```

**My recommendation:** Start with balanced weights (0.30/0.35/0.35), test on your data, then adjust based on results.
