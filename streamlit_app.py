import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Initialize Selenium WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for Streamlit Cloud
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Scrape election data using Selenium
def get_election_data(driver):
    url = "https://www.theguardian.com/us-news/ng-interactive/2024/nov/05/us-election-results-2024-live-donald-trump-kamala-harris-president"
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load content
    
    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    results = []
    # Update selectors based on actual HTML structure
    for candidate_section in soup.select(".candidate-class"):  # Adjust selector
        candidate = candidate_section.select_one(".candidate-name").text  # Adjust selector
        votes = candidate_section.select_one(".votes-count").text  # Adjust selector
        percentage = candidate_section.select_one(".percentage").text  # Adjust selector
        results.append({"Candidate": candidate, "Votes": votes, "Percentage": percentage})
    
    return results

# Streamlit app layout
st.title("2024 U.S. Election Results")
st.write("Data sourced from The Guardian")

# Main loop to refresh data every 60 seconds
driver = get_driver()  # Initialize driver once
while True:
    data = get_election_data(driver)
    if data:
        for entry in data:
            st.write(f"**Candidate:** {entry['Candidate']}")
            st.write(f"**Votes:** {entry['Votes']}")
            st.write(f"**Percentage:** {entry['Percentage']}")
            st.write("---")
    else:
        st.write("No data available at the moment. Please try refreshing.")
    
    time.sleep(60)  # Wait for 60 seconds before refreshing
    st.experimental_rerun()  # Rerun the app to fetch new data
