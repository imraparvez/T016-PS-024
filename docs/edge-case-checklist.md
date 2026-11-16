# Business Rule and Edge-Case Checklist — PS-024

Use this checklist while implementing and testing. A checked item means a test exists and passes; it does not mean the feature is already implemented.

## Tax and place of supply

- [ ] Same-state supply calculates CGST and SGST at half the GST rate each.
- [ ] Inter-state supply calculates IGST at the full GST rate.
- [ ] Karnataka seller/customer with goods delivered in Tamil Nadu uses Tamil Nadu as place of supply and IGST.
- [ ] B2C goods use the customer's state as place of supply.
- [ ] Unregistered service recipient follows the assignment's place-of-supply rule.

## Rates and rounding

- [ ] Only GST rates 0%, 5%, 12%, 18% and 28% are accepted.
- [ ] Cess is applied only to tagged items.
- [ ] Each invoice tax head is rounded as required by the assignment.
- [ ] Values at half-paise boundaries are tested.

## Invoice, IRN and numbering

- [ ] B2B e-invoice requirement is triggered only when turnover is above ₹5 crore.
- [ ] IRN exactly 24 hours after invoice date/time is tested.
- [ ] Invalid IRN invoice is excluded from outward register until regenerated.
- [ ] Invoice numbers are sequential per financial year.
- [ ] Cancelled invoice retains its number and CANCELLED status.
- [ ] Cancellation at and beyond the 24-hour limit is tested.

## Credit and debit notes

- [ ] Credit note references an existing original invoice.
- [ ] Cumulative credit-note taxable value cannot exceed original invoice taxable value.
- [ ] 30 November deadline is accepted.
- [ ] 1 December after the deadline is rejected.
- [ ] Debit note validation is tested separately.

## Reconciliation and ITC

- [ ] `INV-0012`, `0012` and `inv-12` normalization is tested against the agreed matching rule.
- [ ] Difference of exactly ₹1.00 is within tolerance.
- [ ] Difference of ₹1.01 is outside tolerance.
- [ ] Every tax head is compared independently.
- [ ] Missing-in-2B entries are rechecked for the permitted two periods.
- [ ] Blocked credit remains INELIGIBLE even if matched.
- [ ] Mismatch ITC is limited to the lower eligible amount as specified.
- [ ] Purchase paid on day 180 and day 181 are both tested.
- [ ] Reversal interest at 18% is tested from the claim date.
- [ ] Proportionate reversal for exempt supplies is tested.

## Liability

- [ ] ITC set-off follows the exact order in BR-10.
- [ ] CGST and SGST credits are never cross-utilized.
- [ ] Excess IGST credit with unequal CGST and SGST liabilities is tested.
- [ ] Interest is 18% per annum on net cash liability using daily calculation.
- [ ] Due date is the 20th of the next month.
- [ ] Late fee is ₹50/day, or ₹20/day for nil return, subject to the ₹10,000 cap.
- [ ] Late nil return is tested.

## Rule precedence

- [ ] Invoice validity is checked before tax computation.
- [ ] Tax computation is completed before reconciliation.
- [ ] Reconciliation is completed before ITC eligibility.
- [ ] Blocked-credit check precedes reversal and set-off.
- [ ] 180-day reversal precedes proportionate reversal and set-off.
