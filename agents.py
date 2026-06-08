from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model Setup with Fallbacks
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.3
)

fallback_1 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3
)

fallback_2 = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

fallback_3 = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0.3
)

fallback_4 = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

llm = primary_llm.with_fallbacks([
    fallback_1,
    fallback_2,
    fallback_3,
    fallback_4
])

# Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools = [web_search]
        )

# Reader Agent
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )

# Writer Chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a rigorous research writer. "
     "Your job is to produce factual, evidence-based, and well-structured research reports. "
     "Never invent facts. If evidence is weak or missing, explicitly mention uncertainty."),

    ("human",
     """Write a detailed research report on the topic below.

Topic:
{topic}

Research Material:
{research}

Instructions:
- Use ONLY the provided research material to form your answer.
- Do NOT assume or invent facts not present in the research.
- If information is uncertain or incomplete, clearly state the limitation.
- Prefer evidence-backed statements over general explanations.

Structure your report as:

1. Introduction
   - Brief context and definition of the topic

2. Key Findings
   - Minimum 3 well-explained points
   - Each point must be supported by evidence from the research material
   - If possible, mention source URLs in-line

3. Analysis
   - Explain patterns, implications, or relationships between findings

4. Conclusion
   - Summarize the overall insight clearly and objectively

5. Sources
   - List ONLY actual URLs found in the research material
   - If no valid URLs exist, explicitly write: "No verifiable sources available"

Quality Rules:
- Be precise, not verbose
- Avoid generic statements
- Prioritize factual correctness over fluency
- Maintain an academic, research-report tone
""")
])

writer_chain = writer_prompt | llm | StrOutputParser()
              

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()


# Revision Chain
revision_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert research writer. Improve reports based on reviewer feedback."),

    ("human",
     """
Original Report:
{report}

Reviewer Feedback:
{feedback}

Revise the report by:
- Fixing weaknesses mentioned in the feedback
- Improving clarity and completeness
- Keeping factual information intact
- Maintaining professional structure

Return only the improved final report.
""")
])

revision_chain = revision_prompt | llm | StrOutputParser()



