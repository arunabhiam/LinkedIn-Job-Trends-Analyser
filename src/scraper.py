import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import os
from time import sleep

# Headers to rotate
headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
]

os.makedirs("../data", exist_ok=True)


def scrape_job_details(job_url):
    """Fetch job type and salary info from individual job pages."""
    try:
        response = requests.get(job_url, headers=random.choice(headers_list), timeout=5)
        if response.status_code != 200:
            return None, None

        soup = BeautifulSoup(response.text, 'html.parser')
        job_type, salary = None, None

        details_section = soup.find_all('li', class_='description__job-criteria-item')
        for li in details_section:
            label = li.find('h3')
            value = li.find('span')
            if label and value:
                label_text = label.text.strip().lower()
                value_text = value.text.strip()
                if 'employment type' in label_text:
                    job_type = value_text
                elif 'salary' in label_text or 'compensation' in label_text:
                    salary = value_text

        return job_type or 'Not specified', salary or 'Not disclosed'

    except Exception:
        return None, None


def scrape_jobs(keyword, location, pages=20):
    jobs = []
    for page in range(pages):
        start = page * 25
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&start={start}"

        try:
            response = requests.get(url, headers=random.choice(headers_list), timeout=5)
            if response.status_code != 200:
                print(f"⚠️ Page {page+1} skipped (status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            postings = soup.find_all('li')

            for post in postings:
                title = post.find('h3')
                company = post.find('h4')
                place = post.find('span', class_='job-search-card__location')
                link = post.find('a', class_='base-card__full-link')

                if not (title and company and place and link):
                    continue

                job_link = link['href']
                job_type, salary = scrape_job_details(job_link)

                jobs.append({
                    'Title': title.text.strip(),
                    'Company': company.text.strip(),
                    'Location': place.text.strip(),
                    'Link': job_link,
                    'Job Type': job_type,
                    'Salary/Stipend': salary,
                    'Keyword': keyword
                })

            print(f"✅ {keyword} | Page {page+1} done | Total jobs: {len(jobs)}")
            sleep(random.uniform(0.3, 1.0))  # avoid detection

        except Exception as e:
            print(f"❌ Error on page {page+1}: {e}")
            continue

    return jobs


if __name__ == "__main__":
    keywords = [
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Data Analyst",
        "Deep Learning Engineer"
    ]

    all_jobs = []
    for kw in keywords:
        print(f"\n🚀 Scraping keyword: {kw}")
        all_jobs.extend(scrape_jobs(kw, "India", pages=20))  # 40 pages per keyword

    df = pd.DataFrame(all_jobs)
    df.drop_duplicates(subset=["Link"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv("../data/raw_jobs.csv", index=False)
    print(f"\n🎯 Done! Scraped {len(df)} job listings → ../data/raw_jobs.csv")
