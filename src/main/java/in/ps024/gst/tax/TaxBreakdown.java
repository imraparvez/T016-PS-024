package in.ps024.gst.tax;

import java.math.BigDecimal;

public record TaxBreakdown(BigDecimal cgst, BigDecimal sgst, BigDecimal igst,
                           BigDecimal cess, BigDecimal total) {}
