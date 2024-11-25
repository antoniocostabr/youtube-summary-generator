from youtube_transcript_api import YouTubeTranscriptApi
import openai
import re
import os
import dotenv
from fpdf import FPDF
from typing import Optional


def load_openai_credentials() -> str:
    dotenv.load_dotenv()
    return os.getenv("OPENAI_API_KEY")


def extract_video_id(youtube_url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    try:
        # Match common YouTube URL formats
        video_id_match = re.search(r"(?:v=|\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})", youtube_url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")
    except Exception as e:
        return f"Error extracting video ID: {e}"


def get_youtube_transcript(video_id: str, language: str='en') -> str:
    """
    Fetch the transcript of a YouTube video given its video ID.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=(language,))
        # Combine transcript into a single string
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"Error fetching transcript: {e}"


def summarize_text(text,
                   max_tokens=150,
                   temperature=0.3,
                   model_string: str = 'gpt-4o-mini') -> Optional[str]:
    """
    Use OpenAI's API to summarize the provided text using GPT-4-turbo.
    """
    # Set your OpenAI API key
    openai.api_key = load_openai_credentials()

    client = openai.OpenAI()

    try:
        completion = client.chat.completions.create(
            model=model_string,
            messages=[
                {   "role": "system", "content": "You are a helpful assistant with the aim of summaryzing youtube videos."},
                {
                    "role": "user",
                    "content": f"""The following is a transcript of a YouTube video.
                    Please summarize it, highlighting the main topics discussed,
                    key conclusions, participants, and any other relevant information.
                    Use clear and concise language to provide a comprehensive overview
                    of the content. Be as detailed as possible using up to {max_tokens} tokens.
                    Transcript:\n\n{text}"""
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing text: {e}"


def save_to_pdf(youtube_url: str,
                summary:str,
                output_path:str,
                transcript: Optional[str] = None ,
                include_transcript: bool=False):
    """
    Save the transcript and summary to a PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "YouTube Video Transcript and Summary", ln=True, align='C')
    pdf.ln(10)  # Add some vertical spacing

    # Add the youtube url
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, youtube_url, ln=True, align='C')
    pdf.ln(10)  # Add some vertical spacing

    # Add Summary
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, "Summary:", ln=True)
    pdf.multi_cell(0, 10, summary)

    if include_transcript:
        pdf.ln(10)  # Add spacing main text

        # Add Transcript
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, "Transcript:", ln=True)
        pdf.multi_cell(0, 10, transcript)

    # Save PDF
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"PDF saved at: {output_path}")


def main():
    youtube_url = input("Enter the YouTube video URL: ")

    model_type = input(
        "Which model do you want to use? (m: gpt-4o-mini or 4: gpt-4o):")

    if model_type == "4":
        model_str = "gpt-4o"
    else:
        model_str = "gpt-4o-mini"

    include_transcript_str = input("Include the transcript in the PDF? (y/n): ")
    include_transcript = include_transcript_str.strip().lower() == "y"

    language = \
        input("Enter the language of the transcript (e.g en for english or pt for portuguese): ")

    if len(language) == 0:
        language = 'en'

    max_tokens = input("Enter the maximum number of tokens: ")

    try:
        max_tokens = int(max_tokens)
    except ValueError:
        print("Invalid input for max_tokens. Using default value of 150.")
        max_tokens = 150

    temperature = input("Enter the temperature for the model (0-1): ")
    try:
        temperature = float(temperature)
    except ValueError:
        print("Invalid input for temperature. Using default value of 0.3.")
        temperature = 0.3



    # Step 1: Extract video ID
    print("Extracting video ID...")
    video_id = extract_video_id(youtube_url)
    if "Error" in video_id:
        print(video_id)
    else:
        print(f"Video ID extracted: {video_id}")

        # Step 2: Fetch the transcript
        print("Fetching YouTube transcript...")
        transcript = get_youtube_transcript(video_id, language=(language))
        if "Error" in transcript:
            print(transcript)
        else:
            print("Transcript fetched successfully.")

            # Step 3: Summarize the transcript
            print("Summarizing transcript...")
            summary = summarize_text(transcript,
                                     max_tokens=1000,
                                     temperature=0.3,
                                     model_string=model_str)

            # Step 4: Save to PDF
            output_path = "./data/youtube_transcript_summary.pdf"
            save_to_pdf(youtube_url,
                        summary,
                        output_path,
                        transcript,
                        include_transcript=include_transcript)


if __name__ == "__main__":
    # Example YouTube video URL
    main()
