import streamlit as st
from jinja2 import Template
from xhtml2pdf import pisa
import io

# === Streamlit UI ===
st.title("📝 Authority Letter Generator")

firm_name = st.text_input("Firm Name")
firm_address = st.text_input("Firm Address")
mobile = st.text_input("Mobile Number")
owner_name = st.text_input("Owner's Name")
father_name = st.text_input("Father's Name")
residence = st.text_input("Residence Address")

if st.button("Generate PDF"):
    # === Load HTML Template ===
    with open("template.html", "r", encoding="utf-8") as file:
        html_template = file.read()

    # === Fill Template ===
    template = Template(html_template)
    filled_html = template.render(
        firm_name=firm_name,
        firm_address=firm_address,
        mobile=mobile,
        owner_name=owner_name,
        father_name=father_name,
        residence=residence
    )

    # === Generate PDF ===
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(filled_html), dest=pdf_buffer)

    if pisa_status.err:
        st.error("❌ PDF generation failed")
    else:
        st.success("✅ PDF generated successfully!")
        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer.getvalue(),
            file_name="Authority_Letter.pdf",
            mime="application/pdf"
        )
