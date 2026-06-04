import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Draw a line above footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(40, 50, 555, 50)
        
        # Draw footer text
        self.drawString(40, 35, "GORAN AI  |  official.goranai@gmail.com  |  https://goran.in")
        self.drawRightString(555, 35, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_invoice(filename, details):
    # Setup document geometry with 40pt margins (approx 14mm)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=65
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom color palette
    c_primary = colors.HexColor("#0f172a") # Navy Dark
    c_accent = colors.HexColor("#2563eb")  # Tech Blue
    c_text_dark = colors.HexColor("#1e293b")
    c_text_muted = colors.HexColor("#64748b")
    c_bg_light = colors.HexColor("#f8fafc")
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='InvoiceTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=2 # Right align
    ))
    
    styles.add(ParagraphStyle(
        name='HeaderBrand',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_accent
    ))
    
    styles.add(ParagraphStyle(
        name='HeaderBrandSub',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text_muted
    ))
    
    styles.add(ParagraphStyle(
        name='MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_text_muted,
        alignment=2
    ))
    
    styles.add(ParagraphStyle(
        name='MetaVal',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_text_dark,
        alignment=2
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='BodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_text_dark
    ))

    styles.add(ParagraphStyle(
        name='BodyNormal',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text_dark
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeaderRight',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=2
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text_dark
    ))

    styles.add(ParagraphStyle(
        name='TableCellRight',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text_dark,
        alignment=2
    ))

    styles.add(ParagraphStyle(
        name='TotalLabel',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_text_dark,
        alignment=2
    ))

    styles.add(ParagraphStyle(
        name='TotalVal',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        alignment=2
    ))

    # --- Header Table ---
    # Left: Brand, Right: Invoice Title & Meta
    brand_p = Paragraph("GORAN AI", styles['HeaderBrand'])
    brand_sub_p = Paragraph("Advanced AI Agents & Web Solutions<br/>Email: official.goranai@gmail.com<br/>Website: https://goran.in", styles['HeaderBrandSub'])
    
    brand_flow = [brand_p, Spacer(1, 4), brand_sub_p]
    
    meta_data = [
        [Paragraph("INVOICE", styles['InvoiceTitle']), ""],
        [Paragraph("Invoice Number:", styles['MetaLabel']), Paragraph(details['invoice_no'], styles['MetaVal'])],
        [Paragraph("Date:", styles['MetaLabel']), Paragraph(details['date'], styles['MetaVal'])],
        [Paragraph("Due Date:", styles['MetaLabel']), Paragraph(details['due_date'], styles['MetaVal'])],
    ]
    
    meta_table = Table(meta_data, colWidths=[110, 90])
    meta_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
    ]))
    
    header_table = Table([[brand_flow, meta_table]], colWidths=[315, 200])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 25))
    
    # --- Client / Bill To and Payment Summary ---
    client_flow = [
        Paragraph("BILLED TO", styles['SectionHeader']),
        Paragraph(details['client_name'], styles['BodyBold']),
        Paragraph(details['project_name'], styles['BodyNormal']),
        Paragraph(details.get('client_address', ''), styles['BodyNormal'])
    ]
    
    payment_method_flow = [
        Paragraph("PAYMENT INFORMATION", styles['SectionHeader']),
        Paragraph("Bank Transfer / UPI", styles['BodyBold']),
        Paragraph(f"Bank: {details['bank_name']}", styles['BodyNormal']),
        Paragraph(f"UPI ID: {details['upi_id']}", styles['BodyNormal']),
    ]
    
    parties_table = Table([[client_flow, payment_method_flow]], colWidths=[260, 255])
    parties_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(parties_table)
    story.append(Spacer(1, 20))
    
    # --- Line Items Table ---
    # Col widths sum to 515 (A4 width 595 - 80 margin)
    col_widths = [385, 130]
    
    table_data = [
        [Paragraph("Description", styles['TableHeader']), Paragraph("Amount", styles['TableHeaderRight'])]
    ]
    
    for item in details['items']:
        table_data.append([
            Paragraph(item['description'], styles['TableCell']),
            Paragraph(f"₹{item['amount']:,}", styles['TableCellRight'])
        ])
        
    items_table = Table(table_data, colWidths=col_widths)
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 10))
    
    # --- Totals Section ---
    total_val = sum(item['amount'] for item in details['items'])
    totals_data = [
        ["", Paragraph("Total Due", styles['TotalLabel']), Paragraph(f"₹{total_val:,}", styles['TotalVal'])]
    ]
    totals_table = Table(totals_data, colWidths=[285, 100, 130])
    totals_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (2, 0), (2, -1), 10),
    ]))
    
    story.append(totals_table)
    story.append(Spacer(1, 25))
    
    # --- Bank / UPI Complete Box ---
    bank_box_data = [
        [Paragraph("<b>RECEIVER BANK / UPI ACCREDITATIONS</b>", styles['SectionHeader']), ""],
        [Paragraph("Bank Name:", styles['MetaLabel']), Paragraph(details['bank_name'], styles['TableCell'])],
        [Paragraph("Account Number:", styles['MetaLabel']), Paragraph(details['bank_account_no'], styles['TableCell'])],
        [Paragraph("IFSC Code:", styles['MetaLabel']), Paragraph(details['bank_ifsc'], styles['TableCell'])],
        [Paragraph("UPI ID:", styles['MetaLabel']), Paragraph(details['upi_id'], styles['TableCell'])],
    ]
    bank_box_table = Table(bank_box_data, colWidths=[110, 405])
    bank_box_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(bank_box_table)
    
    # Build Document using our page numbered canvas
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    # Example values from standard configuration
    invoice_details = {
        'invoice_no': 'INV-001',
        'date': '04 Jun 2026',
        'due_date': '18 Jun 2026',
        'client_name': 'Anaaj AI',
        'project_name': 'Anaaj AI Development',
        'client_address': 'Project Development Contract\nPhase 2 Deliverables',
        'bank_name': 'State Bank of India',
        'bank_account_no': '42002389558',
        'bank_ifsc': 'SBIN0002911',
        'upi_id': 'ranjanashish9992@ybl',
        'items': [
            {
                'description': 'Anaaj AI Development - 2nd Installment',
                'amount': 25000
            }
        ]
    }
    
    output_pdf = "invoice.pdf"
    create_invoice(output_pdf, invoice_details)
    print(f"Successfully generated pdf: {os.path.abspath(output_pdf)}")
