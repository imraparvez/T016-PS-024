
# Business Rules – PS-024

## BR-01: Place of Supply

- Intra-state transactions use CGST + SGST.
- Inter-state transactions use IGST.
- For goods delivered to another state, use the delivery state as the place of supply.
- For B2C goods, use the customer's state as the place of supply.
- For services to unregistered persons, use the supplier's state unless the recipient's address is available on record.

## BR-02: GST Tax Calculation

- Allowed GST rates are 0%, 5%, 12%, 18% and 28%.
- Cess applies only to items tagged for cess.
- Calculate tax separately for each invoice line.
- Round invoice totals per tax head to the nearest rupee.

## BR-03: E-Invoice Validation

- E-invoice is mandatory for B2B transactions when taxpayer turnover is above ₹5 crore.
- IRN must be generated within 24 hours of the invoice date.
- An invoice with an invalid or late IRN must be marked INVALID_IRN.
- Invalid IRN invoices must be excluded from the outward register until regenerated with a fresh number.

## BR-04: Invoice Numbering

- Invoice numbers must be sequential for each financial year.
- There must be no gaps in invoice numbering.
- A cancelled invoice retains its original invoice number and CANCELLED status.
- Cancellation is allowed only within 24 hours of IRN generation.

## BR-05: Credit and Debit Notes

- A credit note must reference its original invoice.
- The cumulative taxable value of credit notes must not exceed the original invoice taxable value.
- Credit notes must be issued by 30 November of the following financial year.
- Debit notes must also reference the relevant original invoice.

## BR-06: Reverse Charge Mechanism (RCM)

- RCM applies to listed services purchased from unregistered suppliers, such as legal services and GTA services.
- The buyer must pay the applicable tax in cash.
- Eligible ITC may be claimed in the same period after payment of RCM tax.

## BR-07: GSTR-2B Matching

- Match purchase invoices using:
  - Supplier GSTIN
  - Normalized invoice number
  - Invoice date
- Invoice number matching must be case-insensitive and ignore leading zeros.
- The allowed amount difference is ₹1 per tax head.
- Reconciliation statuses include MATCHED, MISMATCH_AMOUNT, MISSING_IN_2B and MISSING_IN_BOOKS.

## BR-08: ITC Eligibility

- MATCHED invoices may qualify for ITC.
- MISMATCH_AMOUNT invoices may qualify using the lower amount.
- MISSING_IN_2B invoices must be held and rechecked for up to two periods.
- Pending invoices must be included in the pending report after the permitted recheck period.
- Blocked ITC categories, including motor vehicles, food and club membership, remain INELIGIBLE regardless of matching status.

## BR-09: 180-Day ITC Reversal

- If a supplier invoice remains unpaid beyond 180 days, the related ITC must be reversed.
- Interest of 18% per annum applies from the date ITC was claimed.
- ITC may be re-availed when payment is made.
- Common input credits must be reversed proportionately based on exempt turnover divided by total turnover.

## BR-10: ITC Set-Off

- IGST credit must be used first against IGST liability, then CGST and then SGST.
- CGST credit must be used against CGST first, then IGST.
- SGST credit must be used against SGST first, then IGST.
- CGST and SGST credits cannot be used against each other.
- Any remaining liability must be paid in cash.

## BR-11: Interest and Late Fees

- GST return due date is the 20th of the following month.
- Interest is charged at 18% per annum, calculated daily on the net cash liability.
- Late fee is ₹50 per day for regular returns.
- Late fee is ₹20 per day for nil returns.
- Late fee is capped at ₹10,000.

## BR-12: Processing Precedence

The application must process business rules in the following order:

1. Invoice validity (IRN and numbering).
2. Tax computation.
3. GSTR-2B matching.
4. Blocked ITC check.
5. 180-day ITC reversal.
6. Proportionate ITC reversal.
7. ITC set-off.
