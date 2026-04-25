"""
Experiment 02: Temperature
Runs the same prompt 3 times at T=0.0, T=0.7, and T=1.5 to show variance.
"""
from config import chat

PROMPT = "Write a one-sentence product tagline for a smart water bottle that tracks hydration."

for temp in [0.0, 0.7, 1.5]:
    print(f"\n{'='*50}")
    print(f"Temperature: {temp}")
    print(f"{'='*50}")
    for run in range(3):
        result = chat(
            [{"role": "user", "content": PROMPT}],
            temperature=temp,
        )
        print(f"  Run {run+1}: {result}")
