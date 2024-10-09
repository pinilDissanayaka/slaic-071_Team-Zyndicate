import os
import streamlit as st
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, stream_text
from utils.alignpolicy import get_align_candidate, draw_pie_plot
from utils.policies import get_policies

list_of_selected_policies=[]

# App title
st.set_page_config(page_title="🤗💬 Election-Insight-App ")

#app side bar
with st.sidebar:
    st.subheader("Upload the manifesto of the candidate.")
    
    uploaded_files = st.file_uploader(
    "Choose a PDF, TXT files", accept_multiple_files=True)
    
    
    for uploaded_file in uploaded_files:
        st.write("filename:", uploaded_file.name)
        save_pdf_txt_on_temp_dir(uploaded_file=uploaded_file)
        
    if uploaded_files:
        with st.spinner("Processing..."):
            st.button("Upload to vector store.", on_click=load_into_vector_store())

st.title("💡 Manifesto Matchmaker")
st.write("See which presidential candidate's monitorable promises aligns best with your vision for Sri Lanka")
st.write("-----------------------------------------------------------------------------------------------------------") 

selected_themes=st.multiselect(label="Select Your Themes", 
                               options=["Infrastructure", "Social Protection", "Trade and Export", "Labour", "Governance", "Law and Order", "Corruption", "Agriculture", "Health", "Taxation", "Education", "Supplementary", "Economic Growth", "IMF Programme", "Reconciliation"], 
                               help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme."
                               )

if selected_themes:
    with st.spinner("Processing..."):
        for selected_theme in selected_themes:
            policies=get_policies(theme=selected_theme)
            selected_policies=st.multiselect(label=f"Select Policies related to the {selected_theme}", 
                            options=policies
            )
            for selected_policy in selected_policies:
                list_of_selected_policies.append(selected_policy)
    

if len(list_of_selected_policies) !=0:
    try:
        if st.button("Match"):
            with st.spinner("Matching..."):
                aligned_candidates, aligned_candidate_scores=get_align_candidate(policies=selected_policies)
                
                st.subheader(stream_text(text="Your Manifesto Aligns..."))
                
                for aligned_candidate, aligned_candidate_score in zip(aligned_candidates, aligned_candidate_scores):
                    st.write(stream_text(text=f"candidate {aligned_candidate}", delay=0.06))
                
                st.plotly_chart(figure_or_data=draw_pie_plot(labels=aligned_candidates, sizes=aligned_candidate_scores))
    except Exception as e:
        st.error("Internal Server Error.")
        st.error(e.args)
    

