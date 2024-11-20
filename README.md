
# YouTube Video Transcript and Summary Generator

This project provides a Python script to extract and summarize transcripts from YouTube videos. The summary and (optionally) the full transcript are saved to a PDF file for easy reference.

## Features

- Extract transcripts from YouTube videos (if captions are available).
- Generate detailed summaries using OpenAI's GPT models (`gpt-4o-mini` or `gpt-4o`).
- Save the summary (and optionally, the full transcript) as a well-structured PDF.
- Configure model parameters, such as maximum tokens and temperature, interactively.
- User-friendly CLI-based interaction.

## Motivation

The inspiration for this project came from the valuable but often lengthy interviews found on channels like the [Lex Fridman Podcast](https://www.youtube.com/c/LexFridman). These discussions are rich in content but can be time-consuming to watch in their entirety. This tool allows users to extract and summarize key information, saving time while retaining the value of the content.

## Prerequisites

- Python 3.10.12 or later (Development/testing version, may work with other versions).
- OpenAI API key.
- The YouTube video must have captions (automatic or manual).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/antoniocostabr/youtube-summary-generator.git
   cd youtube-summary-generator
   ```

2. **Install Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

   Dependencies include:
   - `youtube-transcript-api`
   - `openai`
   - `fpdf`
   - `python-dotenv`

3. **Set Up Environment**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. **Run the Script**:
   ```bash
   python src/summary.py
   ```

2. **Provide Input**:
   - Enter the YouTube video URL.
   - Select the OpenAI model (`gpt-4o-mini` or `gpt-4o`).
   - Specify whether to include the transcript in the PDF.
   - Configure maximum tokens and temperature for the model.

3. **Output**:
   A PDF file will be saved in the `./data` folder with the summary. Optionally the full transcript can be added.

## Example Output

The script generates a PDF with the following structure:
- **Title**: "YouTube Video Transcript and Summary"
- **Summary**: A detailed overview of the video, including main topics, participants, and conclusions.
- **Transcript** (optional): The full text of the video transcript.

## Example Input and Output

### Input:
- YouTube Video URL: `https://youtu.be/ugvHCXCOmm4`
- Model Selection: `gpt-4o-mini`
- Include Transcript: `y`
- Maximum Tokens: `1000`
- Temperature: `0.3`

### Output:
PDF saved as `./data/youtube_transcript_summary.pdf`.

---

## Customization

- **Model Selection**:
  - Choose between `gpt-4o-mini` (lighter model) and `gpt-4o` (more detailed responses).
- **Parameters**:
  - Adjust `max_tokens` for summary length and `temperature` for model creativity.
- **Output Path**:
  - The default output path is `./data/youtube_transcript_summary.pdf`, but this can be modified.

## Limitations

- Requires captions for the YouTube video.
- Depends on OpenAI's API for summarization, which may incur usage costs.
- Long transcripts may exceed token limits for summarization.

## Future Enhancements

- Add support for multilingual transcripts and summaries.
- Enhance CLI interactivity and error handling.
- Include advanced PDF formatting for better readability.

## Acknowledgments

Special thanks to:
- [Lex Fridman](https://www.youtube.com/c/LexFridman) for inspiring this project with his thought-provoking interviews.
- [OpenAI](https://openai.com/) for their powerful language models.
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/) for enabling transcript extraction.
