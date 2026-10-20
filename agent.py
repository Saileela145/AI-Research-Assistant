from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

from tools.calculator import calculator
from tools.web_search import web_search
from tools.web_fetch import web_fetch


# ==========================================
# Configuration
# ==========================================

load_dotenv()

MODEL_NAME = "gemini-3.6-flash"
MAX_TOOL_CALLS = 5


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME
)

tools = [
    calculator,
    web_search,
    web_fetch,
]

tool_map = {
    tool.name: tool
    for tool in tools
}

llm_with_tools = llm.bind_tools(tools)


# ==========================================
# System Prompt
# ==========================================

SYSTEM_PROMPT = """
You are an AI research assistant.

Your job is to answer the user's questions accurately and
use available tools when necessary.

TOOLS:

1. web_search
   Use this when the question requires current, recent,
   changing, or externally verifiable information.

2. web_fetch
   Use this ONLY when you need to read or analyze the actual
   contents of a specific webpage.

3. calculator
   Use this when mathematical calculations are required.

TOOL SELECTION RULES:

1. Do not use tools unnecessarily.

2. For a current factual question, normally use web_search
   only. Do NOT automatically use web_fetch after web_search.

3. Use web_fetch only when:
   - the user explicitly asks to find, read, inspect, or explain
     information from a specific webpage,
   - the user asks for the official page and you need to inspect
     that page,
   - or the search results do not contain enough information
     and the actual webpage content is required.

4. If web_search already provides enough reliable information
   to answer the question, stop using tools and answer.

5. When searching for factual information, prefer authoritative
   and primary sources over third-party sources.

6. If an official source exists, prefer it over blogs,
   forums, aggregators, or other secondary sources.

7. Carefully evaluate search results before answering.
   Do not simply use the first search result.

8. If multiple sources give different answers, determine which
   source is more authoritative and which information is more
   recent.

9. You may use a tool multiple times if the available
   information is insufficient.

10. Once you have enough reliable information, stop using tools
    and provide the final answer.

11. Clearly explain the answer to the user.

IMPORTANT:
Do not call web_fetch merely because a webpage URL appeared
in web_search results. Fetch the page only when its actual
contents are necessary.

RESEARCH STOPPING RULES:

12. Treat each tool result as evidence. After receiving a tool
    result, first determine whether it contains enough reliable
    information to answer the user's question.

13. Do not perform another search simply to confirm information
    that is already supported by a reliable source.

14. For simple factual questions, normally perform only one
    web_search unless the result is missing, ambiguous,
    contradictory, or clearly unreliable.

15. If a search result from an authoritative source directly
    answers the user's question, stop researching and answer.

16. For questions asking for an official page or verification,
    web_search may be followed by web_fetch of the most relevant
    official page.

17. Avoid repeating searches with slightly different queries
    when previous results already provide the answer.

18. Before requesting another tool call, ask yourself:
    "What specific information am I missing that this tool call
    will provide?"
    If there is no clear missing information, stop and answer.
"""


# ==========================================
# Helper Functions
# ==========================================

def get_text_content(content):
    """Extract text from an LLM response."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []

        for block in content:
            if (
                isinstance(block, dict)
                and block.get("type") == "text"
            ):
                texts.append(
                    block.get("text", "")
                )

        return "\n".join(texts)

    return str(content)


def collect_sources(
    tool_name,
    tool_result,
    sources_found,
):
    """Collect unique sources returned by web_search."""

    if tool_name != "web_search":
        return

    if not isinstance(tool_result, str):
        return

    current_source = {}

    for line in tool_result.splitlines():

        line = line.strip()

        if line.startswith("Title:"):

            current_source["title"] = (
                line.replace(
                    "Title:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("URL:"):

            current_source["url"] = (
                line.replace(
                    "URL:",
                    "",
                    1
                ).strip()
            )

        elif line.startswith("Snippet:"):

            current_source["snippet"] = (
                line.replace(
                    "Snippet:",
                    "",
                    1
                ).strip()
            )

            if current_source.get("url"):

                source = {
                    "title": current_source.get(
                        "title",
                        "Untitled source"
                    ),
                    "url": current_source["url"],
                    "snippet": current_source.get(
                        "snippet",
                        ""
                    ),
                }

                if not any(
                    existing["url"] == source["url"]
                    for existing in sources_found
                ):
                    sources_found.append(source)

            current_source = {}


def select_sources(
    user_query,
    sources_found,
):
    """
    Ask Gemini to select the most relevant sources.
    """

    if not sources_found:
        return []

    source_text = "\n\n".join(
        f"{i + 1}. {source['title']}\n"
        f"URL: {source['url']}\n"
        f"Snippet: {source['snippet']}"
        for i, source in enumerate(sources_found)
    )

    selection_prompt = f"""
You are selecting sources for a research answer.

Choose only the sources that are directly relevant to
answering the user's question.

Prefer:

1. Official/primary sources
2. Recent sources
3. Sources that directly support the final answer

Avoid:

- irrelevant search results
- duplicate sources
- platform-specific pages unless relevant
- unrelated older releases

Return ONLY the source numbers separated by commas.

Available sources:

{source_text}
"""

    messages = [
        SystemMessage(
            content=selection_prompt
        ),
        HumanMessage(
            content=user_query
        ),
    ]

    response = llm.invoke(messages)

    selected_text = get_text_content(
        response.content
    )

    try:

        selected_indexes = [
            int(value.strip())
            for value in selected_text.split(",")
            if value.strip().isdigit()
        ]

        sources_used = []

        for index in selected_indexes:

            if 1 <= index <= len(sources_found):

                source = sources_found[index - 1]

                if source not in sources_used:

                    sources_used.append(
                        {
                            "title": source["title"],
                            "url": source["url"],
                        }
                    )

        return sources_used

    except Exception as e:

        print(
            f"Source selection failed: {e}"
        )

        return [
            {
                "title": source["title"],
                "url": source["url"],
            }
            for source in sources_found[:5]
        ]


# ==========================================
# Research Agent
# ==========================================

def research(
    user_query,
    status_callback=None,
):
    """
    Run the research agent.

    Returns:
        tuple[str, list[dict]]
        final answer and selected sources
    """

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=user_query
        ),
    ]

    tool_call_count = 0
    sources_found = []

    def update_status(message):
        if status_callback:
            status_callback(message)

    while True:

        response = llm_with_tools.invoke(
            messages
        )

        messages.append(response)

        # ==================================
        # Final Answer
        # ==================================

        if not response.tool_calls:

            final_answer = get_text_content(
                response.content
            )

            sources_used = select_sources(
                user_query,
                sources_found,
            )

            return final_answer, sources_used

        # ==================================
        # Tool Execution
        # ==================================

        for tool_call in response.tool_calls:

            if tool_call_count >= MAX_TOOL_CALLS:

                messages.append(
                    ToolMessage(
                        content=(
                            "Maximum tool-call limit reached. "
                            "Use the information already collected "
                            "and provide the best possible answer."
                        ),
                        tool_call_id=tool_call["id"],
                        name=tool_call["name"],
                    )
                )

                final_response = llm.invoke(
                    messages
                )

                final_answer = get_text_content(
                    final_response.content
                )

                sources_used = select_sources(
                    user_query,
                    sources_found,
                )

                return final_answer, sources_used

            tool_call_count += 1

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # ----------------------------------
            # Progress
            # ----------------------------------

            if tool_name == "web_search":

                update_status(
                    "Searching the web..."
                )

            elif tool_name == "web_fetch":

                update_status(
                    "Reading webpage content..."
                )

            elif tool_name == "calculator":

                update_status(
                    "Performing calculation..."
                )

            else:

                update_status(
                    f"Using {tool_name}..."
                )

            # ----------------------------------
            # Find Tool
            # ----------------------------------

            tool = tool_map.get(tool_name)

            if tool is None:

                tool_result = (
                    f"Tool '{tool_name}' does not exist."
                )

            else:

                try:

                    tool_result = tool.invoke(
                        tool_args
                    )

                except Exception as e:

                    tool_result = (
                        f"Tool '{tool_name}' failed: "
                        f"{str(e)}"
                    )

            # ----------------------------------
            # Collect Sources
            # ----------------------------------

            collect_sources(
                tool_name,
                tool_result,
                sources_found,
            )

            # ----------------------------------
            # Return Tool Result to Gemini
            # ----------------------------------

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )