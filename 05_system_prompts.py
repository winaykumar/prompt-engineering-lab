"""
Experiment 05: System Prompts
Same user question with 3 different system prompts showing persona effects.
"""
from config import chat

USER_Q = "Should I use microservices for my new project?"

PERSONAS = [
    ("Startup CTO", "You are a pragmatic startup CTO. Keep answers short. Prioritize shipping fast over architectural purity. Be direct and opinionated."),
    ("Enterprise Architect", "You are a senior enterprise architect at a Fortune 500 company. Consider scalability, team structure, compliance, and long-term maintenance. Be thorough."),
    ("5-year-old explainer", "You explain everything as if talking to a 5-year-old. Use simple words, analogies with toys and food, and keep it under 3 sentences."),
]

for name, system in PERSONAS:
    print(f"\n{'='*50}")
    print(f"Persona: {name}")
    print(f"{'='*50}")
    result = chat([
        {"role": "system", "content": system},
        {"role": "user", "content": USER_Q},
    ])
    print(result)

