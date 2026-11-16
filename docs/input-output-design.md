# Input and Output File Design — PS-024

## 1. General conventions

- Input files are CSV files stored in `input/`.
- The first row contains column headers.
- Use UTF-8 text.
- Dates use `YYYY-MM-DD`.
- Decimal amounts use a dot as the decimal separator and must not contain currency symbols or thousands separators.
- GSTINs should be stored as text, not numeric values.
- The program should validate required columns and report the CSV row number for invalid data.
- Output files are written to `output/`.

The exact official sample-data headers supplied by the organizer take priority. If they differ from these proposed headers, update the parser and this document rather than manually changing the supplied data.

## 2. Proposed input files

### `taxpayer.csv`

| Column | Meaning |
|---|---|
| `gstin` | Taxpayer GSTIN |
| `state_code` | State code |
| `annual_turnover` | Annual turnover in rupees |

### `parties.csv`

| Column | Meaning |
|---|---|
| `party_id` | Internal unique party ID |
| `name` | Customer or supplier name |
| `gstin` | GSTIN; blank only where permitted for an unregistered party |
| `state_code` | Party state |
| `party_type` | `CUSTOMER`, `SUPPLIER` or `BOTH` |
| `registered` | `true` or `false` |

### `items.csv`

| Column | Meaning |
|---|---|
| `item_code` | Internal item ID |
| `description` | Item description |
| `hsn` | HSN/SAC code |
| `gst_rate` | One of 0, 5, 12, 18 or 28 |
| `cess_rate` | Cess rate; 0 if not applicable |
| `blocked_for_itc` | `true` or `false` |

### `sales.csv`

| Column | Meaning |
|---|---|
| `invoice_number` | Sequential invoice number |
| `invoice_date` | Invoice date |
| `customer_gstin` | Customer GSTIN, if registered |
| `customer_state` | Customer state |
| `place_of_supply` | Place of supply |
| `item_code` | Item reference |
| `quantity` | Quantity |
| `unit_price` | Price per unit |
| `document_type` | `INVOICE`, `CREDIT_NOTE` or `DEBIT_NOTE` |
| `original_invoice_number` | Required for credit/debit note where applicable |

### `purchases.csv`

| Column | Meaning |
|---|---|
| `supplier_gstin` | Supplier GSTIN |
| `invoice_number` | Supplier invoice number |
| `invoice_date` | Supplier invoice date |
| `item_code` | Item reference or classification |
| `taxable_value` | Taxable amount |
| `cgst` | CGST amount |
| `sgst` | SGST amount |
| `igst` | IGST amount |
| `cess` | Cess amount |
| `payment_date` | Payment date; blank if unpaid |

### `gstr2b.csv`

| Column | Meaning |
|---|---|
| `supplier_gstin` | Supplier GSTIN |
| `invoice_number` | Invoice number reported in GSTR-2B |
| `invoice_date` | Invoice date |
| `taxable_value` | Taxable amount |
| `cgst` | CGST amount |
| `sgst` | SGST amount |
| `igst` | IGST amount |
| `cess` | Cess amount |

## 3. Proposed output files

| File | Contents |
|---|---|
| `outward-register.csv` | Valid outward invoices and notes, with taxable value and tax heads |
| `reconciliation-report.csv` | Book entry, 2B entry, reconciliation status, differences and reason |
| `itc-summary.csv` | Eligible, ineligible, held, reversed and re-availed ITC |
| `liability-summary.csv` | Output tax, ITC used by tax head, cash payable, interest and late fee |

## 4. Reconciliation statuses

- `MATCHED` — key fields match and each tax head is within the permitted ₹1 tolerance.
- `MISMATCH_AMOUNT` — invoice identity matches but one or more amounts exceed tolerance.
- `MISSING_IN_2B` — purchase exists in books but not in the imported 2B data.
- `MISSING_IN_BOOKS` — 2B contains an invoice that is absent from the purchase books.

## 5. Important note

These are the initial design headers, not a replacement for the organizer's sample-data format. Once the official Week 2 files arrive, compare their headers and map them exactly.
