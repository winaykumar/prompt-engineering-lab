"""
Experiment 04: Structured Output
Extracts structured JSON from a product review using schema + Pydantic validation.
"""
import json
from pydantic import BaseModel, ValidationError
from config import chat


# Define the expected schema
class ProductReview(BaseModel):
    product_name: str
    sentiment: str       # POSITIVE, NEGATIVE, NEUTRAL
    key_pros: list[str]
    key_cons: list[str]
    score: float         # 1.0 to 5.0


REVIEW = """The Sony WH-1000XM5 headphones have amazing noise cancellation 
and very comfortable ear cups. Battery lasts about 30 hours which is great. 
However, they don't fold flat anymore which makes travel harder, and the 
price of $400 feels steep compared to alternatives."""

result = chat([
    {"role": "system", "content": """You are a product review analyser. 
Extract structured data from reviews. 
Respond with ONLY valid JSON matching this schema:
{
  "product_name": "string",
  "sentiment": "POSITIVE | NEGATIVE | NEUTRAL",
  "key_pros": ["string"],
  "key_cons": ["string"],
  "score": 1.0 to 5.0
}"""},
    {"role": "user", "content": REVIEW},
])

print("Raw output:")
print(result)
print()

# Parse and validate
try:
    data = json.loads(result)
    review = ProductReview(**data)
    print(f"✅ Valid! Product: {review.product_name}")
    print(f"   Sentiment: {review.sentiment}, Score: {review.score}")
    print(f"   Pros: {review.key_pros}")
    print(f"   Cons: {review.key_cons}")
except (json.JSONDecodeError, ValidationError) as e:
    print(f"❌ Parse error: {e}")
