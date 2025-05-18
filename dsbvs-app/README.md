# Decentralized Sentiment-Based Voting System (DSBVS)

## Overview
The Decentralized Sentiment-Based Voting System (DSBVS) is a web application that allows users to cast votes based on sentiment analysis of comments. The application leverages blockchain technology to ensure the integrity and transparency of the voting process.

## Features
- **Sentiment Analysis**: Utilizes the TextBlob library to analyze user comments and determine their sentiment, which influences the weight of the vote.
- **Decentralized Voting**: Implements a blockchain-inspired approach to securely store votes and maintain a transparent voting process.
- **User-Friendly Interface**: A modern and responsive design that allows users to easily navigate and participate in the voting process.

## Project Structure
```
dsbvs-app
├── app.py                  # Main entry point for the Flask application
├── requirements.txt        # Python dependencies for the project
├── README.md               # Project documentation
├── static
│   ├── css
│   │   └── style.css       # Custom CSS styles
│   └── js
│       └── main.js         # JavaScript for user interactions
├── templates
│   └── index.html          # Main HTML template for the application
├── modules
│   ├── sentiment_analysis.py # Functions for sentiment analysis
│   ├── voting.py           # Voting logic and storage
│   └── blockchain.py       # Blockchain functionality for hashing
└── tests
    ├── test_sentiment_analysis.py # Unit tests for sentiment analysis
    ├── test_voting.py      # Unit tests for voting logic
    └── test_blockchain.py  # Unit tests for blockchain functions
```

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd dsbvs-app
   ```

2. **Install Dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the Flask application by running:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage Guidelines
- Navigate to the main page to view the voting form.
- Enter your comment and submit your vote.
- The results will be displayed based on the sentiment analysis of the comments.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.