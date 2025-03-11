from langchain.agents import initialize_agent
import os
from dotenv import load_dotenv

class SearchTools:
    def __init__(self):
        self.search = DuckDuckGoSearchAPIWrapper()
    
    def get_tools(self):
        return [
            Tool(
                name="DuckDuckGo Search",
                func=self.search.run,
                description="Searches the web using DuckDuckGo"
            )
        ]

class RAGEngine:
    def __init__(self):
        load_dotenv()
       
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.search_tools = SearchTools()
      
        self.agent = initialize_agent(
            tools=self.search_tools.get_tools(),
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    
    def process_query(self, query):
        """Process a user query and return the response."""
        response = self.agent.run(query)
        return response
    
    def get_chat_history(self):
        """Return the current chat history."""
        return self.memory.chat_memory.messages
from langchain.agents import initialize_agent
import os
from dotenv import load_dotenv

class SearchTools:
    def __init__(self):
        self.search = DuckDuckGoSearchAPIWrapper()
    
    def get_tools(self):
        return [
            Tool(
                name="DuckDuckGo Search",
                func=self.search.run,
                description="Searches the web using DuckDuckGo"
            )
        ]

class RAGEngine:
    def __init__(self):
        load_dotenv()
        
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo"
        )
        
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        self.search_tools = SearchTools()
        
        self.agent = initialize_agent(
            tools=self.search_tools.get_tools(),
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    def process_query(self, query):
        """Process a user query and return the response."""
        response = self.agent.run(query)
        return response
    
    def get_chat_history(self):
        """Return the current chat history."""
        return self.memory.chat_memory.messages
