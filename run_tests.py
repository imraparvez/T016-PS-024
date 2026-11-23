#!/usr/bin/env python3
"""Regression checks for the Team T016 PS-024 sample output."""
import csv, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
def rows(name):
    with open(OUT/name,newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
class PS024Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.out=rows("outward_register.csv")
    cls.rec=rows("reconciliation.csv")
    cls.itc=rows("itc_summary.csv")
    cls.li=rows("liability_setoff.csv")
 def doc(self,no): return [r for r in self.out if r["doc_no"]==no]
 def recon(self,pid,period): return next(r for r in self.rec if r["purchase_id"]==pid and r["period"]==period)
 def test_goods_delivered_outside_customer_state(self):
    r=self.doc("INV/26-27/0394")[0]
    self.assertEqual(r["place_of_supply"],"TN"); self.assertGreater(float(r["igst"]),0); self.assertEqual(float(r["cgst"]),0)
 def test_irn_boundary(self):
    self.assertEqual(self.doc("INV/26-27/0402")[0]["irn_status"],"VALID")
    self.assertEqual(self.doc("INV/26-27/0403")[0]["irn_status"],"INVALID_IRN")
    self.assertEqual(float(self.doc("INV/26-27/0403")[0]["igst"])+float(self.doc("INV/26-27/0403")[0]["cgst"]),0)
 def test_cancellation_window(self):
    self.assertEqual(self.doc("INV/26-27/0416")[0]["doc_status"],"CANCELLED")
    self.assertEqual(self.doc("INV/26-27/0417")[0]["doc_status"],"ACTIVE")
    self.assertIn("CANCELLATION_WINDOW",self.doc("INV/26-27/0417")[0]["reason"])
 def test_duplicate_and_gap(self):
    self.assertEqual(len(self.doc("INV/26-27/0426")),2)
    self.assertEqual(self.doc("INV/26-27/0426")[1]["doc_status"],"REJECTED")
    self.assertEqual(self.doc("INV/26-27/0428")[0]["doc_status"],"REJECTED")
 def test_credit_note_limits(self):
    self.assertEqual(self.doc("CN/26-27/0028")[0]["doc_status"],"ACTIVE")
    self.assertEqual(self.doc("CN/26-27/0029")[0]["doc_status"],"REJECTED")
    self.assertEqual(self.doc("CN/26-27/0027")[0]["doc_status"],"REJECTED")
 def test_invoice_number_normalization(self):
    for pid in ("PUR-0023","PUR-0024","PUR-0027"):
      self.assertEqual(self.recon(pid,"2026-10")["match_status"],"MATCHED")
 def test_amount_tolerance(self):
    self.assertEqual(self.recon("PUR-0033","2026-10")["match_status"],"MATCHED")
    self.assertEqual(self.recon("PUR-0034","2026-10")["match_status"],"MISMATCH_AMOUNT")
 def test_missing_2b_retry(self):
    self.assertEqual(self.recon("PUR-0032","2026-10")["itc_decision"],"HELD")
    self.assertEqual(self.recon("PUR-0032","2026-11")["itc_decision"],"HELD")
    self.assertEqual(self.recon("PUR-0032","2026-12")["itc_decision"],"PENDING")
    self.assertEqual(self.recon("PUR-0035","2026-10")["itc_decision"],"HELD")
    self.assertEqual(self.recon("PUR-0035","2026-11")["itc_decision"],"ELIGIBLE")
 def test_blocked_and_rcm(self):
    for pid in ("PUR-0044","PUR-0049","PUR-0054"):
      self.assertEqual(self.recon(pid,"2026-11")["itc_decision"],"INELIGIBLE")
    self.assertEqual(self.recon("PUR-0056","2026-11")["itc_decision"],"RCM_CASH_AND_ITC")
 def test_180_day_rule(self):
    nov=next(r for r in self.itc if r["period"]=="2026-11" and r["tax_head"]=="CGST")
    dec=next(r for r in self.itc if r["period"]=="2026-12" and r["tax_head"]=="CGST")
    self.assertGreater(float(nov["reversed_180_day"]),0)
    self.assertGreater(float(nov["reavailed"]),0)
    self.assertGreater(float(dec["reavailed"]),0)
 def test_nil_return_late_fee(self):
    r=next(r for r in self.li if r["gstin"]=="33DKQCQ1399R1ZM" and r["period"]=="2026-10")
    self.assertEqual(r["days_late"],"7"); self.assertEqual(float(r["late_fee"]),140)
    self.assertEqual(float(r["interest"]),0)
 def test_output_columns(self):
    self.assertEqual(len(self.out),80)
    self.assertEqual(len(self.itc),12)
    self.assertTrue(any(r["match_status"]=="MISSING_IN_BOOKS" for r in self.rec))
if __name__=="__main__": unittest.main(verbosity=2)
