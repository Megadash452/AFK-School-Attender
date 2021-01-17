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


errorNote_newLine = "\n                   "


def log(msg, end="\n"):
    print(f"@[{datetime.datetime.now().strftime('%H:%M:%S')}]", msg, end=end)


def error_note(*notes, sep="\n", end="\n"):
    if sep[0] == '\n':
        sep = errorNote_newLine + sep[1:]

    print("  ^^^^^^^^   Note:", end=" ")
    for note in notes:
        for n in note:
            if n is not note[-1]:
                print(n, end=sep)
            else:
                print(n)
    if '\n' not in sep:
        print(end=end)


def warn(warning: str, *msgs):
    log(f"-Error-: {warning}")
    error_note(msgs)


def exit_error(error: str, msg):
    exit(f"@[{datetime.datetime.now().strftime('%H:%M:%S')}] Error: {error}\n  ^^^^^^^^   Note: {msg}")


class Student:
    def __init__(self, name, id, password, schedule, counselor, email):
        self.name = name
        self.first_name = self.name.split(' ', 1)[0]
        try:
            self.last_name = self.name.split(' ', 1)[1]
        except Exception:
            exit_error(
                "No Last Name Provided",
                "Make sure you put your full name in \"student.json\""
            )

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
    def __init__(self):
        """
        Required properties:
            student["name"],
            student["id"],
            student["password"],
            student["schedule"],
            student["counselor"]
        """
        with open("student.json", 'r') as f:
            student = json.load(f)
            self.student = Student(
                student["name"],
                student["id"],
                student["password"],
                student["schedule"],
                student["counselor"],
                student["email"]
            )

        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # self.browser = webdriver.Chrome("chromedriver.exe")

    """If Anything fails, increase the wait time"""

    def google_logIn(self):
        """
        Required Properties:
            student["email"],
            student["password"]
        May require:
            student["name"]
            student["id"]
        """
        self.browser.get("https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        log("Signing in to Google Account...")

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
        except Exception as error:
            self.browser.quit()
            exit_error(
                error,
                "Could not load Google Sign In page{}".format(errorNote_newLine) +
                "Re-run the program."
            )

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
        except Exception as error:
            self.browser.quit()
            exit_error(
                error,
                f"Email Address <{self.student.email}> does not exist{errorNote_newLine}"
                "Make sure you have the right email address in \"student.json\""
            )

        try:
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(
                    (By.ID, "gsr")
                )
            )
        except Exception as error:
            self.browser.quit()
            exit_error(
                error,
                "Your password is incorrect{}".format(errorNote_newLine) +
                "Make sure your password is correct in \"student.json\""
            )

        log(f"Logged in to Google account <{self.student.email}>")

    def submit_school_attendance(self):
        """
        Required properties:
            Google - Logged in,
            student["name"],
            student["id"],
            student["counselor"]
        """
        self.browser.get("https://docs.google.com/forms/d/e/1FAIpQLSeob9jBxe46TJk8QR9qpzdHz_DBBY_AL7wzlLxCbDw7CDO9BA/viewform?gxids=7628")
        log("Completing School Attendance...")

        try:
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
                )
            )
            self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[0]\
                        .send_keys(bot.student.first_name)

            self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[1]\
                        .send_keys(bot.student.last_name)

            self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[2]\
                        .send_keys(str(bot.student.id))
        except Exception as error:
            warn(
                error,
                "Could not load School Attendance page",
                "Proceeding without submitting attendance"
            )
            return

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
        except Exception as warning:
            warn(
                warning,
                "Counselor not found in Attendance Form."
                "Proceeding without Attendance"
            )
            return

        # self.browser.find_element_by_class_name("freebirdFormviewerViewNavigationSubmitButton").send_keys(Keys.RETURN)

        log("Submitted School Attendance")

    def join_Google_Meet(self, class_number):
        self.browser.get(self.student.schedule[class_number]["meet url"])
        log(f"Joining '{self.student.schedule[class_number]['course name']}'...")

        try:
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable(
                    (By.TAG_NAME, "svg")[0]
                )
            ).click()
            self.browser.find_elements_by_tag_name("svg")[6].click()

            # TODO: Click "Join now" button
        except Exception as warning:
            self.browser.get("https://google.com/")
            warn(
                warning,
                "Could not load {} meet link",
                "Make sure the link is correct in \"student.json\""
            )

        log(f"Entered ~~{self.student.schedule[class_number]['course name']}~~.")


if __name__ == "__main__":
    bot = web_bot()

    bot.google_logIn()
    # bot.submit_school_attendance()
    bot.join_Google_Meet(0)

    # -for when no mic/cam perms: bot.browser.find_elements_by_class_name("U26fgb")[4].send_keys(Keys.RETURN)

    input("\nPress ENTER to Quit")
    bot.browser.quit()
    exit(0)
