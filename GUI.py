import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame, Label
import threading
from PIL import Image, ImageTk
import datetime

class RAGGUI:
    def __init__(self, rag_engine):
        self.rag_engine = rag_engine
        
        self.root = tk.Tk()
        self.root.title("Chat Assistant")
        self.root.geometry("500x600")
        
        self.bg_color = "#FFFFFF"
        self.header_color = "#90ee90"  # Purple header
        self.user_bubble_color = "#9C27B0"  # Purple user messages
        self.assistant_bubble_color = "#E1F5FE"  # Light blue assistant messages
        self.text_color_dark = "#333333"
        self.text_color_light = "#FFFFFF"
        
        self.root.configure(bg=self.bg_color)
        
        self.header_frame = Frame(self.root, bg=self.header_color, height=60)
        self.header_frame.pack(fill=tk.X)
        
        self.name_label = Label(self.header_frame, text="Movie RAG Agent", font=("Arial", 14, "bold"), 
                               bg=self.header_color, fg=self.text_color_light)
        self.name_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.menu_button = Label(self.header_frame, text="•••", font=("Arial", 16, "bold"), 
                                bg=self.header_color, fg=self.text_color_light)
        self.menu_button.pack(side=tk.RIGHT, padx=15, pady=10)
        
        self.chat_frame = Frame(self.root, bg=self.bg_color)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_canvas = tk.Canvas(self.chat_frame, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.scrollable_frame = Frame(self.chat_canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )
        )
        
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.input_frame = Frame(self.root, bg=self.bg_color, height=60)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = Entry(self.input_frame, font=("Arial", 12), bd=1, relief=tk.SOLID)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.input_field.bind("<Return>", self.send_message)
        
        self.emoji_button = Button(self.input_frame, text="😊", font=("Arial", 14), 
                                 bg=self.bg_color, relief=tk.FLAT)
        self.emoji_button.pack(side=tk.RIGHT, padx=5)
        
        self.add_message("assistant", "Welcome to Movie RAG Agent,\n\nIf you need any details about a movie, just ask and i will provide you with the information.")
    
    def add_message(self, sender, message):
        
        """Add a message bubble to the chat"""
        if sender == "user":
            bubble_frame = Frame(self.scrollable_frame, bg=self.user_bubble_color, padx=10, pady=10)
            bubble_frame.pack(anchor="e", padx=10, pady=5, fill=tk.X)
            
            message_label = Label(bubble_frame, text=message, font=("Arial", 11), 
                                 bg=self.user_bubble_color, fg=self.text_color_light,
                                 justify=tk.LEFT, wraplength=300)
            message_label.pack(anchor="e")
            
        else:  
            bubble_frame = Frame(self.scrollable_frame, bg=self.assistant_bubble_color, padx=10, pady=10)
            bubble_frame.pack(anchor="w", padx=10, pady=5, fill=tk.X)
                
            message_label = Label(bubble_frame, text=message, font=("Arial", 11), 
                                 bg=self.assistant_bubble_color, fg=self.text_color_dark,
                                 justify=tk.LEFT, wraplength=300)
            message_label.pack(anchor="w")
            
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M%p").lower()
            time_label = Label(bubble_frame, text=time_str, font=("Arial", 8), 
                              bg=self.assistant_bubble_color, fg="#888888")
            time_label.pack(anchor="se", padx=5)
        
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def send_message(self, event=None):
        """Process the user's message and display the response."""
        user_input = self.input_field.get()
        if not user_input:
            return
        
        self.input_field.delete(0, tk.END)
        
        self.add_message("user", user_input)
        
        threading.Thread(target=self.process_message, args=(user_input,)).start()
    
    def process_message(self, user_input):
        """Process the message in a separate thread."""
        try:
            
            response = self.rag_engine.process_query(user_input)
           
            self.add_message("assistant", response)
            
        except Exception as e:
            self.add_message("assistant", f"Sorry, I encountered an error: {str(e)}")
    
    def run(self):
        """Run the GUI main loop."""
        self.root.mainloop()
