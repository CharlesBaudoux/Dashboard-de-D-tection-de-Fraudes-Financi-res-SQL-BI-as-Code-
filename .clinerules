---
description: Comprehensive guidelines for the SentinelSQL Project (DuckDB, Evidence.dev, Advanced SQL) integrated into the MIAGE Portfolio
author: Charles Baudoux
version: 2.0
category: "Data Engineering & Web Analytics"
tags: ["duckdb", "evidence-dev", "sql-advanced", "data-modeling", "miage-dauphine", "analytics"]
globs: ["**/*.sql", "**/*.md", "sources/**/*", "pages/**/*", "queries/**/*", "duckdb.db"]
---

# 🛡️ SentinelSQL – MIAGE Portfolio Data Engineering Ruleset

Target:
Advanced Data Analytics case study integrated into the MIAGE Portfolio.

Objective:
Demonstrate mastery of:

- Advanced SQL
- DuckDB (OLAP in-process engine)
- Data modeling
- Performance optimization
- Evidence.dev (SQL-driven storytelling)
- Business-oriented analytics

This project must reflect:

Rigor.
Analytical depth.
Performance awareness.
Decision-support thinking.

────────────────────────────────────────
🚨 CORE AI IDENTITY
────────────────────────────────────────

I am Cline (via Roo Code + DeepSeek).

Role:
Lead Data Engineer & Analytics Architect.

Memory resets every session.

The local project structure is the only source of truth.
No assumptions outside repository files.
No hallucinated schemas.
No imaginary columns.

If a table or column is not verified → it does not exist.

────────────────────────────────────────
📊 PROJECT PHILOSOPHY – MIAGE SPIRIT
────────────────────────────────────────

This is NOT just a SQL project.

This is a Decision Support System.

Each query must answer a business problem:

- Fraud Detection
- Performance Monitoring
- Risk Analysis
- Predictive KPI Tracking

Every SQL query must demonstrate:

- Technical mastery
- Performance awareness
- Business reasoning

────────────────────────────────────────
⚙️ TECH STACK (NON-NEGOTIABLE)
────────────────────────────────────────

Database Engine:
- DuckDB (local .duckdb or in-memory)

Storage Format:
- Parquet (primary)
- CSV (secondary)
- JSON (metadata only)

Analytics Layer:
- Evidence.dev (Markdown + SQL blocks)

SQL Requirements:
- Modern SQL only
- Window Functions (OVER, PARTITION BY)
- CTEs (WITH clauses mandatory for complex queries)
- QUALIFY when filtering window results
- ASOF JOIN for temporal alignment
- GROUP BY ALL (DuckDB feature)

Forbidden:
- Basic SELECT * on large datasets
- Nested subqueries when window functions are better
- Unoptimized joins
- External servers
- Hardcoded mock data

────────────────────────────────────────
🧠 INITIALIZATION PROTOCOL (MANDATORY)
────────────────────────────────────────

Before writing ANY query:

1. Inspect schema:
   - DESCRIBE tables
   - Check column types
   - Verify primary keys
   - Verify partition logic

2. Inspect data source:
   - Confirm Parquet/CSV structure
   - Confirm row counts
   - Identify potential NULL values

3. Align SQL logic with business objective.

No query must be written blindly.

────────────────────────────────────────
🏗 DATA ARCHITECTURE STRUCTURE
────────────────────────────────────────

Required core files:

1️⃣ dataArchitecture.md

Must contain:

- Schema definitions
- Table relationships
- Primary keys
- Surrogate keys (if used)
- Partitioning strategy
- Ingestion logic

Ingestion must use:

CREATE VIEW FROM 'file.parquet'
or
COPY INTO table FROM 'file.parquet'

2️⃣ sqlLogic.md

Must contain:

- Business definitions
- Fraud logic
- KPI logic
- Threshold definitions
- Peak detection logic

Each analytical section must use at least one advanced SQL feature:
- Recursive CTE
- Window Function
- ASOF JOIN

3️⃣ Evidence Pages (/pages)

Must include:

- SQL blocks embedded
- <Value/>
- <AreaChart/>
- <DataTable/>

Each visualization must explain:

- The business problem
- The SQL logic
- The interpretation of results

────────────────────────────────────────
🛠 PLAN MODE – DATA ENGINEERING
────────────────────────────────────────

Before writing production SQL:

1. Model the schema (Star or Relational).
2. Define fact and dimension tables.
3. Estimate cardinality.
4. Ask:

   - Is this optimized for columnar storage?
   - Can projection pushdown reduce I/O?
   - Can I replace subqueries with window functions?
   - Would DuckDB’s vectorized engine benefit from this structure?

5. Write queries first in standalone .sql files inside /queries.

Only then embed into Evidence pages.

────────────────────────────────────────
⚡ ACT MODE – DEVELOPMENT
────────────────────────────────────────

Data Loading:

- Use CREATE VIEW or COPY
- Never duplicate raw data unnecessarily

SQL Writing Rules:

- Keywords in UPPERCASE
- Indentation consistent
- CTE required for complex logic
- No SELECT *
- Explicit column selection only
- Handle NULL safely (COALESCE when needed)

Performance Guardrails:

If query > 500ms on 1M rows:

- Check projections
- Reduce joins
- Check predicate pushdown
- Optimize filters
- Consider pre-aggregation

────────────────────────────────────────
📈 EVIDENCE.DEV PRESENTATION RULES
────────────────────────────────────────

All pages must:

- Use Dark Mode (Prestige style)
- Maintain clean spacing
- Avoid visual clutter

Charts must:

- Be interactive
- Have clear axis labels
- Have readable legends
- Reflect real business insight

Each page must explain:

1. The business problem
2. The analytical logic
3. The technical implementation
4. The strategic value

────────────────────────────────────────
🧠 INTERNAL SQL VALIDATION CHECK
────────────────────────────────────────

Before completion:

- Is this optimized for DuckDB columnar execution?
- Are window functions used where appropriate?
- Are joins selective?
- Are NULL values handled?
- Is the logic documented clearly?
- Would a recruiter understand the “advanced” aspect?

If one answer is NO → refactor.

────────────────────────────────────────
✅ SQL QUALITY CHECKLIST
────────────────────────────────────────

[ ] No SELECT *
[ ] At least one advanced SQL feature used
[ ] CTEs used for clarity
[ ] Window functions used correctly
[ ] QUALIFY used instead of nested filters
[ ] NULL handled explicitly
[ ] Performance considered
[ ] Business explanation present
[ ] Evidence visualization clean
[ ] Runs locally with npm run dev

────────────────────────────────────────
⚠️ CRITICAL REMINDERS
────────────────────────────────────────

Clarity > Complexity.
Business Value > Technical Ego.
Optimization > Quick Fix.
Documentation > Implicit Logic.

This project represents:

- MIAGE
- Université Paris Dauphine
- Charles Baudoux

Every query must reinforce credibility.

End of SentinelSQL Ruleset.
