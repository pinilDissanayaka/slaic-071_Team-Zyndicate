import os
import streamlit as st
from utils.utils import save_pdf_txt_on_temp_dir, load_into_vector_store, stream_text
from utils.manifestomatchmaker import get_relevant_policies
from utils.alignpolicy import get_align_candidate, draw_pie_plot

selected_policies=[]

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
st.write("-----------------------------------------------------------------------------------------------------------") 
st.write("See which presidential candidate's monitorable promises aligns best with your vision for Sri Lanka")

selected_themes=st.multiselect(label="Select Your Themes", 
                               options=["Infrastructure", "Social Protection", "Trade and Export", "Labour", "Governance", "Law and Order", "Corruption", "Agriculture", "Health", "Taxation", "Education", "Supplementary", "Economic Growth", "IMF Programme", "Reconciliation"], 
                               help="Every promise has an associated topic. In this section, select which topics you wish to focus on, under each of your chosen themes. A topic is a distinct subject area that classifies individual promises. Each theme has multiple topics, though not all topics are represented under every theme."
                               )

if selected_themes:
    with st.spinner("Processing..."):
        list_of_policies=get_relevant_policies(themes=selected_themes)
        st.markdown(list_of_policies)
        selected_policies=st.multiselect(label="Select Policies", 
                            options=list_of_policies[0]
        )

if len(selected_policies) > 0:
    if st.button("Match"):
        with st.spinner("Matching..."):
            for selected_policy in selected_policies:
                candidates, scores=get_align_candidate(policies=selected_policy)
                
                st.write("-----------------------------------------------------------------------------------------------------------")
                st.write(selected_policy)
                st.write("-----------------------------------------------------------------------------------------------------------")
                st.subheader("Which Presidential Candidate Aligns Most with Your Policy Choices?")
                pie_plot=draw_pie_plot(labels=candidates, sizes= scores)
                st.plotly_chart(pie_plot)
                st.write("-----------------------------------------------------------------------------------------------------------")
                st.subheader("Your Policies Aligns...")
                for candidate, score in zip(candidates, scores):
                    st.write_stream(stream=stream_text(text=f"{score * 100} % with {candidate} policy."))
                        
                st.write("-----------------------------------------------------------------------------------------------------------")





