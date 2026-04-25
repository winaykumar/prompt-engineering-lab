"""
Experiment 06: Self-Critique
Generate → Critique → Revise pattern for code generation.
"""
from config import chat

TASK = "Write a Python function that checks if a string is a valid email address."

# Step 1: Generate draft
print("═══ Step 1: Draft ═══")
draft = chat([{"role": "user", "content": TASK}])
print(draft)

# Step 2: Critique
print("\n═══ Step 2: Critique ═══")
critique = chat([
    {"role": "user", "content": TASK},
    {"role": "assistant", "content": draft},
    {"role": "user", "content": """Review the code above for:
1. Edge cases not handled
2. Security issues
3. Missing error handling
4. Code style problems
List each issue on a new line."""},
])
print(critique)

# Step 3: Revise
print("\n═══ Step 3: Revised Version ═══")
revised = chat([
    {"role": "user", "content": TASK},
    {"role": "assistant", "content": draft},
    {"role": "user", "content": f"Issues found:\n{critique}\n\nRewrite the function addressing ALL issues above."},
])
print(revised)

