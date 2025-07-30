import streamlit as st
import pdfkit
from jinja2 import Template
import tempfile
import os

# === PDFKit configuration ===
path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Change this if needed
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# === Streamlit UI ===
st.title("📄 Authority Letter Generator")

with st.form("letter_form"):
    firm_name = st.text_input("Firm Name")
    firm_address = st.text_area("Firm Address")
    mobile = st.text_input("Mobile Number")
    owner_name = st.text_input("Owner's Name")
    father_name = st.text_input("Father's Name")
    residence = st.text_area("Residence Address")

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    # Load the HTML template
    with open("template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Fill in the template
    template = Template(html_template)
    filled_html = template.render(
        firm_name=firm_name,
        firm_address=firm_address,
        mobile=mobile,
        owner_name=owner_name,
        father_name=father_name,
        residence=residence
    )

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(filled_html.encode("utf-8"))
        tmp_html_path = tmp_html.name

    # Output PDF path
    output_pdf_path = tmp_html_path.replace(".html", ".pdf")

    # Generate PDF
    pdfkit.from_file(tmp_html_path, output_pdf_path, configuration=config)

    # Offer download
    with open(output_pdf_path, "rb") as f:
        st.success("✅ PDF generated!")
        st.download_button("📥 Download Authority Letter", f, "Authority_Letter.pdf", mime="application/pdf")

    # Clean up
    os.remove(tmp_html_path)
    os.remove(output_pdf_path)
