# Fulfillment Hub — Karmic Seed Round 3

A simple operations dashboard for XYZ's e-commerce fulfillment workflow.

## Problem focus
I prioritized four operational problems from the case:
- lack of order visibility
- priority orders getting mixed with regular orders
- inventory mismatches between warehouses
- operational exceptions being handled informally

## What the prototype does
- Dashboard with fulfillment KPIs
- Order tracking and search
- Priority and delayed-order queue
- Status progression from Received → Processing → Picking → Packing → Staged → Shipped
- Inventory shortage detection
- Secondary → Main stock movement
- Issue tracking and resolution
- Sample data representing a 200–300 order/day operation

## Run locally — Windows

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

## Demo flow
1. Start on Dashboard and explain the operational KPIs.
2. Open Priority Queue and show urgent orders surfaced first.
3. Open Orders and demonstrate search/filter + Advance status.
4. Open Inventory and show a shortage plus Secondary → Main movement.
5. Open Issues and resolve an exception.
6. Explain that the tool focuses on visibility and exception handling rather than trying to automate the whole warehouse.

## Submission note
This is a prototype using generated dummy operational data because the case provides no real store or courier integrations.
