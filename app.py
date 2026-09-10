import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="AI Research Assistant", page_icon="🔍", layout="wide")

st.title("🤖 Autonomous Multi-Agent Research System")
st.write("Enter a topic to initiate autonomous search, web scraping, writing, and critic evaluation.")

topic = st.text_input("Research Topic", placeholder="e.g., Quantum Computing breakthroughs")

if st.button("Run Research Pipeline", type="primary"):
    if not topic.strip():
        st.warning("Please enter a valid research topic.")
    else:
        with st.status("Executing Research Pipeline...", expanded=True) as status:
            try:
                st.write("🔍 Step 1: Running Search Agent...")
                state = run_research_pipeline(topic)
                status.update(label="Research Complete!", state="complete", expanded=False)
                
                # Display outputs in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📝 Final Report", "🧐 Critic Review", "🔎 Search Data", "🌐 Scraped Content"])
                
                with tab1:
                    st.subheader("Research Report")
                    st.markdown(state.get("report", "No report generated."))
                    
                with tab2:
                    st.subheader("Critic Feedback")
                    st.markdown(state.get("feedback", "No feedback generated."))
                    
                with tab3:
                    st.subheader("Raw Search Results")
                    st.text(state.get("search_results", ""))
                    
                with tab4:
                    st.subheader("Scraped Page Content")
                    st.text(state.get("scraped_content", ""))

            except Exception as e:
                status.update(label="Pipeline Failed", state="error")
                st.error(f"Error during execution: {str(e)}")
