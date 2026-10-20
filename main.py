from agent import research


def main():

    print("\n=== AI Research Assistant ===")

    user_query = input(
        "\nWhat would you like me to research? "
    ).strip()

    if not user_query:
        print("\nPlease enter a research question.")
        return

    print("\nResearching...\n")

    try:

        answer, sources = research(user_query)

        print("\n=== FINAL ANSWER ===")
        print(answer)

        if sources:

            print("\n=== SOURCES USED ===")

            for i, source in enumerate(
                sources,
                start=1
            ):

                print(
                    f"{i}. {source['title']}"
                )

                print(
                    f"   {source['url']}"
                )

        else:

            print(
                "\nNo web sources were used."
            )

    except Exception as e:

        print(
            f"\nResearch failed: {e}"
        )


if __name__ == "__main__":
    main()