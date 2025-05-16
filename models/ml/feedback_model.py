from textblob import TextBlob

def process_feedback(feedback_text: str) -> str:
    analysis = TextBlob(feedback_text)
    score = analysis.sentiment.polarity

    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    else:
        return "neutral"

# Optional: CLI testing
if __name__ == "__main__":
    import sys
    feedback_input = sys.stdin.read()
    result = process_feedback(feedback_input)
    print(result)
