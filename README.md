============================================================
BLACKROCK MICRO-INVESTMENT CHALLENGE: TECHNICAL DOCUMENTATION
============================================================

PROJECT TITLE: Enterprise Micro-Investment Orchestrator
DEVELOPER: Prijith Ayure
DEPLOYMENT PORT: 5477

------------------------------------------------------------
1. PROJECT OVERVIEW
------------------------------------------------------------
This application implements a high-scale financial data pipeline designed to transform daily 
micro-expenses into long-term wealth projections. 
The system is built to handle up to 1 million transactions while maintaining mathematical 
accuracy across complex temporal rules.

------------------------------------------------------------
2. SYSTEM ARCHITECTURE & LOGIC PIPELINE
------------------------------------------------------------
The system follows a modular five-stage processing architecture:

A. TRANSACTION BUILDING (:parse)
   - Automatically rounds raw expenses to the nearest ₹100 ceiling to calculate initial 
     remanents.

B. VALIDATION LAYER (:validator)
   - Ensures data integrity by filtering out negative amounts and invalid entry formats.

C. TEMPORAL RULE ENGINE
   - Q-Rules: Applies fixed overrides (e.g., setting remanent to 0) for specific exclusion 
     windows.
   - P-Rules: Injects proactive increases (e.g., +₹25) to boost savings during target 
     ranges.

D. K-PERIOD GROUPING
   - Aggregates total investment amounts across multiple, overlapping evaluation date 
     ranges.

E. PROJECTION ENGINE
   - NPS Returns: Projected at 7.11% compound interest.
   - Index Fund Returns: Projected at 14.49% compound interest.
   - Inflation Adjustment: All values are adjusted for a 5.5% annual inflation rate to 
     show realistic future purchasing power.

------------------------------------------------------------
3. INFRASTRUCTURE & DEPLOYMENT
------------------------------------------------------------
- DOCKER: The application is fully containerized with an image named 
  'blk-hacking-ind-prijith-ayure'.
- PORT: Accessible via port 5477 inside and outside the container.
- PERFORMANCE MONITOR: A dedicated endpoint (/performance) provides real-time tracking 
  of memory usage (MB) and active threads.

------------------------------------------------------------
4. SETUP & USAGE
------------------------------------------------------------
1. Build and Run:
   docker compose up --build

2. Access Interactive Docs:
   http://localhost:5477/docs

3. Run Automated Tests:
   pytest test/test_investments.py

------------------------------------------------------------
5. INNOVATIVE APPROACH
------------------------------------------------------------
Beyond the basic requirements, this solution uses indexed temporal grouping to achieve O(n) 
efficiency, allowing the system to process massive datasets without memory degradation. 
The inclusion of a real-time performance monitor ensures the system maintains high 
availability in production environments.
============================================================