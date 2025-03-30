st.title("PDF to DOCX Converter")
st.write("Upload a PDF file and convert it to DOCX format")

# Custom CSS for the drag-and-drop area
st.markdown("""
<style>
.uploadedFile {
    border: 2px dashed #1E88E5;
    border-radius: 5px;
    padding: 30px;
    text-align: center;
    margin: 10px 0;
}
.uploadedFile:hover {
    background-color: #f0f8ff;
}
</style>
""", unsafe_allow_html=True)

# File uploader with enhanced drag-and-drop
st.markdown('<div class="uploadedFile">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop a PDF file here", type="pdf", accept_multiple_files=False)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Display file information
    file_size = round(uploaded_file.size / 1024, 2)  # Size in KB
    st.success(f"File uploaded: {uploaded_file.name}")
    st.info(f"File size: {file_size} KB")
    
    # Check if file size is too large (optional - adjust the limit as needed)
    if file_size > 10240:  # 10MB limit
        st.warning("File is large and may take longer to convert.")
    
    # Add a button to trigger the conversion
    if st.button("Convert to DOCX"):
        with st.spinner("Converting PDF to DOCX. Please wait..."):
            try:
                # Create a temporary file for the DOCX output
                output_docx_path = os.path.join(tempfile.gettempdir(), "converted_document.docx")
                
                # Convert the file
                if convert_pdf_to_docx(uploaded_file, output_docx_path):
                    # Provide download button for the converted file
                    with open(output_docx_path, "rb") as docx_file:
                        docx_data = docx_file.read()
                        st.download_button(
                            label="Download DOCX file",
                            data=docx_data,
                            file_name=uploaded_file.name.replace(".pdf", ".docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    # Remove temporary output file
                    os.unlink(output_docx_path)
                    st.success("Conversion completed successfully!")
                else:
                    st.error("Conversion failed. Please try again with a different PDF file.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.info("Tips: Make sure your PDF is not password-protected and is a valid document.")
