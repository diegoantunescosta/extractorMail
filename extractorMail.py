import re
import time
import pandas as pd
import streamlit as st
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver

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

    # Set up the Selenium web driver (you need to download the appropriate driver for your browser)
    driver = webdriver.Chrome()

    # Extract emails and filter
    for page_idx in range(1, num_pages + 1):
        url = f"https://www.google.com/search?q={search_query}&start={(page_idx - 1) * 10}"
        driver.get(url)

        # Wait for the page to load (adjust the sleep time as needed)
        time.sleep(5)

        # Get the page source after scrolling to the bottom to load all content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        page_source = driver.page_source

        # Extract emails using regex from the search result HTML content
        emails_from_html = extract_emails_from_html(page_source)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract emails from the title, description, and meta tags
        title_emails = extract_emails_from_html(soup.title.text)

        # Check if the meta tags exist before accessing their attributes
        meta_tag_description = soup.find("meta", {"name": "description"})
        description_emails = extract_emails_from_html(meta_tag_description.get("content", "")) if meta_tag_description else []

        meta_tag_keywords = soup.find("meta", {"name": "keywords"})
        meta_emails = extract_emails_from_html(meta_tag_keywords.get("content", "")) if meta_tag_keywords else []

        # Combine all extracted emails and remove duplicates
        all_emails = set(emails_from_html + title_emails + description_emails + meta_emails)

        # Filter valid emails as before
        valid_emails = {email.lower() for email in all_emails if validate_email(email) and not has_variables(email) and has_two_characters_before_at(email) and not contains_keyword(email, keyword)}

        unique_emails.update(valid_emails)

    # Close the web driver
    driver.quit()

    # Print the total number of results found
    st.write(f"Total number of email addresses found: {len(unique_emails)}")

    # Save unique emails to CSV file
    save_to_csv(unique_emails)

if __name__ == "__main__":
    main()
