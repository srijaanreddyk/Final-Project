import streamlit as st
from scraper import scrape_with_subpages, save_to_csv

st.set_page_config(page_title="🌐 Web Scraper App", layout="wide")

st.title("🌍 Universal Web Scraper")
st.markdown("Scrape any website (including subpages & JS-rendered content) and download it as CSV.")

# Input fields
url = st.text_input("🔗 Enter Website URL", "https://example.com")
max_pages = st.slider("📄 Maximum Pages to Scrape (including main page)", 1, 30, 5)

# Start Scraping
if st.button("🚀 Start Scraping"):
    with st.spinner("Scraping... please wait"):
        data = scrape_with_subpages(url, max_pages)
        file_path = save_to_csv(data)

    st.success(f"✅ Scraping completed! {len(data)} pages saved.")
    st.code(file_path)

    # CSV download button
    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Download CSV File",
            data=f,
            file_name="scraped_output.csv",
            mime="text/csv"
        )

    # Preview Results
    st.subheader("🔍 Preview of Scraped Pages")
    for i, page in enumerate(data[:3]):
        st.markdown(f"**🔗 URL:** {page['url']}")
        st.markdown(f"**📌 Title:** {page['title']}")
        snippet = (page.get("text") or "")[:500] + "..."
        st.text_area("📄 Content Snippet", snippet, height=150, key=f"snippet_{i}")

