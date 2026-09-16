# Skill Creator Examples: Benchmark and Evaluation Patterns

## 1. Evaluation Cases (`evals/evals.json`)

### Bad (Trivial and Vague Assertions)

```json
[
  {
    "id": "eval-1",
    "prompt": "Fix this skill",
    "expected_output": "The skill should be better and work properly.",
    "assertions": [
      "output is good",
      "no errors"
    ]
  }
]
```

Defects:
- Vague prompt with no concrete input files or explicit constraints.
- Subjective assertion ("output is good") that cannot be automatically evaluated.

### Good (Objective, Falsifiable Criteria)

```json
[
  {
    "skill_name": "data-pipeline",
    "id": "batch-processing-csv",
    "prompt": "Process the sensor reading files in input/ and produce hourly summaries in output/summary.csv with null values filled with 0.0.",
    "files": ["input/readings_01.csv", "input/readings_02.csv"],
    "expected_output": "output/summary.csv exists, contains headers [timestamp, sensor_id, mean_val], and contains zero empty cells.",
    "assertions": [
      "test -f output/summary.csv",
      "python3 -c 'import pandas as pd; df = pd.read_csv(\"output/summary.csv\"); assert df.isna().sum().sum() == 0'",
      "python3 -c 'import pandas as pd; df = pd.read_csv(\"output/summary.csv\"); assert list(df.columns) == [\"timestamp\", \"sensor_id\", \"mean_val\"]'"
    ]
  }
]
```

Advantages:
- Realistic prompt with explicit input and output files.
- Falsifiable deterministic bash and python assertions.
- Reproducible across baseline and skill-augmented runs.
