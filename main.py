from agent import run_agent


def main():

    print("=" * 50)
    print("SAFE SHOPPING AGENT")
    print("=" * 50)

    role = input(
        "Enter your role (customer/admin): "
    ).strip().lower()

    if role not in ("customer", "admin"):
        print("Invalid role.")
        return

    messages = [
        {
            "role": "system",
            "content": (
                "You are a shopping assistant."
            ),
        }
    ]

    print("\nYou can start chatting with the shopping agent.")
    print("Type 'goodbye' to exit.\n")

    while True:

        request = input("You: ").strip()

        if request.lower() in (
            "goodbye",
            "bye",
            "exit",
            "quit",
        ):
            print("Agent: Goodbye! 👋")
            break

        if not request:
            print("Agent: Please enter a request.")
            continue

        print("\n" + "=" * 50)
        print("AGENT STARTED")
        print("=" * 50)

        print("Role:", role)
        print("Request:", request)

        run_agent(
            user_request=request,
            role=role,
            messages=messages,
        )

        print("\n" + "=" * 50)
        print("Ready for your next request.")
        print("=" * 50)


if __name__ == "__main__":
    main()