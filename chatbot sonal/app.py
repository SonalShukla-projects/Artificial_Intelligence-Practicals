from __future__ import annotations


import math
import re
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

FAQS = [
    {
        "q": "What is this AI post lab?",
        "a": "This lab demonstrates how AI-style tools can answer FAQs using intent + keyword matching. It's a lightweight offline chatbot you can extend.",
        "tags": ["ai", "lab", "post", "overview", "purpose"],
    },
    {
        "q": "How does the chatbot work?",
        "a": "It scores your question against FAQ keywords, picks the best match, and replies. If nothing matches, it generates a helpful fallback answer.",
        "tags": ["work", "working", "algorithm", "intent", "matching", "keywords"],
    },
    {
        "q": "Can I add more questions?",
        "a": "Yes. Add items in the FAQS list in app.py. Include tags to improve matching accuracy.",
        "tags": ["add", "questions", "faq", "update", "edit"],
    },
    {
        "q": "Does it need the internet?",
        "a": "No. This chatbot works offline. You can later connect it to an API for real AI responses.",
        "tags": ["offline", "internet", "api", "online"],
    },
    {
        "q": "Can it generate images?",
        "a": "This version is text-based. You can upgrade it by calling an image generation API and showing the image in the chat window.",
        "tags": ["image", "generate", "generation", "picture"],
    },
]

SMALL_TALK = [
    "Hello! Ask me anything, and I'll do my best to help.",
    "Hi there! You can ask about tech, study topics, or math.",
    "Hey! I'm an offline smart bot. Try asking a clear question.",
]

MATH_FUNCS: Dict[str, Any] = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
    "round": round,
    "log10": math.log10,
    "log": math.log10,  # user-friendly log base 10
    "ln": math.log,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
}


@app.route("/")
def index() -> str:
    return render_template("index.html")


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score_match(user_input: str, faq: Dict[str, Any]) -> int:
    words = normalize(user_input).split()
    score = 0
    for word in words:
        if word in faq["tags"]:
            score += 2
        if word in normalize(faq["q"]):
            score += 1
    return score


def try_greeting(user_input: str) -> str | None:
    text = normalize(user_input)
    if re.search(r"\b(hi|hello|hey|namaste)\b", text):
        return SMALL_TALK[int(datetime.now().timestamp()) % len(SMALL_TALK)]
    return None


def try_time_date(user_input: str) -> str | None:
    text = normalize(user_input)
    if "time" in text or "date" in text or "day" in text:
        now = datetime.now()
        return f"Right now it is {now.strftime('%H:%M:%S')} on {now.strftime('%d %b %Y')}."
    return None


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Negative factorial")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def safe_eval_math(expr: str) -> float | None:
    expr = expr.replace(",", "").lower()
    if not re.fullmatch(r"[0-9+\-*/().\s^%!a-z]+", expr):
        return None

    expr = expr.replace("^", "**")
    expr = re.sub(r"(\d+)\s*!", r"factorial(\1)", expr)

    safe_env: Dict[str, Any] = {"__builtins__": {}}
    safe_env.update(MATH_FUNCS)
    safe_env["factorial"] = factorial

    try:
        value = eval(expr, safe_env, {})
    except Exception:
        return None

    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
    return None


def get_response(user_input: str) -> str:
    greeting = try_greeting(user_input)
    if greeting:
        return greeting

    time_date = try_time_date(user_input)
    if time_date:
        return time_date

    math_answer = safe_eval_math(user_input)
    if math_answer is not None:
        if math_answer.is_integer():
            return f"Answer: {int(math_answer)}"
        return f"Answer: {math_answer}"

    best = None
    best_score = 0
    for faq in FAQS:
        score = score_match(user_input, faq)
        if score > best_score:
            best_score = score
            best = faq

    if best and best_score >= 2:
        return best["a"]

    return (
        f"I couldn't find an exact FAQ for \"{user_input}\". "
        "This is an offline smart bot. Try a simpler question, or add knowledge inside app.py."
    )


@app.route("/chat", methods=["POST"])
def chat() -> Any:
    data = request.get_json(silent=True) or {}
    text = str(data.get("message", "")).strip()
    if not text:
        return jsonify({"reply": "Please type a question."})
    return jsonify({"reply": get_response(text)})


if __name__ == "__main__":
    app.run(debug=True)
