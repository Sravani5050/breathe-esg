# Decisions — Breathe ESG

## 1. SAP Data Format
**Decision:** Flat file CSV export (not IDoc or OData)
**Why:** Flat file exports are the most common way SAP data 
leaves enterprise systems for third-party tools. IDoc is 
complex XML used for system-to-system integration. For an 
ESG platform ingesting data, a flat file export is realistic 
and practical.
**What I ignored:** German column headers, plant code lookup 
tables, multi-currency amounts.
**What I'd ask the PM:** Do clients have SAP export templates 
already configured, or do we need to guide them?

## 2. Utility Data Format
**Decision:** Portal CSV export
**Why:** Most utility portals (MSEDCL, BESCOM etc.) offer CSV 
downloads of meter readings. PDF bills are harder to parse 
reliably. APIs are rare in Indian utilities.
**What I ignored:** Tariff structure details, billing periods 
that cross calendar months, multiple meters per building.
**What I'd ask the PM:** Do clients have multiple meters? 
How do they handle estimated vs actual readings?

## 3. Travel Data Format
**Decision:** CSV export with category column
**Why:** Platforms like Concur and Navan allow CSV exports of 
expense reports. Each row has a category (Flight/Hotel/Ground) 
which maps to different emission factors.
**What I ignored:** Airport code to distance conversion, 
cabin class emission multipliers, hotel star rating factors.
**What I'd ask the PM:** Do clients use Concur or Navan? 
Can we get API access or only manual exports?

## 4. Ingestion Mechanism
**Decision:** File upload (CSV)
**Why:** Most realistic for an MVP. Clients can export from 
their systems and upload. API integrations require client 
IT involvement which slows onboarding.

## 5. Suspicious Record Detection
**Decision:** Flag records where co2_kg > 10000 automatically
**Why:** Simple heuristic catches obvious data entry errors 
like wrong units (tonnes entered as kg).