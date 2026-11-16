# Initial Class Diagram — PS-024 GST Application

This is the planned domain design. The implementation may add fields or split classes as the detailed requirements and sample files are received.

```mermaid
classDiagram
    class Taxpayer {
        +String gstin
        +String stateCode
        +BigDecimal annualTurnover
    }
    class Party {
        +String gstin
        +String name
        +String stateCode
        +PartyType type
    }
    class Item {
        +String itemCode
        +String description
        +String hsn
        +BigDecimal gstRate
        +BigDecimal cessRate
        +boolean blockedForItc
    }
    class Invoice {
        +String invoiceNumber
        +LocalDate invoiceDate
        +InvoiceType type
        +String supplierGstin
        +String recipientGstin
        +String placeOfSupply
        +InvoiceStatus status
        +List~InvoiceLine~ lines
    }
    class InvoiceLine {
        +Item item
        +BigDecimal quantity
        +BigDecimal unitPrice
        +BigDecimal taxableValue
        +TaxBreakdown tax
    }
    class TaxBreakdown {
        +BigDecimal cgst
        +BigDecimal sgst
        +BigDecimal igst
        +BigDecimal cess
    }
    class PurchaseRecord {
        +String supplierGstin
        +String invoiceNumber
        +LocalDate invoiceDate
        +BigDecimal taxableValue
        +TaxBreakdown tax
        +LocalDate paymentDate
    }
    class Gstr2bRecord {
        +String supplierGstin
        +String invoiceNumber
        +LocalDate invoiceDate
        +BigDecimal taxableValue
        +TaxBreakdown tax
    }
    class ReconciliationResult {
        +ReconciliationStatus status
        +BigDecimal eligibleAmount
        +String reason
    }

    Taxpayer "1" --> "*" Invoice : issues
    Party "1" --> "*" Invoice : customer/supplier
    Invoice "1" *-- "*" InvoiceLine
    InvoiceLine "*" --> "1" Item
    InvoiceLine *-- TaxBreakdown
    PurchaseRecord *-- TaxBreakdown
    Gstr2bRecord *-- TaxBreakdown
    PurchaseRecord --> ReconciliationResult
    Gstr2bRecord --> ReconciliationResult
```

## Design notes

- `Party` represents a customer or supplier; a party type distinguishes its role.
- `Invoice` contains one or more `InvoiceLine` objects.
- `TaxBreakdown` keeps the tax heads separate so matching and set-off can compare each head.
- `PurchaseRecord` represents the buyer's books entry. `Gstr2bRecord` represents the corresponding imported 2B entry.
- `ReconciliationResult` stores the comparison outcome; it should not overwrite the original source records.
- Enums such as `InvoiceType`, `InvoiceStatus`, `PartyType` and `ReconciliationStatus` should be implemented as separate enum types when coding.
