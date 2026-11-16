# PS-024 — GST Invoicing, E-Invoice Validation & GSTR-2B Reconciliation

Java 17 command-line starter implementation for the PS-024 assignment.

## Requirements
- JDK 17+
- Apache Maven 3.9+

## Run
From the folder containing `pom.xml`:
```powershell
mvn clean test
mvn package
mvn exec:java -Dexec.mainClass="in.ps024.gst.Main"
```
Or run `in.ps024.gst.Main` from VS Code. The packaged JAR is in `target/`.

## Commands
The current CLI provides:
- `help` — show available commands
- `demo` — run a GST tax-calculation demonstration
- `exit` — quit

This is an extensible MVP, not a production GST filing system. IRN generation is simulated; it does not connect to the IRP/GST portal. The organizers' actual CSV schemas, sample files, and hidden tests must be used to complete integration and validate assumptions.

## Implemented core rules
- Intra-state CGST+SGST and inter-state IGST computation
- GST rates 0, 5, 12, 18, 28; optional cess
- BigDecimal monetary arithmetic
- Invoice-number normalization helper
- GSTR-2B line comparison with ₹1 per-head tolerance
- Blocked ITC category check
- IGST/CGST/SGST utilization in the assignment's stated order
- Daily simple interest helper

## Important assumptions to confirm
See `docs/decision-log.md`. In particular: exact 24-hour IRN boundary, rounding policy, invoice-number normalization collisions, matching granularity, missing-in-2B hold period, 180-day trigger, and allocation when IGST credit is insufficient for both CGST and SGST liabilities.

## Project structure
`src/main/java/in/ps024/gst/` contains the CLI and business modules. `src/test/java/` contains automated tests. `input/` and `output/` contain sample files and generated report examples.


## Week 1 design documents

- `docs/architecture.md` — application layers and processing flow
- `docs/class-diagram.md` — initial domain model
- `docs/input-output-design.md` — proposed CSV inputs and reports
- `docs/edge-case-checklist.md` — business-rule test checklist
- `docs/week-1-checkpoint.md` — Week 1 scope and completion status

These documents describe the initial design. Official organizer sample-file headers and written clarifications take priority when they become available.
