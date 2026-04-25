"""
Experiment 03: Chain-of-Thought
Compares direct answer vs step-by-step reasoning on a math problem.
"""
from config import chat

PROBLEM = """A store sells apples for $2 each. If you buy 5 or more, you get a 20% discount.
Tax is 8%. How much do you pay for 7 apples?"""

# ═══ WITHOUT CoT ═══
direct = chat([
    {"role": "user", "content": PROBLEM + "\n\nAnswer with just the final dollar amount."}
])
print(f"Direct answer: {direct}")

# ═══ WITH CoT ═══
cot = chat([
    {"role": "user", "content": PROBLEM + """

Think step by step:
1. Calculate the base price
2. Apply the discount
3. Add tax
4. State the final amount"""}
])
print(f"\nChain-of-Thought:\n{cot}")

