import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# My Title\n\nSome content here."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")
        
    def test_extract_title_no_title(self):
        markdown = "No title here."
        with self.assertRaises(ValueError):
            extract_title(markdown)
            
if __name__ == '__main__':
    unittest.main()