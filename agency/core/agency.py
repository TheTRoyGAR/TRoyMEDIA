from agency.departments.marketing import MarketingDepartment
from agency.departments.sales import SalesDepartment
from agency.departments.finance import FinanceDepartment
from agency.departments.production import ProductionDepartment


class TRoyMEDIAAgency:
    """TRoy Media Agency (TRoyMEDIA) — Core Orchestrator + 4 departments, 21 agents, zero employees."""

    CEO = "I. Ertan Govdeli"
    NAME = "TRoy Media Agency (TRoyMEDIA)"

    def __init__(self):
        self.marketing = MarketingDepartment()
        self.sales = SalesDepartment()
        self.finance = FinanceDepartment()
        self.production = ProductionDepartment()

        from agency.core.orchestrator import CoreOrchestrator
        self.orchestrator = CoreOrchestrator(self)

    def intake_brief(self, brief: str) -> str:
        return self.orchestrator.intake_brief(brief)

    def run_daily_briefing(self, context: str = "") -> str:
        return self.production.run_task(context or "daily production briefing")

    def run_sales_pipeline(self, brief: str) -> str:
        return self.sales.run_pipeline(brief)

    def run_marketing_campaign(self, brief: str) -> str:
        return self.marketing.run_campaign(brief)

    def run_finance_report(self, period: str = "monthly") -> str:
        return self.finance.generate_report(period)

    def run_production_task(self, brief: str) -> str:
        return self.production.run_task(brief)

    def status(self) -> dict:
        return {
            "agency": self.NAME,
            "ceo": self.CEO,
            "orchestrator": {
                "agent": "CEO Assistant",
                "skills": ["DELEGATE", "REVIEW", "FINAL_QA"],
            },
            "departments": 4,
            "agents_per_department": "5 (Production has 6)",
            "total_agents": 22,
            "department_skills": {
                "marketing": ["TREND_SCRAPE", "CONTENT_GEN", "PUBLICITY_AUDIT"],
                "sales": ["PITCH_DEVELOPMENT", "DISTRIBUTION_DEAL", "OBJECTION_HANDLER"],
                "finance": ["PRODUCTION_BUDGET", "ROYALTY_TRACKING", "REPORTING"],
                "production": ["CASTING_CALL", "PRODUCTION_SCHEDULE", "TALENT_SUPPORT", "SCRIPT_DEVELOPMENT", "CREW_SUPPORT"],
            },
            "shared_memory": "all departments read/write one cross-department knowledge store (agency/core/memory.py)",
            "status": "online",
        }
