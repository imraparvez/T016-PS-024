# PS-024 — GST Invoicing, E-Invoice Validation & GSTR-2B ITC Reconciliation

**Team:** T016  
**Language:** Python 3.10+  
**Dependencies:** Python standard library only  
**Mode:** Command-line / command-file driven (no UI)

## Project contents

```text
PS024_GST_Engine/
├── gst_engine.py
├── DESIGN_BUSINESS_RULES.md
├── README.md
├── run_tests.py
├── data/
│   ├── taxpayer.csv
│   ├── customers.csv
│   ├── suppliers.csv
│   ├── items.csv
│   ├── prior_invoices.csv
│   ├── purchase_register.csv
│   ├── gstr2b_2026_10.csv
│   ├── gstr2b_2026_11.csv
│   ├── gstr2b_2026_12.csv
│   └── commands.txt
└── output/
    ├── outward_register.csv
    ├── reconciliation.csv
    ├── itc_summary.csv
    ├── liability_setoff.csv
    └── engine_log.txt
```

The `data/` directory contains the actual Team T016 sample data uploaded for this task.

## Run in VS Code / Windows

1. Extract the ZIP file.
2. Open the extracted `PS024_GST_Engine` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Check Python:

   ```powershell
   python --version
   ```

   Python 3.10 or newer is required.

5. Run:

   ```powershell
   python gst_engine.py --data data --out output
   ```

   If `python` is not recognized, try:

   ```powershell
   py -3 gst_engine.py --data data --out output
   ```

6. Open the `output` folder to view the generated CSV files.

## Run tests

```powershell
python run_tests.py
```

The tests validate important planted scenarios in the generated outputs. They are regression checks for this implementation, not official expected-output certification.

## Output files

| File | Contents |
|---|---|
| `outward_register.csv` | Sales invoices, credit notes and debit notes in command order |
| `reconciliation.csv` | Line-wise book vs GSTR-2B matching, status and ITC decision |
| `itc_summary.csv` | Eligible, held, blocked, reversed, re-availed, RCM and net ITC by tax head |
| `liability_setoff.csv` | Liability, credit utilization, cash tax, filing date, interest and late fee per GSTIN/period |
| `pending_itc_report.csv` | Lines that exhausted the two-period GSTR-2B recheck window |\n| `engine_log.txt` | Processing notes and recoverable command errors |

## Design and viva preparation

Read `DESIGN_BUSINESS_RULES.md` for BR-01 onwards, edge-case mapping, set-off order and the explanation of why missing 2B lines are held instead of rejected.

### Viva: set-off order
1. IGST credit → IGST liability.
2. Remaining IGST credit → CGST liability.
3. Remaining IGST credit → SGST liability.
4. CGST credit → CGST, then IGST.
5. SGST credit → SGST, then IGST.
6. CGST and SGST credits cannot cross-set-off.
7. Remaining amount, including RCM tax, is paid in cash.

### Viva: missing in 2B
`MISSING_IN_2B` is held because the supplier may upload the invoice in a later return period. The engine checks it again for two further reconciliation periods. If it still does not appear, the line is marked `PENDING`; it is not silently discarded.

## Important implementation assumptions

The assignment brief and sample README do not specify every internal accounting convention. This implementation makes the following explicit choices:

- Invoice normalization removes punctuation, ignores case, strips an optional `INV`/`INVOICE` prefix, then strips leading zeroes. This makes `INV-0012`, `0012` and `inv-12` equivalent, as required by the planted scenario.
- B2C goods use the customer's state as place of supply. Registered goods use the supplied ship-to state. Unregistered services use the customer's state only when `address_on_record=true`; otherwise the taxpayer's state.
- RCM tax is treated as cash-only liability; the corresponding eligible RCM credit is added to same-period ITC.
- Reversal interest for the 180-day rule is included in the `interest` output column alongside late-payment interest.
- Output is generated using the business rules in the brief and sample README. The pack explicitly states that it does **not** contain official expected outputs. Therefore the included CSVs are computed sample outputs, not a claim of field-for-field official verification.

## Evaluation readiness

The engine reads the same input schemas and command stream structure as the sample pack, so a new compatible data pack can be processed by changing `--data`. Always run the tests and review the generated CSVs before submitting. The hidden evaluation may enforce interpretations of ambiguous GST/legal rules that are not fully specified in the sample README; confirm those conventions with the project mentor if an official expected-output file becomes available.
