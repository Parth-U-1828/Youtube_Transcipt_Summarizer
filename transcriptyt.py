import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Configure Gemini API
API_KEY = "paste your Gemini API key here"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|/v/|/e/|watch\?v=|&v=)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_url):
    """Fetches the transcript from a YouTube video."""
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL"
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def summarize_text(text):
    """Summarizes the text using the Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Summarize the following YouTube transcript into detailed bullet points:\n{text}"
    response = model.generate_content(prompt)
    return response.text if response.text else "Failed to generate summary."

def main():
    st.set_page_config(page_title="YouTube Transcript Summarizer", page_icon="🎥", layout="wide")
    st.title("📜 YouTube Transcript Summarizer")
    st.markdown("## Get crisp, detailed notes from YouTube videos!")
    
    url = st.text_input("Enter YouTube Video URL:")
    if st.button("Summarize Video"):
        with st.spinner("Fetching transcript..."):
            transcript = get_transcript(url)
        
        if "Error" in transcript or "Invalid" in transcript:
            st.error(transcript)
        else:
            with st.spinner("Summarizing transcript..."):
                summary = summarize_text(transcript)
            
            st.subheader("🔹 Summary Notes")
            st.markdown(summary.replace("-", "\n-"))  # Format as bullet points

if __name__ == "__main__":
    main()
