from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime
import time
import os


class Student:
    def __init__(self, name, id, password, email='', schedule='', counselor=0):
        self.name = name
        self.first_name = self.name.split(' ', 1)[0]
        self.last_name = self.name.split(' ', 1)[1]

        self.id = id
        self.password = password

        if not email:
            self.email = self.first_name[0].lower() + self.last_name.lower() + str(self.id)[-4:] + "@clintonhs.net"
        else:
            self.email = email

        if not schedule:
            self.schedule = [
                {
                    'name': "AP Physics C: E & M",
                    'teacher': "Mr. Miller",
                    'meet url': "https://meet.google.com/fqh-jthx-ixp"
                }, {
                    'name': "Physical Education",
                    'teacher': "Mr. Reyes",
                    'meet url': "https://meet.google.com/pui-oqsz-tek"
                }, {
                    'name': "AP Government & Politics",
                    'teacher': "Ms. Krazmien",
                    'meet url': "https://meet.google.com/lookup/eepj5nmr6x?authuser=0&hs=179"
                }, {
                    'name': "SUPA Web Design",
                    'teacher': "Mr. Comeaux",
                    'meet url': "http://meet.google.com/cgt-wbrv-mgw"
                }, {
                    'name': "Mural Design",
                    'teacher': "Ms. Alvarado",
                    'meet url': "https://meet.google.com/dqj-zvza-zuk"
                }, {
                    'name': "AP Literature",
                    'teacher': "Ms. Hagan",
                    'meet url': "https://meet.google.com/vap-uijt-mzi"
                }
            ]
        else:
            self.schedule = schedule

        if not counselor:
            self.counselor = 4
        else:
            self.counselor = counselor

        self.app_urls = {
            "email": "https://mail.google.com/mail/u/0/#inbox",
            "classroom": "https://classroom.google.com/u/0/h",
        }


class web_bot:
    """If Anything fails, increase the sleep time"""

    def __init__(self, student_name, student_id, student_password):
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

        # self.browser = webdriver.Chrome("chromedriver.exe")
        self.student = Student(student_name, student_id, password=student_password)

    def google_logIn(self):
        self.browser.get("https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

        self.browser.find_element_by_id("identifierId")\
                    .send_keys(self.student.email)
        self.browser.find_element_by_id("identifierNext")\
                    .find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb")\
                    .find_element_by_class_name("VfPpkd-LgbsSe")\
                    .send_keys(Keys.RETURN)

        time.sleep(1)
        self.browser.find_element_by_id("password")\
                    .find_element_by_name("password")\
                    .send_keys(self.student.password)
        self.browser.find_element_by_id("passwordNext")\
                    .find_element_by_class_name("AjY5Oe")\
                    .send_keys(Keys.RETURN)

        print("Successfully logged in to Google account <" + self.student.email + ">")
        time.sleep(1)

    def submit_school_attendance(self):
        self.browser.get("https://docs.google.com/forms/d/e/1FAIpQLSeob9jBxe46TJk8QR9qpzdHz_DBBY_AL7wzlLxCbDw7CDO9BA/viewform?gxids=7628")
        time.sleep(0.2)

        self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[0]\
                    .send_keys(bot.student.first_name)

        self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[1]\
                    .send_keys(bot.student.last_name)

        self.browser.find_elements_by_class_name("quantumWizTextinputPaperinputInput")[2]\
                    .send_keys(str(bot.student.id))

        self.browser.find_elements_by_class_name("freebirdFormviewerViewNumberedItemContainer")[3]\
                    .find_elements_by_class_name("freebirdFormviewerComponentsQuestionRadioChoice")[
                        bot.student.counselor
                    ].click()

        self.browser.find_element_by_class_name("freebirdFormviewerViewNavigationSubmitButton").send_keys(Keys.RETURN)

        print("Submitted School Attendance")
        time.sleep(0.8)

    def go_to_class(self, class_number):
        self.browser.get(self.student.schedule[class_number]["meet url"])

        print("Entered ~~{}~~".format(self.student.schedule[class_number]["name"]))
        time.sleep(0.8)


if __name__ == "__main__":
    bot = web_bot("Martin Molina", 234142156, input("School Account Password: "))
    bot.google_logIn()

    # bot.submit_school_attendance()
    bot.go_to_class(0)

    # -for when no mic/cam perms: bot.browser.find_elements_by_class_name("U26fgb")[4].send_keys(Keys.RETURN)

    input("Enter to Quit")
    bot.browser.quit()
