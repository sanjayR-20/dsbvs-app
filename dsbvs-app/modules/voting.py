from flask import jsonify
import json
import os

VOTES_FILE = 'votes.json'

def load_votes():
    if not os.path.exists(VOTES_FILE):
        return []
    with open(VOTES_FILE, 'r') as file:
        return json.load(file)

def save_votes(votes):
    with open(VOTES_FILE, 'w') as file:
        json.dump(votes, file)

def process_vote(voter_id, vote):
    votes = load_votes()
    
    # Check for duplicate voter ID
    if any(vote['voter_id'] == voter_id for vote in votes):
        return jsonify({'error': 'Voter ID already exists'}), 400
    
    # Store the vote
    votes.append({'voter_id': voter_id, 'vote': vote})
    save_votes(votes)
    
    return jsonify({'message': 'Vote processed successfully'}), 200

def get_votes():
    votes = load_votes()
    return jsonify(votes), 200

def clear_votes():
    if os.path.exists(VOTES_FILE):
        os.remove(VOTES_FILE)
    return jsonify({'message': 'Votes cleared successfully'}), 200