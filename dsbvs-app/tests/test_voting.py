import unittest
from modules.voting import process_vote, store_vote

class TestVoting(unittest.TestCase):

    def setUp(self):
        self.vote_data = {
            'voter_id': 'test_voter_1',
            'vote': 'positive'
        }

    def test_process_vote_valid(self):
        result = process_vote(self.vote_data['voter_id'], self.vote_data['vote'])
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Vote processed successfully.')

    def test_process_vote_duplicate(self):
        process_vote(self.vote_data['voter_id'], self.vote_data['vote'])
        result = process_vote(self.vote_data['voter_id'], 'negative')
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Duplicate voter ID detected.')

    def test_store_vote(self):
        result = store_vote(self.vote_data['voter_id'], self.vote_data['vote'])
        self.assertTrue(result)
        # Additional checks can be added here to verify the storage mechanism

if __name__ == '__main__':
    unittest.main()