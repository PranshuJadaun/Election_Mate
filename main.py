import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# Define a function to scrape election data
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
    # Modify these selectors to match actual tags/classes on the page
    results = []
    for candidate_section in soup.select(".candidate-class"):  # Change this selector
        candidate = candidate_section.select_one(".candidate-name").text  # Change this selector
        votes = candidate_section.select_one(".votes-count").text  # Change this selector
        percentage = candidate_section.select_one(".percentage").text  # Change this selector
        results.append({"Candidate": candidate, "Votes": votes, "Percentage": percentage})
    
    return results

# Streamlit app layout
st.title("2024 U.S. Election Results")
st.write("Data sourced from The Guardian")

# Refresh data button
if st.button("Refresh Data"):
    data = get_election_data()
    if data:
        for entry in data:
            st.write(f"**Candidate:** {entry['Candidate']}")
            st.write(f"**Votes:** {entry['Votes']}")
            st.write(f"**Percentage:** {entry['Percentage']}")
            st.write("---")
    else:
        st.write("No data available at the moment. Please try refreshing.")

st.write("This application updates data upon clicking the 'Refresh Data' button.")
