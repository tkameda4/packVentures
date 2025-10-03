'''
Author: Yoshi Kameda
Edited: 10-03-2025

Description: Finds the name of the founders given a list of companies and its url.
'''
import google.generativeai as genai
import requests, json, os
from bs4 import BeautifulSoup

# API key for Gemini AI
API_KEY = "AIzaSyCxsQoudVL365liQpWVXGBzN-66kd-wgNk"
genai.configure(api_key=API_KEY)

# Finds the company name and url from given file
def loadCompanies(file):
    companies = []
    with open(file, "r", encoding="utf-8") as f:
        # parse through each line in the file
        for line in f:
            line = line.strip()
            url = None

            if "http" in line:
                start = line.find("http") # sets "http" as the starting point
                url = line[start:].rstrip(")") # url ends right before ")"
                name = line[:start].strip().rstrip("(").strip()
            else:
                name = line
            companies.append({"name": name, "base_url": url})
        
    # return list of dict containing company name and base url
    return companies

# Fetch html text from a url
def fetch_text(url):
    try:
        # make http request with a timeout
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}) 

         # raise http error if there are any
        response.raise_for_status()

        # parse the html content
        soup = BeautifulSoup(response.text, "html.parser") 

        # remove elements that don't contribute visible text
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        
        # extract visible text, join nodes with spaces, trim extra whitespace
        return soup.get_text(" ", strip=True)
    
    # if url is not accessible
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# for formatting AI output
def parseLine(company_name, line):
    line = line.strip()
    prefix = f"{company_name}:"
    if line.startswith(prefix):
        tail = line[len(prefix):].strip()
    else:
        tail = line
    if tail == "[]":
        return []
    return [n.strip() for n in tail.split(",") if n.strip()]

# Looks for the name of founders given a company url
# If the url does not contain any information about the founders, return []
def getFounders(company):
    model = genai.GenerativeModel("gemini-2.5-flash") # the model we are using

    # Collect text from /about, /founder, /team
    base = company["base_url"].rstrip("/")
    urls = [base + "/about", base + "/founders", base + "/team"]
    combined_text = ""

    for u in urls:
        combined_text += fetch_text(u) + "\n"

    # Send the scraped text into Gemini with the following prompt
    # The prompt allows Gemini to look at the first 6000 characters and see if there are any information about the founders
    prompt = f"""
    From the following website text, extract the names of all the founders or co-founders of {company['name']}.
    Use only the provided text, do not rely on outside knowledge.
    If no founders are mentioned, return exactly:

    {company['name']}: []

    Website text:
    {combined_text[:6000]}

    Format the answer exactly like this:
    ["Name 1","Name 2"]
    """
    
    response = model.generate_content(prompt)

    # change to correct json format
    try:
        data = json.loads((response.text or "").strip())
        return [n.strip() for n in data if isinstance(n, str) and n.strip()]
    except Exception:
        return []

if __name__ == "__main__":
    companies = loadCompanies("companies.txt")
    results = {}
    # for each company, get the founder names
    for c in companies:
        founders = getFounders(c)
        results[c["name"]] = founders

    # print the result
    for company, founders in results.items():
        print(f"{founders}")

    # load results to founders.json
    existing = {}
    if os.path.exists("founders.json"):
        try:
            with open("founders.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
            if not isinstance(existing, dict):
                existing = {}
        except Exception:
            existing = {}

    # merge new results
    existing.update(results)

    # write back (creates the file if it doesn't exist)
    with open("founders.json", "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
