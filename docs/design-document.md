# PS-024 Design Document

## 1. Project overview
A command-line Java application to manage GST invoices, validate e-invoice requirements, reconcile purchase records against GSTR-2B, determine ITC eligibility, calculate tax liability and produce reports.

## 2. Users
Primary user: accountant/operator entering master data and loading monthly transaction files.

## 3. Scope
### Included
- Taxpayer, customer, supplier and item master data
- Sales invoices, credit notes and debit notes
- GST computation and validation
- Purchase register and GSTR-2B reconciliation
- ITC eligibility, RCM and reversal calculations
- Liability, set-off, interest and late-fee calculations
- CLI and text/CSV reports

### Excluded / external
- Direct GST portal filing
- Real IRP authentication or IRN generation
- Payments and banking integration
- Legal advice or automated interpretation of changes in GST law

## 4. Technology
Java 17, Maven, JUnit 5, `BigDecimal`, `java.time`, CSV-friendly text files.

## 5. Architecture
CLI -> Application services -> Domain models and rule services -> CSV/text input-output.
Services are separated by responsibility: invoice validation, tax calculation, reconciliation, ITC, liability and reporting.

## 6. Processing sequence
1. Load master data and transactions.
2. Validate invoice numbering and e-invoice conditions.
3. Calculate line taxes and invoice totals.
4. Match purchase records with GSTR-2B.
5. Apply blocked-credit and ITC eligibility rules.
6. Apply 180-day and exempt-supply reversals.
7. Calculate net liability and utilize eligible credits.
8. Calculate interest/late fee and generate reports.

## 7. Data precision
Use `BigDecimal` for all currency and tax values. Never use binary floating-point for money. Assignment rounding is applied at invoice tax-head total level; exact tie-breaking policy should be confirmed.

## 8. Limitations
The project uses simulated IRN validation. The final organizer-provided input schemas and sample files are required to complete the file-ingestion adapters and verify expected outputs.
