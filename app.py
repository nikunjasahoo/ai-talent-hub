import streamlit as st
import subprocess
import sys
import os
import base64

# Set page configuration
st.set_page_config(
    page_title="AI Talent Hub",
    page_icon="👥",
    layout="wide"
)

# Function to run the command based on selected workflow
def run_workflow(workflow, email=None, job_title=None, skills=None, experience=None):
    cmd = ["python3", "main.py", "--workflow", workflow]
    
    if job_title:
        cmd.extend(["--job-title", job_title])
    
    if skills:
        cmd.extend(["--skills", skills])
    
    if experience:
        cmd.extend(["--experience", experience])
    
    if email:
        cmd.extend(["--email", email])
    
    st.info(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Display output in real-time
        output_placeholder = st.empty()
        output_text = ""
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_text += output
                output_placeholder.text_area("Output", output_text, height=400)
        
        # Get return code and remaining output
        return_code = process.poll()
        if return_code == 0:
            st.success("Workflow completed successfully!")
        else:
            st.error(f"Workflow failed with return code {return_code}")
            
    except Exception as e:
        st.error(f"Error executing workflow: {str(e)}")

# Function to get a download link for a file
def get_file_download_link(file_path):
    with open(file_path, "r") as f:
        file_content = f.read()
    
    # Create a download link
    b64 = base64.b64encode(file_content.encode()).decode()
    file_name = os.path.basename(file_path)
    href = f'<a href="data:text/plain;base64,{b64}" download="{file_name}" target="_blank">{file_name}</a>'
    return href

# Function to delete a resume file
def delete_resume(file_path):
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        st.error(f"Error deleting file: {str(e)}")
        return False

# Add CSS styling for the title section
st.markdown("""
<style>
    .title-container {
        background-color: #4267B2;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.5em;
        font-weight: normal;
    }
    .resume-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px;
        border-bottom: 1px solid #f0f0f0;
    }
    .delete-btn {
        color: #ff4b4b;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Main layout with styled title
st.markdown("""
<div class="title-container">
    <div class="title">AI Talent Hub</div>
    <div class="subtitle">Intelligent Recruitment Assistant</div>
</div>
""", unsafe_allow_html=True)

# Set default recruiter email
email = "airecruiter@talenthub.com"

# Initialize session state for tracking deleted resumes
if 'deleted_resume' not in st.session_state:
    st.session_state.deleted_resume = None

# Create two columns for the form
col1, col2 = st.columns(2)

# Left section
with col1:
    st.markdown("### Resume Store")
    uploaded_file = st.file_uploader("Upload a text resume", type=["txt"])
    
    if uploaded_file is not None:
        # Create directory if it doesn't exist
        os.makedirs("data/resumes", exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join("data/resumes", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Resume saved: {uploaded_file.name}")
    
    # Display success message if a file was deleted
    if st.session_state.deleted_resume:
        st.success(f"Deleted: {st.session_state.deleted_resume}")
        st.session_state.deleted_resume = None
    
    # Check if the directory exists
    if os.path.exists("data/resumes"):
        resumes = [f for f in os.listdir("data/resumes") if f.endswith(".txt")]
        if resumes:
            # Display the first 2 resumes
            for i, resume in enumerate(resumes[:2]):
                resume_path = os.path.join("data/resumes", resume)
                col_link, col_delete = st.columns([9, 1])
                
                with col_link:
                    st.markdown(get_file_download_link(resume_path), unsafe_allow_html=True)
                
                with col_delete:
                    delete_key = f"delete_{i}"
                    if st.button("🗑️", key=delete_key):
                        if delete_resume(resume_path):
                            st.session_state.deleted_resume = resume
                            st.rerun()
            
            # Display remaining resumes in a collapsible section if there are more than 2
            if len(resumes) > 2:
                with st.expander(f"Show {len(resumes) - 2} more resumes"):
                    for i, resume in enumerate(resumes[2:], start=2):
                        resume_path = os.path.join("data/resumes", resume)
                        col_link, col_delete = st.columns([9, 1])
                        
                        with col_link:
                            st.markdown(get_file_download_link(resume_path), unsafe_allow_html=True)
                        
                        with col_delete:
                            delete_key = f"delete_{i}"
                            if st.button("🗑️", key=delete_key):
                                if delete_resume(resume_path):
                                    st.session_state.deleted_resume = resume
                                    st.rerun()
        else:
            st.info("No resumes found in the store.")
    else:
        st.info("Resume store directory not found.")

# Requirements section
with col2:
    st.markdown("### Job Requirements")
    st.info(f"Recruiter Email: {email}")
    
    job_title = st.text_input("Job Title", key="job_title", placeholder="e.g., Python Developer")
    skills = st.text_input("Skills (comma-separated)", key="skills", placeholder="e.g., Python, Django, Flask, FastAPI")
    experience = st.text_input("Experience Level", key="experience", placeholder="e.g., 3+ years")

# Workflow selection
st.markdown("### Select Workflow")

# Create a layout for buttons
col1, col2, col3, col4 = st.columns(4)

# Add buttons for each workflow
with col1:
    if st.button("Full Recruitment", use_container_width=True):
        if not job_title or not skills or not experience:
            st.warning("Please fill in all job requirement fields.")
        else:
            run_workflow("recruitment_process", email, job_title, skills, experience)

with col2:
    if st.button("Job Posting", use_container_width=True):
        if not job_title or not skills or not experience:
            st.warning("Please fill in all job requirement fields.")
        else:
            run_workflow("job_posting", email, job_title, skills, experience)

with col3:
    if st.button("Candidate Selection", use_container_width=True):
        if not job_title or not skills or not experience:
            st.warning("Please fill in all job requirement fields.")
        else:
            run_workflow("candidate_selection", email, job_title, skills, experience)

with col4:
    if st.button("Interview Process", use_container_width=True):
        if not job_title or not skills or not experience:
            st.warning("Please fill in all job requirement fields.")
        else:
            run_workflow("interview_process", email, job_title, skills, experience)

# Add information about the application
st.markdown("---")
st.markdown("""
### About AI Talent Hub

AI Talent Hub automates recruitment tasks using multiple AI agents:

- **Job Description Generator**: Creates professional job descriptions
- **Resume Ranker**: Analyzes and ranks candidate resumes
- **Email Automation**: Sends professional communications
- **Interview Scheduler**: Coordinates interview schedules
- **Interview Agent**: Conducts technical interviews
- **Hire Recommendation**: Provides objective hiring recommendations
- **Sentiment Analyzer**: Analyzes interview sentiment
""") 