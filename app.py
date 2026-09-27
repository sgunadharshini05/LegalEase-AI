import streamlit as st
import requests
from utils.docx_formatter import generate_docx_file
from utils.pdf_formatter import generate_pdf_file

# Page Config
st.set_page_config(
    page_title="LegalEase AI - Smart Legal Document Generator",
    page_icon="⚖️",
    layout="wide"
)

# Header Section with Title
st.title("⚖️ LegalEase AI Platform")
st.markdown("### Automated Legal Document Drafting & Export Tool")
st.write("---")

# Sidebar - Document Parameters
st.sidebar.header("📋 Document Parameters")

doc_type = st.sidebar.selectbox(
    "📄 Document Type",
    [
        "Non-Disclosure Agreement (NDA)",
        "Employment Contract",
        "Freelance Work Contract",
        "Rental Lease Agreement",
        "Employment Offer Letter"
    ]
)

parties = st.sidebar.text_input(
    "👥 Parties Involved", 
    "Jane Doe (Service Provider), TechNova Inc. (Client)"
)

terms_raw = st.sidebar.text_area(
    "📝 Terms & Conditions (Semicolon ';' separated)", 
    "Payment to be made within 30 days of invoice; Provider agrees to deliver work by deadline; Confidentiality strictly enforced; Either party may terminate with 15 days notice"
)

effective_date = st.sidebar.text_input("📅 Effective Date", "April 15, 2026")

generate_btn = st.sidebar.button("🚀 Generate Document", type="primary")

# Main Screen Layout
col1, col2 = st.columns([1.1, 0.9])

if generate_btn:
    terms_list = [t.strip() for t in terms_raw.split(";") if t.strip()]
    
    payload = {
        "doc_type": doc_type,
        "parties": parties,
        "terms": terms_list,
        "effective_date": effective_date
    }

    with st.spinner("🤖 Gemini 1.5 Pro AI is drafting your legal document..."):
        try:
            response = requests.post("http://127.0.0.1:8000/generate-document", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("document", "")
                
                st.session_state["generated_text"] = generated_text
                st.session_state["terms_list"] = terms_list
                st.session_state["doc_type"] = doc_type
                st.success("✅ Legal Document Successfully Drafted!")
            else:
                st.error(f"❌ Backend Error: {response.status_code} - Check FastAPI server.")
        except Exception as e:
            st.error(f"⚠️ Connection Error: Ensure backend is running on port 8000. Detail: {e}")

if "generated_text" in st.session_state:
    with col1:
        st.subheader("📄 Edit & Preview Drafted Document")
        
        # Tabs for Live Edit and Styled Dark Mode Preview
        tab1, tab2 = st.tabs(["📝 Click to Edit Document", "🌙 Dark Mode HTML Preview"])
        
        with tab1:
            edited_doc = st.text_area(
                "Document Editor", 
                value=st.session_state["generated_text"], 
                height=480
            )
            # Sync edited text
            st.session_state["generated_text"] = edited_doc

        with tab2:
            # HTML Dark Mode Container required in Project Description
            dark_html = f"""
            <div style="background-color: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; height: 480px; overflow-y: auto;">
            {st.session_state['generated_text']}
            </div>
            """
            st.components.v1.html(dark_html, height=500, scrolling=True)

    with col2:
        st.subheader("📥 Export & Download Options")
        st.info("Download ready-to-use branded legal document with logo & headers.")
        
        doc_type_val = st.session_state["doc_type"]
        terms_val = st.session_state["terms_list"]
        current_text = st.session_state["generated_text"]
        
        # 1. TXT Export
        st.download_button(
            label="📄 Download as .TXT",
            data=current_text,
            file_name=f"{doc_type_val.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.write("")
        
        # 2. DOCX Export
        try:
            docx_bytes = generate_docx_file(doc_type_val, current_text, terms_val)
            st.download_button(
                label="📝 Download as .DOCX (Word)",
                data=docx_bytes,
                file_name=f"{doc_type_val.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")
            
        st.write("")
        
        # 3. PDF Export
        try:
            pdf_bytes = generate_pdf_file(doc_type_val, current_text, terms_val)
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_bytes,
                file_name=f"{doc_type_val.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")