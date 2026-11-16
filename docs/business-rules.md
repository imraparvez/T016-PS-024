# PS-024 Business Rules

1. **Place of supply:** Intra-state uses CGST + SGST; inter-state uses IGST. For goods delivered to another state, use the delivery state as place of supply.
2. **Tax rates:** 0%, 5%, 12%, 18%, 28%; cess applies only to tagged items. Round invoice totals per tax head to rupees.
3. **E-invoice:** Mandatory for B2B when turnover is above ₹5 crore. IRN within 24 hours of invoice date; invalid IRN excluded from outward register until regenerated.
4. **Numbering:** Sequential per financial year with no gaps. Cancelled invoice retains number/status. Cancellation only within 24 hours of IRN.
5. **Credit notes:** Must reference original invoice; cumulative taxable value cannot exceed original. Deadline 30 November of following FY.
6. **RCM:** Buyer pays tax in cash for listed services from unregistered suppliers (e.g. legal, GTA); eligible ITC may be claimed in same period.
7. **2B matching:** Supplier GSTIN + normalized invoice number + invoice date. Amount tolerance ₹1 per tax head.
8. **ITC:** MATCHED and MISMATCH_AMOUNT may qualify; mismatch uses lower amount. MISSING_IN_2B held/rechecked up to two periods. Blocked categories remain ineligible.
9. **180 days:** Reverse ITC for unpaid invoices beyond 180 days, with 18% annual interest from claim date; re-avail on payment. Reverse common inputs proportionately for exempt turnover.
10. **Set-off:** IGST -> IGST, CGST, SGST; CGST -> CGST, IGST; SGST -> SGST, IGST. No CGST/SGST cross-utilization. Balance paid in cash.
11. **Due date and charges:** Due 20th of next month; interest 18% p.a. daily on net cash liability; late fee ₹50/day or ₹20/day for nil return, capped at ₹10,000.
12. **Precedence:** invoice validity -> tax computation -> 2B matching -> blocked list -> 180-day reversal -> proportionate reversal -> set-off.
