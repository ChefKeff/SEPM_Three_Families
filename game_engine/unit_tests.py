import unittest
import json
import sys
sys.path.insert(0, '../')
from game_engine.generateOutputFile import generate_move_create_output

class TestMethods(unittest.TestCase):

    def test_basic(self):
        with open('outputFile.json', 'r') as f:
            File1 = json.load(f)  
        generate_move_create_output()
        with open('outputFile.json', 'r') as f:
            File2 = json.load(f)  
        self.assertNotEqual(File1, File2)

        



if __name__ == '__main__':
    unittest.main()