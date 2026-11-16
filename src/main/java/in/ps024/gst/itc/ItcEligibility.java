package in.ps024.gst.itc;

import in.ps024.gst.reconciliation.ReconciliationStatus;
import java.util.Set;

public final class ItcEligibility {
    private static final Set<String> BLOCKED = Set.of("MOTOR_VEHICLE", "FOOD", "CLUB_MEMBERSHIP");
    private ItcEligibility() {}
    public static boolean isBlocked(String category) {
        return category != null && BLOCKED.contains(category.trim().toUpperCase());
    }
    public static boolean isEligible(ReconciliationStatus status, String category) {
        if (isBlocked(category)) return false;
        return status == ReconciliationStatus.MATCHED || status == ReconciliationStatus.MISMATCH_AMOUNT;
    }
}
