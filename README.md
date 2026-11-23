
# GST Invoicing, E-Invoice Validation and GSTR-2B Input Tax Credit Reconciliation

**Project ID:** T016-PS-024

**Language:** Java 17+

**Build Tool:** Apache Maven

## 1. Project Overview

This project is a command-file-driven GST application developed to manage GST invoicing, e-invoice validation, purchase reconciliation and Input Tax Credit (ITC) calculations.

The application processes taxpayer details, customers, suppliers, items, sales invoices, purchase records and GSTR-2B data.

It validates invoices, calculates GST, reconciles purchase records with GSTR-2B, determines eligible ITC and calculates GST liability and applicable interest.

The application is designed as a command-line application without a graphical user interface.

## 2. Project Objectives

- Register taxpayer, customer and supplier details.
- Maintain item information and applicable GST rates.
- Create and validate sales invoices.
- Generate and validate e-invoice IRNs.
- Create credit notes and debit notes.
- Calculate CGST, SGST, IGST and cess.
- Import purchase register and GSTR-2B data.
- Reconcile purchase invoices with GSTR-2B.
- Determine eligible and ineligible ITC.
- Calculate ITC reversals and re-availment.
- Calculate GST liability and ITC set-off.
- Generate outward register, reconciliation report, ITC summary and liability report.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Java 17+ | Application development |
| Apache Maven | Build and dependency management |
| JUnit 5 | Unit testing |
| CSV | Input and output data files |
| Git | Version control |
| GitHub | Source code hosting |

## 4. Business Rules

The project follows 12 identified business rules.

### BR-01: Place of Supply
- Intra-state transactions use CGST + SGST.
- Inter-state transactions use IGST.
- For goods delivered to another state, use the delivery state as the place of supply.
- For B2C goods, use the customer's state as the place of supply.
- For services to unregistered persons, use the supplier's state unless the recipient's address is available on record.

### BR-02: GST Tax Calculation
- Allowed GST rates are 0%, 5%, 12%, 18% and 28%.
- Cess applies only to items tagged for cess.
- Calculate tax separately for each invoice line.
- Round invoice totals per tax head to the nearest rupee.

### BR-03: E-Invoice Validation
- E-invoice is mandatory for B2B transactions when taxpayer turnover is above ₹5 crore.
- IRN must be generated within 24 hours of the invoice date.
- Invalid or late IRN invoices must be marked INVALID_IRN.
- Invalid IRN invoices are excluded from the outward register until regenerated with a fresh number.

### BR-04: Invoice Numbering
- Invoice numbers must be sequential for each financial year.
- There must be no gaps in invoice numbering.
- Cancelled invoices retain their original number and CANCELLED status.
- Cancellation is allowed only within 24 hours of IRN generation.

### BR-05: Credit and Debit Notes
- A credit note must reference its original invoice.
- Cumulative credit note taxable value cannot exceed the original invoice taxable value.
- Credit notes must be issued by 30 November of the following financial year.
- Debit notes must reference the relevant original invoice.

### BR-06: Reverse Charge Mechanism (RCM)
- RCM applies to listed services purchased from unregistered suppliers, such as legal and GTA services.
- The buyer must pay applicable tax in cash.
- Eligible ITC may be claimed in the same period after payment of RCM tax.

### BR-07: GSTR-2B Matching
- Purchase invoices are matched using supplier GSTIN, normalized invoice number and invoice date.
- Invoice number matching is case-insensitive and ignores leading zeros.
- The allowed amount difference is ₹1 per tax head.
- Reconciliation statuses include MATCHED, MISMATCH_AMOUNT, MISSING_IN_2B and MISSING_IN_BOOKS.

### BR-08: ITC Eligibility
- MATCHED invoices may qualify for ITC.
- MISMATCH_AMOUNT invoices may qualify using the lower amount.
- MISSING_IN_2B invoices are held and rechecked for up to two periods.
- Pending invoices are included in the pending report after the permitted recheck period.
- Blocked ITC categories, including motor vehicles, food and club membership, remain INELIGIBLE regardless of matching status.

### BR-09: 180-Day ITC Reversal
- If a supplier invoice remains unpaid beyond 180 days, related ITC must be reversed.
- Interest of 18% per annum applies from the date ITC was claimed.
- ITC may be re-availed when payment is made.
- Common input credits must be reversed proportionately based on exempt turnover divided by total turnover.

### BR-10: ITC Set-Off
- IGST credit is used first against IGST liability, then CGST and then SGST.
- CGST credit is used against CGST first, then IGST.
- SGST credit is used against SGST first, then IGST.
- CGST and SGST credits cannot be used against each other.
- Remaining liability must be paid in cash.

### BR-11: Interest and Late Fees
- GST return due date is the 20th of the following month.
- Interest is charged at 18% per annum, calculated daily on net cash liability.
- Late fee is ₹50 per day for regular returns.
- Late fee is ₹20 per day for nil returns.
- Late fee is capped at ₹10,000.

### BR-12: Processing Precedence
The application processes business rules in this order:

1. Invoice validity (IRN and numbering).
2. Tax computation.
3. GSTR-2B matching.
4. Blocked ITC check.
5. 180-day ITC reversal.
6. Proportionate ITC reversal.
7. ITC set-off.

## 5. Project Structure

```text
T016-PS-024/
│
├── docs/
│   ├── architecture.md
│   ├── business-rules.md
│   ├── class-diagram.md
│   ├── decision-log.md
│   ├── design-document.md
│   ├── edge-case-checklist.md
│   ├── input-output-design.md
│   └── test-plan.md
│
├── input/
│   ├── sample-sales.csv
│   ├── sample-purchases.csv
│   └── sample-gstr2b.csv
│
├── output/
│
├── src/
│   ├── main/java/in/ps024/gst/
│   └── test/java/in/ps024/gst/
│
├── pom.xml
├── .gitignore
└── README.md
```

## 6. Application Modules

| Module | Responsibility |
|---|---|
| Master | Taxpayer, customer, supplier and item management |
| Invoice | Invoice, credit note and debit note processing |
| Tax | GST calculation |
| Validation | Invoice and IRN validation |
| Purchase | Purchase register processing |
| Reconciliation | GSTR-2B matching |
| ITC | ITC eligibility and reversal |
| Liability | Interest and ITC set-off |
| Reports | Output report generation |
| IO | Command-file reading and input/output handling |

## 7. Input Files

The application is designed to process:

- Taxpayer master data.
- Customer master data.
- Supplier master data.
- Item master data.
- Prior invoice records.
- Purchase register.
- Monthly GSTR-2B files.
- Command file containing application operations.

## 8. Expected Output Files

The application is designed to generate:

1. `outward_register.csv`
2. `reconciliation.csv`
3. `itc_summary.csv`
4. `liability_setoff.csv`

## 9. Build and Run

### Prerequisites

- Java 17 or later.
- Apache Maven.
- Git.

### Run tests

```bash
mvn clean test
```

### Build the project

```bash
mvn clean package
```

### Run the application

The application entry point is:

```text
in.ps024.gst.Main
```

The command-line execution workflow and input arguments will be documented as the application is implemented.

## 10. Testing

JUnit 5 is used for unit testing.

Testing covers:

- GST calculations.
- Invoice number normalization.
- Amount matching.
- Business rule validation.
- Edge cases and reconciliation scenarios.

## 11. Project Status

**Development is in progress.**

Initial project structure, documentation, Java foundation and initial unit tests have been created.

Further development includes command processing, invoice management, validation, purchase reconciliation, ITC calculations, liability calculations and report generation.

## 12. Repository

GitHub: https://github.com/imraparvez/T016-PS-024
