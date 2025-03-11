
from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from pytube import Search
import re

class SearchTools:
    def __init__(self):
        self.ddg_search = DuckDuckGoSearchAPIWrapper()
    
    def search_duckduckgo(self, query):
        """Search DuckDuckGo for the given query."""
        results = self.ddg_search.run(query)
        return results[:5]  # Return top 5 results
    
    def search_movie_info(self, movie_name):
        """Search for movie information including IMDB rating and release date."""
        query = f"{movie_name} IMDB rating release date"
        results = self.search_duckduckgo(query)
        
        # Extract IMDB rating using regex
        rating_pattern = r'(\d\.\d)/10'
        rating_match = re.search(rating_pattern, results)
        rating = rating_match.group(1) if rating_match else "Rating not found"
        
        # Extract release year using regex
        year_pattern = r'\((\d{4})\)'
        year_match = re.search(year_pattern, results)
        year = year_match.group(1) if year_match else "Year not found"
        
        return {
            "title": movie_name,
            "rating": rating,
            "year": year,
            "source_data": results
        }
    
    def search_youtube_trailer(self, movie_name):
        """Search YouTube for movie trailers."""
        query = f"{movie_name} official trailer"
        search_results = Search(query)
        
        # Get top 3 results
        videos = []
        for video in search_results.results[:3]:
            videos.append({
                "title": video.title,
                "url": f"https://www.youtube.com/watch?v={video.video_id}"
            })
        
        return videos
    
    def get_tools(self):
        """Return a list of tools that can be used by the agent."""
        tools = [
            Tool(
                name="DuckDuckGoSearch",
                func=self.search_duckduckgo,
                description="Search the web using DuckDuckGo."
            ),
            Tool(
                name="MovieInfoSearch",
                func=self.search_movie_info,
                description="Search for movie information including IMDB rating and release date."
            ),
            Tool(
                name="YouTubeTrailerSearch",
                func=self.search_youtube_trailer,
                description="Search YouTube for movie trailers."
            )
        ]
        return tools
