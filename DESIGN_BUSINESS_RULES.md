# PS-024 Design Document — Business Rules

## Architecture
The engine is a deterministic, command-file-driven Python application. `GSTEngine` loads the supplied master CSV files, processes `commands.txt` in physical file order, retains document/payment/reconciliation state, and writes the four evaluation CSVs. It uses Python's `decimal.Decimal` for financial arithmetic and the standard library only.

## Business rules

| ID | Rule implemented |
|---|---|
| BR-01 | Place of supply: registered goods use the ship-to state; B2C goods use the customer's state. Services to unregistered customers use the customer's state only when an address is recorded; otherwise the supplier's state. |
| BR-02 | Intra-state supply computes CGST and SGST at half the item GST rate; inter-state supply computes IGST at the full rate. Cess is computed at the item-master rate. |
| BR-03 | E-invoice is mandatory for B2B when PAN-level turnover exceeds ₹5 crore. IRN generated at or before 24 hours is valid; after 24 hours is `INVALID_IRN` and tax values are zeroed in the outward register. |
| BR-04 | Invoice, credit-note and debit-note sequences are independent per FY. New numbers must be exactly sequential; duplicate numbers and gaps are rejected. A cancelled number remains consumed. |
| BR-05 | Cancellation is allowed only within 24 hours of IRN generation. A refused cancellation leaves the document active and records a reason. |
| BR-06 | Credit notes require an original invoice, must remain within its taxable-value ceiling cumulatively, and must be issued no later than 30 November after the original invoice's FY. |
| BR-07 | Purchase matching uses supplier GSTIN + normalized invoice number + invoice date. Invoice numbers are uppercased, punctuation removed, optional leading `INV`/`INVOICE` prefix removed, and leading zeroes stripped. |
| BR-08 | Each tax head has ₹1.00 tolerance. A difference of exactly ₹1.00 is `MATCHED`; any head exceeding ₹1.00 makes the line `MISMATCH_AMOUNT`. Eligible mismatch lines claim the lower of book and 2B amounts per head. |
| BR-09 | Purchase payments are applied in command order. ITC is reversed after the 180-day payment window when still unpaid; when paid after the window, the reversal is recorded and the credit is re-availed in the payment period. Reversal interest is 18% p.a. from claim date to reversal date. |
| BR-10 | Only matched/mismatched lines can be eligible. Missing 2B is held and rechecked for two following evaluations; after the hold window it becomes `PENDING`. A 2B-only line is `MISSING_IN_BOOKS`. |
| BR-11 | Motor vehicle, food and club-membership categories are blocked regardless of match status. |
| BR-12 | Common-input ITC is proportionately reversed using exempt outward turnover divided by total outward turnover for the period. |
| BR-13 | Notified services purchased from unregistered suppliers are RCM. RCM tax is a cash liability; corresponding ITC is included in the same-period credit summary. |
| BR-14 | ITC set-off order: IGST credit against IGST, then CGST, then SGST; CGST credit against CGST then IGST; SGST credit against SGST then IGST. CGST and SGST credits never cross-set-off. Cess credit is used only against cess. |
| BR-15 | Remaining tax, including RCM, is cash payable. Interest is 18% p.a. daily on net cash tax liability. |
| BR-16 | Due date is the 20th of the next month. Late fee is ₹50/day for regular returns and ₹20/day for nil returns, capped at ₹10,000. |
| BR-17 | Tax is calculated line-wise using the item master; tax heads are rounded to the nearest rupee per invoice total using half-up rounding. |
| BR-18 | Commands are processed in file order. `LOAD_2B`, `RECONCILE`, `FILE_RETURN` and print commands take effect at their command positions. |
| BR-19 | Outward register contains documents in command order. Invalid-IRN and rejected documents remain visible with zero tax and an explanatory reason. |
| BR-20 | Output CSV column names and order follow the sample-pack README exactly. |

## Set-off explanation for viva
IGST credit is the most flexible credit: it is first used against IGST liability, then any balance is used against CGST, then SGST. CGST credit can only offset CGST and then IGST; SGST credit can only offset SGST and then IGST. CGST and SGST credits cannot be used against each other. Any remaining amount is paid in cash. RCM tax is kept in cash because reverse-charge tax must be discharged in cash; its corresponding ITC may then be claimed in the same period.

## Why `MISSING_IN_2B` is held
A purchase may be genuine and correctly recorded even though the supplier has not yet uploaded or reported the invoice. Rejecting it immediately would permanently deny credit for a supplier-side reporting delay. The engine therefore holds the line, retries it in the next two reconciliation periods, and then moves it to `PENDING` if it never appears. A `MISSING_IN_BOOKS` 2B row is reported separately because the portal shows an invoice that the taxpayer has not recorded.

## Explicit sample edge cases
- `INV/26-27/0394`: KA customer, goods shipped to TN → TN place of supply and IGST.
- `INV-0012`, `0012`, `inv-12`: normalized to the same invoice key after removing the optional `INV` prefix and leading zeroes.
- ₹1.00 tax-head difference is within tolerance; ₹1.01 is a mismatch.
- IRN at exactly 24 hours is valid; 24 hours and one second is invalid.
- Credit note on 30 November is within the reporting window; 1 December is rejected.
- Payment on day 180 avoids reversal; payment on day 181 triggers reversal and re-availment.
- November set-off follows IGST → CGST → SGST; any RCM remains cash payable.
- October TN additional GSTIN is a nil return filed seven days late, so ₹140 late fee and no interest.
