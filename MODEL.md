# Data Model — Breathe ESG

## Overview
This app ingests emissions data from 3 sources, normalizes it, 
and lets analysts review and approve before audit.

## Tables

### 1. Company
Stores client companies using the platform.
- id, name, industry, created_at
- Supports multi-tenancy — each record belongs to one company

### 2. DataUpload
Tracks every file uploaded — who uploaded what and when.
- id, company, source_type (SAP/UTILITY/TRAVEL)
- file_name, uploaded_at, row_count
- Source-of-truth tracking — every EmissionRecord links back here

### 3. EmissionRecord
The core table — one row per emission activity.
- scope (1/2/3) — Scope 1=fuel, Scope 2=electricity, Scope 3=travel
- category, description, quantity, unit, co2_kg
- status: pending → approved or flagged
- is_suspicious: auto-flagged if co2_kg > 10000
- Links to both Company and DataUpload

### 4. AuditLog
Every approval or flag action is recorded here.
- Links to EmissionRecord
- Records who did what and when
- Immutable trail for auditors

## Key Design Decisions
- Multi-tenancy via Company foreign key on every record
- Scope 1/2/3 stored as integer field for easy filtering
- Unit stored as raw string — normalization happens at ingestion
- is_suspicious auto-calculated at upload time
- audit trail is append-only