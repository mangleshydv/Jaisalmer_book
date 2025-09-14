# utils.py
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

def generate_pdf(template_src, context_dict={}):
    """
    Generate PDF from HTML template using WeasyPrint (better CSS support than xhtml2pdf).
    Returns PDF as BytesIO.
    """
    html_string = render_to_string(template_src, context_dict)
    pdf_file = BytesIO()

    HTML(string=html_string, base_url=None).write_pdf(pdf_file)

    pdf_file.seek(0)
    return pdf_file
