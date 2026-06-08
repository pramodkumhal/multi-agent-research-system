from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
    revision_chain
)

import re


def extract_urls(text: str, limit: int = 3):
    """Extract top URLs from search results"""
    urls = re.findall(r'https?://[^\s]+', text)
    return urls[:limit]


def run_research_pipeline(topic: str) -> dict:

    state = {}


    # STEP 1 - SEARCH AGENT
    print("\n" + "=" * 50)
    print("Step 1 - Search Agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]
    })

    state["search_results"] = search_result["messages"][-1].content
    print("\nSearch Results:\n", state["search_results"])


    # STEP 2 - URL EXTRACTION
    urls = extract_urls(state["search_results"], limit=3)

    print("\nExtracted URLs:")
    for u in urls:
        print("-", u)


    # STEP 3 - READER AGENT
    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent is scraping top sources...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            ("user",
             f"You MUST use the scrape_url tool for each of the following URLs:\n\n"
             f"{chr(10).join(urls)}\n\n"
             f"Extract and combine the most important insights into a structured summary.")
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content
    print("\nScraped Content:\n", state["scraped_content"])


    # STEP 4 - WRITER
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nInitial Report:\n", state["report"])


    # STEP 5 - CRITIC
    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Feedback:\n", state["feedback"])


    # STEP 6 - REVISION WRITER
    print("\n" + "=" * 50)
    print("Step 5 - Revising report based on feedback...")
    print("=" * 50)

    state["final_report"] = revision_chain.invoke({
        "report": state["report"],
        "feedback": state["feedback"]
    })

    print("\nFinal Improved Report:\n")
    print(state["final_report"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)