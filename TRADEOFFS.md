# Tradeoffs — Breathe ESG

## 1. No Real Authentication System
**What I didn't build:** Proper login system with JWT tokens,
role-based access (analyst vs admin vs client).
**Why:** Would have taken a full day to implement properly.
For a prototype, the Django admin handles basic auth.
**What a real system needs:** Each client company should have
their own login. Analysts should only see their assigned
companies. Audit logs should record real usernames.

## 2. No Emission Factor Calculation Engine
**What I didn't build:** Automatic CO2 calculation from
activity data using standard emission factors (IPCC, GHG
Protocol).
**Why:** Emission factors vary by region, year, and fuel type.
Building a reliable factor database takes significant research.
For now, CO2 values are pre-calculated in the CSV.
**What a real system needs:** A factor table that maps
(category, unit, region, year) to a CO2 multiplier. Then
co2_kg = quantity × factor.

## 3. No Real Deployment Pipeline
**What I didn't build:** Production-ready deployment with
proper database (PostgreSQL), environment variables,
static file serving, and CI/CD pipeline.
**Why:** Time constraint. SQLite works for prototype.
**What a real system needs:** PostgreSQL on Railway/Render,
environment variables for secrets, gunicorn for serving,
whitenoise for static files.