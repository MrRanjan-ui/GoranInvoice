# GORAN AI - Invoice Generator Toolset

This directory contains two powerful tools for managing, editing, and generating invoice PDFs for GORAN AI clients.

## Tool 1: Interactive Web Invoice Generator & Ledger (Recommended)
This is an interactive browser-based tool. It works completely offline and runs locally.
* **File:** [generator.html](file:///f:/Agency%20CLients%20works/GoranInvoice/generator.html)
* **How to use:**
  1. Open [generator.html](file:///f:/Agency%20CLients%20works/GoranInvoice/generator.html) in your web browser (Chrome, Edge, Safari, Firefox).
  2. Fill in the invoice details (Invoice Number, Client Name, Project, Amounts, Bank/UPI details) in the left panel.
  3. The right panel will show a **live, pixel-perfect preview** of your invoice.
  4. Select a preset (Development Installment or Monthly Maintenance) to auto-fill items and messages.
  5. Go to the **WhatsApp Send** tab to copy a pre-formatted message for the client or launch WhatsApp directly.
  6. Go to the **Sheet Ledger** tab to keep a local tracking log of all generated invoices (equivalent to the Google Sheet structure).
  7. Click **Print / Save PDF** at the top right, select **Save as PDF** in the print destination, and download your clean PDF!

---

## Tool 2: Python ReportLab Script
A Python script that compiles a highly professional vector PDF directly.
* **File:** [generate_pdf.py](file:///f:/Agency%20CLients%20works/GoranInvoice/generate_pdf.py)
* **How to use:**
  1. Open [generate_pdf.py](file:///f:/Agency%20CLients%20works/GoranInvoice/generate_pdf.py) in your text editor.
  2. Scroll to the bottom `__main__` section and edit the `invoice_details` dictionary:
     ```python
     invoice_details = {
         'invoice_no': 'INV-001',
         'date': '04 Jun 2026',
         'due_date': '18 Jun 2026',
         'client_name': 'Anaaj AI',
         # ... modify fields as needed
     }
     ```
  3. Run the script in your terminal:
     ```bash
     py generate_pdf.py
     ```
  4. The script will output [invoice.pdf](file:///f:/Agency%20CLients%20works/GoranInvoice/invoice.pdf) in this directory.
