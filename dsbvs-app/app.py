import os
import json
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

VOTES_FILE = 'votes.json'
RESULTS_IMG = os.path.join('static', 'results.png')
PARTIES = ["DMK", "TVK", "AIADMK", "BJP", "INC", "NTK", "DMDK"]

# --- Sentiment Analysis Module ---
def analyze_sentiment(comment):
    """
    Analyze comment sentiment and return a weight between 0.5 and 1.0.
    The stronger the sentiment (positive or negative), the closer to 1.0 or 0.5.
    """
    if not comment.strip():
        return 0.75, 0.0  # Neutral weight, neutral polarity
    try:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity  # -1.0 (neg) to 1.0 (pos)
        # Map polarity [-1, 1] to weight [0.5, 1.0]
        weight = 0.75 + 0.25 * polarity  # 0.5 for -1, 0.75 for 0, 1.0 for +1
        weight = max(0.5, min(1.0, weight))
        return round(weight, 2), round(polarity, 2)
    except Exception:
        return 0.75, 0.0

# --- Vote Hashing Module ---
def generate_hash(vote_data, prev_hash):
    """Generate SHA-256 hash for the vote."""
    vote_string = (
        vote_data['voterId'] + vote_data['voterName'] + vote_data['party'] +
        vote_data['comment'] + str(vote_data['timestamp']) + (prev_hash or '')
    )
    return hashlib.sha256(vote_string.encode('utf-8')).hexdigest()

# --- Data Storage Module ---
def load_votes():
    """Load votes from the JSON file."""
    if not os.path.exists(VOTES_FILE):
        return []
    with open(VOTES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_votes(votes):
    """Save votes to the JSON file."""
    with open(VOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(votes, f, indent=2, ensure_ascii=False)

def is_duplicate_voter(votes, voter_id):
    """Check for duplicate voter ID."""
    return any(v['voterId'] == voter_id for v in votes)

# --- Result Visualization Module ---
def aggregate_results(votes):
    """Aggregate weighted votes per party."""
    results = {party: 0.0 for party in PARTIES}
    for v in votes:
        if v['party'] in results:
            results[v['party']] += v['weight']
    return results

def generate_bar_chart(results):
    """Generate and save a bar chart of results."""
    parties = list(results.keys())
    votes = [results[p] for p in parties]
    plt.figure(figsize=(8, 5))
    colors = ['#ef4444', '#3b82f6', '#f59e42', '#10b981', '#a21caf', '#fbbf24', '#6366f1']
    bars = plt.bar(parties, votes, color=colors)
    plt.xlabel('Party')
    plt.ylabel('Total Weighted Votes')
    plt.title('Sentiment-Weighted Voting Results')
    plt.ylim(0, max(votes + [1]) * 1.2)
    for bar, vote in zip(bars, votes):
        height = bar.get_height()
        # Always show label, even if height is zero
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.05, f"{vote:.2f}", ha='center', va='bottom', fontsize=10)
        # If bar is zero, draw a faint line for visibility
        if height == 0:
            plt.plot([bar.get_x(), bar.get_x() + bar.get_width()], [0.02, 0.02], color=bar.get_facecolor(), linewidth=6, alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_IMG)
    plt.close()
    
    # Ensure the image is saved in the static directory    
def results_summary(results):
    """Create a text summary of results."""
    lines = [f"{party}: {votes:.2f} weighted votes" for party, votes in results.items()]
    return "\n".join(lines)

# --- Main Voting Logic ---
def process_vote(data):
    """Process a vote: validate, analyze, hash, store."""
    # Validate input
    voter_id = data.get('voterId', '').strip()
    voter_name = data.get('voterName', '').strip()
    party = data.get('party', '').strip()
    comment = data.get('comment', '').strip()
    if not voter_id or len(voter_id) > 10:
        return False, "Invalid Voter ID.", None
    if not voter_name or len(voter_name) > 50:
        return False, "Invalid Voter Name.", None
    if party not in PARTIES:
        return False, "Invalid party selection.", None
    if len(comment) > 200:
        return False, "Comment too long.", None

    votes = load_votes()
    if is_duplicate_voter(votes, voter_id):
        return False, "Duplicate Voter ID. Only one vote allowed per ID.", None

    weight, polarity = analyze_sentiment(comment)
    timestamp = datetime.now().isoformat()
    prev_hash = votes[-1]['hash'] if votes else ''
    vote_data = {
        'voterId': voter_id,
        'voterName': voter_name,
        'party': party,
        'comment': comment,
        'sentiment': polarity,
        'weight': weight,
        'timestamp': timestamp,
        'prev_hash': prev_hash
    }
    vote_hash = generate_hash(vote_data, prev_hash)
    vote_data['hash'] = vote_hash
    votes.append(vote_data)
    save_votes(votes)
    return True, f"Vote recorded! Sentiment weight: {weight:.2f}", votes

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    success, message, votes = process_vote(data)
    if not success:
        return jsonify({'success': False, 'message': message})
    results = aggregate_results(votes)
    summary = results_summary(results)
    generate_bar_chart(results)
    return jsonify({'success': True, 'message': message, 'summary': summary})

@app.route('/results', methods=['GET'])
def results():
    votes = load_votes()
    if not votes:
        return jsonify({'success': False, 'message': 'No votes yet.', 'summary': ''})
    results = aggregate_results(votes)
    summary = results_summary(results)
    generate_bar_chart(results)
    return jsonify({'success': True, 'message': 'Results updated.', 'summary': summary})

# --- Sample Votes for Testing ---
def add_sample_votes():
    """Add 10 sample votes if votes.json is empty."""
    if os.path.exists(VOTES_FILE) and load_votes():
        return
    sample_data = [
        {"voterId": f"TN00{i:02d}", "voterName": f"User{i}", "party": party, "comment": comment}
        for i, (party, comment) in enumerate([
            ("DMK", "Great vision for the state!"),
            ("AIADMK", "Stable leadership and good governance."),
            ("BJP", "Development and national integration."),
            ("INC", "Historic party with new ideas."),
            ("NTK", "Focus on environment and youth."),
            ("DMDK", "Fresh perspective in politics."),
            ("DMK", "Progressive policies."),
            ("AIADMK", "Strong welfare schemes."),
            ("BJP", "Bold reforms."),
            ("TVK", "Youthful energy and new leadership.")  # Added TVK sample
        ], 1)
    ]
    votes = []
    prev_hash = ''
    for entry in sample_data:
        weight, polarity = analyze_sentiment(entry['comment'])
        timestamp = datetime.now().isoformat()
        vote_data = {
            'voterId': entry['voterId'],
            'voterName': entry['voterName'],
            'party': entry['party'],
            'comment': entry['comment'],
            'sentiment': polarity,
            'weight': weight,
            'timestamp': timestamp,
            'prev_hash': prev_hash
        }
        vote_hash = generate_hash(vote_data, prev_hash)
        vote_data['hash'] = vote_hash
        votes.append(vote_data)
        prev_hash = vote_hash
    save_votes(votes)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    add_sample_votes()
    app.run(debug=True)