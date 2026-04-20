# Main Data Types in Streaming Platform Recommendation Systems

## Overview
Streaming platforms collect and use several categories of data to power their recommendation engines. These data types feed into both collaborative filtering and content-based filtering approaches.

---

## 1. User Behavior Signals (Implicit Feedback)

### Skip Data
```
{
  "user_id": 12345,
  "song_id": 67890,
  "skip_time": 3.5,        // seconds into song when skipped
  "total_song_length": 210, // seconds
  "timestamp": "2024-01-15T14:23:00Z",
  "device": "mobile"
}
```
- **What it means**: If user skips after 3 seconds of a 3:30 song, that's strong negative signal
- **Why it matters**: Skips are more honest than ratings—users skip when they truly dislike something
- **Value in CF**: Used to identify users with opposite taste
- **Value in CB**: Flag that this song doesn't match user's current mood

### Replay/Repeat Listens
```
{
  "user_id": 12345,
  "song_id": 67890,
  "play_count": 47,         // times user replayed this song
  "total_listens_this_month": 3,
  "added_to_favorites": true,
  "replay_intervals": [1, 2, 2, 3, 4, 1, ...] // days between replays
}
```
- **What it means**: Replay count = user loyalty to a song
- **Why it matters**: Replays indicate STRONG preference (more valuable than a single play)
- **Value in CF**: High replay songs cluster similar users
- **Value in CB**: Songs with features from replayed tracks should be ranked higher

### Playlist Additions
```
{
  "user_id": 12345,
  "song_id": 67890,
  "playlist_id": 111,
  "playlist_name": "Summer Vibes", // or "Breakup Songs"
  "position_in_playlist": 5,
  "date_added": "2024-01-15",
  "context": "user_created"  // vs "platform_suggested"
}
```
- **What it means**: User intentionally saved song to a playlist they care about
- **Why it matters**: Explicit positive signal (stronger than just playing)
- **Value in CF**: Playlist curation shows taste preferences; find users with similar playlists
- **Value in CB**: Playlist theme reveals mood/context preferences

### Listen Time / Total Playtime
```
{
  "user_id": 12345,
  "song_id": 67890,
  "listen_session": {
    "start_time": "2024-01-15T14:23:00Z",
    "duration_listened": 180,     // seconds actually listened
    "song_length": 210,           // seconds
    "completion_rate": 0.857,     // 85.7% of song heard
    "paused_count": 2,
    "skipped_forward": false
  }
}
```
- **What it means**: Did user listen to whole song or bail halfway?
- **Why it matters**: 100% completion = love; 20% = disinterest
- **Value in CF**: Completion rates cluster similar users
- **Value in CB**: Songs with similar completion patterns to user's favorites = good recommendations

### Shares & Social Actions
```
{
  "user_id": 12345,
  "song_id": 67890,
  "shared_to": ["instagram", "spotify_friends_feed"],
  "shared_timestamp": "2024-01-15T14:25:00Z",
  "comment": "obsessed with this song",
  "likes_on_share": 23
}
```
- **What it means**: User shared song with friends = strong endorsement
- **Why it matters**: Social sharing indicates the song is memorable and sharable
- **Value in CF**: Shared songs are high-signal positive indicators
- **Value in CB**: Highly shareable songs often share similar attributes

### Search & Exploration
```
{
  "user_id": 12345,
  "search_query": "upbeat indie pop",
  "timestamp": "2024-01-15T14:20:00Z",
  "clicked_results": [67890, 67891, 67892],
  "dwell_time": 45,  // seconds spent looking at results
  "interaction": "clicked_song"
}
```
- **What it means**: Search intent shows what user is looking for RIGHT NOW
- **Why it matters**: Real-time signal of current mood/context
- **Value in CF**: Search queries reveal current user state
- **Value in CB**: Query terms suggest mood/mood keywords

---

## 2. Song Audio Features (Attributes)

### Spotify's Audio Feature Set
```
{
  "song_id": 67890,
  "title": "Blinding Lights",
  "artist": "The Weeknd",
  
  // Continuous features (0.0 to 1.0 scale)
  "energy": 0.73,            // intensity, 0=calm, 1=intense
  "valence": 0.82,           // positivity, 0=sad, 1=happy
  "danceability": 0.81,      // rhythm suitability, 0=not danceable, 1=perfect for dancing
  "acousticness": 0.11,      // 0=electric/synth, 1=acoustic instruments
  "instrumentalness": 0.0,   // 0=has vocals, 1=pure instruments
  "liveness": 0.14,          // 0=studio, 1=live recording with crowd
  "speechiness": 0.04,       // 0=no speech, 1=pure spoken words
  
  // Discrete features
  "tempo_bpm": 103,          // beats per minute (60 = slow, 180+ = fast)
  "time_signature": "4/4",   // most common
  "key": "D",                // musical key
  "mode": "Minor",           // major vs minor scale
  "duration_ms": 200040,     // song length in milliseconds
  
  // Categorical
  "genre": "Synthwave/Electronic",
  "subgenres": ["synthwave", "electronic", "pop"],
  "lyrical_themes": ["longing", "night", "love"]
}
```

### Feature Explanations

| Feature | Low (0.0) | High (1.0) | Example |
|---------|-----------|-----------|---------|
| **Energy** | Smooth, calm | Aggressive, intense | Lullaby vs. Death Metal |
| **Valence** | Dark, sad, angry | Bright, happy, cheerful | Funeral March vs. Party Song |
| **Danceability** | Irregular beat | Strong, regular beat | Talk Radio vs. EDM |
| **Acousticness** | Electronic, produced | Acoustic instruments | Synth vs. Acoustic Guitar |
| **Instrumentalness** | Vocals prominent | Pure instruments | Pop Song vs. Jazz Instrumental |
| **Liveness** | Studio recording | Live concert | Album Track vs. Live Album |
| **Speechiness** | Singing/music | Spoken words | Song vs. Audiobook Excerpt |

---

## 3. User Profile Data

### Demographic & Explicit Preferences
```
{
  "user_id": 12345,
  "profile": {
    "age_group": "18-24",
    "country": "US",
    "language": "en",
    "timezone": "America/New_York",
    "subscription_tier": "premium",
    
    // Explicit preferences (from settings/surveys)
    "preferred_genres": ["indie", "pop", "electronic"],
    "disliked_genres": ["country", "explicit_content"],
    "mood_preferences": ["upbeat", "chill", "workout"],
    "onboarding_survey_responses": {...}
  }
}
```

### Aggregated User Taste Profile
```
{
  "user_id": 12345,
  
  // Computed from listening history
  "average_energy": 0.68,
  "average_valence": 0.65,
  "average_danceability": 0.62,
  "average_acousticness": 0.28,
  "average_tempo": 115,  // BPM
  
  // Top preferences
  "top_5_genres": ["indie", "alternative", "pop", "electronic", "folk"],
  "top_5_artists": ["Radiohead", "Arctic Monkeys", "Tame Impala", "Mac DeMarco", "Death Grips"],
  "top_5_moods": ["melancholic", "upbeat", "chill", "experimental", "nostalgic"],
  
  // Time-based preferences
  "morning_preference": "upbeat_energetic",
  "evening_preference": "chill_acoustic",
  "workout_preference": "high_energy_electronic",
  
  "taste_diversity_score": 0.72,  // how eclectic (0=only one genre, 1=very diverse)
  "novelty_seeking": 0.45  // how open to new artists (0=same songs, 1=always new)
}
```

---

## 4. Contextual Data

### Time & Device Context
```
{
  "user_id": 12345,
  "listening_session": {
    "timestamp": "2024-01-15T14:23:00Z",
    "time_of_day": "afternoon",      // morning, afternoon, evening, night
    "day_of_week": "Monday",
    "season": "winter",
    "device_type": "mobile",         // mobile, desktop, tablet, speaker, car
    "device_os": "iOS",
    "app_version": "8.0.54",
    
    // Activity context (inferred or explicit)
    "inferred_activity": "workout",  // vs commuting, working, relaxing, party
    "location": "gym",
    "location_type": "public_space",
    
    // Session characteristics
    "session_duration": 45,          // minutes
    "num_skips": 3,
    "num_songs_played": 12,
    "repeated_artists": ["Taylor Swift", "The Weeknd"]
  }
}
```

### Temporal Patterns
```
{
  "user_id": 12345,
  "listening_patterns": {
    "peak_hours": ["6-9am", "12-1pm", "5-7pm"],  // when user listens most
    "peak_days": ["Monday", "Friday", "Saturday"],
    "seasonal_trends": {
      "summer": "more_dance_pop",
      "winter": "more_indie_folk",
      "holiday_season": "more_festive_upbeat"
    },
    
    // Recency weighting
    "last_7_days_top_genres": ["indie", "rock", "electronic"],
    "last_30_days_top_genres": ["indie", "pop", "alternative"],
    "all_time_top_genres": ["indie", "electronic", "pop"]
  }
}
```

---

## 5. Explicit Feedback

### Ratings & Thumbs Up/Down
```
{
  "user_id": 12345,
  "song_id": 67890,
  "rating": {
    "type": "thumbs_up",           // or thumbs_down
    "timestamp": "2024-01-15T14:25:00Z",
    
    // Alternative: star rating (if platform uses it)
    // "stars": 5,  // 1-5 stars
    
    "context": "from_recommendation" // vs user_search, vs playlist
  }
}
```

### "Save to Library"
```
{
  "user_id": 12345,
  "song_id": 67890,
  "action": "saved_to_library",
  "timestamp": "2024-01-15T14:25:00Z",
  "intent": "return_later"  // indicates user wants to revisit
}
```

---

## 6. Social & Network Data

### Friend Following & Activity
```
{
  "user_id": 12345,
  "social": {
    "followers": 234,
    "following": 156,
    "friend_ids": [111, 222, 333, ...],
    
    "recent_friend_activity": [
      {
        "friend_id": 111,
        "action": "liked_song",
        "song_id": 67890,
        "timestamp": "2024-01-15T10:00:00Z"
      }
    ]
  }
}
```

### Playlist Interactions
```
{
  "playlist_id": 111,
  "created_by_user": 12345,
  "title": "Summer Road Trip",
  "description": "High energy upbeat songs for long drives",
  
  "collaborative_data": {
    "num_followers": 342,
    "num_collaborators": 5,
    "is_collaborative": true,
    "num_songs": 28,
    "duration_hours": 1.95,
    
    "contributor_user_ids": [12345, 67890, 111111, ...]
  }
}
```

---

## 7. Metadata & Content Features

### Artist Information
```
{
  "artist_id": 999,
  "name": "The Weeknd",
  "genres": ["synthwave", "r&b", "electronic"],
  "popularity_score": 0.9,
  "num_monthly_listeners": 42000000,
  "related_artists": [888, 777, 666, ...],
  "debut_year": 2010,
  "follower_count": 15000000
}
```

### Album & Release Info
```
{
  "album_id": 555,
  "title": "After Hours",
  "artist_id": 999,
  "release_date": "2020-03-20",
  "genre": "Synthwave, R&B, Electronic",
  "num_tracks": 14,
  "producer": ["Oscar Holter", "Max Martin"],
  "lyricist": "The Weeknd",
  "record_label": "Republic Records"
}
```

---

## How These Data Types Connect in Recommendation Systems

### Collaborative Filtering Uses:
- ✅ User behavior signals (skips, replays, playlist adds)
- ✅ Social/network data (what similar users liked)
- ✅ Explicit feedback (thumbs up)
- ✅ Temporal patterns (current activity)

```
GOAL: Find users with similar taste
INPUT: User A skipped 5 songs, replayed 3, added 2 to playlists
FIND: User B with identical pattern
OUTPUT: Recommend songs User B likes to User A
```

### Content-Based Filtering Uses:
- ✅ Song audio features (energy, valence, tempo, etc.)
- ✅ User taste profile (avg energy they prefer)
- ✅ Metadata (genre, artist, album)
- ✅ Context (workout = high energy recommendation)

```
GOAL: Match song attributes to user preferences
INPUT: User loves high-energy pop (0.7+ energy, upbeat valence)
NEW SONG: energy=0.74, valence=0.78, genre=pop
OUTPUT: Match score = 92% → Recommend
```

### Hybrid Systems Use Both:
```
final_score = 
  0.6 * collaborative_score +
  0.4 * content_based_score +
  0.1 * temporal_boost +
  0.05 * diversity_factor
```

---

## Connecting to Your Music Recommender Project

### Data Types Your System Currently Has:
✅ Song attributes: `genre, mood, energy, tempo_bpm, valence, danceability, acousticness`
✅ User profile: `favorite_genre, favorite_mood, target_energy, likes_acoustic`

### Data Types to Add for Enhanced Recommendations:
1. **User behavior** – Track skips, replays, playlist adds
2. **Temporal context** – Time of listening (morning = more upbeat?)
3. **Feedback signals** – Thumbs up/down on recommendations
4. **User history** – Keep stats on avg energy/valence user prefers
5. **Artist data** – Find related artists, popularity

### Example Enhancement:
```python
# Current (content-based only):
score = match_energy_to_profile(song, user)

# Enhanced (hybrid):
score = 0.6 * collaborative_score(song, user_history) + \
        0.4 * content_based_score(song.features, user.preferences)
```

---

## Key Insight: Why Both Types Matter

**Content-based alone** → Echo chamber (only similar songs)
**Collaborative alone** → Cold start problem (new users/songs)
**Together** → Personalized + serendipitous + scalable

This is why Spotify and YouTube use hybrid approaches—each data type reveals different aspects of what users want.
