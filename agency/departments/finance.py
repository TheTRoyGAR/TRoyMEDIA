from crewai import Agent, Task, Crew, Process
from agency.core.llm import get_llm
from agency.core.memory import shared_memory, remember, recall_context
from agency.tools import write


class FinanceDepartment:
    """Finance Department — 1 head + 4 specialists. Skills: PRODUCTION_BUDGET, ROYALTY_TRACKING, REPORTING."""

    def __init__(self):
        llm = get_llm("haiku")

        self.finance_head = Agent(
            role="Head of the AI Finance Department",
            goal="Build real production budgets, track real talent royalties/payments, and keep TRoyMEDIA's finances accurate.",
            backstory=(
                "You are the Head of the AI Finance Department at TRoy Media Agency "
                "(TRoyMEDIA). Production finance is unforgiving — a wrong budget line or a "
                "missed royalty payment is a real, costly problem for real people.\n\n"
                "Your specific skills and responsibilities:\n"
                "1. PRODUCTION_BUDGET — Build a real, itemized production budget (cast, crew, "
                "locations, post-production) with stated assumptions, never invented figures.\n"
                "2. ROYALTY_TRACKING — Track real talent payments and royalty obligations "
                "accurately.\n"
                "3. REPORTING — Generate accurate, client-facing financial summary reports.\n\n"
                "All financial models must be transparent, defensible, and based on stated assumptions.\n\n"
                "Operating rules: split CONFIRMED vs ESTIMATED for every budget line. Never invent "
                "a royalty figure without a real, signed source. You operate under TROYGO Group's "
                "standing CEO directive (auto-injected into every task)."
            ),
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.budget_planner = Agent(
            role="Production Budget Planner",
            goal="Build real, itemized production budgets.",
            backstory="You are the Production Budget Planner at TRoy Media Agency. You itemize real production costs — cast, crew, locations, post-production — never invented figures.",
            llm=llm,
            verbose=False,
        )

        self.royalty_clerk = Agent(
            role="Royalty & Payments Clerk",
            goal="Track real talent payments and royalty obligations.",
            backstory="You are the Royalty & Payments Clerk at TRoy Media Agency. You track real talent payments and royalty obligations accurately and transparently.",
            llm=llm,
            verbose=False,
        )

        self.invoice_manager = Agent(
            role="Invoice Manager",
            goal="Create, send, and track all client invoices and payments.",
            backstory="You are the Invoice Manager at TRoy Media Agency. You manage the full invoicing lifecycle — creation through payment-failure follow-up and reconciliation.",
            llm=llm,
            tools=[write],
            verbose=False,
        )

        self.cost_optimizer = Agent(
            role="Cost Optimizer",
            goal="Identify real cost-saving opportunities without compromising production quality.",
            backstory="You are the Cost Optimizer at TRoy Media Agency. You look for real ways to reduce production costs without cutting corners on quality.",
            llm=llm,
            verbose=False,
        )

    def production_budget(self, brief: str) -> str:
        task = Task(
            description=(
                f"{recall_context(brief)}"
                f"PRODUCTION_BUDGET: Build an itemized production budget for: {brief}\n\n"
                "List real cost categories (cast, crew, locations, post-production, other) with "
                "amounts (or clearly-labeled placeholder ranges + assumption if real figures "
                "aren't provided) — state all assumptions explicitly."
            ),
            expected_output="## Production Budget\n**Itemized Costs** — category, description, amount/range\n**Total**\n**Assumptions** — listed explicitly",
            agent=self.budget_planner,
        )
        crew = Crew(agents=[self.budget_planner], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Finance PRODUCTION_BUDGET for '{brief}':\n{result}", scope="/dept/finance/production_budget", categories=["finance", "budget"])
        return result

    def royalty_tracking(self, brief: str) -> str:
        task = Task(
            description=f"{recall_context(brief)}ROYALTY_TRACKING: Set up a real royalty/payment tracking plan for: {brief}",
            expected_output="## Royalty Tracking Plan\n**Payment Schedule**\n**Obligations**\n**Tracking Method**",
            agent=self.royalty_clerk,
        )
        crew = Crew(agents=[self.royalty_clerk], tasks=[task], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Finance ROYALTY_TRACKING for '{brief}':\n{result}", scope="/dept/finance/royalty_tracking", categories=["finance", "royalty"])
        return result

    def reporting(self, period: str = "monthly") -> str:
        task_books = Task(
            description=f"Summarize the {period} financial transactions and categorize income vs expenses.",
            expected_output="Categorized summary: revenue streams, expense categories, net position.",
            agent=self.budget_planner,
        )
        task_report = Task(
            description=f"REPORTING: Generate a {period} client-facing financial summary report using the budget summary.",
            expected_output="## Financial Summary Report\n**Revenue**\n**Expenses**\n**Profit Margin**\n**Cash Flow**\n**Key Insights**\n**Recommendations**",
            agent=self.finance_head,
            context=[task_books],
        )
        crew = Crew(agents=[self.budget_planner, self.finance_head], tasks=[task_books, task_report], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Finance REPORTING ({period}):\n{result}", scope="/dept/finance/reporting", categories=["finance", "reporting"])
        return result

    def generate_report(self, period: str = "monthly") -> str:
        task_report = Task(
            description=f"Generate a {period} financial report for TRoy Media Agency. Include revenue, expenses, profit margin, cash flow.",
            expected_output="Financial report with sections: REVENUE, EXPENSES, PROFIT MARGIN, CASH FLOW, KEY INSIGHTS. If no real data is available for a figure, state '$0 / unconfirmed — no real data available' plainly — never invent a placeholder number and present it as if it were real.",
            agent=self.finance_head,
        )
        task_optimize = Task(
            description="Based on the financial report, identify 3 real cost-saving opportunities.",
            expected_output="3 specific cost-saving actions with estimated savings.",
            agent=self.cost_optimizer,
            context=[task_report],
        )
        crew = Crew(agents=[self.finance_head, self.cost_optimizer], tasks=[task_report, task_optimize], process=Process.sequential, memory=shared_memory, verbose=False)
        result = str(crew.kickoff())
        remember(f"Finance report ({period}):\n{result}", scope="/dept/finance/generate_report", categories=["finance", "reporting"])
        return result
