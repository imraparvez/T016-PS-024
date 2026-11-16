package in.ps024.gst.tax;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Set;

public final class GstCalculator {
    private static final Set<BigDecimal> ALLOWED = Set.of(
        new BigDecimal("0"), new BigDecimal("5"), new BigDecimal("12"),
        new BigDecimal("18"), new BigDecimal("28"));
    private GstCalculator() {}

    public static TaxBreakdown calculate(BigDecimal taxable, BigDecimal rate,
                                          BigDecimal cessRate, boolean interState) {
        if (taxable == null || rate == null || cessRate == null || taxable.signum() < 0)
            throw new IllegalArgumentException("Taxable value and rates must be valid and non-negative.");
        if (ALLOWED.stream().noneMatch(r -> r.compareTo(rate) == 0))
            throw new IllegalArgumentException("Unsupported GST rate: " + rate);
        if (cessRate.signum() < 0) throw new IllegalArgumentException("Cess rate cannot be negative.");
        BigDecimal gst = taxable.multiply(rate).divide(new BigDecimal("100"), 8, RoundingMode.HALF_UP);
        BigDecimal cess = taxable.multiply(cessRate).divide(new BigDecimal("100"), 8, RoundingMode.HALF_UP);
        BigDecimal cgst = interState ? BigDecimal.ZERO : gst.divide(new BigDecimal("2"), 8, RoundingMode.HALF_UP);
        BigDecimal sgst = interState ? BigDecimal.ZERO : gst.divide(new BigDecimal("2"), 8, RoundingMode.HALF_UP);
        BigDecimal igst = interState ? gst : BigDecimal.ZERO;
        cgst = rupee(cgst); sgst = rupee(sgst); igst = rupee(igst); cess = rupee(cess);
        return new TaxBreakdown(cgst, sgst, igst, cess,
            taxable.add(cgst).add(sgst).add(igst).add(cess).setScale(2, RoundingMode.HALF_UP));
    }
    private static BigDecimal rupee(BigDecimal value) {
        return value.setScale(0, RoundingMode.HALF_UP);
    }
}
