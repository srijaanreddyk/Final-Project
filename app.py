import streamlit as st
from scraper import scrape_content_only, save_to_txt, save_to_csv

st.set_page_config(page_title="📄 Web Content Scraper", layout="wide")
st.title("🕸️ Crawl and Scrape Web Page Content")

url = st.text_input("Enter a base URL (static site recommended):", placeholder="https://books.toscrape.com")
file_format = st.selectbox("Select download format:", ["TXT", "CSV"])
max_pages = st.slider("Max number of subpages to crawl:", 1, 30, 5)

if st.button("Scrape Content"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Scraping content from subpages..."):
            results = scrape_content_only(url, max_pages)

        if results:
            st.success(f"Scraped content from {len(results)} pages.")

            if file_format == "TXT":
                txt = save_to_txt(results)
                st.download_button("Download .txt", txt, file_name="scraped_content.txt")
            else:
                csv_data = save_to_csv(results)
                st.download_button("Download .csv", csv_data, file_name="scraped_content.csv", mime="text/csv")

            # Display content preview
            st.subheader("📄 Scraped Content Preview")
            for item in results[:5]:  # show first 5
                with st.expander(f"{item['url']}"):
                    st.markdown(item['content'].replace("\n", "  \n"))
        else:
            st.error("No content found or unable to scrape the site.")
