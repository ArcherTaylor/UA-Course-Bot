from bs4 import BeautifulSoup
import requests

def scrape_course(course_prefix, course_number):
    course_info = {}
    url = f"https://ssb.ua.edu/pls/PROD/bwckctlg.p_disp_course_detail?cat_term_in=202340&subj_code_in={course_prefix}&crse_numb_in={course_number}"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    td_element = soup.find("td", class_="ntdefault")

    if "Return to Previous" in td_element.text:
        return None

    course_info["Description"] = td_element.find("br").previous_element.strip()
    course_info["Credit Hours"] = td_element.find("br").next_element.strip().replace("Credit hours", "")
    course_info["Levels"] = td_element.find("span", class_="fieldlabeltext", text="Levels: ").next_sibling.strip()
    course_info["Schedule Types"] = td_element.find("span", class_="fieldlabeltext", text="Schedule Types: ").next_sibling.strip()

    print(course_info["Schedule Types"])
    
    return course_info

scrape_course("CS", "407")