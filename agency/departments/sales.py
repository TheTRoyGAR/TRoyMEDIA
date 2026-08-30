from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import search, scrape, write


class SalesDepartment:
    """Sales & Distribution Department — 1 head + 4 specialists. Skills: PITCH_DEVELOPMENT, DISTRIBUTION_DEAL, OBJECTION_HANDLER."""

    def __init__(self):
        llm = get_llm("haiku")

        self.sales_head = Agent(
            role="Head of the AI Sales & Distribution Department",
            goal=(
                "Win real broadcast/streaming deals for TRoyMEDIA's productions, and grow real "
                "relationships with networks, streamers, and distributors."
            ),
            backstory=(
                "You are the Head of Sales & Distribution at TRoy Media Agency (TRoyMEDIA). "
                "Your goal is to get real productions picked up by real networks/streamers, and "
                "grow real distribution relationships — this industry runs on trust and real "
                "track record, not hype.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. PITCH_DEVELOPMENT — Build a real, structured pitch for a series/drama "
                "concept — never invent audience data or comparable-show numbers you can't "
                "verify.\n"
                "2. DISTRIBUTION_DEAL — Identify real broadcasters, streamers, or distributors "
                "who genuinely fit a given production, based on real research into what they "
                "actually air.\n"
                "3. OBJECTION_HANDLER — Handle real objections from networks/partners with "
                "honest, credible responses.\n\n"
                "Coordinate with Marketing's real trend research to target real, fitting partners.\n\n"
                "Operating rules: a negotiated deal is a draft until TRoy confirms it as real and "
                "signed — never report it as closed. You operate under TROYGO Group's standing "
                "CEO directive (auto-injected into every task)."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.pitch_developer = Agent(
            role="Pitch Developer",
            goal="Build real, structured pitches for productions.",
            backstory="You are the Pitch Developer at TRoy Media Agency. You build real, structured show pitches — grounded in real facts, never invented numbers.",
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.distribution_researcher = Agent(
            role="Distribution Researcher",
            goal="Identify real broadcasters, streamers, and distributors that fit a production.",
            backstory="You are the Distribution Researcher at TRoy Media Agency. You research real networks/streamers and what they actually air — always from real, checkable sources.",
            llm=llm,
            tools=[search, scrape],
            verbose=False,
        )

        self.deal_negotiator = Agent(
            role="Deal Negotiator",
            goal="Move a qualified distribution opportunity toward a real, confirmed deal.",
            backstory="You are the Deal Negotiator at TRoy Media Agency. You handle the final steps of confirming a real distribution or broadcast deal — clear terms, no ambiguity.",
            llm=llm,
            verbose=False,
        )

        self.client_relations_manager = Agent(
            role="Client & Talent Relations Manager",
            goal="Maintain real, honest relationships with productions' clients and talent.",
            backstory="You are the Client & Talent Relations Manager at TRoy Media Agency. You handle real client and talent relationships with honesty and professionalism.",
            llm=llm,
            verbose=False,
        )

    def pitch_development(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"PITCH_DEVELOPMENT: Build a real, structured pitch for: {brief}\n\n"
                "Never invent audience numbers, comparable-show data, or ratings you can't verify."
            ),
            expected_output="## Production Pitch\n**Concept**\n**Target Audience**\n**Comparable Real Shows (if any, sourced)**\n**Why Now**",
            agent=self.pitch_developer,
        )
        crew = Crew(agents=[self.pitch_developer], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Sales PITCH_DEVELOPMENT for '{brief}':\n{result}", scope="/dept/sales/pitch_development", categories=["sales", "pitch"])
        return result

    def distribution_deal(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"DISTRIBUTION_DEAL: Identify real broadcasters/streamers/distributors that "
                f"genuinely fit: {brief}\n\nOnly include real, confirmed findings with sources."
            ),
            expected_output="## Distribution Targets\n**Real Candidates** — name, what they actually air, source URL, why they fit\n**Approach Recommendation**",
            agent=self.distribution_researcher,
        )
        task_close = Task(
            description="Add real next-step negotiation guidance for the top candidate.",
            expected_output="Negotiation next steps for the top candidate.",
            agent=self.deal_negotiator,
            context=[task],
        )
        crew = Crew(agents=[self.distribution_researcher, self.deal_negotiator], tasks=[task, task_close], process=Process.sequential, memory=shared_memory, verbose=False)
        crew_output = crew.kickoff()
        result = (
            f"{str(crew_output.tasks_output[0])}\n\n---\n\n{str(crew_output.tasks_output[1])}"
            if len(crew_output.tasks_output) >= 2 else str(crew_output)
        )
        remember(f"Sales DISTRIBUTION_DEAL for '{brief}':\n{result}", scope="/dept/sales/distribution_deal", categories=["sales", "distribution"])
        return result

    def objection_handler(self, objection: str) -> str:
        task = Task(
            description=f"OBJECTION_HANDLER: Write an honest, credible response to this real objection: {objection}",
            expected_output="A clear, honest, professional response — no overpromising to close a deal.",
            agent=self.sales_head,
        )
        crew = Crew(agents=[self.sales_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Sales OBJECTION_HANDLER for '{objection}':\n{result}", scope="/dept/sales/objection_handler", categories=["sales", "objection"])
        return result

    def run_pipeline(self, brief: str) -> str:
        task = Task(
            description=f"Plan the full sales/distribution pipeline for: {brief}. Cover pitch, distribution targets, and closing steps.",
            expected_output="Sales pipeline plan with concrete next steps.",
            agent=self.sales_head,
        )
        crew = Crew(agents=[self.sales_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Sales pipeline for '{brief}':\n{result}", scope="/dept/sales/run_pipeline", categories=["sales", "pipeline"])
        return result
