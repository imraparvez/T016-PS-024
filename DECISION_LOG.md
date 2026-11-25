# Decision Log

## PS-024: GST Invoicing, E-Invoice Validation and GSTR-2B ITC Reconciliation

**Team:** T016\
**Repository:** https://github.com/imraparvez/T016-PS-024\
**Version:** 1.0\
**Date:** 25 November 2026

------------------------------------------------------------------------

## 1. Purpose

This document records the key implementation decisions for the PS-024
project. It explains the choices made and the requirements they address.
It describes the academic project implementation and is not legal or tax
advice.

## 2. Decision register

  --------------------------------------------------------------------------
  ID                Area              Decision             Reason /
                                                           requirement
  ----------------- ----------------- -------------------- -----------------
  DEC-01            Language          Use Python for the   Supports CSV
                                      engine and           processing,
                                      regression tests.    decimal
                                                           arithmetic and
                                                           command-line
                                                           execution.

  DEC-02            Input format      Use the supplied CSV Keeps data
                                      master files,        structured and
                                      purchase register    aligned with the
                                      and period-wise      sample pack.
                                      GSTR-2B files.       

  DEC-03            Command interface Use a pipe-delimited Provides one
                                      `commands.txt` file. auditable event
                                                           stream for
                                                           invoices,
                                                           payments,
                                                           reconciliation
                                                           and filing.

  DEC-04            Execution order   Execute commands in  Later commands
                                      strict physical file may depend on
                                      order.               state created by
                                                           earlier commands;
                                                           implements BR-18.

  DEC-05            Processing state  Maintain run-time    Supports
                                      state for documents, command-order
                                      sequences,           effects and
                                      purchases, payments, period
                                      portal records and   calculations.
                                      evaluations.         

  DEC-06            Money             Use decimal monetary Avoids binary
                                      arithmetic and       floating-point
                                      half-up rounding per issues and
                                      invoice tax head.    follows BR-17.

  DEC-07            Place of supply   Apply the specified  Implements BR-01.
                                      goods / services     
                                      rules using          
                                      registration status, 
                                      ship-to state,       
                                      customer state and   
                                      address-on-record.   

  DEC-08            GST heads         Split intra-state    Implements BR-02.
                                      GST into CGST and    
                                      SGST; use full-rate  
                                      IGST for inter-state 
                                      supplies; read cess  
                                      from item master.    

  DEC-09            Numbering         Maintain independent Implements BR-04.
                                      FY sequences; reject 
                                      duplicates and gaps; 
                                      cancelled numbers    
                                      remain consumed.     

  DEC-10            IRN timing        IRN generated at or  Implements BR-03
                                      before 24 hours from and its boundary
                                      issue time is valid; cases.
                                      later generation is  
                                      invalid.             

  DEC-11            Cancellation      Allow cancellation   Implements BR-05.
                                      only within 24 hours 
                                      of IRN generation.   

  DEC-12            Credit notes      Require original     Implements BR-06.
                                      invoice, enforce     
                                      cumulative           
                                      taxable-value        
                                      ceiling and apply    
                                      the 30 November      
                                      cut-off.             

  DEC-13            Normalization     Normalize            Supports
                                      invoice-number case  equivalent
                                      and punctuation,     invoice-number
                                      strip optional `INV` formats under
                                      / `INVOICE` prefix   BR-07.
                                      and remove leading   
                                      zeroes.              

  DEC-14            Match key         Match purchases      Implements BR-07.
                                      using supplier       
                                      GSTIN, normalized    
                                      invoice number and   
                                      invoice date.        

  DEC-15            Tolerance         Apply ₹1.00          Implements BR-08.
                                      tolerance separately 
                                      per tax head; a      
                                      difference above     
                                      ₹1.00 is a mismatch. 

  DEC-16            Missing 2B        Hold missing         Implements BR-10.
                                      purchase entries for 
                                      the next two         
                                      reconciliation       
                                      evaluations; then    
                                      classify as pending  
                                      if still absent.     

  DEC-17            2B-only entries   Report portal        Implements BR-10
                                      entries without a    and preserves
                                      purchase-book match  unmatched portal
                                      as missing in books. data.

  DEC-18            ITC eligibility   Apply blocked-credit Implements BR-11
                                      categories and       and BR-12.
                                      proportionate        
                                      common-credit        
                                      reversal for exempt  
                                      turnover.            

  DEC-19            Payment reversal  Reverse ITC when     Implements BR-09.
                                      unpaid beyond 180    
                                      days; allow          
                                      re-availment when    
                                      later payment is     
                                      recorded.            

  DEC-20            RCM               Treat notified       Implements BR-13.
                                      services from        
                                      unregistered         
                                      suppliers as RCM;    
                                      include tax in cash  
                                      liability and        
                                      corresponding        
                                      same-period credit   
                                      in ITC summary.      

  DEC-21            Set-off           Apply the specified  Implements BR-14.
                                      IGST, CGST, SGST and 
                                      cess utilization     
                                      order; prohibit      
                                      CGST-SGST            
                                      cross-utilization.   

  DEC-22            Interest / late   Apply 18% annual     Implements BR-15
                    fee               interest on the      and BR-16.
                                      specified daily      
                                      basis and the        
                                      regular / nil        
                                      late-fee rates and   
                                      cap.                 

  DEC-23            Audit trail       Retain invalid or    Implements BR-19.
                                      rejected outward     
                                      documents with       
                                      status and reason    
                                      instead of silently  
                                      omitting them.       

  DEC-24            Output schema     Generate the         Implements BR-20.
                                      required CSV reports 
                                      with specified       
                                      column names and     
                                      order.               

  DEC-25            Regression tests  Maintain a           Supports
                                      repeatable test      verification
                                      suite separate from  after code
                                      sample-data          changes. Current
                                      processing.          recorded run:
                                                           12/12 tests
                                                           passed.
  --------------------------------------------------------------------------

## 3. Boundary-case decisions

The sample pack includes deliberate boundary cases. The implementation
follows these exact boundaries:

-   **IRN timing:** exactly 24 hours is valid; 24 hours and one second
    is late.
-   **Amount tolerance:** ₹1.00 is within tolerance; ₹1.01 is a
    mismatch.
-   **Payment period:** day 180 is within the 180-day period; day 181 is
    beyond it.
-   **Credit-note cut-off:** 30 November is permitted under the supplied
    rule; 1 December is outside the cut-off.
-   **Command order:** each command takes effect at its physical
    position in `commands.txt`.
-   **Invoice numbering:** duplicates and gaps are rejected;
    cancellation does not release a consumed number.

## 4. Scope boundaries

1.  The project processes the supplied sample pack and command language.
    It does not connect to GSTN, e-invoice portals, banks or live
    accounting systems.
2.  Generated reports are for academic evaluation; they are not official
    GST returns or legal certification.
3.  The implementation follows the PS-024 specification. Changes to the
    specification should be reflected in code, tests, README and design
    documentation.
4.  The recorded 12/12 result applies to the project's current
    regression suite and does not prove coverage of every possible GST
    scenario.

## 5. Verification record

  -------------------------------------------------------------------------------------
  Check                               Recorded result
  ----------------------------------- -------------------------------------------------
  Regression test command             `python run_tests.py`

  Regression test result              12/12 tests passed

  Sample processing command           `python gst_engine.py --data data --out output`

  Outward register records            80

  Reconciliation records              121

  ITC summary records                 12

  Liability set-off records           6
  -------------------------------------------------------------------------------------

## 6. Change control

When a rule, input field, output schema or processing decision changes:

1.  Update the implementation.
2.  Add or update a regression test.
3.  Update `DESIGN_BUSINESS_RULES.md` and the design document where
    applicable.
4.  Add a new decision or revision note to this log.
5.  Re-run the regression suite and sample command before committing.

------------------------------------------------------------------------

**End of Decision Log --- Team T016, PS-024**
