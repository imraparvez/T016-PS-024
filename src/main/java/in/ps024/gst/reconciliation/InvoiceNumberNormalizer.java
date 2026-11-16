package in.ps024.gst.reconciliation;

public final class InvoiceNumberNormalizer {
    private InvoiceNumberNormalizer() {}
    public static String normalize(String invoiceNumber) {
        if (invoiceNumber == null) return "";
        String value = invoiceNumber.trim().toUpperCase().replaceAll("\\s+", "");
        // Normalize numeric suffix only: INV-0012 -> INV-12; 0012 -> 12.
        int split = value.length();
        while (split > 0 && Character.isDigit(value.charAt(split - 1))) split--;
        if (split == value.length()) return value;
        String prefix = value.substring(0, split);
        String digits = value.substring(split).replaceFirst("^0+(?!$)", "");
        return prefix + digits;
    }
}
