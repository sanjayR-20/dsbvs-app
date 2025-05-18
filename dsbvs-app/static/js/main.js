// This file contains JavaScript code for form validation, handling user interactions, and making API calls to the Flask backend using the fetch API.

document.addEventListener('DOMContentLoaded', function() {
    const voteForm = document.getElementById('vote-form');
    const resultContainer = document.getElementById('result-container');

    voteForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const voterId = document.getElementById('voter-id').value;
        const comment = document.getElementById('comment').value;
        const vote = document.querySelector('input[name="vote"]:checked').value;

        if (!voterId || !comment || !vote) {
            alert('Please fill in all fields.');
            return;
        }

        const payload = {
            voter_id: voterId,
            comment: comment,
            vote: vote
        };

        fetch('/submit_vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResults(data.results);
                voteForm.reset();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function displayResults(results) {
        resultContainer.innerHTML = '';
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.textContent = `${result.comment}: ${result.vote}`;
            resultContainer.appendChild(resultItem);
        });
    }
});