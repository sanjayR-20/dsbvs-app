def generate_hash(data):
    import hashlib
    import json

    # Convert the data to a JSON string and encode it
    json_data = json.dumps(data, sort_keys=True).encode()
    
    # Create a SHA-256 hash of the data
    return hashlib.sha256(json_data).hexdigest()