from bs4 import BeautifulSoup
import requests
import re

def scrape_course(course_prefix, course_number):
    course_info = {}
    url = f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in=202340&subj_code_in={course_prefix}&crse_numb_in={course_number}"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # On a valid course, the information will always be contained in the first ntdefault class
    td_element = soup.find("td", class_="ntdefault")

    # Based on the pattern of UA's website, if no course is found then this will be the first "ntdefault" class found
    if "Return to Previous" in td_element.text:
        return None

    # Finds the course description, credit hours, and levels based off of the pattern of UA's website
    course_info["Description"] = td_element.find("br").previous_element.strip()
    course_info["Credit Hours"] = td_element.find("br").next_element.strip().replace("Credit hours", "")
    course_info["Levels"] = td_element.find("span", class_="fieldlabeltext", text="Levels: ").next_sibling.strip()

    # Navigates through UA's website and strips away all the <a> tags from the schedule types (if they have one)
    schedule_types = td_element.find("span", class_="fieldlabeltext", text="Schedule Types: ")
    schedule_types_result = ''
    for sibling in schedule_types.next_siblings:
        if sibling.name == "br":
            break
        schedule_types_result += sibling.get_text()
    course_info["Schedule Types"] = schedule_types_result.strip()

    # Get's the raw text for prerequisites from UA's website
    prerequisites = td_element.find("span", class_="fieldlabeltext", text="Prerequisites: ")
    if prerequisites is None:
        course_info["Prerequisites"] = None
    else:
        prerequisites_result = ''
        for sibling in prerequisites.next_sibling.next_sibling.next_siblings:
            if sibling.name == "br":
                break
            prerequisites_result += sibling.get_text()

        # Uses regular expression to remove additional information that will not be included
        pattern = r'(?:(?:Undergraduate|Graduate)\s?level\s\s?)|\(Concurrent Enrollment Allowed\)\s*|\b\s?Minimum Grade of [A-F][\+-]?'
        prerequisites_result = re.sub(pattern, '', prerequisites_result)
        prerequisites_result = re.sub(r'\s{2,}', ' ', prerequisites_result)
        
        course_info["Prerequisites"] = prerequisites_result.strip()

    return course_info