from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import search, scrape, write


class MarketingDepartment:
    """Marketing Department — 1 head + 4 specialists. Skills: TREND_SCRAPE, CONTENT_GEN, PUBLICITY_AUDIT."""

    def __init__(self):
        llm = get_llm("haiku")

        self.marketing_head = Agent(
            role="Head of the AI Marketing Department",
            goal=(
                "Build real audience awareness and publicity for TRoyMEDIA's series, dramas, "
                "and talent — grounded in real industry trends, never invented buzz."
            ),
            backstory=(
                "You are the Head of the AI Marketing Department at TRoy Media Agency "
                "(TRoyMEDIA) — a real TV/film production and talent agency. Your goal is to "
                "build genuine audience awareness for real productions and the real actors/"
                "actresses TRoyMEDIA supports.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. TREND_SCRAPE — Research real, current entertainment industry trends "
                "(streaming platform demand, genre popularity, audience behavior) via live web "
                "search — never invent a trend.\n"
                "2. CONTENT_GEN — Write press releases, promotional copy, and social content for "
                "real productions and real talent — grounded in real facts about the project.\n"
                "3. PUBLICITY_AUDIT — Review a production or talent's existing public presence "
                "and flag real gaps or opportunities.\n\n"
                "Never fabricate a review, a trend, or an audience statistic."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.trend_researcher = Agent(
            role="Entertainment Trend Researcher",
            goal="Research real, current entertainment industry trends via live web search.",
            backstory=(
                "You are the Entertainment Trend Researcher at TRoy Media Agency. You research "
                "real streaming and broadcast trends — always from real, checkable sources."
            ),
            llm=llm,
            tools=[search, scrape],
            verbose=False,
        )

        self.content_creator = Agent(
            role="Content Creator",
            goal="Write accurate, compelling promotional content for real productions and talent.",
            backstory=(
                "You are the Content Creator at TRoy Media Agency. You write press releases, "
                "promotional copy, and social content grounded in real project facts, never "
                "invented details."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.press_relations_manager = Agent(
            role="Press & Publicity Relations Manager",
            goal="Identify and pursue real media coverage opportunities for productions and talent.",
            backstory=(
                "You are the Press & Publicity Relations Manager at TRoy Media Agency. You "
                "identify real outlets and journalists covering entertainment, and plan credible "
                "publicity approaches."
            ),
            llm=llm,
            tools=[search],
            verbose=False,
        )

        self.analytics_reporter = Agent(
            role="Audience & Analytics Reporter",
            goal="Track real public presence and engagement, and report on it honestly.",
            backstory=(
                "You are the Audience & Analytics Reporter at TRoy Media Agency. You monitor "
                "real audience presence and engagement, and report real findings — never "
                "invented metrics."
            ),
            llm=llm,
            verbose=False,
        )

    def trend_scrape(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"TREND_SCRAPE: Research real, current entertainment industry trends relevant "
                f"to: {brief}\n\nSearch for real, current data — never invent a trend or statistic."
            ),
            expected_output=(
                "## Entertainment Trend Report\n**Real Trends Found** — each with source URL\n"
                "**Relevance** — how each connects to the brief"
            ),
            agent=self.trend_researcher,
        )
        crew = Crew(agents=[self.trend_researcher], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Marketing TREND_SCRAPE for '{brief}':\n{result}", scope="/dept/marketing/trend_scrape", categories=["marketing", "trends"])
        return result

    def content_gen(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"CONTENT_GEN: Write promotional content for: {brief}\n\n"
                "Ground it in real, stated facts about the production/talent — no invented "
                "reviews, cast members, or plot details not actually provided."
            ),
            expected_output="Ready-to-publish promotional copy, professional tone, no fabricated claims.",
            agent=self.marketing_head,
        )
        task_polish = Task(
            description="Polish the draft into final, publish-ready content with clear structure.",
            expected_output="Final, publish-ready content.",
            agent=self.content_creator,
            context=[task],
        )
        crew = Crew(agents=[self.marketing_head, self.content_creator], tasks=[task, task_polish], process=Process.sequential, memory=shared_memory, verbose=False)
        crew_output = crew.kickoff()
        result = (
            f"{str(crew_output.tasks_output[0])}\n\n---\n\n{str(crew_output.tasks_output[1])}"
            if len(crew_output.tasks_output) >= 2 else str(crew_output)
        )
        remember(f"Marketing CONTENT_GEN for '{brief}':\n{result}", scope="/dept/marketing/content_gen", categories=["marketing", "content"])
        return result

    def publicity_audit(self, target: str) -> str:
        task = Task(
            description=(
                f"{recall_context(target)}"
                f"PUBLICITY_AUDIT: Review the real public presence of: {target}\n\n"
                "Flag anything inaccurate, outdated, unclear, or missing that would matter to "
                "an audience or industry partner."
            ),
            expected_output="## Publicity Audit\n**Findings** — specific, real issues found\n**Recommendations** — concrete fixes, prioritized",
            agent=self.analytics_reporter,
        )
        crew = Crew(agents=[self.analytics_reporter], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Marketing PUBLICITY_AUDIT for '{target}':\n{result}", scope="/dept/marketing/publicity_audit", categories=["marketing", "publicity"])
        return result

    def run_campaign(self, brief: str) -> str:
        task = Task(
            description=f"Plan a full marketing push for: {brief}. Cover trend research, content, and publicity targets.",
            expected_output="Marketing plan: trend findings, content pieces, and publicity targets.",
            agent=self.marketing_head,
        )
        crew = Crew(agents=[self.marketing_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Marketing campaign for '{brief}':\n{result}", scope="/dept/marketing/run_campaign", categories=["marketing", "campaign"])
        return result
