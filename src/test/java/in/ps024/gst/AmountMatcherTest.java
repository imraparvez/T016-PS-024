package in.ps024.gst;
import in.ps024.gst.reconciliation.AmountMatcher;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class AmountMatcherTest {
 @Test void oneRupeeIsWithinTolerance() {
  assertTrue(AmountMatcher.withinTolerance(new BigDecimal("101"),new BigDecimal("100")));
 }
 @Test void oneRupeeAndOnePaiseIsOutsideTolerance() {
  assertFalse(AmountMatcher.withinTolerance(new BigDecimal("101.01"),new BigDecimal("100")));
 }
}
