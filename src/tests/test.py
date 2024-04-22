import unittest

from passlib.context import CryptContext

from src.domain.features.parse_chatgpt_transcription.services.transcription_formatter import extract_title_and_summary

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MyTestCase(unittest.TestCase):
    def test_something(self):
        markdown = """
        # Title: The Future of Junior Engineers in the Age of AI

# Summary
The speaker discusses the changing landscape of software engineering, particularly for junior engineers, due to the rise of AI technologies like CHAT GPT. They suggest that the traditional path of starting as a junior engineer and working up to senior levels may no longer exist, as AI can automate many tasks previously done by junior engineers. The speaker advises those considering a career in computer science to focus on AI and creating programs with computers.


## Main Points
1. AI technologies like CHAT GPT are automating tasks traditionally done by junior engineers.
2. The traditional career path in software engineering may be disappearing due to AI.
3. Future junior engineers may focus more on decomposing problems for AI to handle.
4. AI currently lacks the ability to innovate and see the bigger picture, roles still needed by human engineers.
5. Those considering computer science should focus on AI and creating programs with computers.

## Action Items
1. Consider the impact of AI on traditional software engineering roles.
2. Evaluate the focus of computer science degrees, considering ones with a focus on AI.
3. Understand the current limitations of AI, such as lack of innovation.
4. Consider how to decompose problems for AI to handle.
5. Prepare for a future where AI may replace many engineering jobs.

## Follow Up Questions
1. How quickly will AI technologies like CHAT GPT evolve to take on more complex tasks?
2. What specific skills should future engineers focus on developing?
3. How can education systems adapt to prepare future engineers for this changing landscape?
4. What roles will remain for human engineers as AI continues to advance?
5. How will the job market change as AI takes over more tasks?

## Potential Arguments Against
1. AI technologies may not advance as quickly or as comprehensively as predicted.
2. Human engineers may still be needed for their unique problem-solving and innovative abilities.
3. The ethical implications of AI taking over human jobs need to be considered.
4. Not all tasks can be decomposed into smaller parts for AI to handle.
5. The reliance on AI could lead to a loss of important human skills and knowledge.
        """

        print(extract_title_and_summary(markdown))


if __name__ == '__main__':
    unittest.main()
