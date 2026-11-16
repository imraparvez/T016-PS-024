# Test Plan

Automated tests currently cover:
- Intra-state tax split
- Inter-state IGST calculation
- Unsupported GST rate rejection
- Invoice number normalization examples
- ₹1.00 and ₹1.01 tolerance boundaries

Additional required tests before submission:
- Place of supply / delivery-state scenarios
- E-invoice turnover and exact 24-hour boundary
- Sequential invoice numbering and cancellation
- Credit-note cumulative cap and 30-Nov deadline
- RCM categories and cash payment
- Missing-in-2B hold periods
- Blocked ITC categories
- Day 180 vs day 181 reversal and interest
- Exempt-supply proportionate reversal
- All set-off order and cash remainder combinations
- Due date, daily interest and late fee cap
- Full organizer-provided sample files and hidden-case rehearsal
