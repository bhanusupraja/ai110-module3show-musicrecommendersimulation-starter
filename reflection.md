# Reflection — Profile Comparisons

Plain-language observations on what changed between profiles and why it makes sense.

---

## Pair 1: High-Energy Pop (Alex) vs. Chill Lofi (Sam)

**Alex** wants pop, happy, energy=0.85.
**Sam** wants lofi, chill, energy=0.38.

These two profiles produced completely different top-5 lists with zero overlap. That is exactly what you would expect — a gym playlist and a study playlist have nothing in common. The interesting thing is *why* they diverged so cleanly: both genre and mood pointed in opposite directions, and energy reinforced that split. High-energy pop songs (energy 0.82–0.93) scored well for Alex and terribly for Sam. Quiet lofi songs (energy 0.35–0.42) scored well for Sam and were invisible to Alex.

The one thing that stood out: `Coffee Shop Stories` (jazz, relaxed) appeared at #5 for Sam even though it is not lofi. This makes real-world sense — jazz and lofi feel similar. A person studying to lofi would probably also enjoy a quiet jazz track. The system found this connection not by understanding music but purely because the energy was close (0.37 vs target 0.38). It got the right answer by accident.

---

## Pair 2: Chill Lofi (Sam) vs. Deep Intense Rock (Jordan)

**Sam** wants lofi, chill, energy=0.38.
**Jordan** wants rock, intense, energy=0.91.

These are the most opposite profiles possible — one wants the quietest, most relaxed experience and the other wants the loudest, most aggressive. The results reflected this perfectly. Not a single song appeared in both lists. Sam's top songs clustered around energy 0.28–0.42. Jordan's top songs clustered around energy 0.85–0.97.

What was revealing here is the *shape* of the two lists. Sam got a genuine variety of reasonable results — three lofi songs, an ambient song, and a jazz song. Jordan got one great match (`Storm Runner`, perfect 4.00) and then four songs that a rock fan would shrug at. The difference is catalog size: there are three lofi songs and only one rock song. Jordan's profile has nowhere to go after `Storm Runner`.

---

## Pair 3: High-Energy Pop (Alex) vs. Deep Intense Rock (Jordan)

**Alex** wants pop, happy, energy=0.85.
**Jordan** wants rock, intense, energy=0.91.

These two profiles are close in energy but completely different in genre and mood. You might expect their lists to overlap — both want loud, driving music — but they barely do. Only `Gym Hero` appears in both (at #2 for Alex, #2 for Jordan).

Here is where it gets interesting. For **Alex**, `Gym Hero` appears because it is a pop song (genre match). For **Jordan**, the same song appears because it is intense (mood match). The same song scored well for two completely different reasons. This is a sign the system is somewhat fragile — it can reach the right answer through the wrong logic.

The key difference: Alex's list has three pop-flavored songs in the top 4. Jordan's list has one rock song and then increasingly unrelated music. A real pop fan and a real rock fan would agree Alex's list is better — not because the algorithm is smarter for Alex, but because the catalog simply has more pop-adjacent songs.

---

## Pair 4: Conflicting Preferences vs. Unknown Genre

**Conflicting**: blues, melancholic, energy=0.90 — wants sad blues but with high intensity.
**Unknown genre**: metal, intense, energy=0.95 — wants a genre that does not exist in the catalog.

Both of these are stress tests and they failed in different ways.

The **conflicting profile** failed quietly. `Rainy Season` ranked #1 because it matched blues and melancholic — but it has energy=0.44, which is the opposite of what the user asked for (0.90). The system picked a slow, quiet song for someone who wanted something intense and driving. Genre and mood together outweighed the energy preference by 3 full points. A real user would be confused and frustrated.

The **unknown genre profile** actually handled itself better. Since nothing in the catalog is "metal," the genre check never fired — so the system fell back to mood and energy. It surfaced `Gym Hero` and `Storm Runner` as the top results, which are at least intense and high-energy. Not perfect, but not offensive. When the system does not know the genre, it makes a reasonable guess based on feel. When it does know the genre but the energy conflicts, it ignores the energy entirely. The second failure mode is worse.

---

## Why Does "Gym Hero" Keep Showing Up for Happy Pop Users?

Imagine you are looking for a happy pop song — something like a feel-good radio hit. The system gives you `Gym Hero` — a workout track with intense, pumping energy and the mood of someone training for a marathon, not dancing at a party.

Here is why this happens in plain terms:

The scoring system looks at three things: genre, mood, and energy. Genre match gives 1.0 point (or 2.0 in the original recipe). Mood match gives 1.0 point. Energy gives up to 1.0 point based on closeness.

`Gym Hero` is tagged as "pop" — so it gets the full genre bonus immediately. Once it has that, it only needs to be close on energy to rank well. It does not matter that the mood is "intense" instead of "happy" — it already has enough points to beat songs that match mood but not genre.

Think of it like a job application scoring system. Genre is worth 40 points, mood is worth 20, energy is worth 20. A candidate who scores 40 on the first category and 15 on the third (total 55) beats a candidate who scores 20+20+19 (total 59)... wait, that would not happen with those numbers. But with the original weights (genre=2.0, mood=1.0, energy=1.0), genre dominates enough that `Gym Hero` at 2.92 beats `Rooftop Lights` at 1.91 even though Rooftop Lights matches the mood Alex actually asked for.

The fix is either to lower the genre weight so mood has more influence, or to add more pop songs so the system has better pop/happy options to choose from in the first place. Both are valid — and the weight shift experiment confirmed that lowering genre to 1.0 made the list feel more natural.
