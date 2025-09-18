
import re
from collections import Counter

def financial_analyst(text: str) -> dict:
    """
    Simple rule-based financial analysis:
    - counts words
    - finds mentions of key financial terms
    - extracts numbers that look like amounts
    """
    if not text:
        return {"error": "no text provided"}
    # lowercase for counting
    lc = text.lower()
    words = re.findall(r"\b\w+\b", lc)
    word_count = len(words)
    common = Counter(words).most_common(10)
    keywords = {}
    for kw in ["revenue", "profit", "loss", "net", "income", "expense", "cash", "ebitda", "guidance", "growth"]:
        keywords[kw] = lc.count(kw)
    # find numbers (simple)
    numbers = re.findall(r"[\$]?\d{1,3}(?:[,]\d{3})*(?:\.\d+)?", text)
    return {
        "word_count": word_count,
        "top_words": common,
        "keyword_counts": keywords,
        "found_numbers_sample": numbers[:20]
    }
