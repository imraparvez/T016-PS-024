PS-024 – GST Invoicing, E-Invoice Validation and GSTR-2B Input Tax Credit Reconciliation — Sample Data Pack
Prepared by 10 SECONDS for Team T016.

Return periods covered: October, November and December 2026 (FY 2026-27). The taxpayer trades electrical goods, FMCG and services from Karnataka. Documents are numbered per series per FY (INV/26-27/nnnn, CN/26-27/nnnn, DN/26-27/nnnn); SET_SEQUENCE tells you where each series stands on 1 October.
Files
File	What it holds	Row count
taxpayer.csv	The taxpayer's two GSTINs (KA primary, TN additional place of business with no activity)	2 data rows
items.csv	Item / service master with HSN/SAC, GST rate, cess, exempt, blocked and RCM tags	20 data rows
customers.csv	10 customers (8 registered, 2 unregistered)	10 data rows
suppliers.csv	12 suppliers (10 registered, 2 unregistered RCM service providers)	12 data rows
prior_invoices.csv	FY 2025-26 sales invoices referenced by credit notes in this period	4 data rows
purchase_register.csv	120 purchase lines (one supplier invoice per line), incl. opening lines from Apr-May 2026 for the 180-day rule	120 data rows
gstr2b_2026_10.csv	GSTR-2B for October 2026 as downloaded from the portal	33 data rows
gstr2b_2026_11.csv	GSTR-2B for November 2026	45 data rows
gstr2b_2026_12.csv	GSTR-2B for December 2026	37 data rows
commands.txt	Sales documents (80 invoices/notes), IRNs, cancellations, purchase payments, 2B loads, reconciliation, return filing, prints	212 command lines (excluding comments)


Row numbers quoted below are 1-based data-row numbers (the header is row 0). Line numbers for commands.txt are physical line numbers including comment lines.
Column reference
Conventions: dates YYYY-MM-DD; timestamps YYYY-MM-DD HH:MM:SS (24h, IST, no timezone suffix); money in Rs as plain decimals with 2 places (no commas, no symbol); percentages as plain numbers (12.5 means 12.5%); booleans true/`false`; IDs uppercase with a fixed prefix.
taxpayer.csv
Column	Type	Units / format	Allowed values	Notes
gstin	string	15-char GSTIN	—	same PAN for both rows
legal_name	string	—	—	—
state	string	2-letter code	KA, TN	—
registration_type	enum	—	PRIMARY, ADDITIONAL	—
aggregate_turnover	decimal	Rs	—	PAN-level, previous FY; > 5 crore means e-invoice mandatory for B2B
fy_start	date	—	—	financial year runs 1 Apr - 31 Mar


items.csv
Column	Type	Units / format	Allowed values	Notes
item_code	string	ITM-nn	—	—
description	string	—	—	—
hsn_sac	string	8-digit HSN / 6-digit SAC	—	—
item_type	enum	—	GOODS, SERVICE	drives place-of-supply rule
gst_rate	int	%	0, 5, 12, 18, 28	—
cess_rate	decimal	%	—	0 = no cess
exempt	bool	—	—	exempt supply (counts to exempt turnover)
blocked_category	enum	—	NONE, MOTOR_VEHICLE, FOOD, CLUB_MEMBERSHIP	blocked ITC list
rcm_notified	bool	—	—	reverse charge when bought from an unregistered supplier


customers.csv
Column	Type	Units / format	Allowed values	Notes
customer_id	string	CUST-nn	—	—
name	string	—	—	—
gstin	string	15-char GSTIN	—	empty = unregistered (B2C)
state	string	2-letter code	—	—
registered	bool	—	—	—
address_on_record	bool	—	—	for services to unregistered persons (BR-01)


suppliers.csv
Column	Type	Units / format	Allowed values	Notes
supplier_id	string	SUP-nn	—	—
name	string	—	—	—
gstin	string	15-char GSTIN	—	empty = unregistered
state	string	2-letter code	—	—
registered	bool	—	—	—


prior_invoices.csv
Column	Type	Units / format	Allowed values	Notes
doc_no	string	INV/25-26/nnnn	—	—
doc_date	date	—	—	FY 2025-26
customer_id	string	—	customers.csv	—
taxable_value	decimal	Rs	—	credit-note ceiling
cgst	decimal	Rs	—	—
sgst	decimal	Rs	—	—
igst	decimal	Rs	—	—
cess	decimal	Rs	—	—
irn	string	64 hex chars	—	—


purchase_register.csv
Column	Type	Units / format	Allowed values	Notes
purchase_id	string	PUR-nnnn	—	—
supplier_id	string	—	suppliers.csv	—
supplier_gstin	string	—	—	empty for unregistered suppliers
invoice_no	string	—	—	as keyed in your books
invoice_date	date	—	—	—
book_period	string	YYYY-MM	—	period the purchase was booked
item_code	string	—	items.csv	—
taxable_value	decimal	Rs	—	—
cgst	decimal	Rs	—	—
sgst	decimal	Rs	—	—
igst	decimal	Rs	—	—
cess	decimal	Rs	—	—
usage	enum	—	BUSINESS, COMMON	COMMON = used for taxable and exempt supplies (proportionate reversal)
itc_claimed_on	date	—	—	only for opening lines (book_period before 2026-10): date ITC was claimed; empty otherwise


gstr2b_2026_10.csv
Column	Type	Units / format	Allowed values	Notes
return_period	string	YYYY-MM	2026-10..2026-12	2B period the row was reported in
supplier_gstin	string	15-char GSTIN	suppliers.csv	—
supplier_name	string	—	—	trade name as on portal
invoice_no	string	—	—	as reported by the supplier — may differ in case/zeros from your books
invoice_date	date	—	—	—
taxable_value	decimal	Rs	—	—
igst	decimal	Rs	—	—
cgst	decimal	Rs	—	—
sgst	decimal	Rs	—	—
cess	decimal	Rs	—	—
itc_available	enum	—	Y, N	portal flag; always Y here


gstr2b_2026_11.csv
Column	Type	Units / format	Allowed values	Notes
return_period	string	YYYY-MM	2026-10..2026-12	2B period the row was reported in
supplier_gstin	string	15-char GSTIN	suppliers.csv	—
supplier_name	string	—	—	trade name as on portal
invoice_no	string	—	—	as reported by the supplier — may differ in case/zeros from your books
invoice_date	date	—	—	—
taxable_value	decimal	Rs	—	—
igst	decimal	Rs	—	—
cgst	decimal	Rs	—	—
sgst	decimal	Rs	—	—
cess	decimal	Rs	—	—
itc_available	enum	—	Y, N	portal flag; always Y here


gstr2b_2026_12.csv
Column	Type	Units / format	Allowed values	Notes
return_period	string	YYYY-MM	2026-10..2026-12	2B period the row was reported in
supplier_gstin	string	15-char GSTIN	suppliers.csv	—
supplier_name	string	—	—	trade name as on portal
invoice_no	string	—	—	as reported by the supplier — may differ in case/zeros from your books
invoice_date	date	—	—	—
taxable_value	decimal	Rs	—	—
igst	decimal	Rs	—	—
cgst	decimal	Rs	—	—
sgst	decimal	Rs	—	—
cess	decimal	Rs	—	—
itc_available	enum	—	Y, N	portal flag; always Y here


Command file format
commands.txt holds one command per line in the form COMMAND_NAME|arg1|arg2|.... Commands must be processed strictly in file order. Lines starting with # are comments and blank lines are ignored. An empty argument (two pipes in a row) means "not supplied". Every command used in this pack:
Command	Arguments (in order)	Meaning
SET_SEQUENCE	series|last_used_number	Last number already used in the series this FY (INV, CN, DN are separate series)
LOAD_PURCHASES	file_name	Load purchase_register.csv
INVOICE	doc_no|issue_ts|customer_id|ship_to_state|lines	Raise a tax invoice; lines = item_code:qty:unit_price joined by ';' (unit price excl. GST)
CREDIT_NOTE	doc_no|issue_ts|original_doc_no|lines	Credit note against an invoice (this FY or prior_invoices.csv); lines as above (taxable value = qty x price)
DEBIT_NOTE	doc_no|issue_ts|original_doc_no|lines	Debit note against an invoice
IRN	doc_no|generated_ts	IRN generated for a B2B document at this instant (BR-03 24-hour window from issue_ts)
CANCEL	doc_no|cancel_ts	Cancel a document (allowed only within 24 h of its IRN)
PURCHASE_PAYMENT	purchase_id|payment_date	Supplier invoice paid in full on this date (BR-09)
LOAD_2B	period|file_name	Ingest the GSTR-2B file for the period
RECONCILE	period	Run line-wise matching and ITC decisions for the period
PRINT_OUTWARD_REGISTER	period	Print the outward register
PRINT_RECON	period	Print the reconciliation report
FILE_RETURN	gstin|period|filing_date	File the return and pay net cash liability on filing_date (due on the 20th of the next month)
PRINT_LIABILITY	period	Print the liability / set-off / cash table


Planted scenarios
Every edge case in the brief, mapped to the exact record where it occurs, followed by extra traps.
- EC-01 Supplier in Karnataka billing a Karnataka customer with goods delivered to Tamil Nadu
  - INV/26-27/0394: customer CUST-04 is registered in KA but ship_to_state is TN — place of supply is TN, so IGST at full rate, not CGST+SGST — commands.txt line 20
- EC-02 Invoice number 'INV-0012' vs '0012' vs 'inv-12' in 2B
  - Three suppliers each with supplier invoice 12: books 'INV-0012' vs 2B '0012' (SUP-04), books 'INV-0012' vs 2B 'inv-12' (SUP-02), books '0012' vs 2B 'INV-0012' (SUP-08) — apply the BR-07 normalisation (case-insensitive, strip leading zeros) and state how you treat the 'INV-' prefix — purchase_register.csv PUR-0023, PUR-0024, PUR-0027; gstr2b_2026_10.csv invoice_no 0012 / inv-12 / INV-0012
- EC-03 Amount differs by exactly Rs 1.00 and Rs 1.01
  - PUR-0033: 2B IGST is exactly Rs 1.00 above books (within tolerance -> MATCHED); PUR-0034: 2B CGST is Rs 1.01 below books (MISMATCH_AMOUNT -> claim the lower 2B CGST) — purchase_register.csv PUR-0033 (row 33), PUR-0034 (row 34); gstr2b_2026_10.csv invoice MH/26-27/0781 and CHO/2210
- EC-04 IRN generated at hour 24 exactly
  - INV/26-27/0402 issued 2026-10-21 16:45:00, IRN at 2026-10-22 16:45:00 = exactly 24:00:00 later (boundary); INV/26-27/0403 gets its IRN 24:00:01 after issue -> INVALID_IRN, excluded from the register, and is re-raised as INV/26-27/0405 with a fresh number — commands.txt lines 39, 45 (exact 24 h); 40, 46 (late); 47 (regenerated)
- EC-05 Credit note on 30 November vs 1 December
  - CN/26-27/0028 dated 2026-11-30 against FY 2025-26 invoice INV/25-26/1180 is on the last allowed day; CN/26-27/0029 dated 2026-12-01 against INV/25-26/1277 must be rejected — commands.txt lines 138, 141; prior_invoices.csv rows 1-2
- EC-06 Purchase paid on day 180 vs 181
  - PUR-0002 dated 2026-05-20 is paid 2026-11-16 = day 180 (no reversal); PUR-0003 dated 2026-05-21 is paid 2026-11-18 = day 181 (reverse the ITC with 18% interest from the claim date 2026-06-20, then re-avail on payment) — purchase_register.csv PUR-0002, PUR-0003; commands.txt lines 98, 104
- EC-07 IGST credit larger than IGST liability with CGST and SGST liabilities unequal
  - November: inter-state purchases (IGST credit Rs 283640.00) far exceed the few small IGST sales, so IGST credit is left over after IGST and spills to CGST then SGST; PUR-0059 has 2B SGST Rs 4.50 lower than books, so the claimable CGST and SGST credits — and the net CGST/SGST liabilities after set-off — are unequal — purchase_register.csv PUR-0047, PUR-0057, PUR-0065, PUR-0072, PUR-0059; commands.txt line 198 (FILE_RETURN 2026-11)
- EC-08 Nil return filed late
  - Additional-place GSTIN 33DKQCQ1399R1ZM (TN) has no supplies or purchases at all; its October nil return is filed 2026-11-27, 7 days after the 20th — nil-return late fee Rs 20/day, no interest — taxpayer.csv row 2; commands.txt line 128
- Extra traps (not in the brief, but realistic):
  - CANCEL of INV/26-27/0416 23 h after its IRN is allowed (keeps its number, status CANCELLED); CANCEL of INV/26-27/0417 25 h after its IRN must be refused — commands.txt lines 82, 83
  - INV/26-27/0426 is raised twice (the second INVOICE reuses the number and must be rejected); number INV/26-27/0427 is never issued, so INV/26-27/0428 creates a gap and must be rejected/flagged — commands.txt lines 112, 115 (duplicate), 116 (gap)
  - INV/26-27/0441: installation service to unregistered CUST-09 (TN, address_on_record=false) — POS falls back to supplier state KA (CGST+SGST); INV/26-27/0442: AMC to unregistered CUST-10 (MH, address on record) — POS MH (IGST) — commands.txt lines 158, 160
  - INV/25-26/1374 (taxable 123400.00): CN/26-27/0023 credits 60% and CN/26-27/0027 another 45% — cumulative 105% exceeds the taxable value, so the second must be rejected — commands.txt lines 35, 88
  - PUR-0035 (Oct books) is missing in the Oct 2B and appears in the Nov 2B (held, then MATCHED on re-check); PUR-0032 never appears in any 2B (held Oct, re-checked Nov and Dec, then pending report); 2B Nov invoice VER/3391 has no books entry (MISSING_IN_BOOKS) — purchase_register.csv PUR-0035, PUR-0032; gstr2b_2026_11.csv VER/3391
  - Blocked credits that are MATCHED in the Nov 2B but must be INELIGIBLE: motor car (with cess), staff catering, club membership — purchase_register.csv PUR-0044, PUR-0049, PUR-0054
  - RCM purchases from unregistered suppliers (legal consultancy, GTA freight) never appear in any 2B; tax is paid in cash and claimed as ITC in the same period — purchase_register.csv PUR-0056, PUR-0093
  - PUR-0001 dated 2026-04-10 is still unpaid on day 180 (2026-10-07): reverse in October with interest from 2026-05-20; re-avail in December when paid on 2026-12-05 — purchase_register.csv PUR-0001; commands.txt line 150
  - October return for the KA GSTIN is filed on the due date 2026-11-20 itself (no interest, no late fee); November is filed 2026-12-23, 3 days late (interest 18% p.a. daily on net cash liability + Rs 50/day late fee) — commands.txt lines 110, 198
What is NOT in this pack
Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-nn). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.
Output format expected at evaluation
Produce these CSV files (header row, same conventions as above, rows sorted as stated). Where the brief is silent on a format detail the choice below is binding for evaluation.
outward_register.csv
One row per document accepted into the register (invoices, credit and debit notes), in command order; INVALID_IRN and rejected documents appear with their status and zero tax.

Columns, in order: period, doc_no, doc_type, doc_date, customer_id, customer_gstin, place_of_supply, taxable_value, cgst, sgst, igst, cess, irn_status, doc_status, reason
reconciliation.csv
One row per purchase line and per unmatched 2B row, per period it is evaluated in.

Columns, in order: period, purchase_id, supplier_gstin, books_invoice_no, 2b_invoice_no, invoice_date, match_status, itc_decision, itc_igst, itc_cgst, itc_sgst, itc_cess, held_count, reason
itc_summary.csv
One row per period and tax head.

Columns, in order: period, tax_head, eligible, held, blocked, reversed_180_day, reversed_proportionate, reavailed, rcm_credit, net_itc
liability_setoff.csv
One row per GSTIN and period.

Columns, in order: gstin, period, igst_liability, cgst_liability, sgst_liability, cess_liability, igst_credit_used_igst, igst_credit_used_cgst, igst_credit_used_sgst, cgst_credit_used_cgst, cgst_credit_used_igst, sgst_credit_used_sgst, sgst_credit_used_igst, cash_igst, cash_cgst, cash_sgst, cash_cess, filing_date, days_late, interest, late_fee

Binding choices: doc_type is INVOICE, CREDIT_NOTE or DEBIT_NOTE; irn_status is VALID, INVALID_IRN or NOT_REQUIRED; doc_status is ACTIVE, CANCELLED or REJECTED; match_status is MATCHED, MISMATCH_AMOUNT, MISSING_IN_2B or MISSING_IN_BOOKS (RCM lines use NOT_APPLICABLE); itc_decision is ELIGIBLE, HELD, PENDING, INELIGIBLE, REVERSED or REAVAILED; tax_head is IGST, CGST, SGST or CESS. Interest is rounded to the rupee per tax head; days_late = filing_date - due date (0 if on time).
Implementation business-rule cross-reference (BR-01 to BR-20)
The following identifiers are used by DESIGN_BUSINESS_RULES.md. The planted-scenario section above maps the sample's edge cases to exact commands.txt physical line numbers and/or exact CSV record IDs.
Rule ID	Implemented rule	Planted scenario reference
BR-01	Place of supply: registered goods use ship-to state; B2C goods use customer state; unregistered services use customer state only when address is recorded, otherwise taxpayer state.	EC-01; extra unregistered-service POS trap
BR-02	Intra-state supply uses CGST + SGST at half rate; inter-state supply uses IGST at full rate; cess uses item-master rate.	EC-01 and unregistered-service POS trap
BR-03	B2B e-invoice requirement applies when PAN-level turnover exceeds ₹5 crore; IRN at or before 24 hours is valid, later IRN is invalid.	EC-04
BR-04	Invoice, credit-note and debit-note sequences are independent per FY; duplicates and gaps are rejected; cancelled numbers remain consumed.	Extra duplicate-number and sequence-gap trap
BR-05	Cancellation is allowed only within 24 hours of IRN generation; refused cancellation leaves the document active with a reason.	Extra cancellation-window trap
BR-06	Credit notes require an original invoice, cumulative credit cannot exceed original taxable value, and the reporting cut-off is 30 November after the original FY.	EC-05 and cumulative-credit-note trap
BR-07	Purchase matching key is supplier GSTIN + normalized invoice number + invoice date; normalization ignores case/punctuation and strips optional INV/INVOICE prefix and leading zeroes.	EC-02; invoice normalization examples
BR-08	₹1.00 per tax head is within tolerance; a difference above ₹1.00 is a mismatch and claim is limited to lower book/2B amount per head.	EC-03
BR-09	Payments are applied in command order; unpaid ITC is reversed after 180 days and may be re-availed on later payment; reversal interest is 18% p.a.	EC-06 and unpaid-then-paid trap
BR-10	Missing-in-2B ITC is held and retried for two following evaluations, then becomes pending; 2B-only entries are missing in books.	Missing-later-appears, never-appears and 2B-only scenarios
BR-11	Motor vehicle, food/catering and club-membership ITC is blocked regardless of match status.	Blocked-credit scenario
BR-12	Common-input ITC is proportionately reversed using exempt outward turnover divided by total outward turnover.	See rule implementation and period ITC summary; sample planted scenario details are in the scenario section above if present
BR-13	Notified services from unregistered suppliers attract RCM; tax is cash liability and corresponding eligible credit is included in same-period ITC.	RCM purchase scenarios
BR-14	ITC set-off: IGST → IGST, CGST, SGST; CGST → CGST, IGST; SGST → SGST, IGST; no CGST/SGST cross-set-off; cess credit only offsets cess.	EC-07
BR-15	Remaining tax including RCM is cash payable; interest is 18% p.a. daily on net cash tax liability.	EC-07 and on-time/late return scenarios
BR-16	Due date is the 20th of next month; late fee ₹50/day regular and ₹20/day nil, capped at ₹10,000.	EC-08 and on-time/late return scenarios
BR-17	Tax is calculated line-wise from item master; tax heads are rounded to nearest rupee per invoice total using half-up rounding.	Verified through outward-register tax calculations and regression tests
BR-18	Commands are processed in physical file order; load, reconcile, return and print commands take effect at their position in the stream.	Command stream ordering across commands.txt
BR-19	Outward register preserves document command order; invalid-IRN and rejected documents remain visible with zero tax and reason where applicable.	EC-04 and document rejection traps
BR-20	Output CSV column names and order follow the sample-pack output specification.	Output format section above


Run the project
From the repository root, use Python 3.10+:
python gst_engine.py --data data --out output
python run_tests.py
The engine uses only the Python standard library. The supplied regression suite has 12 tests. In the recorded sample run, all 12 passed. The sample pack does not include official expected-output files; generated reports are computed outputs from this implementation and are not represented as official field-for-field certification.