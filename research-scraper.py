import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "https://www.khoury.northeastern.edu/people/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Step 1: Get faculty profile links from pages 1 to 55
def get_profile_links():
    profile_links = set()

    for page_num in range(1, 56):  # Loop from page 1 to 55
        page_url = f"{BASE_URL}page/{page_num}/"
        response = requests.get(page_url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed to load page {page_num}, skipping.")
            continue  # Skip if the page doesn't load

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all faculty profile links inside correct divs
        for h3_tag in soup.find_all("h3", class_="standard-card__title"):
            a_tag = h3_tag.find("a", href=True)
            if a_tag:
                link = a_tag["href"]
                if link.startswith("http"):  # If absolute URL, use it directly
                    profile_links.add(link)
                else:  # If relative URL, add the base URL
                    profile_links.add(BASE_URL.rstrip("/") + link)

        print(f"Collected {len(profile_links)} total profile links after page {page_num}.")

    return list(profile_links)

profile_links = get_profile_links()

# Step 2: Visit each profile page and extract details
def extract_info(profile_url):
    profile_response = requests.get(profile_url, headers=HEADERS)
    profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
    
    # Extract name
    name_tag = profile_soup.find("h1", class_="single-people__header-title")
    name = name_tag.text.strip() if name_tag else "No name found"
    
    # Extract email
    email_tag = profile_soup.find("a", href=lambda href: href and "mailto:" in href)
    email = email_tag.text.strip() if email_tag else None
    
    # Extract position
    position_tag = profile_soup.find("p", class_="single-people__aside-roles")
    position = position_tag.text.strip() if position_tag else "NA"
    
    # Extract research interests
    research_interest_button = profile_soup.find("button", class_="accordion-header", text=lambda text: text and "Research interests" in text)
    if research_interest_button:
        content_div = research_interest_button.find_next_sibling("div", class_="accordion-content")
        research_interests = "; ".join(item.strip() for item in content_div.stripped_strings) if content_div else "NA"
        has_research_interests = True if content_div else False
    else:
        research_interests, has_research_interests = "NA", False
    
    # Extract campus (Now Correct!)
    campus = get_campus_location(profile_url)
    
    # Extract personal website
    website = "NA"
    website_section = profile_soup.find("h3", string="Website")
    if website_section:
        website_link = website_section.find_next("a")
        if website_link:
            website = website_link["href"]
    
    # Extract Google Scholar Citations
    google_scholar = "NA"
    scholar_section = profile_soup.find("h3", string="Google Scholar")
    if scholar_section:
        scholar_link = scholar_section.find_next("a")
        if scholar_link:
            google_scholar = scholar_link["href"]

    return name, email, position, has_research_interests, research_interests, campus, website, google_scholar

# Helper Function For Campus Location
def get_campus_location(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href and "/locations/" in href and "khoury.northeastern.edu/locations/" in href:
                location_name = href.split("/locations/")[1].rstrip("/")
                full_location_url = f"https://www.khoury.northeastern.edu/locations/{location_name}/"
                try:
                    location_response = requests.get(full_location_url)
                    location_response.raise_for_status()
                    location_soup = BeautifulSoup(location_response.content, "html.parser")
                    location_title = location_soup.find("h3", string="Campus")
                    if location_title:
                        return location_title.text.strip()
                    else:
                        return location_name.replace("-", " ").title()
                except requests.exceptions.RequestException as e:
                    return location_name.replace("-", " ").title()
        return "NA"  
    except requests.exceptions.RequestException:
        return "NA"

# Step 3: Scrape all profiles
results = []
for link in profile_links:
    name, email, position, has_research_interests, research_interests, campus, website, google_scholar = extract_info(link)
    
    if email:  # Only add if email exists
        results.append((name, email, position, has_research_interests, research_interests, campus, website, google_scholar))
        print(f"Scraped: {name}, {email}, {position}, {has_research_interests}, {research_interests}, {campus}, {website}, {google_scholar}")

# Step 4: Save results to CSV
csv_filename = "khoury_faculty_data.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Position", "Has Research Interests", "Research Interests", "Campus", "Website", "Google Scholar"])
    writer.writerows(results)

print(f"Data saved to {csv_filename}")