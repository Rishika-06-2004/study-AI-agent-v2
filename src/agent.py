from tools import ask_gemini, generate_summary, generate_flashcards

def study_agent(request):
    request_lower = request.lower()

    # Detect student level
    if "beginner" in request_lower:
        level = "beginner"

    elif "advanced" in request_lower:
        level = "advanced"

    elif "intermediate" in request_lower:
        level = "intermediate"

    else:
        level = "intermediate"

    # Detect requested task
    if "summary" in request_lower or "summarize" in request_lower:
        return generate_summary(level)

    elif "flashcard" in request_lower:
        return generate_flashcards(level)

    else:
        return ask_gemini(request)
