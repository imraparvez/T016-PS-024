# Decision Log

| ID | Topic | Current implementation / assumption | Status |
|---|---|---|---|
| D-001 | Money precision | Use `BigDecimal`, never `double` | Adopted |
| D-002 | Interface | Command-line, file-oriented | Adopted |
| D-003 | IRN | Simulated validation; no GST portal integration | Confirm with organizers |
| D-004 | Invoice normalization | Uppercase, trim, remove leading zeros in numeric suffix | Confirm collision behavior |
| D-005 | Exactly 24 hours | Treat duration <= 24h as within window | Confirm inclusive boundary |
| D-006 | IGST allocation | Apply in listed sequence: IGST, CGST, SGST | Confirm ordering if credit insufficient |
| D-007 | File formats | CSV adapters are illustrative; await official sample files | Open |
| D-008 | Rounding | Round invoice tax-head total to whole rupee using HALF_UP | Confirm tie policy |
| D-009 | 2B matching | Compare tax heads independently; <= ₹1 difference tolerated | Confirm line vs invoice matching |
| D-010 | 180-day rule | Trigger when elapsed days > 180 | Confirm day-180 boundary |
