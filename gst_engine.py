#!/usr/bin/env python3
"""PS-024 GST compliance engine — Python 3.10+; standard library only."""
from __future__ import annotations
import csv, sys, re, argparse
from pathlib import Path
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict

D=Decimal
ZERO=D("0")
HEADS=("igst","cgst","sgst","cess")
def money(x): return D(str(x or "0")).quantize(D("0.01"), rounding=ROUND_HALF_UP)
def rupee(x): return D(x).quantize(D("1"), rounding=ROUND_HALF_UP)
def dt(s): return datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
def dte(s): return date.fromisoformat(str(s)[:10])
def readcsv(p):
    with open(p,newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def writecsv(p, rows, fields):
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader()
        for r in rows:
            w.writerow({k: (fmt(r.get(k,"")) if isinstance(r.get(k),Decimal) else r.get(k,"")) for k in fields})
def fmt(v): return f"{v.quantize(D('0.01'), rounding=ROUND_HALF_UP):.2f}"

class GSTEngine:
 def __init__(self,data,out):
    self.data=Path(data); self.out=Path(out); self.out.mkdir(parents=True,exist_ok=True)
    self.taxpayers=readcsv(self.data/"taxpayer.csv"); self.primary=next(x for x in self.taxpayers if x["registration_type"]=="PRIMARY")
    self.items={x["item_code"]:x for x in readcsv(self.data/"items.csv")}
    self.customers={x["customer_id"]:x for x in readcsv(self.data/"customers.csv")}
    self.suppliers={x["supplier_id"]:x for x in readcsv(self.data/"suppliers.csv")}
    self.prior={x["doc_no"]:x for x in readcsv(self.data/"prior_invoices.csv")}
    self.purchases={x["purchase_id"]:x for x in readcsv(self.data/"purchase_register.csv")}
    self.payments={}; self.docs=[]; self.docmap={}; self.sequences={}; self.loaded2b={}; self.recon={}; self.recon_rows=[]
    self.held_age=defaultdict(int); self.claimed={}; self.reversed=set(); self.reversal_interest=defaultdict(Decimal); self.reavailed=defaultdict(lambda:defaultdict(Decimal))
    self.outward=[]; self.liability=[]; self.returns={}; self.events=[]
 def event(self,msg): self.events.append(msg)
 def tax_for_lines(self,lines,pos,supplier_state=None):
    vals={k:ZERO for k in ("taxable_value",)+HEADS}
    for code,qty,price in lines:
      it=self.items[code]; taxable=money(D(qty)*D(price)); rate=D(it["gst_rate"]); cessrate=D(it["cess_rate"])
      vals["taxable_value"]+=taxable
      if it["exempt"]=="True" or it["exempt"].lower()=="true": continue
      tax=taxable*rate/100; cess=taxable*cessrate/100
      if (supplier_state or self.primary["state"])==pos:
       vals["cgst"]+=tax/2; vals["sgst"]+=tax/2
      else: vals["igst"]+=tax
      vals["cess"]+=cess
    for h in HEADS: vals[h]=rupee(vals[h])
    vals["taxable_value"]=money(vals["taxable_value"])
    return vals
 def parse_lines(self,s):
    out=[]
    for x in s.split(";"):
      a=x.split(":")
      if len(a)!=3 or a[0] not in self.items: raise ValueError("Invalid item line "+x)
      out.append((a[0],int(a[1]),D(a[2])))
    return out
 def next_number_ok(self,docno,series):
    try: n=int(docno.split("/")[-1])
    except: return False
    expected=self.sequences.get(series)
    if expected is None: return True
    return n==expected+1
 def doc_command(self,typ,a):
    if typ=="INVOICE":
      no,ts,cid,ship,raw=a; issue=dt(ts); c=self.customers[cid]; lines=self.parse_lines(raw)
      series="INV"; status="ACTIVE"; reason=""
      if no in self.docmap: status="REJECTED"; reason="DUPLICATE_DOCUMENT_NUMBER"
      elif not self.next_number_ok(no,series+"/26-27"): status="REJECTED"; reason="SEQUENCE_GAP_OR_OUT_OF_ORDER"
      else: self.sequences[series+"/26-27"]=int(no.split("/")[-1])
      pos=ship or c["state"]
      # B2C goods use customer state; unregistered services use recorded address, else supplier state.
      if c["registered"].lower()!="true":
       if any(self.items[x[0]]["item_type"]=="SERVICE" for x in lines):
        pos=c["state"] if c["address_on_record"].lower()=="true" else self.primary["state"]
       else: pos=c["state"]
      tax=self.tax_for_lines(lines,pos)
      required=c["registered"] and D(self.primary["aggregate_turnover"])>D("50000000")
      doc={"doc_no":no,"doc_type":"INVOICE","issue":issue,"period":issue.strftime("%Y-%m"),"customer_id":cid,"customer_gstin":c["gstin"],"pos":pos,"tax":tax,"irn_required":required,"irn_status":"NOT_REQUIRED" if not required else "PENDING","doc_status":status,"reason":reason,"irn_time":None,"original":None,"lines":lines}
    else:
      no,ts,orig,raw=a; issue=dt(ts); lines=self.parse_lines(raw); status="ACTIVE"; reason=""
      series="CN" if typ=="CREDIT_NOTE" else "DN"
      if no in self.docmap: status="REJECTED"; reason="DUPLICATE_DOCUMENT_NUMBER"
      elif not self.next_number_ok(no,series+"/26-27"): status="REJECTED"; reason="SEQUENCE_GAP_OR_OUT_OF_ORDER"
      else: self.sequences[series+"/26-27"]=int(no.split("/")[-1])
      original=self.docmap.get(orig)
      if original is None and orig in self.prior: original=self.prior[orig]
      if original is None: status="REJECTED"; reason="ORIGINAL_INVOICE_NOT_FOUND"
      else:
       orig_date=original["issue"].date() if "issue" in original else dte(original["doc_date"])
       # Statutory window: 30 November following the FY in which original invoice was issued.
       fy_end=date(orig_date.year+1,3,31) if orig_date.month>=4 else date(orig_date.year,3,31)
       deadline=date(fy_end.year,11,30)
       if typ=="CREDIT_NOTE" and issue.date()>deadline: status="REJECTED"; reason="CREDIT_NOTE_TIME_LIMIT_EXCEEDED"
       base_tax=original["tax"]["taxable_value"] if "tax" in original else D(original["taxable_value"])
       already=original.get("credited",ZERO)
       value=sum((money(D(q)*p) for _,q,p in lines),ZERO)
       if typ=="CREDIT_NOTE" and already+value>base_tax: status="REJECTED"; reason="CUMULATIVE_CREDIT_EXCEEDS_ORIGINAL"
       if typ=="CREDIT_NOTE" and status=="ACTIVE": original["credited"]=already+value
       pos=original.get("pos",self.primary["state"])
       tax=self.tax_for_lines(lines,pos)
       if typ=="CREDIT_NOTE": tax={k:-v for k,v in tax.items()}
      doc={"doc_no":no,"doc_type":typ,"issue":issue,"period":issue.strftime("%Y-%m"),"customer_id":original.get("customer_id","") if isinstance(original,dict) else "","customer_gstin":original.get("customer_gstin","") if isinstance(original,dict) else "","pos":pos if original else self.primary["state"],"tax":tax if original else {k:ZERO for k in ("taxable_value",)+HEADS},"irn_required":bool(original and original.get("irn_required", self.customers[original["customer_id"]]["registered"].lower()=="true" and D(self.primary["aggregate_turnover"])>D("50000000"))),"irn_status":"NOT_REQUIRED" if not (original and original.get("irn_required", self.customers[original["customer_id"]]["registered"].lower()=="true" and D(self.primary["aggregate_turnover"])>D("50000000"))) else "PENDING","doc_status":status,"reason":reason,"irn_time":None,"original":orig,"lines":lines}
    self.docs.append(doc)
    if no not in self.docmap: self.docmap[no]=doc
 def process(self):
    commands=self.data/"commands.txt"
    for lineno,line in enumerate(commands.read_text(encoding="utf-8-sig").splitlines(),1):
      if not line.strip() or line.startswith("#"): continue
      p=line.split("|"); cmd=p[0]; a=p[1:]
      try:
       if cmd=="SET_SEQUENCE":
        self.sequences[a[0]]=int(a[1])
       elif cmd=="LOAD_PURCHASES": self.event("Loaded purchase register: "+a[0])
       elif cmd in ("INVOICE","CREDIT_NOTE","DEBIT_NOTE"): self.doc_command(cmd,a)
       elif cmd=="IRN":
        no,ts=a; doc=self.docmap.get(no)
        if doc:
         generated=dt(ts); doc["irn_time"]=generated
         if doc["irn_required"]:
          hours=(generated-doc["issue"]).total_seconds()
          doc["irn_status"]="VALID" if 0<=hours<=86400 else "INVALID_IRN"
         else: doc["irn_status"]="NOT_REQUIRED"
       elif cmd=="CANCEL":
        no,ts=a; doc=self.docmap.get(no)
        if doc and doc["doc_status"]=="ACTIVE":
         allowed=(not doc["irn_required"] or (doc["irn_time"] and 0<=(dt(ts)-doc["irn_time"]).total_seconds()<=86400))
         if allowed: doc["doc_status"]="CANCELLED"
         else: doc["reason"]="CANCELLATION_WINDOW_EXCEEDED"
       elif cmd=="PURCHASE_PAYMENT": self.payments[a[0]]=dte(a[1])
       elif cmd=="LOAD_2B": self.loaded2b[a[0]]=readcsv(self.data/a[1])
       elif cmd=="RECONCILE": self.reconcile(a[0])
       elif cmd=="FILE_RETURN":
        gstin,period,filing=a; self.returns[(gstin,period)]=dte(filing)
       elif cmd=="PRINT_OUTWARD_REGISTER": self.build_outward(a[0])
       elif cmd=="PRINT_RECON": pass
       elif cmd=="PRINT_LIABILITY": self.build_liability(a[0])
      except Exception as e: self.event(f"LINE {lineno} {cmd} ERROR: {e}")
    # Finalize IRN-required documents that never got an IRN.
    for d in self.docs:
      if d["irn_required"] and d["irn_status"]=="PENDING":
       d["irn_status"]="INVALID_IRN"; d["reason"]=d["reason"] or "IRN_NOT_GENERATED_WITHIN_24_HOURS"
    # Refresh outputs after all commands (late IRN commands may follow document creation).
    for period in ("2026-10","2026-11","2026-12"):
      self.build_outward(period)
      if period in self.loaded2b and period not in self.recon: self.reconcile(period)
      if any(pp==period for gg,pp in self.returns): self.build_liability(period)
    self.write_outputs()
 def reconcile(self,period):
    b2=self.loaded2b.get(period,[])
    eligible_books=[p for p in self.purchases.values() if p["book_period"]==period or (p["purchase_id"] in self.held_age and self.held_age[p["purchase_id"]]>0)]
    used=set(); rows=[]
    for p in eligible_books:
      if not p["supplier_gstin"] and self.items[p["item_code"]]["rcm_notified"].lower()=="true": # notified RCM
       rows.append(self.purchase_row(period,p,None,"NOT_APPLICABLE","RCM_CASH_AND_ITC",p,"RCM notified purchase; tax discharged in cash and credit taken in same period")); continue
      found=None; idx=None
      for i,b in enumerate(b2):
       if i in used: continue
       if b["supplier_gstin"]==p["supplier_gstin"] and self.norm_invoice(b["invoice_no"])==self.norm_invoice(p["invoice_no"]) and b["invoice_date"]==p["invoice_date"]:
        found=b; idx=i; break
      if found is None:
       age=self.held_age[p["purchase_id"]]+1
       self.held_age[p["purchase_id"]]=age
       decision="HELD" if age<=2 else "PENDING"
       rows.append(self.purchase_row(period,p,None,"MISSING_IN_2B",decision,p,f"Not present in 2B; recheck {age}/2"))
      else:
       used.add(idx); self.held_age.pop(p["purchase_id"],None); diffs=[abs(money(p[h])-money(found[h])) for h in HEADS]
       status="MATCHED" if all(x<=D("1.00") for x in diffs) else "MISMATCH_AMOUNT"
       it=self.items[p["item_code"]]; blocked=it["blocked_category"]!="NONE"
       decision="INELIGIBLE" if blocked else "ELIGIBLE"
       if status=="MISMATCH_AMOUNT" and not blocked: decision="ELIGIBLE"
       rows.append(self.purchase_row(period,p,found,status,decision,p,"Blocked ITC" if blocked else "Claim lower of books and 2B per tax head" if status=="MISMATCH_AMOUNT" else "Exact match within Rs 1 tolerance"))
       if not blocked: self.claimed[p["purchase_id"]]={h:min(money(p[h]),money(found[h])) for h in HEADS}
    for i,b in enumerate(b2):
      if i not in used:
       rows.append({"period":period,"purchase_id":"","supplier_gstin":b["supplier_gstin"],"books_invoice_no":"","2b_invoice_no":b["invoice_no"],"invoice_date":b["invoice_date"],"match_status":"MISSING_IN_BOOKS","itc_decision":"INELIGIBLE","itc_igst":"0.00","itc_cgst":"0.00","itc_sgst":"0.00","itc_cess":"0.00","held_count":0,"reason":"2B row has no matching purchase book line"})
    self.recon[period]=rows; self.recon_rows.extend(rows)
 def norm_invoice(self,s):
    x=re.sub(r"[^A-Z0-9]","",str(s).upper())
    x=re.sub(r"^(INV|INVOICE)","",x)
    return x.lstrip("0") or "0"
 def purchase_row(self,period,p,b,status,decision,book,reason):
    vals={}
    for h in HEADS:
      bv=money(book[h]); vals[h]=bv if b is None else min(bv,money(b[h]))
      if decision in ("HELD","PENDING","INELIGIBLE","NOT_APPLICABLE"): vals[h]=ZERO
    return {"period":period,"purchase_id":p["purchase_id"],"supplier_gstin":p["supplier_gstin"],"books_invoice_no":p["invoice_no"],"2b_invoice_no":b["invoice_no"] if b else "","invoice_date":p["invoice_date"],"match_status":status,"itc_decision":decision,"itc_igst":vals["igst"],"itc_cgst":vals["cgst"],"itc_sgst":vals["sgst"],"itc_cess":vals["cess"],"held_count":self.held_age[p["purchase_id"]],"reason":reason}
 def build_outward(self,period):
    rows=[]
    for d in self.docs:
      if d["period"]!=period: continue
      status=d["doc_status"]; irn=d["irn_status"]; reason=d["reason"]
      tax=d["tax"].copy()
      if status=="REJECTED" or irn=="INVALID_IRN":
       if irn=="INVALID_IRN": reason=reason or "IRN_INVALID_OR_LATE"
       tax={k:ZERO for k in ("taxable_value",)+HEADS}
      rows.append({"period":period,"doc_no":d["doc_no"],"doc_type":d["doc_type"],"doc_date":d["issue"].date().isoformat(),"customer_id":d["customer_id"],"customer_gstin":d["customer_gstin"],"place_of_supply":d["pos"],"taxable_value":tax["taxable_value"],"cgst":tax["cgst"],"sgst":tax["sgst"],"igst":tax["igst"],"cess":tax["cess"],"irn_status":irn,"doc_status":status,"reason":reason})
    self.outward=[x for x in self.outward if x["period"]!=period]+rows
 def build_itc(self,period):
    # ITC summary aggregates reconciled eligible lines, reversals, re-availments and RCM.
    totals={h:defaultdict(Decimal) for h in ("IGST","CGST","SGST","CESS")}
    self.reversal_interest[period]=ZERO
    for r in self.recon.get(period,[]):
      hmap={"IGST":"itc_igst","CGST":"itc_cgst","SGST":"itc_sgst","CESS":"itc_cess"}
      for h,col in hmap.items():
       v=money(r[col])
       if r["itc_decision"]=="ELIGIBLE": totals[h]["eligible"]+=v
       elif r["itc_decision"] in ("HELD","PENDING"): totals[h]["held"]+=money(self.purchases.get(r["purchase_id"],{}).get(h.lower(),0))
       elif r["itc_decision"]=="INELIGIBLE": totals[h]["blocked"]+=money(self.purchases.get(r["purchase_id"],{}).get(h.lower(),0))
    # 180-day payment test. Opening claims are identified by itc_claimed_on;
    # current-period claims are identified by successful 2B reconciliation.
    for pid,p in self.purchases.items():
      claimdate=dte(p["itc_claimed_on"]) if p["itc_claimed_on"] else dte(p["invoice_date"])
      invdate=dte(p["invoice_date"]); paid=self.payments.get(pid)
      day180=invdate+timedelta(days=180); breach=day180+timedelta(days=1)
      was_claimed=bool(p["itc_claimed_on"]) or pid in self.claimed
      if not was_claimed: continue
      if breach.strftime("%Y-%m")==period and (paid is None or paid>day180):
       self.reversed.add(pid)
       for h in HEADS:
        amount=money(p[h]); totals[h.upper()]["reversed_180_day"]+=amount
        days=max(0,(breach-claimdate).days)
        self.reversal_interest[period]+=amount*D("0.18")*D(days)/D("365")
      if paid and paid>day180 and paid.strftime("%Y-%m")==period and pid in self.reversed:
       for h in HEADS: totals[h.upper()]["reavailed"]+=money(p[h])
    # Common input reversal ratio based on outward exempt taxable value / total outward taxable value.
    docs=[d for d in self.docs if d["period"]==period and d["doc_status"]=="ACTIVE" and d["irn_status"]!="INVALID_IRN"]
    exempt=ZERO; total=ZERO
    for d in docs:
      sign=D("-1") if d["doc_type"]=="CREDIT_NOTE" else D("1")
      for code,q,price in d["lines"]:
       v=money(D(q)*price)*sign; total+=v
       if self.items[code]["exempt"].lower()=="true": exempt+=v
    ratio=(exempt/total) if total else ZERO
    for p in self.purchases.values():
      if p["book_period"]==period and p["usage"]=="COMMON":
       for h in HEADS: totals[h.upper()]["reversed_proportionate"]+=money(p[h])*ratio
    # RCM tax on unregistered notified services; pay cash then claim same-period credit.
    for p in self.purchases.values():
      it=self.items[p["item_code"]]
      if not p["supplier_gstin"] and it["rcm_notified"] and p["book_period"]==period:
       for h in HEADS:
        v=money(p[h]); totals[h.upper()]["rcm_credit"]+=v
    rows=[]
    for h in ("IGST","CGST","SGST","CESS"):
      t=totals[h]
      net=t["eligible"]+t["reavailed"]+t["rcm_credit"]-t["reversed_180_day"]-t["reversed_proportionate"]
      rows.append({"period":period,"tax_head":h,"eligible":t["eligible"],"held":t["held"],"blocked":t["blocked"],"reversed_180_day":t["reversed_180_day"],"reversed_proportionate":t["reversed_proportionate"],"reavailed":t["reavailed"],"rcm_credit":t["rcm_credit"],"net_itc":max(ZERO,net)})
    return rows
 def build_liability(self,period):
    
    itc=self.build_itc(period); credits={x["tax_head"].lower():x["net_itc"] for x in itc}
    tax={h:ZERO for h in ("igst","cgst","sgst","cess")}
    for r in self.outward:
      if r["period"]==period and r["doc_status"]=="ACTIVE" and r["irn_status"]!="INVALID_IRN":
       for h in tax: tax[h]+=money(r[h])
    # RCM is added to cash liability for its respective tax head.
    rcm={h:ZERO for h in tax}
    for p in self.purchases.values():
      it=self.items[p["item_code"]]
      if p["book_period"]==period and not p["supplier_gstin"] and it["rcm_notified"]:
       for h in tax: rcm[h]+=money(p[h])
    gross_tax={h:tax[h]+rcm[h] for h in tax}
    ig=credits["igst"]; cg=credits["cgst"]; sg=credits["sgst"]; cess=credits["cess"]
    used={k:ZERO for k in ["igst_credit_used_igst","igst_credit_used_cgst","igst_credit_used_sgst","cgst_credit_used_cgst","cgst_credit_used_igst","sgst_credit_used_sgst","sgst_credit_used_igst"]}
    def consume(cr,liab,key):
      x=min(cr,liab); used[key]=x; return cr-x,liab-x
    ig, tax["igst"]=consume(ig,tax["igst"],"igst_credit_used_igst")
    ig, tax["cgst"]=consume(ig,tax["cgst"],"igst_credit_used_cgst")
    ig, tax["sgst"]=consume(ig,tax["sgst"],"igst_credit_used_sgst")
    cg,tax["cgst"]=consume(cg,tax["cgst"],"cgst_credit_used_cgst")
    cg,tax["igst"]=consume(cg,tax["igst"],"cgst_credit_used_igst")
    sg,tax["sgst"]=consume(sg,tax["sgst"],"sgst_credit_used_sgst")
    sg,tax["igst"]=consume(sg,tax["igst"],"sgst_credit_used_igst")
    cash={h:tax[h]+rcm[h] for h in tax}
    cash["cess"]=max(ZERO,cash["cess"]-credits["cess"])
    gstin,filing=(next((g for (g,pp) in self.returns if pp==period and g==self.primary["gstin"]),self.primary["gstin"]), self.returns.get((self.primary["gstin"],period),date.fromisoformat(period+"-01")+timedelta(days=50)))
    due=(date.fromisoformat(period+"-01")+timedelta(days=32)).replace(day=20) # next month 20th
    # safer next calendar month
    y,m=map(int,period.split("-")); due=date(y+1,1,20) if m==12 else date(y,m+1,20)
    late=max(0,(filing-due).days); netcash=sum(cash.values(),ZERO)
    interest=rupee(netcash*D("0.18")*D(late)/D("365")+self.reversal_interest[period])
    fee=min(D("10000"),D(late)*D("50"))
    row={"gstin":gstin,"period":period,"igst_liability":gross_tax["igst"],"cgst_liability":gross_tax["cgst"],"sgst_liability":gross_tax["sgst"],"cess_liability":gross_tax["cess"],**used,"cash_igst":cash["igst"],"cash_cgst":cash["cgst"],"cash_sgst":cash["sgst"],"cash_cess":cash["cess"],"filing_date":filing.isoformat(),"days_late":late,"interest":interest,"late_fee":fee}
    if not any(x["period"]==period and x["gstin"]==gstin for x in self.liability): self.liability.append(row)
    # Additional GST registrations with no activity still require a separate nil-return row.
    for tp in self.taxpayers:
      if tp["gstin"]==gstin: continue
      if (tp["gstin"],period) in self.returns and not any(x["period"]==period and x["gstin"]==tp["gstin"] for x in self.liability):
       fdate=self.returns[(tp["gstin"],period)]; late2=max(0,(fdate-due).days)
       self.liability.append({"gstin":tp["gstin"],"period":period,"igst_liability":ZERO,"cgst_liability":ZERO,"sgst_liability":ZERO,"cess_liability":ZERO,
        **{k:ZERO for k in used},"cash_igst":ZERO,"cash_cgst":ZERO,"cash_sgst":ZERO,"cash_cess":ZERO,"filing_date":fdate.isoformat(),"days_late":late2,"interest":ZERO,"late_fee":min(D("10000"),D(late2)*D("20"))})
 def write_outputs(self):
    self.build_outward("2026-10"); self.build_outward("2026-11"); self.build_outward("2026-12")
    writecsv(self.out/"outward_register.csv",self.outward,["period","doc_no","doc_type","doc_date","customer_id","customer_gstin","place_of_supply","taxable_value","cgst","sgst","igst","cess","irn_status","doc_status","reason"])
    allrecon=[]
    for p in ("2026-10","2026-11","2026-12"): allrecon+=self.recon.get(p,[])
    writecsv(self.out/"reconciliation.csv",allrecon,["period","purchase_id","supplier_gstin","books_invoice_no","2b_invoice_no","invoice_date","match_status","itc_decision","itc_igst","itc_cgst","itc_sgst","itc_cess","held_count","reason"])
    itcs=[]
    for p in ("2026-10","2026-11","2026-12"): itcs+=self.build_itc(p)
    writecsv(self.out/"itc_summary.csv",itcs,["period","tax_head","eligible","held","blocked","reversed_180_day","reversed_proportionate","reavailed","rcm_credit","net_itc"])
    self.liability.sort(key=lambda r:(r["period"], next((i for i,t in enumerate(self.taxpayers) if t["gstin"]==r["gstin"]),99)))
    writecsv(self.out/"pending_itc_report.csv",[r for r in allrecon if r["itc_decision"]=="PENDING"],["period","purchase_id","supplier_gstin","books_invoice_no","invoice_date","held_count","reason"])
    writecsv(self.out/"liability_setoff.csv",self.liability,["gstin","period","igst_liability","cgst_liability","sgst_liability","cess_liability","igst_credit_used_igst","igst_credit_used_cgst","igst_credit_used_sgst","cgst_credit_used_cgst","cgst_credit_used_igst","sgst_credit_used_sgst","sgst_credit_used_igst","cash_igst","cash_cgst","cash_sgst","cash_cess","filing_date","days_late","interest","late_fee"])
    (self.out/"engine_log.txt").write_text("\n".join(self.events),encoding="utf-8")

def period_date(p): return date.fromisoformat(p+"-01")
def main():
 ap=argparse.ArgumentParser(description="PS-024 GST engine")
 ap.add_argument("--data",default="data",help="input data directory")
 ap.add_argument("--out",default="output",help="output directory")
 args=ap.parse_args()
 e=GSTEngine(args.data,args.out); e.process()
 print("PS-024 processing complete.")
 for f in ["outward_register.csv","reconciliation.csv","itc_summary.csv","liability_setoff.csv","engine_log.txt"]:
  p=Path(args.out)/f; print(f"{f}: {sum(1 for _ in open(p,encoding='utf-8'))-1 if f.endswith('.csv') else p.stat().st_size} records/bytes")
if __name__=="__main__": main()
