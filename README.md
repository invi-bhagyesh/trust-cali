# Trust Experiment: A/B Cue Manipulation Prototype

## What This Does

A minimal web-based experiment that measures how AI agent presentation affects user trust decisions.

**Two conditions (A/B) differing in agent name + tone:**

| Condition | Agent Name | Tone                 | Example                                                                 |
| --------- | ---------- | -------------------- | ----------------------------------------------------------------------- |
| A         | "Aria"     | Warm, conversational | "Hey! I think you'd really enjoy the Kindle Paperwhite..."              |
| B         | "System"   | Formal, neutral      | "Recommendation: Kindle Paperwhite. Category: E-Reader. Price: $140..." |

**Task:** 5 product recommendations. Participant accepts or rejects each.

**Logging:** Every trial logs `participant_id`, `condition`, `trial`, `product`, `decision`, `timestamp`, `latency_ms` to both JSON and CSV.

## Condition Logic

- On session start, the server randomly assigns condition A or B
- Condition A: agent named "Aria", warm blue background, friendly emoji avatar, conversational recommendation text
- Condition B: agent named "System", neutral gray background, robot emoji avatar, formal recommendation text
- AI accuracy is not varied (all recommendations are presented as genuine)
- The only difference between conditions is the presentation cue

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

Open http://localhost:5000 in your browser. Complete the 5 trials. Logs are saved to `out/`.

## Logging Implementation

- **Client-side**: `performance.now()` measures latency from trial render to button click (sub-ms precision, no network delay)
- **Server-side**: Flask receives POST per trial, appends to in-memory list, writes to `out/experiment_log.json` and `out/experiment_log.csv` after each trial
- **Schema**: Each row contains `participant_id` (UUID), `condition` (A/B), `trial` (1-5), `product`, `decision` (accept/reject), `timestamp` (ISO), `latency_ms`

## Sample Output

Run `python generate_sample.py` to generate sample data for 6 participants, or just run the experiment yourself.

### out/experiment_log.json (excerpt)

```json
[
  {
    "participant_id": "a1b2c3d4",
    "condition": "A",
    "trial": 1,
    "product": "Sony WH-1000XM5",
    "decision": "accept",
    "timestamp": "2026-03-31T14:00:02",
    "latency_ms": 1823
  }
]
```

### out/experiment_log.csv (excerpt)

```
participant_id,condition,trial,product,decision,timestamp,latency_ms
a1b2c3d4,A,1,Sony WH-1000XM5,accept,2026-03-31T14:00:02,1823
```

## File Structure

```
main.py              # Flask server + experiment logic
static/index.html    # Single-page experiment UI
generate_sample.py   # Generate sample output data
requirements.txt     # flask
out/
  experiment_log.json
  experiment_log.csv
```
