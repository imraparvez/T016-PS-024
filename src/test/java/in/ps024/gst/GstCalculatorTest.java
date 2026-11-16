package in.ps024.gst;

import in.ps024.gst.tax.GstCalculator;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

class GstCalculatorTest {
 @Test void intraStateSplitsTax() {
  var r=GstCalculator.calculate(new BigDecimal("10000"),new BigDecimal("18"),BigDecimal.ZERO,false);
  assertEquals(new BigDecimal("900"),r.cgst());
  assertEquals(new BigDecimal("900"),r.sgst());
  assertEquals(new BigDecimal("0"),r.igst());
  assertEquals(new BigDecimal("11800.00"),r.total());
 }
 @Test void interStateUsesIgst() {
  var r=GstCalculator.calculate(new BigDecimal("10000"),new BigDecimal("18"),BigDecimal.ZERO,true);
  assertEquals(new BigDecimal("1800"),r.igst());
  assertEquals(new BigDecimal("0"),r.cgst());
 }
 @Test void rejectsUnsupportedRate() {
  assertThrows(IllegalArgumentException.class,()->GstCalculator.calculate(
   BigDecimal.TEN,new BigDecimal("7"),BigDecimal.ZERO,false));
 }
}
