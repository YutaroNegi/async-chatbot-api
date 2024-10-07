def generate_bot_response(user_input):
    # Enhanced chatbot logic
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "help" in user_input:
        return "Sure, I'm here to help. Please tell me more about what you need."
    elif "weather" in user_input:
        return "The weather is sunny with a chance of rainbows!"
    elif "joke" in user_input:
        return "Why did the developer go broke? Because they used up all their cache!"
    else:
        return "I'm sorry, I didn't quite catch that. Could you please elaborate?"
