import re
from collections import Counter
from typing import Dict, Any

def summarize_text(text: str, max_sentences: int = 3) -> str:
    # naive sentence split and take first N sentences
    sents = [s.strip() for s in re.split(r'(?<=[\.\?\!])\s+', text) if s.strip()]
    return " ".join(sents[:max_sentences])

def extract_key_figures(text: str) -> Dict[str, Any]:
    # look for common financial terms followed by numbers
    key_terms = {
        "revenue": r"(?:revenue|sales)[^\d\$\n\r]{0,40}([\$]?\s?[\d,]+(?:\.\d+)?)",
        "net_income": r"(?:net income|net profit|profit|loss)[^\d\$\n\r]{0,40}([\$]?\s?[-]?\d[\d,\,]*(?:\.\d+)?)",
        "eps": r"(?:eps|earnings per share)[^\d\$\n\r]{0,40}([\$]?\s?[\d,]+(?:\.\d+)?)",
        "ebitda": r"(?:ebitda)[^\d\$\n\r]{0,40}([\$]?\s?[\d,]+(?:\.\d+)?)",
        "cash": r"(?:cash)[^\d\$\n\r]{0,40}([\$]?\s?[\d,]+(?:\.\d+)?)",
        "guidance": r"(?:guidance)[^\d\$\n\r]{0,80}([\$]?\s?[\d,]+(?:\.\d+)?)"
    }
    results = {}
    for k, pat in key_terms.items():
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            results[k] = m.group(1).strip()
    # also find any big numbers standalone
    numbers = re.findall(r"[\$]?\d{1,3}(?:[,]\d{3})*(?:\.\d+)?", text)
    results["numbers_found"] = numbers[:20]
    return results

def compute_simple_metrics(figures: dict) -> dict:
    res = {}
    def parse_num(s):
        if not s: return None
        s = s.replace("$","").replace(",","").strip()
        try:
            return float(s)
        except:
            return None
    rev = parse_num(figures.get("revenue","") or "")
    net = parse_num(figures.get("net_income","") or "")
    if rev and net is not None:
        try:
            res["profit_margin"] = net / rev if rev!=0 else None
        except Exception:
            res["profit_margin"] = None
    else:
        res["profit_margin"] = None
    return res

def financial_analyst(text: str) -> dict:
    if not text:
        return {"error": "no text provided"}
    lc = text.lower()
    words = re.findall(r"\b\w+\b", lc)
    word_count = len(words)
    common = Counter(words).most_common(10)
    keywords = {kw: lc.count(kw) for kw in ["revenue","profit","loss","net","income","expense","cash","ebitda","guidance","growth"]}
    summary = summarize_text(text, max_sentences=3)
    figures = extract_key_figures(text)
    metrics = compute_simple_metrics(figures)
    recommendation = "insufficient data"
    if metrics.get("profit_margin"):
        pm = metrics["profit_margin"]
        if pm is not None:
            if pm > 0.15:
                recommendation = "positive"
            elif pm > 0.05:
                recommendation = "neutral"
            else:
                recommendation = "negative"
    return {
        "word_count": word_count,
        "top_words": common,
        "keyword_counts": keywords,
        "summary": summary,
        "key_figures": figures,
        "metrics": metrics,
        "recommendation": recommendation
    }
