package in.ps024.gst;
import in.ps024.gst.reconciliation.InvoiceNumberNormalizer;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class NormalizerTest {
 @Test void normalizesSuffixZerosAndCase() {
  assertEquals("INV-12",InvoiceNumberNormalizer.normalize("inv-0012"));
  assertEquals("12",InvoiceNumberNormalizer.normalize("0012"));
 }
}
