import streamlit as st
import fitz  # PyMuPDF
import os
import tempfile

def remove_highlights_from_pdf(input_pdf, output_pdf_path):
    pdf_document = fitz.open(stream=input_pdf.read(), filetype="pdf")

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        for annot in page.annots():
            if annot.type[0] == 8:  # Typ 8 ist für Highlights
                page.delete_annot(annot)

    pdf_document.save(output_pdf_path)
    pdf_document.close()

def main():
    st.title("PDF Highlight Remover")
    
    uploaded_file = st.file_uploader("Lade ein PDF-Dokument hoch", type=["pdf"])

    if uploaded_file is not None:
        # Extract the original filename (without extension)
        original_filename = os.path.splitext(uploaded_file.name)[0]
        new_filename = f"{original_filename}_no_highlights.pdf"

        # Create a temporary file path without immediately opening it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            output_pdf_path = temp_pdf.name
        
        # Remove highlights and save to temporary file
        remove_highlights_from_pdf(uploaded_file, output_pdf_path)
        
        st.success("Highlights wurden entfernt!")
        
        # Provide a download button for the processed PDF with the new filename
        with open(output_pdf_path, "rb") as file:
            st.download_button(
                label="Download bereinigtes PDF",
                data=file,
                file_name=new_filename,
                mime="application/pdf"
            )
        
        # Remove the temporary file after the user has had the chance to download it
        os.remove(output_pdf_path)

if __name__ == "__main__":
    main()

