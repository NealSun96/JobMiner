from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from subprocess import Popen, PIPE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import info

debug_mode = False
class CygwinFirefoxProfile(FirefoxProfile):
	@property
	def path(self):
		path = self.profile_dir
		try:
			proc = Popen(['cygpath','-d',path], stdout=PIPE, stderr=PIPE)
			stdout, stderr = proc.communicate()
			path = stdout.split('\n', 1)[0]
		except OSError:
			print("No cygwin path found")
		return path

def debugg(text):
	if debug_mode:
		print text
	
driver = webdriver.Firefox(CygwinFirefoxProfile())
driver.maximize_window()
driver.get("https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBSRCH.GBL?pslnkid=UW_CO_JOBSRCH_LINK&FolderPath=PORTAL_ROOT_OBJECT.UW_CO_JOBSRCH_LINK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder/")
ele = driver.find_element_by_id("userid")
ele.send_keys(info.userid)
ele = driver.find_element_by_id("pwd")
ele.send_keys(info.pwd)
ele = driver.find_element_by_class_name("PSPUSHBUTTON")
ele.click()

time.sleep(1)
ele = driver.find_element_by_partial_link_text("Job Short List")
ele.click()
ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
ele = driver.find_element_by_class_name("PSGRIDCOUNTER")
number_of_cycles = int(ele.text.split(" ")[-1])

for i in range(0, number_of_cycles):
	time.sleep(1)
	ele = driver.find_element_by_name("UW_CO_STUJOBLST$delete$0$$img$0")
	ele.click()
	driver.switch_to_default_content() 
	ele = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_id("#ALERTOK")))
	ele.click()
	ele = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))


