import streamlit as st
from scraper import get_jobs

st.title("AI Job Automation Tool")

st.write("Latest Jobs from Trusted Sources")

jobs = get_jobs()

for job in jobs:
    st.subheader(job["title"])
    st.write(job["company"])
    st.write(job["location"])
    st.write(job["link"])
    st.markdown("---")
