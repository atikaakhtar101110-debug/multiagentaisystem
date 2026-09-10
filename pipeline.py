from agents import (
    build_reader_agent,
    build_search_agent,
    run_writer_chain,
    run_critic_chain
)


def extract_agent_output(result) -> str:
    if isinstance(result, dict):
        if "output" in result:
            return result["output"]
        if "messages" in result and len(result["messages"]) > 0:
            return result["messages"][-1].content
    return str(result)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1 - Search Agent
    print("\n" + " =" * 50)
    print("Step 1 - Search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = extract_agent_output(search_result)
    print("\nSearch Result:\n", state['search_results'])

    # Step 2 - Reader Agent
    print("\n" + " =" * 50)
    print("Step 2 - Reader agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })
    state['scraped_content'] = extract_agent_output(reader_result)
    print("\nScraped Content:\n", state['scraped_content'])

    # Step 3 - Writer Chain
    print("\n" + " =" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = run_writer_chain({
        "topic": topic,
        "research": research_combined
    })
    print("\nFinal Report:\n", state['report'])

    # Step 4 - Critic Chain
    print("\n" + " =" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = run_critic_chain({
        "report": state['report']
    })
    print("\nCritic Report:\n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)
