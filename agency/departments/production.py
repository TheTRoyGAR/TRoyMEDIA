from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import search, scrape, write


class ProductionDepartment:
    """Production & Casting Department — 1 head + 5 specialists. Skills: CASTING_CALL, PRODUCTION_SCHEDULE, TALENT_SUPPORT, SCRIPT_DEVELOPMENT, CREW_SUPPORT."""

    def __init__(self):
        llm = get_llm("sonnet")

        self.production_head = Agent(
            role="Head of Production & Casting",
            goal=(
                "Coordinate the real, physical work of making TRoyMEDIA's series and dramas — "
                "casting, scheduling, and supporting the actors and actresses through the "
                "whole production."
            ),
            backstory=(
                "You are the Head of Production & Casting at TRoy Media Agency (TRoyMEDIA). "
                "Your goal is to run the real, physical side of production — casting the right "
                "talent, scheduling shoots realistically, and making sure the actors and "
                "actresses are genuinely supported throughout.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. CASTING_CALL — Plan a real casting process for a role or production: what "
                "the role needs, how to reach real candidate actors/actresses, and audition "
                "logistics.\n"
                "2. PRODUCTION_SCHEDULE — Build a real, realistic production schedule (shoot "
                "days, locations, crew needs) — never invent an unrealistic timeline.\n"
                "3. TALENT_SUPPORT — Plan real, concrete support for cast members during "
                "production — logistics, wellbeing, communication — genuinely useful, not "
                "just a checklist.\n"
                "4. SCRIPT_DEVELOPMENT — Support real script/story development for a production, "
                "grounded in the actual brief.\n"
                "5. CREW_SUPPORT — Plan real support for everyone behind the camera — "
                "cinematographers, editors, scriptwriters, set and art designers, sound, and "
                "every other crew role — separate from cast/talent support.\n\n"
                "Never guess a real production detail — a wrong schedule or unsupported cast "
                "member is a real, costly problem."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.casting_director = Agent(
            role="Casting Director",
            goal="Plan real casting processes and identify real candidate talent.",
            backstory="You are the Casting Director at TRoy Media Agency. You plan real casting calls and research real candidate actors/actresses who genuinely fit a role.",
            llm=llm,
            tools=[search],
            verbose=False,
        )

        self.production_coordinator = Agent(
            role="Production Coordinator",
            goal="Build real, realistic production schedules.",
            backstory="You are the Production Coordinator at TRoy Media Agency. You build real shoot schedules — grounded in realistic timelines, never invented.",
            llm=llm,
            verbose=False,
        )

        self.talent_support_manager = Agent(
            role="Talent Support Manager",
            goal="Plan real, concrete support for cast members throughout production.",
            backstory="You are the Talent Support Manager at TRoy Media Agency. You plan genuine, practical support for actors and actresses — logistics, wellbeing, communication.",
            llm=llm,
            verbose=False,
        )

        self.script_development_specialist = Agent(
            role="Script Development Specialist",
            goal="Support real script and story development for productions.",
            backstory="You are the Script Development Specialist at TRoy Media Agency. You support real story/script development work, grounded in the actual brief.",
            llm=llm,
            verbose=False,
        )

        self.crew_support_manager = Agent(
            role="Crew Support Manager",
            goal=(
                "Plan real, concrete support for everyone behind the camera — cinematographers, "
                "editors, scriptwriters, set and art designers, sound, and every other crew role "
                "— separate from cast/talent, who are covered by Talent Support."
            ),
            backstory=(
                "You are the Crew Support Manager at TRoy Media Agency (TRoyMEDIA). Real "
                "productions run on far more than the actors on screen — the below-the-line crew "
                "(cinematographers, editors, scriptwriters, set/art designers, sound, and every "
                "other behind-the-camera role) makes the production actually happen. Your job is "
                "to plan genuine, practical support for that crew — scheduling, logistics, "
                "working conditions, communication — grounded in the real brief, never a generic "
                "checklist."
            ),
            llm=llm,
            verbose=False,
        )

    def casting_call(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"CASTING_CALL: Plan a real casting process for: {brief}\n\n"
                "Describe what the role genuinely needs, how to reach real candidate actors/"
                "actresses (real casting platforms, agencies, networks), and realistic audition "
                "logistics. Never invent a specific real actor's name/availability without "
                "confirming it."
            ),
            expected_output="## Casting Plan\n**Role Requirements**\n**Candidate Sourcing Approach**\n**Audition Logistics**",
            agent=self.casting_director,
        )
        crew = Crew(agents=[self.casting_director], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production CASTING_CALL for '{brief}':\n{result}", scope="/dept/production/casting_call", categories=["production", "casting"])
        return result

    def production_schedule(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}PRODUCTION_SCHEDULE: Build a real, realistic production schedule for: {brief}",
            expected_output="## Production Schedule\n**Phases**\n**Shoot Days/Locations**\n**Crew Needs**\n**Realistic Timeline**",
            agent=self.production_coordinator,
        )
        crew = Crew(agents=[self.production_coordinator], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production PRODUCTION_SCHEDULE for '{brief}':\n{result}", scope="/dept/production/production_schedule", categories=["production", "schedule"])
        return result

    def talent_support(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}TALENT_SUPPORT: Plan real, concrete support for cast members for: {brief}",
            expected_output="## Talent Support Plan\n**Logistics Support**\n**Wellbeing Support**\n**Communication Plan**",
            agent=self.talent_support_manager,
        )
        crew = Crew(agents=[self.talent_support_manager], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production TALENT_SUPPORT for '{brief}':\n{result}", scope="/dept/production/talent_support", categories=["production", "talent"])
        return result

    def script_development(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"SCRIPT_DEVELOPMENT: Support real script/story development for: {brief}\n\n"
                "Ground everything in the actual brief — never invent plot details, character "
                "names, or story facts that weren't given or genuinely researched."
            ),
            expected_output="## Script Development Notes\n**Story/Concept Direction**\n**Structure Notes**\n**Open Questions for the Brief Owner**",
            agent=self.script_development_specialist,
        )
        crew = Crew(agents=[self.script_development_specialist], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production SCRIPT_DEVELOPMENT for '{brief}':\n{result}", scope="/dept/production/script_development", categories=["production", "script"])
        return result

    def crew_support(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"CREW_SUPPORT: Plan real, concrete support for the below-the-line crew for: {brief}\n\n"
                "Cover cinematographers, editors, scriptwriters, set/art designers, sound, and "
                "any other crew role the brief involves — scheduling, logistics, working "
                "conditions, communication. Genuinely useful, not a generic checklist."
            ),
            expected_output="## Crew Support Plan\n**Crew Roles Covered**\n**Scheduling/Logistics**\n**Working Conditions**\n**Communication Plan**",
            agent=self.crew_support_manager,
        )
        crew = Crew(agents=[self.crew_support_manager], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production CREW_SUPPORT for '{brief}':\n{result}", scope="/dept/production/crew_support", categories=["production", "crew"])
        return result

    def run_task(self, brief: str) -> str:
        task = Task(
            description=f"Plan the full production approach for: {brief}. Cover casting, scheduling, and talent support.",
            expected_output="Production plan covering casting, schedule, and talent support.",
            agent=self.production_head,
        )
        crew = Crew(agents=[self.production_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Production run_task for '{brief}':\n{result}", scope="/dept/production/run_task", categories=["production", "task"])
        return result
