import unittest

from passlib.context import CryptContext

from src.domain.features.parse_chatgpt_transcription.services.transcription_formatter import extract_title_and_summary

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MyTestCase(unittest.TestCase):
    def test_something(self):
        markdown = """
        # Title: This is the title
        This is the first line of the summary.
        This is the second line of the summary.
        """

        print(extract_title_and_summary(markdown))


if __name__ == '__main__':
    unittest.main()
