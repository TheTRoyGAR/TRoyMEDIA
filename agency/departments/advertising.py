from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import search, scrape, write


class AdvertisingDepartment:
    """Advertising Department — 1 head + 5 specialists. Skills: AD_CAMPAIGN_STRATEGY, CREATIVE_CONCEPT, MEDIA_PLANNING, VIDEO_AD_PRODUCTION."""

    def __init__(self):
        llm = get_llm("haiku")

        self.advertising_head = Agent(
            role="Head of the AI Advertising Department",
            goal=(
                "Build real advertising campaigns for client companies and products — "
                "strategy, creative, and media placement — grounded in the client's actual "
                "brief and real market/channel data, never invented numbers or platforms."
            ),
            backstory=(
                "You are the Head of the AI Advertising Department at TRoy Media Agency "
                "(TRoyMEDIAgency) — a real advertising agency function, separate from the "
                "Marketing department (which promotes TRoyMEDIA's own productions and talent). "
                "This department builds real advertising campaigns FOR client companies and "
                "their products — the classic advertising-agency job of strategy, creative, "
                "and media buying.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. AD_CAMPAIGN_STRATEGY — Build a real campaign strategy for a client's "
                "product/company: target audience, core message, and channel mix, grounded in "
                "the actual brief.\n"
                "2. CREATIVE_CONCEPT — Develop a real creative concept and ad copy/script for "
                "a campaign — never invent a client fact, statistic, or claim not in the brief.\n"
                "3. MEDIA_PLANNING — Plan real media placement: which real channels/platforms "
                "fit the audience and budget, and why.\n"
                "4. VIDEO_AD_PRODUCTION — Plan a real video ad (TV/YouTube) production using "
                "real AI video-generation tools (e.g. Google's AI Studio/Veo class tools) — "
                "script, shot/scene breakdown, and how it maps to a real YouTube ad format or "
                "Google Ads campaign structure.\n\n"
                "Never guess a real client fact, a real platform's ad rates, or an audience "
                "statistic — if it isn't in the brief or genuinely researched, say so instead "
                "of inventing it.\n\n"
                "Operating rules: never claim a video/ad asset has been produced unless TRoy or "
                "the Production dept has confirmed the real render exists. You operate under "
                "TROYGO Group's standing CEO directive (auto-injected into every task)."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.creative_director = Agent(
            role="Creative Director",
            goal="Develop real, on-brief creative concepts and ad copy for client campaigns.",
            backstory=(
                "You are the Creative Director at TRoy Media Agency. You develop creative "
                "concepts and write ad copy/scripts grounded strictly in the client's actual "
                "brief — never inventing a product feature, claim, or fact not provided."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.media_planner = Agent(
            role="Media Planner & Buyer",
            goal="Plan real media placement across channels that genuinely fit the audience and budget.",
            backstory=(
                "You are the Media Planner & Buyer at TRoy Media Agency. You research real "
                "advertising channels and platforms and recommend a real, justified placement "
                "plan — never invent a platform, rate, or reach figure you haven't checked."
            ),
            llm=llm,
            tools=[search, scrape],
            verbose=False,
        )

        self.copywriter = Agent(
            role="Copywriter",
            goal="Write clear, compelling, honest ad copy grounded in the client's real brief.",
            backstory=(
                "You are the Copywriter at TRoy Media Agency. You write ad copy that is "
                "persuasive but strictly accurate to the client's real brief — no invented "
                "claims, no fabricated testimonials."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.video_production_specialist = Agent(
            role="AI Video Production Specialist",
            goal=(
                "Plan real video ad production for TV and YouTube using real AI "
                "video-generation tools, mapped to real ad-platform formats."
            ),
            backstory=(
                "You are the AI Video Production Specialist at TRoy Media Agency. You plan "
                "video ad production using real AI video-generation tools (e.g. Google's AI "
                "Studio/Veo class tools) — writing the script and shot/scene breakdown, and "
                "mapping the finished ad to a real YouTube ad format (skippable in-stream, "
                "bumper, etc.) or Google Ads campaign structure. This connects TRoyMEDIA's "
                "production capability directly to TRoyAI's client work — when TRoyAI brings "
                "in a client that needs real video ads made, this is the real fulfillment. "
                "Never invent a platform spec, format name, or capability you haven't actually "
                "confirmed — flag it instead."
            ),
            llm=llm,
            tools=[search, scrape, write],
            verbose=False,
        )

        self.account_strategist = Agent(
            role="Account Strategist",
            goal="Turn a client's real brief into a clear, actionable campaign strategy.",
            backstory=(
                "You are the Account Strategist at TRoy Media Agency. You translate a client's "
                "real goals and constraints into a workable campaign strategy — grounded in "
                "what the client actually told you, asking for clarification rather than "
                "guessing when the brief is incomplete."
            ),
            llm=llm,
            verbose=False,
        )

    def ad_campaign_strategy(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"AD_CAMPAIGN_STRATEGY: Build a real campaign strategy for: {brief}\n\n"
                "Define the target audience, the core message, and the real channel mix — "
                "grounded strictly in the brief. If the brief is missing something essential "
                "(budget, target market, goal), say so explicitly rather than assuming it."
            ),
            expected_output=(
                "## Campaign Strategy\n**Target Audience**\n**Core Message**\n"
                "**Channel Mix** — real channels, with reasoning\n**Open Questions** — anything the brief didn't cover"
            ),
            agent=self.account_strategist,
        )
        crew = Crew(agents=[self.account_strategist], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Advertising AD_CAMPAIGN_STRATEGY for '{brief}':\n{result}", scope="/dept/advertising/ad_campaign_strategy", categories=["advertising", "strategy"])
        return result

    def creative_concept(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"CREATIVE_CONCEPT: Develop a real creative concept and ad copy for: {brief}\n\n"
                "Ground every claim in the actual brief — never invent a product feature, "
                "statistic, or testimonial."
            ),
            expected_output="## Creative Concept\n**Concept**\n**Ad Copy/Script**\n**Why It Fits The Brief**",
            agent=self.creative_director,
        )
        task_copy = Task(
            description="Polish the ad copy into final, ready-to-use form.",
            expected_output="Final, polished ad copy.",
            agent=self.copywriter,
            context=[task],
        )
        crew = Crew(agents=[self.creative_director, self.copywriter], tasks=[task, task_copy], process=Process.sequential, memory=shared_memory, verbose=False)
        crew_output = crew.kickoff()
        result = (
            f"{str(crew_output.tasks_output[0])}\n\n---\n\n{str(crew_output.tasks_output[1])}"
            if len(crew_output.tasks_output) >= 2 else str(crew_output)
        )
        remember(f"Advertising CREATIVE_CONCEPT for '{brief}':\n{result}", scope="/dept/advertising/creative_concept", categories=["advertising", "creative"])
        return result

    def media_planning(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"MEDIA_PLANNING: Plan real media placement for: {brief}\n\n"
                "Research real channels/platforms that genuinely fit the target audience and "
                "any stated budget — never invent a platform, rate, or reach figure."
            ),
            expected_output="## Media Plan\n**Recommended Channels** — real platforms, with reasoning\n**Budget Notes**\n**Confidence Note** — flag anything unverified",
            agent=self.media_planner,
        )
        crew = Crew(agents=[self.media_planner], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Advertising MEDIA_PLANNING for '{brief}':\n{result}", scope="/dept/advertising/media_planning", categories=["advertising", "media"])
        return result

    def video_ad_production(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"VIDEO_AD_PRODUCTION: Plan a real video ad production for: {brief}\n\n"
                "Write a script and shot/scene breakdown, planned around real AI "
                "video-generation tools. Map the finished ad to a real YouTube ad format or "
                "Google Ads campaign structure. Never invent a platform spec or capability you "
                "haven't confirmed — flag anything uncertain instead."
            ),
            expected_output=(
                "## Video Ad Production Plan\n**Script**\n**Shot/Scene Breakdown**\n"
                "**AI Video Tooling** — what would actually be used and how\n"
                "**Target Ad Format** — real YouTube/Google Ads format this fits\n"
                "**Confidence Note** — anything unverified"
            ),
            agent=self.video_production_specialist,
        )
        crew = Crew(agents=[self.video_production_specialist], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Advertising VIDEO_AD_PRODUCTION for '{brief}':\n{result}", scope="/dept/advertising/video_ad_production", categories=["advertising", "video"])
        return result

    def run_campaign(self, brief: str) -> str:
        task = Task(
            description=f"Plan a full advertising campaign for: {brief}. Cover strategy, creative, and media placement.",
            expected_output="Advertising campaign plan: strategy, creative concept, and media plan.",
            agent=self.advertising_head,
        )
        crew = Crew(agents=[self.advertising_head], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Advertising run_campaign for '{brief}':\n{result}", scope="/dept/advertising/run_campaign", categories=["advertising", "campaign"])
        return result
