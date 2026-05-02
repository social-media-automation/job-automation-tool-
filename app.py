import streamlit as st
import requests
from bs4 import BeautifulSoup
import feedparser

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Job Automation Tool", layout="wide")

st.title("🚀 AI Job Automation Tool")
st.write("Govt + Private + Scheme Jobs (Auto Aggregation System)")

# =========================
# GOVT JOBS (RSS FEED)
# =========================
def get_govt_jobs():
    url = "https://feeds.feedburner.com/ndtvjobs"
    feed = feedparser.parse(url)

    jobs = []
    for entry in feed.entries[:10]:
        jobs.append({
            "title": entry.title,
            "company": "Government / News Source",
            "location": "Various",
            "link": entry.link,
            "source": "Govt"
        })
    return jobs

# =========================
# PRIVATE JOBS (SCRAPING)
# =========================
def get_private_jobs():
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    jobs = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for job in soup.select(".job")[:10]:
            title = job.select_one(".company_and_position [itemprop='title']")
            link = job.get("data-href")

            if title and link:
                jobs.append({
                    "title": title.text.strip(),
                    "company": "RemoteOK",
                    "location": "Remote",
                    "link": "https://remoteok.com" + link,
                    "source": "Private"
                })
    except:
        jobs.append({
            "title": "Error fetching private jobs",
            "company": "System",
            "location": "N/A",
            "link": "#",
            "source": "Private"
        })

    return jobs

# =========================
# SCHEME / PROGRAMS
# =========================
def get_schemes():
    return [
        {
            "title": "Youth Employment Program 2026",
            "company": "Government Scheme",
            "location": "Pakistan",
            "link": "https://example.com",
            "source": "Scheme"
        },
        {
            "title": "Skill Development Initiative",
            "company": "Govt Program",
            "location": "Pakistan",
            "link": "https://example.com",
            "source": "Scheme"
        }
    ]

# =========================
# LOAD ALL JOBS
# =========================
def get_all_jobs():
    jobs = []
    jobs += get_govt_jobs()
    jobs += get_private_jobs()
    jobs += get_schemes()
    return jobs

jobs = get_all_jobs()

# =========================
# FILTER SECTION
# =========================
st.sidebar.header("🔍 Filters")

keyword = st.sidebar.text_input("Search Job Title")
source_filter = st.sidebar.selectbox("Source", ["All", "Govt", "Private", "Scheme"])

filtered_jobs = []

for job in jobs:
    if keyword.lower() in job["title"].lower() or keyword == "":
        if source_filter == "All" or job["source"] == source_filter:
            filtered_jobs.append(job)

# =========================
# DISPLAY RESULTS
# =========================
st.write(f"### 📊 Total Jobs Found: {len(filtered_jobs)}")

for job in filtered_jobs:
    st.subheader(job["title"])
    st.write("🏢 Company:", job["company"])
    st.write("📍 Location:", job["location"])
    st.write("🔗 Link:", job["link"])
    st.caption(f"Source: {job['source']}")
    st.markdown("---")
