def analyze_sentiment(comment):
    from textblob import TextBlob

    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity

    # Determine vote weight based on polarity
    if polarity > 0:
        vote_weight = 1  # Positive sentiment
    elif polarity < 0:
        vote_weight = -1  # Negative sentiment
    else:
        vote_weight = 0  # Neutral sentiment

    return polarity, vote_weight