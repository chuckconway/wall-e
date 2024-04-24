import json
import re
import unittest

from passlib.context import CryptContext

from src.domain.features.parse_chatgpt_transcription.services.transcription_formatter import extract_title_and_summary

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MyTestCase(unittest.TestCase):

    def extract_title_state_body(self, markdown_text):
        title = None
        state = None
        body = None

        # Split the text into lines
        lines = markdown_text.splitlines()
        copy_lines = lines.copy()

        # Find the title
        for line in lines:
            copy_lines.remove(line)
            if line.lstrip().startswith("# "):
                title = line.strip("# ")

            if line.lstrip().startswith("State: "):
                state = line.replace("State: ", "")

            if title is not None and state is not None:
                body = "\n".join(copy_lines)
                break

        return title, state, body

    def test_extract_markdown(self):

        markdown_text = """
        # Async/Await

State: Concept

- Use the pancake idea
- Doing synchronous request with a server who waits for the pancakes and can’t help anyone
- asynchronous server who puts the order in and then waits on other folks, when the cook dings the bell, the server returns and serves the pancakes.\n
        """

        v = self.extract_title_state_body(markdown_text)
        print(v)

    def test_something(self):
        markdown = """
# Writing Expressive Code: Strategies for Human Readability

## Summary
The transcript discusses the importance of writing expressive code that is not just understandable by the compiler, but also by future software engineers. It emphasizes the need for code to demonstrate not just the 'how', but also the 'why'. The talk provides strategies for writing human-readable code and aims to equip the audience with tools to write more expressive code.

### Main Points
- Importance of writing expressive code for future software engineers.
- Most code demonstrates the 'how' but lacks the 'why'.
- The need for strategies to write human-readable code.
- The goal is to provide new tools for writing more expressive code.

### Action Items
- Implement strategies for writing human-readable code.
- Practice writing code that demonstrates the 'why' not just the 'how'.
- Use the new tools provided to write more expressive code.
- Review and revise existing code for expressiveness and readability.

### Follow Up Questions
- What are some common pitfalls when trying to write expressive code?
- Can you provide more examples of tools for writing expressive code?
- How can we measure the expressiveness of our code?
- What are some best practices for maintaining code expressiveness in a team setting?

### Potential Arguments Against
- Writing expressive code might take more time than writing code that just works.
- Not all code may need to be human-readable if it's not going to be maintained or revisited.
- The 'why' behind the code might be better documented in comments or external documentation, not in the code itself.
- Overemphasis on expressiveness might lead to overcomplication of simple code.
        """

        print(extract_title_and_summary(markdown))


if __name__ == '__main__':
    unittest.main()
