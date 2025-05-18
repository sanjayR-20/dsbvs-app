import unittest
from modules.blockchain import generate_hash

class TestBlockchain(unittest.TestCase):

    def test_generate_hash(self):
        data = "test_vote_data"
        expected_length = 64  # SHA-256 hash length
        hash_result = generate_hash(data)
        
        self.assertEqual(len(hash_result), expected_length)
        self.assertIsInstance(hash_result, str)

    def test_generate_hash_different_inputs(self):
        data1 = "vote1"
        data2 = "vote2"
        hash1 = generate_hash(data1)
        hash2 = generate_hash(data2)
        
        self.assertNotEqual(hash1, hash2)

if __name__ == '__main__':
    unittest.main()