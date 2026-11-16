package in.ps024.gst.liability;

import java.math.BigDecimal;
import java.util.LinkedHashMap;
import java.util.Map;

public final class ItcSetOff {
    public record Result(Map<String, BigDecimal> used, Map<String, BigDecimal> cashPayable) {}
    private ItcSetOff() {}

    public static Result apply(BigDecimal igstCredit, BigDecimal cgstCredit, BigDecimal sgstCredit,
                               BigDecimal igstDue, BigDecimal cgstDue, BigDecimal sgstDue) {
        BigDecimal iC = nz(igstCredit), cC = nz(cgstCredit), sC = nz(sgstCredit);
        BigDecimal iD = nz(igstDue), cD = nz(cgstDue), sD = nz(sgstDue);
        Map<String, BigDecimal> used = new LinkedHashMap<>();
        // IGST credit is applied in the assignment's stated order.
        BigDecimal x = min(iC, iD); iC=iC.subtract(x); iD=iD.subtract(x); used.put("IGST->IGST",x);
        x=min(iC,cD); iC=iC.subtract(x); cD=cD.subtract(x); used.put("IGST->CGST",x);
        x=min(iC,sD); iC=iC.subtract(x); sD=sD.subtract(x); used.put("IGST->SGST",x);
        x=min(cC,cD); cC=cC.subtract(x); cD=cD.subtract(x); used.put("CGST->CGST",x);
        x=min(cC,iD); cC=cC.subtract(x); iD=iD.subtract(x); used.put("CGST->IGST",x);
        x=min(sC,sD); sC=sC.subtract(x); sD=sD.subtract(x); used.put("SGST->SGST",x);
        x=min(sC,iD); sC=sC.subtract(x); iD=iD.subtract(x); used.put("SGST->IGST",x);
        Map<String, BigDecimal> cash = Map.of("IGST",iD,"CGST",cD,"SGST",sD);
        return new Result(Map.copyOf(used), cash);
    }
    private static BigDecimal nz(BigDecimal v){ return v==null?BigDecimal.ZERO:v; }
    private static BigDecimal min(BigDecimal a,BigDecimal b){ return a.min(b); }
}
