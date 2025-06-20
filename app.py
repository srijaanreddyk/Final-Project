import streamlit as st
from scraper import scrape_with_subpages, save_to_csv

st.set_page_config(page_title="🌐 Web Scraper with Subpages", layout="wide")

st.title("🌍 Web Scraper App")
st.markdown("Enter a website URL to scrape main content and internal links. Data will be saved to a CSV file.")

url = st.text_input("Enter Website URL", "https://example.com")
max_pages = st.slider("Maximum Pages to Scrape (including main)", 1, 30, 5)

if st.button("Start Scraping"):
    with st.spinner("Scraping website and subpages..."):
        data = scrape_with_subpages(url, max_pages)
        file_path = save_to_csv(data)

    st.success(f"✅ Scraping Complete! Saved {len(data)} pages to:")
    st.code(file_path)

    st.download_button(
        label="📥 Download CSV",
        data=open(file_path, "rb"),
        file_name="scraped_output.csv",
        mime="text/csv"
    )

    st.subheader("🔍 Preview of Scraped Data")
    for page in data[:3]:
        st.write(f"**URL:** {page['url']}")
        st.write(f"**Title:** {page['title']}")
        st.text_area("Content Snippet", page['text'][:500] + "...", height=150)
