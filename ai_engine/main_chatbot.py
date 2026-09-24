from router import ai_router

print("🔥 AI Tourism Chatbot Ready")
print("Type 'quit' to exit.\n")

while True:
    user_in = input("You: ")

    if user_in == "quit":
        break

    # For now, set image_path=None
    response = ai_router(user_in, image_path=None)

    print("\nBot:", response)
    print("\n" + "-"*50 + "\n")
