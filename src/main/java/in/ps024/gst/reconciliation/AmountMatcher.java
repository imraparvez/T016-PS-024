package in.ps024.gst.reconciliation;

import java.math.BigDecimal;

public final class AmountMatcher {
    private AmountMatcher() {}
    public static boolean withinTolerance(BigDecimal books, BigDecimal portal) {
        return books != null && portal != null &&
            books.subtract(portal).abs().compareTo(new BigDecimal("1.00")) <= 0;
    }
    public static BigDecimal eligibleLowerAmount(BigDecimal books, BigDecimal portal) {
        return books.min(portal);
    }
}
