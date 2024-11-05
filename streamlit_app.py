import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# Function to scrape election data
def get_election_data():
    url = "https://www.theguardian.com/us-news/ng-interactive/2024/nov/05/us-election-results-2024-live-donald-trump-kamala-harris-president"
    response = requests.get(url)
    
    # Ensure successful response
    if response.status_code != 200:
        st.error("Failed to retrieve data. Please try again later.")
        return None
    
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Placeholder for data extraction - Adjust selectors based on actual HTML
    results = []
    for candidate_section in soup.select(".candidate-class"):  # Update this selector based on actual HTML structure
        candidate = candidate_section.select_one(".candidate-name").text  # Update this selector
        votes = candidate_section.select_one(".votes-count").text  # Update this selector
        percentage = candidate_section.select_one(".percentage").text  # Update this selector
        results.append({"Candidate": candidate, "Votes": votes, "Percentage": percentage})
    
    return results

# Streamlit app layout
st.title("2024 U.S. Election Results")
st.write("Data sourced from The Guardian")

# Main loop to refresh data every 60 seconds
while True:
    data = get_election_data()
    if data:
        for entry in data:
            st.write(f"**Candidate:** {entry['Candidate']}")
            st.write(f"**Votes:** {entry['Votes']}")
            st.write(f"**Percentage:** {entry['Percentage']}")
            st.write("---")
    else:
        st.write("No data available at the moment. Please try refreshing.")

    # Wait for 60 seconds before refreshing the data
    time.sleep(60)
    st.experimental_rerun()  # Reruns the app to fetch new data
