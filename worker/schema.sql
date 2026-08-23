-- TRoyMEDIAgency — D1 Database Schema

CREATE TABLE IF NOT EXISTS departments (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  agent_count INTEGER DEFAULT 5,
  status TEXT DEFAULT 'active',
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  department TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  goal TEXT,
  status TEXT DEFAULT 'active',
  tasks_completed INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  department TEXT NOT NULL,
  agent TEXT,
  task TEXT NOT NULL,
  input TEXT,
  output TEXT,
  status TEXT DEFAULT 'queued',
  created_at TEXT,
  completed_at TEXT
);

-- Seed departments
INSERT OR IGNORE INTO departments (id, name, description, agent_count) VALUES
  ('orchestrator', 'Management', 'CEO Assistant — DELEGATE, REVIEW, FINAL_QA', 1),
  ('marketing', 'Marketing', 'Trend research, content, publicity — 5 agents', 5),
  ('sales', 'Sales & Distribution', 'Pitches, distribution deals — 5 agents', 5),
  ('finance', 'Finance', 'Production budgets, royalties — 5 agents', 5),
  ('production', 'Production & Casting', 'Casting, scheduling, cast & crew support — 6 agents', 6),
  ('advertising', 'Advertising', 'Client ad campaigns — strategy, creative, media planning, AI video ad production — 6 agents', 6);

-- Seed agents
INSERT OR IGNORE INTO agents (id, department, name, role) VALUES
  ('mkt-1', 'marketing', 'marketing_head', 'Head of the AI Marketing Department'),
  ('mkt-2', 'marketing', 'entertainment_trend_researcher', 'Entertainment Trend Researcher'),
  ('mkt-3', 'marketing', 'content_creator', 'Content Creator'),
  ('mkt-4', 'marketing', 'press_publicity_relations_manager', 'Press & Publicity Relations Manager'),
  ('mkt-5', 'marketing', 'audience_analytics_reporter', 'Audience & Analytics Reporter'),
  ('sales-1', 'sales', 'sales_head', 'Head of the AI Sales & Distribution Department'),
  ('sales-2', 'sales', 'pitch_developer', 'Pitch Developer'),
  ('sales-3', 'sales', 'distribution_researcher', 'Distribution Researcher'),
  ('sales-4', 'sales', 'deal_negotiator', 'Deal Negotiator'),
  ('sales-5', 'sales', 'client_talent_relations_manager', 'Client & Talent Relations Manager'),
  ('fin-1', 'finance', 'finance_head', 'Head of the AI Finance Department'),
  ('fin-2', 'finance', 'production_budget_planner', 'Production Budget Planner'),
  ('fin-3', 'finance', 'royalty_payments_clerk', 'Royalty & Payments Clerk'),
  ('fin-4', 'finance', 'invoice_manager', 'Invoice Manager'),
  ('fin-5', 'finance', 'cost_optimizer', 'Cost Optimizer'),
  ('prod-1', 'production', 'production_head', 'Head of Production & Casting'),
  ('prod-2', 'production', 'casting_director', 'Casting Director'),
  ('prod-3', 'production', 'production_coordinator', 'Production Coordinator'),
  ('prod-4', 'production', 'talent_support_manager', 'Talent Support Manager'),
  ('prod-5', 'production', 'script_development_specialist', 'Script Development Specialist'),
  ('prod-6', 'production', 'crew_support_manager', 'Crew Support Manager'),
  ('adv-1', 'advertising', 'advertising_head', 'Head of the AI Advertising Department'),
  ('adv-2', 'advertising', 'creative_director', 'Creative Director'),
  ('adv-3', 'advertising', 'media_planner', 'Media Planner & Buyer'),
  ('adv-4', 'advertising', 'copywriter', 'Copywriter'),
  ('adv-5', 'advertising', 'account_strategist', 'Account Strategist'),
  ('adv-6', 'advertising', 'video_production_specialist', 'AI Video Production Specialist');
