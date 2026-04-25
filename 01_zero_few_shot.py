"""
Experiment 01: Zero-Shot vs Few-Shot
Shows how providing examples constrains output format and prevents label invention.
"""
from config import chat

# ═══ ZERO-SHOT ═══
# No examples — just the instruction
zero_shot = chat([
    {"role": "user", "content": """Classify the sentiment of this review as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The battery life is incredible but the screen is too dim outdoors."
Sentiment:"""}
])
print(f"Zero-shot: {zero_shot}")

# ═══ FEW-SHOT ═══
# Provide 3 examples of the expected pattern
few_shot = chat([
    {"role": "user", "content": """Classify the sentiment of each review as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "Absolutely love this product, best purchase ever!"
Sentiment: POSITIVE

Review: "Terrible quality, broke after one week."
Sentiment: NEGATIVE

Review: "It works as described, nothing special."
Sentiment: NEUTRAL

Review: "The battery life is incredible but the screen is too dim outdoors."
Sentiment:"""}
])
print(f"Few-shot: {few_shot}")

