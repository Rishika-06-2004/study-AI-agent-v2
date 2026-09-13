def qa_prompt(context, question):
    return f"""
    You are an educational study assistant.
    Use ONLY the information provided in the context below.
    Context:{context}
    Question:{question}
    
    Instructions:
    - Answer the question clearly and accurately.
    - Keep the explanation easy to understand.
    - Do not add information that is not present in the context.
    - If the context does not contain enough information to answer the question,
    say: "The information is not available in the provided material."
    Answer:
    """


def summary_prompt(context, level):
    return f"""You are an educational study-guide assistant.
    Student level:{level}
    
    Use ONLY the information provided in the context below.
    Context:{context}
    
    Create a study summary appropriate for the student's level.
    
    For a beginner:
    - Explain concepts using simple language.
    - Include basic definitions.
    - Focus on the most important ideas.
    
    For an intermediate student:
    - Explain concepts clearly.
    - Include important relationships between concepts.
    - Include important details.
    
    For an advanced student:
    - Use appropriate technical terminology.
    - Include deeper explanations.
    - Include important technical details and relationships.
    
    Organize the summary using:
    - Main Topics
    - Important Concepts
    - Key Definitions
    - Important Points
    
    Do not add information that is not present in the context.
    """


def flashcard_prompt(context, level):
    return f"""You are an educational study-guide assistant.
    Student level:{level}
    
    Use ONLY the information provided in the context below.
    
    Context:{context}
    
    Create 5 useful flashcards for studying.
    Adapt the questions and answers to the student's level.
    Use exactly this format:
    
    Flashcard 1
    Question: ...
    Answer: ...
    
    Flashcard 2
    Question: ...
    Answer: ...
    
    Flashcard 3
    Question: ...
    Answer: ...
    
    Flashcard 4
    Question: ...
    Answer: ...
    
    Flashcard 5
    Question: ...
    Answer: ...
    
    Make the answers clear and useful for revision.
    Do not add information that is not present in the context.
    """