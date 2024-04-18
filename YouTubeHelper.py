from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
import re


class YouTubeHelper:
    def __init__(self, url: str):
        self.url = url
        self.languages = ['en', 'vi']
        self.video_id = self.extract_video_id()


    def extract_video_id(self) -> str:
        """ Extracts the video ID from the YouTube URL. """
        # Regular expression for extracting the video ID from a YouTube URL
        regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/" \
                r"|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, self.url)
        if not match:
            raise ValueError("Invalid YouTube URL")
        return match.group(1)


    def get_transcript(self) -> List | str:
        """ Fetches the transcript of the YT video as a list of dict items """
        try:
            return YouTubeTranscriptApi.get_transcript(
                video_id=self.video_id,
                languages=self.languages
            )
        except Exception as e:
            return str(e)


    def get_formatted_transcript(self) -> str:
        """ Returns transcript formatted w/ timestamps for easy processing """
        try:
            transcript_list = self.get_transcript()
            if isinstance(transcript_list, str):  # In case of an error message
                return transcript_list

            formatted_transcript = ""
            for item in transcript_list:
                time = self.convert_seconds_to_time(item['start'])
                text = item['text']
                formatted_transcript += f"[{time}] {text}\n"

            return formatted_transcript
        except Exception as e:
            return str(e)


    @staticmethod
    def convert_seconds_to_time(seconds: float) -> str:
        """ Converts seconds to a time format (HH:MM:SS). """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
