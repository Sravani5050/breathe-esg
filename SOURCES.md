# Sources Research — Breathe ESG

## 1. SAP Data (Fuel & Procurement)

### What I researched
SAP exports data in several formats: IDoc (XML-based),
flat file (CSV/TXT), OData API, and BAPI function calls.
For sustainability reporting, companies typically use
SAP Environment Health & Safety (EHS) or manually export
from MM (Materials Management) module.

### What I chose
Flat file CSV export from SAP MM module.
Columns: date, material, plant, quantity, unit, amount.

### What my sample data looks like
- Fuel purchases (diesel, petrol) in litres
- Procurement (natural gas, coal) in cubic meters and kg
- Dates in YYYY-MM-DD format
- CO2 pre-calculated using standard emission factors
- Scope 1 for all SAP records (direct emissions)

### What would break in real deployment
- SAP exports often have German headers (MENGE, WERKS)
- Plant codes need lookup table to get location
- Units inconsistent (L, LTR, LITRE all mean litres)
- Dates in DD.MM.YYYY German format
- Character encoding issues (umlauts)

## 2. Utility Data (Electricity)

### What I researched
Utility portals in India (MSEDCL, BESCOM, TATA Power)
provide monthly billing CSV downloads. Each row represents
one billing period for one meter. Fields include meter
number, reading dates, units consumed (kWh), and amount.

### What I chose
Portal CSV export with monthly meter readings.

### What my sample data looks like
- Monthly electricity consumption in kWh
- Separate rows for factory, office, warehouse meters
- CO2 calculated using India grid emission factor
  (0.45 kg CO2 per kWh as per CEA 2023)
- Scope 2 for all utility records

### What would break in real deployment
- Billing periods don't align with calendar months
- Multiple tariff slabs within one bill
- Estimated readings vs actual readings not distinguished
- Different utilities use different CSV formats
- Power factor corrections affect actual consumption

## 3. Corporate Travel

### What I researched
Platforms like Concur SAP, Navan (formerly TripActions),
and Amadeus GBT provide expense report exports. Each
booking has a category (Air, Hotel, Car, Rail), dates,
origin/destination, and cost. For flights, IATA airport
codes are given but distances must be calculated separately.

### What I chose
CSV export with pre-categorized travel records.
Categories: Flight, Hotel, Ground transport.

### What my sample data looks like
- Flights with passenger count and route description
- Hotels with room-nights
- Ground transport with distance in km
- Emission factors: Flight ~0.255kg/km, Hotel ~30kg/night
- Scope 3 for all travel records

### What would break in real deployment
- Airport codes need distance matrix lookup
- Business vs economy class have different factors
  (business class = 3x economy emissions)
- Hotel emissions vary by country and star rating
- Car rental emissions depend on vehicle type
- Missing data: many records have cost but no distance