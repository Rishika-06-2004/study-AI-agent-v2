from tools import ask_gemini, generate_summary, generate_flashcards


def detect_level(request):
    request_lower = request.lower()

    if "beginner" in request_lower:
        return "beginner"

    if "advanced" in request_lower:
        return "advanced"

    if "intermediate" in request_lower:
        return "intermediate"

    return "intermediate"


def detect_task(request):
    request_lower = request.lower()

    if "summary" in request_lower or "summarize" in request_lower:
        return "summary"

    if "flashcard" in request_lower:
        return "flashcards"

    return "question"


def study_agent(request):
    level = detect_level(request)
    task = detect_task(request)

    if task == "summary":
        return generate_summary(level)

    if task == "flashcards":
        return generate_flashcards(level)

    return ask_gemini(request)