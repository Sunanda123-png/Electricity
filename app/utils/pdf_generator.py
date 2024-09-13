import pdfkit
from io import BytesIO


def generate_pdf(content: str) -> BytesIO:
    # Path to the wkhtmltopdf executable
    path_to_wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"  # Update this path as necessary

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf = pdfkit.from_string(content, False, configuration=config)
    return BytesIO(pdf)
