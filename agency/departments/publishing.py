from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import search, scrape, write


class PublishingDepartment:
    """Publishing Department — 1 head + 5 specialists. Skills: MANUSCRIPT_DEVELOPMENT, COPYEDIT, BOOK_PRODUCTION, ISSUE_PLANNING, RIGHTS_DISTRIBUTION."""

    def __init__(self):
        llm = get_llm("haiku")

        self.publishing_head = Agent(
            role="Head of Publishing",
            goal=(
                "Coordinate TRoyMEDIA's real publishing work — developing manuscripts into "
                "finished books, producing magazines and journals, and managing the real "
                "rights and distribution decisions behind them."
            ),
            backstory=(
                "You are the Head of Publishing at TRoy Media Agency (TRoyMEDIA). Your job is "
                "to run the real editorial and production side of publishing — books, "
                "magazines, and journals — grounded in actual publishing-industry practice, "
                "never invented process.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. MANUSCRIPT_DEVELOPMENT — Structural/developmental editing of a real "
                "manuscript: plot, pacing, character, structure — grounded only in the actual "
                "draft given, never invented plot details.\n"
                "2. COPYEDIT — Real line-level prose editing and consistency checking on an "
                "actual manuscript.\n"
                "3. BOOK_PRODUCTION — Real format specs for a book: trim size, interior "
                "layout, cover brief, ISBN/metadata, print-on-demand vs. offset printing, "
                "ebook formatting — grounded in real industry standards (KDP/IngramSpark-class "
                "specs), never a made-up format.\n"
                "4. ISSUE_PLANNING — Real editorial calendar and issue structure for a "
                "magazine or journal, including a genuine contributor/submission pipeline.\n"
                "5. RIGHTS_DISTRIBUTION — Real publishing-rights guidance (territorial, "
                "translation) and real distribution-channel research — never invent a deal "
                "or a rights holder.\n\n"
                "Never guess a real publishing detail — an invented ISBN, a fabricated rights "
                "holder, or an unrealistic print timeline is a real, costly problem.\n\n"
                "Operating rules: every plan must reflect real, current publishing-industry "
                "practice — flag anything unconfirmed rather than presenting a best guess as "
                "fact. You operate under TROYGO Group's standing CEO directive (auto-injected "
                "into every task)."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.manuscript_development_editor = Agent(
            role="Manuscript Development Editor",
            goal="Provide real structural/developmental editing for an actual manuscript.",
            backstory="You are the Manuscript Development Editor at TRoy Media Agency. You work only from the real manuscript given — plot, pacing, character, structure — never inventing story details that weren't in the actual draft.",
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.copy_line_editor = Agent(
            role="Copy & Line Editor",
            goal="Provide real line-level prose editing and consistency checking.",
            backstory="You are the Copy & Line Editor at TRoy Media Agency. You edit real prose for grammar, clarity, and consistency — grounded in the actual manuscript text, never a generic style pass.",
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.book_production_coordinator = Agent(
            role="Book Production Coordinator",
            goal="Produce real, industry-standard book production specs.",
            backstory="You are the Book Production Coordinator at TRoy Media Agency. You produce real format specs — trim size, interior layout, cover brief, ISBN/metadata, print-on-demand vs. offset, ebook formatting — grounded in actual publishing-industry standards, never invented specs.",
            llm=llm,
            verbose=False,
        )

        self.magazine_journal_editor = Agent(
            role="Magazine & Journal Editor",
            goal="Plan real editorial calendars and issue structures for magazines and journals.",
            backstory="You are the Magazine & Journal Editor at TRoy Media Agency. You plan real editorial calendars, issue structures, and contributor/submission pipelines — grounded in the actual publication's brief, never a generic template.",
            llm=llm,
            verbose=False,
        )

        self.rights_distribution_liaison = Agent(
            role="Rights & Distribution Liaison",
            goal="Research real publishing rights and distribution channels.",
            backstory="You are the Rights & Distribution Liaison at TRoy Media Agency. You research real publishing rights (territorial, translation) and real distribution channels — never inventing a deal, a rights holder, or a distributor relationship that hasn't been confirmed.",
            llm=llm,
            tools=[search],
            verbose=False,
        )

    def manuscript_development(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"MANUSCRIPT_DEVELOPMENT: Provide real structural/developmental editing notes for: {brief}\n\n"
                "Ground everything in the actual manuscript/brief given — never invent plot "
                "details, character names, or story facts that weren't given or genuinely "
                "researched."
            ),
            expected_output="## Manuscript Development Notes\n**Structure/Pacing Assessment**\n**Character Notes**\n**Open Questions for the Author**",
            agent=self.manuscript_development_editor,
        )
        crew = Crew(agents=[self.manuscript_development_editor], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing MANUSCRIPT_DEVELOPMENT for '{brief}':\n{result}", scope="/dept/publishing/manuscript_development", categories=["publishing", "manuscript"])
        return result

    def copyedit(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}COPYEDIT: Provide real line-level copyediting notes for: {brief}",
            expected_output="## Copyedit Notes\n**Grammar/Clarity Issues**\n**Consistency Issues**\n**Style Notes**",
            agent=self.copy_line_editor,
        )
        crew = Crew(agents=[self.copy_line_editor], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing COPYEDIT for '{brief}':\n{result}", scope="/dept/publishing/copyedit", categories=["publishing", "copyedit"])
        return result

    def book_production(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}BOOK_PRODUCTION: Build real, industry-standard book production specs for: {brief}",
            expected_output="## Book Production Specs\n**Trim Size & Interior Layout**\n**Cover Brief**\n**ISBN/Metadata**\n**Print/Ebook Format**",
            agent=self.book_production_coordinator,
        )
        crew = Crew(agents=[self.book_production_coordinator], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing BOOK_PRODUCTION for '{brief}':\n{result}", scope="/dept/publishing/book_production", categories=["publishing", "production"])
        return result

    def issue_planning(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}ISSUE_PLANNING: Build a real editorial calendar and issue structure for: {brief}",
            expected_output="## Issue Plan\n**Editorial Calendar**\n**Issue Structure**\n**Contributor/Submission Pipeline**",
            agent=self.magazine_journal_editor,
        )
        crew = Crew(agents=[self.magazine_journal_editor], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing ISSUE_PLANNING for '{brief}':\n{result}", scope="/dept/publishing/issue_planning", categories=["publishing", "issue"])
        return result

    def rights_distribution(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"RIGHTS_DISTRIBUTION: Research real publishing rights and distribution channels for: {brief}\n\n"
                "Never invent a specific rights holder, distributor relationship, or deal "
                "without confirming it."
            ),
            expected_output="## Rights & Distribution Plan\n**Rights Considerations**\n**Distribution Channel Research**\n**Open Questions**",
            agent=self.rights_distribution_liaison,
        )
        crew = Crew(agents=[self.rights_distribution_liaison], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing RIGHTS_DISTRIBUTION for '{brief}':\n{result}", scope="/dept/publishing/rights_distribution", categories=["publishing", "rights"])
        return result

    def run_task(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}Plan the full publishing approach for: {brief}. Cover manuscript development, production specs, and rights/distribution as relevant.",
            expected_output="Publishing plan covering the relevant stages for this brief.",
            agent=self.publishing_head,
        )
        crew = Crew(agents=[self.publishing_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Publishing run_task for '{brief}':\n{result}", scope="/dept/publishing/run_task", categories=["publishing", "task"])
        return result
