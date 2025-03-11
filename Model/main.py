def main():
    
    rag_engine = RAGEngine()
    
    gui = RAGGUI(rag_engine)
    gui.run()

if __name__ == "__main__":
    main()
