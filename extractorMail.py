import re
import requests
import streamlit as st
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup

def validate_email(email):
    # Simple email validation regex
    email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(email_regex, email)

def has_variables(email):
    # Check if the email contains % or +
    return "%" in email or "+" in email

def has_two_characters_before_at(email):
    # Check if there are at least two characters before the "@"
    return email.index("@") >= 3

def contains_keyword(email, keyword):
    # Check if the email contains the given keyword
    return keyword.lower() in email.lower()

def extract_emails_from_html(html_content):
    # Extract emails from the HTML content using regex
    email_regex = r"[a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_regex, html_content)

    return emails

def save_to_csv(emails):
    csv_data = "Email\n" + "\n".join(emails)
    csv_bytes = csv_data.encode()

    # Set the option to automatically download the CSV file
    st.set_option('deprecation.showfileUploaderEncoding', False)

    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="valid_emails.csv",
        mime="text/csv",
    )

def fetch_google_search_results(search_query):
    # Fetch the search results HTML content from Google
    url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    return response.text

def main():
    st.title("Email Extractor App")

    # Choose the social media platform
    social_media = st.selectbox("Choose the social media platform:", ["instagram", "facebook", "twitter", "linkedin"])

    # Input keyword after "CODIGO:"
    keyword = st.text_input("Enter the keyword after CODIGO:", "Academia")

    # Input the number of pages to extract
    num_pages = st.number_input("Enter the number of pages to extract:", min_value=1, step=1, value=1)

    # Generate the search query
    search_query = f"CODIGO: {keyword} (@gmail.com OR @hotmail.com OR @yahoo.com) AND Brazil site:{social_media}.com/"
    unique_emails = set()

    # Extract emails and filter
    for page_idx in range(1, num_pages + 1):
        # Fetch the search results page HTML content
        response_text = fetch_google_search_results(search_query + f"&start={(page_idx - 1) * 10}")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response_text, "html.parser")

        # Extract emails from span tags
        span_tags = soup.find_all("span")
        emails_from_span = [tag.get_text() for tag in span_tags if re.match(r"[a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", tag.get_text())]

        # Combine all extracted emails and remove duplicates
        all_emails = set(emails_from_span)

        # Filter valid emails as before
        valid_emails = {email.lower() for email in all_emails if validate_email(email) and not has_variables(email) and has_two_characters_before_at(email) and not contains_keyword(email, keyword)}

        unique_emails.update(valid_emails)

    # Print the total number of results found
    st.write(f"Total number of email addresses found: {len(unique_emails)}")

    # Save unique emails to CSV file
    save_to_csv(unique_emails)

if __name__ == "__main__":
    main()
