import streamlit as st
import os

# --- Workaround for CrewAI bug: cache_breakpoint not stripped for non-Anthropic providers ---
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Content Crew", page_icon="📝", layout="centered")
st.title("📝 AI Content Crew")
st.caption("A multi-agent system (Planner → Writer → Editor) built with CrewAI + Groq")

# ---------------------------------------------------------------------------
# API keys — pulled from Streamlit Secrets, never hardcoded
# ---------------------------------------------------------------------------
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
except KeyError:
    st.error(
        "Missing API keys. Add GROQ_API_KEY and SERPER_API_KEY in "
        "Settings → Secrets on Streamlit Community Cloud."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Build the crew (cached so it's only built once per session, not on every rerun)
# ---------------------------------------------------------------------------
@st.cache_resource
def build_crew():
    planner_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)
    writer_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)
    editor_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)

    search_tool = SerperDevTool()

    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory=(
            "You are working on planning a blog article about {topic}. "
            "You collect information that helps the audience learn something "
            "and make informed decisions. Your work is the basis for the "
            "Content Writer to write an article on this topic."
        ),
        tools=[search_tool],
        llm=planner_llm,
        verbose=True,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write insightful and factually accurate opinion pieces about {topic}",
        backstory=(
            "You are working on writing a new opinion piece about {topic}. "
            "You base your writing on the work of the Content Planner, who "
            "provides an outline and relevant context about the topic."
        ),
        llm=writer_llm,
        verbose=True,
    )

    editor = Agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization",
        backstory=(
            "You are an editor who receives a blog post from the Content Writer. "
            "Your goal is to review the blog post to ensure it follows journalistic "
            "best practices, provides balanced viewpoints, and avoids major "
            "controversial topics or opinions when possible."
        ),
        llm=editor_llm,
        verbose=True,
    )

    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering their interests and pain points.\n"
            "3. Develop a detailed content outline including an introduction, key points, "
            "and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document with an outline, "
                         "audience analysis, SEO keywords, and resources.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/subtitles are properly named in an engaging manner.\n"
            "4. Ensure the post is structured with an engaging introduction, "
            "insightful body, and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, "
                         "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    edit = Task(
        description=(
            "Proofread the given blog post for grammatical errors and alignment "
            "with the brand's voice."
        ),
        expected_output="A polished, publish-ready blog post in markdown format.",
        agent=editor,
    )

    return Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        process=Process.sequential,
        verbose=True,
    )


crew = build_crew()

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
topic = st.text_input("Topic", placeholder="e.g. Artificial Intelligence, Telecom Retail in Nigeria")
run = st.button("Generate content", type="primary", disabled=not topic)

if run and topic:
    with st.status("Crew is working...", expanded=True) as status:
        st.write("📋 Planner is researching...")
        result = crew.kickoff(inputs={"topic": topic})
        status.update(label="Done!", state="complete", expanded=False)

    st.markdown("---")
    st.markdown(str(result))

    st.download_button(
        "Download as Markdown",
        data=str(result),
        file_name=f"{topic.replace(' ', '_')}_article.md",
        mime="text/markdown",
    )
