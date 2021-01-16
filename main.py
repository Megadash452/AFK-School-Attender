from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import datetime
import time
import json
import os


def log(*args, end="\n"):
    print(f"@[{datetime.datetime.now().strftime('%H:%M:%S')}] ", args, end=end)


class Student:
    def __init__(self, name, id, password, schedule, counselor, email=''):
        self.name = name
        self.first_name = self.name.split(' ', 1)[0]
        self.last_name = self.name.split(' ', 1)[1]

        self.id = id
        self.password = password
        self.schedule = schedule
        self.counselor = counselor

        if not email or email == "auto":
            self.email = self.first_name[0].lower() + self.last_name.lower() + str(self.id)[-4:] + "@clintonhs.net"
        else:
            self.email = email

        self.app_urls = {
            "email": "https://mail.google.com/mail/u/0/#inbox",
            "classroom": "https://classroom.google.com/u/0/h",
        }


class web_bot:
    """If Anything fails, increase the sleep time"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # self.browser = webdriver.Chrome("chromedriver.exe")

        with open("student.json", 'r') as f:
            student = json.load(f)
            self.student = Student(
                student["name"],
                student["id"],
                student["password"],
                student["schedule"],
                student["counselor"]
            )

    def google_logIn(self):
        self.browser.get("https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "identifierId")
                )
            ).send_keys(self.student.email)

            self.browser.find_element_by_id("identifierNext")\
                .find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb")\
                .find_element_by_class_name("VfPpkd-LgbsSe")\
                .send_keys(Keys.RETURN)
        except:
            self.browser.quit()

        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "password")
                )
            ).find_element_by_name("password")\
             .send_keys(self.student.password)

            self.browser.find_element_by_id("passwordNext")\
                        .find_element_by_class_name("AjY5Oe")\
                        .send_keys(Keys.RETURN)
        except:
            self.browser.quit()

        log(f"Successfully logged in to Google account <{self.student.email}>")
        time.sleep(1)

    def submit_school_attendance(self):
        self.browser.get("https://docs.google.com/forms/d/e/1FAIpQLSeob9jBxe46TJk8QR9qpzdHz_DBBY_AL7wzlLxCbDw7CDO9BA/viewform?gxids=7628")

        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
                )
            )[0].send_keys(bot.student.first_name)

            self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[1] \
                .send_keys(bot.student.last_name)

            self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[2] \
                .send_keys(str(bot.student.id))
        except:
            self.browser.quit()

        try:
            choices = self.browser.find_elements_by_class_name("freebirdFormviewerViewNumberedItemContainer")[3]\
                                  .find_elements_by_class_name("freebirdFormviewerComponentsQuestionRadioChoice")
            i = 0
            while True:
                if self.student.counselor.lower() in choices[i].text.lower() and\
                   not (self.student.counselor.lower() in "Ms."):
                    choices[i].click()
                    break
                i += 1
        except:
            log("Error: Counselor not found in Attendance Form.\nProceeding without Attendance")
            return

        # self.browser.find_element_by_class_name("freebirdFormviewerViewNavigationSubmitButton").send_keys(Keys.RETURN)

        log("Submitted School Attendance")

    def go_to_class(self, class_number):
        self.browser.get(self.student.schedule[class_number]["meet url"])

        try:
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable(
                    (By.TAG_NAME, "svg")[0]
                )
            ).click()
            self.browser.find_elements_by_tag_name("svg")[6].click()
            # TODO: Click "Join now" button
        except:
            self.browser.quit()

        log(f"Entered ~~{self.student.schedule[class_number]['name']}~~")
        time.sleep(0.8)


if __name__ == "__main__":
    bot = web_bot()

    bot.google_logIn()
    # bot.submit_school_attendance()
    # bot.go_to_class(0)

    # -for when no mic/cam perms: bot.browser.find_elements_by_class_name("U26fgb")[4].send_keys(Keys.RETURN)

    input("\nPress ENTER to Quit")
    bot.browser.quit()
