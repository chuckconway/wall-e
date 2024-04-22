import re
import json

from src.domain.features.parse_chatgpt_transcription.title_summary import TitleSummary


# This function takes the output of the create_transcription and chat steps and formats the transcript, summary, and additional info
def run(steps):
    results = {
        "title": "",
        "transcript": "",
        "summary": "",
        "additional_info": ""
    }

    originalTranscript = steps['create_transcription']['return_value']['transcription']

    def splitStringIntoSentences(str):
        if not str:
            return ["Null argument"]

        if not re.search(r'(?:^|[^.!?]+)[.!?]+\s?', str):
            str += str + "."

        sentences = re.findall(r'(?:^|[^.!?]+)[.!?]+\s?', str) or []

        result = []

        if len(sentences) > 1:
            for i in range(0, len(sentences), 3):
                result.append(' '.join(sentences[i:i + 3]))
        else:
            maxLength = 800
            words = sentences[0].split(' ')
            currentLine = ''

            for word in words:
                lengthWithWord = len(currentLine) + len(word)

                if lengthWithWord <= maxLength:
                    currentLine += ('' if len(currentLine) == 0 else ' ') + word
                else:
                    result.append(currentLine)
                    currentLine = word

            if len(currentLine) > 0:
                result.append(currentLine)

        return result

    def joinArrayWithBlankLine(arr):
        return '\n\n'.join(arr)

    transcriptArray = splitStringIntoSentences(originalTranscript)

    results['transcript'] = joinArrayWithBlankLine(transcriptArray)

    summary = steps['chat']['return_value']['choices'][0]['message']['content']

    def splitSummary(str):
        titleDelimiter = r'^.*\n\n'
        summaryDelimiter = r'\n\s*?--Summary--\s*?\n\s*'
        additionalInfoDelimiter = r'\n\s*?--Additional Info--\s*?\n\s*'

        titleMatch = re.search(titleDelimiter, str)
        summaryMatch = re.search(summaryDelimiter, str)
        additionalInfoMatch = re.search(additionalInfoDelimiter, str)

        if not titleMatch or not summaryMatch or not additionalInfoMatch:
            print("One or more delimiters not found")
            return str
        else:
            titleIndex = titleMatch.start()
            summaryIndex = summaryMatch.start()
            additionalInfoIndex = additionalInfoMatch.start()

            results['title'] = str[0:titleIndex + len(titleMatch.group(0))].strip().replace(r'^#\s*', "")
            results['summary'] = str[summaryIndex + len(summaryMatch.group(0)):additionalInfoMatch.start()].strip()
            results['additional_info'] = str[additionalInfoIndex + len(additionalInfoMatch.group(0)):].strip()

    splitSummary(summary)

    return results


def extract_title_and_summary(markdown) -> TitleSummary:
    lines = markdown.split('\n')
    title_line = [line for line in lines if line.lstrip().startswith("# Title:")][0]
    title = title_line.lstrip().replace('# Title: ', '')
    lines.remove(title_line)
    summary = '\n'.join(lines)

    title_summary = TitleSummary()
    title_summary.title = title
    title_summary.summary = summary

    # return json.dumps({'title': title, 'summary': summary})
    return title_summary
