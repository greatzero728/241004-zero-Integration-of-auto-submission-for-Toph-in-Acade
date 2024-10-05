import requests
from bs4 import BeautifulSoup

# Function to fetch problem URLs and names
def fetch_problem_links(page_num):
    url = f"https://toph.co/problems/all?start={25 * page_num}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all problem links
    problem_links = soup.find_all('a', href=True)
    problems = []

    # Only keep the links that match the pattern
    for link in problem_links:
        href = link['href']
        if href.startswith('/p/'):
            problem_name = href.split('/p/')[1]
            problems.append(problem_name)

    return problems

# Function to save problem names to a text file
def save_problems_to_file(problems):
    # Removing duplicates and sorting
    unique_problems = sorted(set(problems))

    # Save to problemList.txt in the desired format
    with open('problemList.txt', 'w') as f:
        for problem in unique_problems:
            # Writing the formatted output
            f.write(f"Please transcribe and solve problem <b>{problem}</b> from <b>toph</b>. Problem statement is here: https://toph.co/p/{problem}\n")

if __name__ == "__main__":
    all_problems = []
    page_num = 0
    
    # Loop through pages until no problems are found
    while True:
        print(f"Scraping page {page_num + 1}...")
        problems = fetch_problem_links(page_num)
        
        if not problems:  # Break if no problems are found on the page
            print(f"No problems found on page {page_num + 1}. Stopping.")
            break
        
        all_problems.extend(problems)
        page_num += 1
    
    # Save problems to a file and create C++ files
    save_problems_to_file(all_problems)
    print("Scraping complete. Check problemList.txt.")
