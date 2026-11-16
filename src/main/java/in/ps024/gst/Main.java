package in.ps024.gst;

import in.ps024.gst.tax.GstCalculator;
import in.ps024.gst.tax.TaxBreakdown;
import in.ps024.gst.reconciliation.InvoiceNumberNormalizer;
import java.math.BigDecimal;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("PS-024 GST Invoicing & Reconciliation");
        System.out.println("Java 17 | Type 'help' for commands.");
        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                System.out.print("ps024> ");
                if (!scanner.hasNextLine()) break;
                String command = scanner.nextLine().trim().toLowerCase();
                switch (command) {
                    case "help" -> printHelp();
                    case "demo" -> runDemo();
                    case "exit", "quit" -> { System.out.println("Goodbye."); return; }
                    case "" -> { }
                    default -> System.out.println("Unknown command. Type 'help'.");
                }
            }
        }
    }

    private static void printHelp() {
        System.out.println("Commands: help, demo, exit");
        System.out.println("Use 'demo' to calculate an illustrative GST invoice.");
    }

    private static void runDemo() {
        TaxBreakdown result = GstCalculator.calculate(
            new BigDecimal("10000.00"), new BigDecimal("18"),
            new BigDecimal("0"), false);
        System.out.println("Illustrative intra-state invoice, taxable value ₹10,000 at 18%");
        System.out.println("CGST: ₹" + result.cgst());
        System.out.println("SGST: ₹" + result.sgst());
        System.out.println("IGST: ₹" + result.igst());
        System.out.println("Cess: ₹" + result.cess());
        System.out.println("Invoice total: ₹" + result.total());
        System.out.println("Normalized INV-0012 -> " + InvoiceNumberNormalizer.normalize("INV-0012"));
    }
}
