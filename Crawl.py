from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import codecs
import sys

pwd = ""
number_of_cycles = 5
list_of_skills = ["django", "python", "sql", "javascript","jquery", "html", "css",
                  "reportlab", "c++", "java", "database", "scala",
                  "linux", " git", "js", "agile", "user interface", "mvc", "oriented",
                  "selenium"]
list_of_locations = ["Waterloo", "Kitchener", "Toronto", "North York", "USA", "Various locations", "CA"]

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")

def handle_text(og_text, x, id, title, location, file=None):
    text = og_text.lower()
    counter = 0
    for skill in list_of_skills:
        if text.find(skill) != -1:
            text = text.replace(skill, "???")
            counter += 1
    # print counter, text
    if counter >= 2:
        file.write(str(x)+ "("+str(counter)+")     "+id + ' '+ title + " "+ location + '\n')
        file.write(og_text.encode('ascii', 'ignore') + '\n\n------------------------------------------'
                                                            +'------------------------------------------\n')



driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder/")
ele = driver.find_element_by_id("userid")
ele.send_keys("j94sun")
ele = driver.find_element_by_id("pwd")
ele.send_keys(pwd)
ele = driver.find_element_by_class_name("PSPUSHBUTTON")
ele.click()

time.sleep(2)
ele = driver.find_element_by_partial_link_text("Job Inquiry")
ele.click()

ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
ele = driver.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN")
ele.click()

window_before = driver.window_handles[0]
time.sleep(12)

ele = driver.find_element_by_id("UW_CO_JOBRES_VW$hviewall$0")
ele.click()
time.sleep(3)

for page in range(0, number_of_cycles):
    file = open(str(page)+".txt", "w")
    print "Page"+ str(page) + " executed"
    for x in range(0, 100):
        try:
            ele = driver.find_element_by_id("UW_CO_JOBRES_VW_UW_CO_JOB_ID$"+str(x))
            id = ele.text
            ele = driver.find_element_by_id("UW_CO_JOBRES_VW_UW_CO_WORK_LOCATN$"+str(x))
            location = ele.text
            ele = driver.find_element_by_id("UW_CO_JOBTITLE_HL$"+str(x))
            title = ele.text

            checkFlag = 0
            for loc in list_of_locations:
                if location.find(loc) != -1:
                    checkFlag = 1

            if title.find("Junior") != -1 or title.find("QA") != -1 or title.find("Quality") != -1:
                checkFlag = 0

            if checkFlag == 1:
                ele.click()

                time.sleep(4)
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)

                time.sleep(2)
                ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                ele = driver.find_element_by_id("UW_CO_JOBDTL_VW_UW_CO_JOB_ID")
                id = ele.text
                ele = driver.find_element_by_id("UW_CO_JOBDTL_VW_UW_CO_WORK_LOCATN")
                location = ele.text
                ele = driver.find_element_by_id("UW_CO_JOBDTL_VW_UW_CO_JOB_TITLE")
                title = ele.text
                ele = driver.find_element_by_id("UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR")
                checkFlag = 0
                for loc in list_of_locations:
                    if location.find(loc) != -1:
                        checkFlag = 1

                if title.find("Junior") != -1 or title.find("QA") != -1 or title.find("Quality") != -1:
                    checkFlag = 0
                if checkFlag == 1:
                    handle_text(ele.text,x,id,title,location,file)

                # print str(len(driver.window_handles))
                length = len(driver.window_handles)
                for w in range(1, length):
                    # print "w=" + str(w)
                    try:
                        driver.switch_to.window(driver.window_handles[w])
                        driver.close()
                    except:
                        pass
                driver.switch_to.window(window_before)
                ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        except:
            e = sys.exc_info()[0]
            msg = "page" + str(page)
            try:
                msg+= " " + id + ": " + str(e)
            except:
                pass
            print msg
            driver.switch_to.window(window_before)
            ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

    file.close()
    try:
        ele = driver.find_element_by_name("UW_CO_JOBRES_VW$hdown$img$0")
        ele.click()
        time.sleep(4)
    except:
        pass

# print driver.current_url
# assert "testing" in driver.title.lower()
# driver.quit()
