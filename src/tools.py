from rag import retrieve_chunks, _genai_client
from prompts import qa_prompt, summary_prompt, flashcard_prompt

def ask_gemini(question):
    chunks = retrieve_chunks(question)  #Retrieve relevant chunks

    context = "\n\n".join(chunks)

    #Use the retrieved information from my PDF to answer the question.
    #This is the important part that makes it RAG,
    #rather than simply asking Gemini a general question

    prompt = prompt = qa_prompt(context, question)

    client = _genai_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def generate_summary(level):
    chunks = retrieve_chunks("main topics and important concepts")

    context = "\n\n".join(chunks)

    prompt = prompt = summary_prompt(context, level)

    client = _genai_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def generate_flashcards(level):
    chunks = retrieve_chunks("important concepts definitions key facts")

    context = "\n\n".join(chunks)

    prompt = prompt = flashcard_prompt(context, level)

    client = _genai_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

