package in.ps024.gst.liability;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public final class InterestCalculator {
    private InterestCalculator() {}
    public static BigDecimal simpleDailyInterest(BigDecimal principal, BigDecimal annualRatePercent,
                                                 LocalDate from, LocalDate to) {
        if (principal.signum() < 0 || annualRatePercent.signum() < 0 || to.isBefore(from))
            throw new IllegalArgumentException("Invalid interest inputs.");
        long days = ChronoUnit.DAYS.between(from, to);
        return principal.multiply(annualRatePercent)
            .multiply(BigDecimal.valueOf(days))
            .divide(new BigDecimal("36500"), 2, RoundingMode.HALF_UP);
    }
}
