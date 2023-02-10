# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QSettings, QDate, QTime, QElapsedTimer

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from ui_MainForm import Ui_MainWidget
from BookItemForm import BookItemWidget
from BookItemForm import Area

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

configFile = "Config.ini"
configGroupUserInfo = "User_Info"
configKeyUserId = "User_id"
configKeyUserPassword = "User_password"
configGroupBookApplicationForm = "Book_Application_Form"
configKeyTeamName = "Team_name"
configKeyPlayerCount = "Player_count"
configKeyPhoneNumber = "Phone_number"
configKeyPurposeOfUse = "Purpose_of_use"
configGroupBookItems = "Book_items"
configKeyBookItemCount = "Book_item_count"
configGroupBookItem = "Book_item"
configKeyBookEnabled = "Enabled"
configKeyBookCenter = "Center"
configKeyBookFacility = "Facility"
configKeyBookArea = "Area"
configKeyBookTime = "Time"
#
configGroupAppSettings = "App_Settings"
configKeyWaitRecaptcha = "Wait_recaptcha"
configKeyWaitRecaptchaTimeout = "Wait_recaptcha_timeout"

def getTimeIndex(hour):
    match hour:
        case 8:
            return 0
        case 10:
            return 1
        case 12:
            return 2
        case 14:
            return 3
        case 16:
            return 4
        case 18:
            return 5
        case 20:
            return 6
        case _:
            return -1

def waitWebElement(driver, timeout, locator):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except:
        return False

def waitWebElementClickable(driver, timeout, locator):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        return True
    except:
        return False

def waitWebElementAttributeText(driver, timeout, locator, attribute, text):
    timer = QElapsedTimer()

    timer.start()
    while not timer.hasExpired(timeout):
        QApplication.processEvents()

        try:
            if WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element_attribute(locator, attribute, text)):
                return True
        except:
            return False

def processEventSleep(msec):
    timer = QElapsedTimer()

    timer.start()
    while not timer.hasExpired(msec):
        QApplication.processEvents()

class MainWidget(QWidget):
    driver: webdriver
    driverOptions: webdriver.ChromeOptions
    bookItemWidgets = []
    currentBookItemWidget: BookItemWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        date = QDate.currentDate()
        date.setDate(date.year(), ((date.month() + 1) % 12), date.day())
        self.ui.calendarWidget.setSelectedDate(date)

        self.ui.pushButtonExecute.clicked.connect(self.onPushButtonExecuteClicked)
        self.ui.pushButtonSave.clicked.connect(self.saveConfig)
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.toolButtonAddBook.clicked.connect(self.onToolButtonAddBookClicked)
        self.ui.toolButtonRemoveBook.clicked.connect(self.onToolButtonRemoveBookClicked)

    def appendLogMessage(self, message):
        self.ui.textEditLog.append(message)
        QApplication.processEvents()

    def loadConfig(self):
        settings = QSettings(configFile, QSettings.IniFormat)

        settings.beginGroup(configGroupUserInfo)
        self.ui.lineEditUserId.setText(settings.value(configKeyUserId))
        self.ui.lineEditUserPassword.setText(settings.value(configKeyUserPassword))
        settings.endGroup() #configGroupUserInfo

        settings.beginGroup(configGroupBookApplicationForm)
        self.ui.lineEditTeamName.setText(settings.value(configKeyTeamName))
        self.ui.spinBoxPlayerCount.setValue(int(settings.value(configKeyPlayerCount, 0, int)))
        self.ui.lineEditPhoneNumber.setText(settings.value(configKeyPhoneNumber))
        self.ui.lineEditPurposeOfUse.setText(settings.value(configKeyPurposeOfUse))
        settings.endGroup() #configGroupBookApplicationForm

        settings.beginGroup(configGroupAppSettings)
        self.ui.checkBoxWaitRecaptcha.setChecked(bool(settings.value(configKeyWaitRecaptcha, False, bool)))
        self.ui.spinBoxWaitRecaptchaTimeout.setValue(int(settings.value(configKeyWaitRecaptchaTimeout, 60, int)))
        settings.endGroup() # configGroupAppSettings

        settings.beginGroup(configGroupBookItems)
        itemCount = int(settings.value(configKeyBookItemCount, 0, int))
        itemIndex = 0
        while itemIndex < itemCount:
            key = configGroupBookItem + '_' + str(itemIndex)
            itemIndex = itemIndex + 1
            settings.beginGroup(key)
            bookItemWidget = BookItemWidget(self)
            self.ui.verticalLayoutBookItems.addWidget(bookItemWidget)
            self.bookItemWidgets.append(bookItemWidget)

            bookItemWidget.setEnabled(settings.value(configKeyBookEnabled, True, bool))
            bookItemWidget.setCenter(int(settings.value(configKeyBookCenter)))
            bookItemWidget.setFacility(int(settings.value(configKeyBookFacility)))
            bookItemWidget.setArea(int(settings.value(configKeyBookArea)))
            bookItemWidget.setTime(settings.value(configKeyBookTime))
            settings.endGroup() #key
        settings.endGroup() #configGroupBookItems

    def saveConfig(self):
        settings = QSettings(configFile, QSettings.IniFormat)
        settings.clear()

        settings.beginGroup(configGroupUserInfo)
        settings.setValue(configKeyUserId, self.ui.lineEditUserId.text())
        settings.setValue(configKeyUserPassword, self.ui.lineEditUserPassword.text())
        settings.endGroup() #configGroupUserInfo

        settings.beginGroup(configGroupBookApplicationForm)
        settings.setValue(configKeyTeamName, self.ui.lineEditTeamName.text())
        settings.setValue(configKeyPlayerCount, self.ui.spinBoxPlayerCount.value())
        settings.setValue(configKeyPhoneNumber, self.ui.lineEditPhoneNumber.text())
        settings.setValue(configKeyPurposeOfUse, self.ui.lineEditPurposeOfUse.text())
        settings.endGroup() #configGroupBookApplicationForm

        settings.beginGroup(configGroupAppSettings)
        settings.setValue(configKeyWaitRecaptcha, self.ui.checkBoxWaitRecaptcha.isChecked())
        settings.setValue(configKeyWaitRecaptchaTimeout, self.ui.spinBoxWaitRecaptchaTimeout.value())
        settings.endGroup() # configGroupAppSettings

        settings.beginGroup(configGroupBookItems)
        settings.setValue(configKeyBookItemCount, len(self.bookItemWidgets))
        itemIndex = 0
        for bookItemWidget in self.bookItemWidgets:
            key = configGroupBookItem + '_' + str(itemIndex)
            itemIndex = itemIndex + 1
            settings.beginGroup(key)
            settings.setValue(configKeyBookEnabled, bookItemWidget.isEnabled())
            settings.setValue(configKeyBookCenter, bookItemWidget.center())
            settings.setValue(configKeyBookFacility, bookItemWidget.facility())
            settings.setValue(configKeyBookArea, bookItemWidget.area())
            settings.setValue(configKeyBookTime, bookItemWidget.time())
            settings.endGroup() #key
        settings.endGroup() #configGroupBookItems

        settings.sync()

    def initWebDriver(self):
        self.driverOptions = webdriver.ChromeOptions()
        self.driverOptions.add_experimental_option("detach", True)
        self.driverOptions.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=self.driverOptions)
        self.driver.implicitly_wait(10)
        return True

    def login(self):
        self.driver.get('https://www.gunpouc.or.kr/fmcs/160')
        if waitWebElement(self.driver, 3, (By.XPATH, '//*[@id="user_id"]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="user_id"]').send_keys(self.ui.lineEditUserId.text())
        self.driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(self.ui.lineEditUserPassword.text())
        self.driver.find_element(By.XPATH, '//*[@id="memberLoginForm"]/fieldset/div/p[3]/button').click()
        return True

    def goToBookPage(self):
        self.driver.get('https://www.gunpouc.or.kr/fmcs/157')
        return True

    def goToMonthPage(self):
        while True:
            QApplication.processEvents()
            if waitWebElement(self.driver, 2, (By.CLASS_NAME, 'title_month')) == False: return False
            currYearMonthText = self.driver.find_element(By.CLASS_NAME, 'title_month').text
            if not currYearMonthText:
                return False

            currYearMonth = QDate.fromString(currYearMonthText, 'yyyy.MM')

            currYear = currYearMonth.year()
            currMonth = currYearMonth.month()

            destYearMonth = self.ui.calendarWidget.selectedDate()
            destYear = destYearMonth.year()
            destMonth = destYearMonth.month()

            #print('currYear:' + str(currYear) + ' / currMonth:' + str(currMonth))
            #print('destYear:' + str(destYear) + ' / destMonth:' + str(destMonth))

            if destYear < currYear:
                self.driver.find_element(By.XPATH, '//*[@id="prev_month"]').click()
            elif destYear > currYear:
                self.driver.find_element(By.XPATH, '//*[@id="next_month"]').click()
            else:
                if destMonth < currMonth:
                    self.driver.find_element(By.XPATH, '//*[@id="prev_month"]').click()
                elif destMonth > currMonth:
                    self.driver.find_element(By.XPATH, '//*[@id="next_month"]').click()
                else:
                    break

            processEventSleep(700)

        return True

    def enquiryBookTime(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="center"]')))

        Select(self.driver.find_element(By.XPATH, '//*[@id="center"]')).select_by_visible_text(self.currentBookItemWidget.centerText()) #"소규모체육시설(송죽체육관)" 선택
        self.driver.implicitly_wait(0.5)
        Select(self.driver.find_element(By.XPATH, '//*[@id="part"]')).select_by_visible_text(self.currentBookItemWidget.facilityText()) #"대야미풋살장" 선택
        self.driver.implicitly_wait(0.5)
        Select(self.driver.find_element(By.XPATH, '//*[@id="place"]')).select_by_visible_text(self.currentBookItemWidget.areaText()) #"대야미A구장(전척쪽) 선택

        if self.goToMonthPage() == False:
            return -1

        dateElementSelector = '#date-' + self.ui.calendarWidget.selectedDate().toString('yyyyMMdd')
        dateElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, dateElementSelector)))
        dateElement.click()
        processEventSleep(300)

        while True:
            QApplication.processEvents()
            dateStateText = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, dateElementSelector + ' > span'))).text

            if (dateStateText == '예약완료') or (dateStateText == '마감'):
                return 1
            elif dateStateText == '예약가능':
                break
            elif dateStateText == '예약불가':
                dateElement = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, dateElementSelector)))
                dateElement.click() # 날짜 클릭
                processEventSleep(500)
            else:
                return -1

        hour = self.currentBookItemWidget.time().hour()
        timeIndex = str(getTimeIndex(hour) + 1)
        timeStateText = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[5]/div[2]/div/div/table/tbody/tr[' + timeIndex + ']/td[3]'))).text

        if (timeStateText == '예약완료') or (timeStateText == '마감'):
            return 1
        elif timeStateText == '-':
            return -1
        else:
            return 0

    def applyBookDateTime(self):
        hour = self.currentBookItemWidget.time().hour()
        timeIndex = getTimeIndex(hour)

        checkboxSellector = '#checkbox_time_' + str(timeIndex)
        if waitWebElementClickable(self.driver, 3, (By.CSS_SELECTOR, checkboxSellector)) == False: return False
        self.driver.find_element(By.CSS_SELECTOR, checkboxSellector).click()
        processEventSleep(1000)

        return True

    def passRecaptcha1(self):
        # 로봇이 아닙니다 프레임으로 전환
        if WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[6]/div[1]/div/div/div/iframe'))) == False:
            return False

        # 로봇이 아닙니다 체크 박스 클릭
        if waitWebElementClickable(self.driver, 5, (By.CSS_SELECTOR, '#recaptcha-anchor')) == False: return False
        self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor').click()
        processEventSleep(1000)

        # 로봇이 아닙니다 체크 기다림
        timeout = 5
        if self.ui.checkBoxWaitRecaptcha.isChecked():
            timeout = self.ui.spinBoxWaitRecaptchaTimeout.value()

        if waitWebElementAttributeText(self.driver, timeout, (By.CSS_SELECTOR, '#recaptcha-anchor'), 'aria-checked', 'true'):
            pass
        else:
            self.driver.switch_to.default_content() # 원래 프레임으로 복귀
            return False

        self.driver.switch_to.default_content() # 원래 프레임으로 복귀

        if waitWebElement(self.driver, 1, (By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[6]/div[2]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[6]/div[2]').click()
        processEventSleep(1000)

        return True

    def applyBookInfo(self):
        if waitWebElement(self.driver, 5, (By.XPATH, '//*[@id="team_nm"]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="team_nm"]').send_keys(self.ui.lineEditTeamName.text())
        processEventSleep(500)

        if waitWebElement(self.driver, 1, (By.XPATH, '//*[@id="users"]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="users"]').send_keys(self.ui.spinBoxPlayerCount.value())
        processEventSleep(400)

        if waitWebElement(self.driver, 1, (By.XPATH, '//*[@id="mobile_tel"]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="mobile_tel"]').send_keys(self.ui.lineEditPhoneNumber.text())
        processEventSleep(700)

        if waitWebElement(self.driver, 1, (By.XPATH, '//*[@id="purpose"]')) == False: return False
        self.driver.find_element(By.XPATH, '//*[@id="purpose"]').send_keys(self.ui.lineEditPurposeOfUse.text())
        processEventSleep(400)

        if waitWebElement(self.driver, 1, (By.CSS_SELECTOR, '#agree_use1')) == False: return False
        self.driver.find_element(By.CSS_SELECTOR, '#agree_use1').click()
        processEventSleep(600)

        return True

    def passRecaptcha2(self):
        # 로봇이 아닙니다 프레임으로 전환
        if WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="writeForm"]/fieldset/table[3]/tbody/tr/td/div/div/div/div/div/iframe'))) == False:
            return False

        if waitWebElementClickable(self.driver, 5, (By.CSS_SELECTOR, '#recaptcha-anchor')) == False: return False
        self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor').click()
        processEventSleep(1000)

        # 로봇이 아닙니다 체크 기다림
        timeout = 5
        if self.ui.checkBoxWaitRecaptcha.isChecked():
            timeout = self.ui.spinBoxWaitRecaptchaTimeout.value()

        if waitWebElementAttributeText(self.driver, timeout, (By.CSS_SELECTOR, '#recaptcha-anchor'), 'aria-checked', 'true'):
            pass
        else:
            self.driver.switch_to.default_content() # 원래 프레임으로 복귀
            return False

        self.driver.switch_to.default_content() # 원래 프레임으로 복귀

        return True

    def submitBook(self):
        if waitWebElement(self.driver, 1, (By.CSS_SELECTOR, '#chkrecapt_btn')) == False: return False
        self.driver.find_element(By.CSS_SELECTOR, '#chkrecapt_btn').click()

        if waitWebElement(self.driver, 1, (By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[1]')) == False: return False
        successText = self.driver.find_element(By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[1]').text
        processEventSleep(1000)

        if successText.endswith('신청완료'):
            return True
        else:
            return False

    def onPushButtonExecuteClicked(self):
        self.ui.textEditLog.clear()
        message = '예약 시작 ' + QTime.currentTime().toString();
        self.appendLogMessage(message)

        if self.initWebDriver():
            self.appendLogMessage("브라우저 실행")
        else:
            self.appendLogMessage("브라우저 실행 실패")
            return

        if self.login():
            self.appendLogMessage("로그인")
        else:
            self.appendLogMessage("로그인 실패")
            return

        if self.goToBookPage():
            self.appendLogMessage("조회 페이지 이동")
        else:
            self.appendLogMessage("조회 실패")
            return

        bookNumber = 0

        for self.currentBookItemWidget in self.bookItemWidgets:
            bookNumber = bookNumber + 1

            if self.currentBookItemWidget.isEnabled() == False:
                continue

            self.appendLogMessage(str(bookNumber) + ' --------------------------------------------')
            message = '조회 시작 ' + QTime.currentTime().toString();
            self.appendLogMessage(message)

            centerText = self.currentBookItemWidget.centerText()
            facilityText = self.currentBookItemWidget.facilityText()
            areaText = self.currentBookItemWidget.areaText()
            dateText = self.ui.calendarWidget.selectedDate().toString(Qt.DateFormat.ISODate)
            timeText = self.currentBookItemWidget.time().toString()
            message = centerText + ' > ' + facilityText + ' > ' + areaText + ' - ' + dateText + ' - ' + timeText
            self.appendLogMessage(message)

            status = self.enquiryBookTime()
            if status == 0:
                self.appendLogMessage("예약 시간 확인")
            elif status > 0:
                self.appendLogMessage("예약 불가")
                continue
            else:
                self.appendLogMessage("예약 시간 확인 실패")
                continue

            if self.applyBookDateTime():
                pass
            else:
                self.appendLogMessage("예약 시간 체크 실패")
                continue

            if self.passRecaptcha1():
                pass
            else:
                self.appendLogMessage("로봇이 아닙니다(1) 에서 막히네.. 글렀어..")
                return

            if self.applyBookInfo():
                pass
            else:
                self.appendLogMessage("예약 정보 입력 실패")
                continue

            if self.passRecaptcha2():
                pass
            else:
                self.appendLogMessage("로봇이 아닙니다(2) 에서 막히네.. 글렀어..")
                return

            if self.submitBook():
                self.appendLogMessage("예약 성공")
                break
            else:
                self.appendLogMessage("예약 실패라고?!")

    def onToolButtonAddBookClicked(self):
        bookItemWidget = BookItemWidget(self)
        self.ui.verticalLayoutBookItems.addWidget(bookItemWidget)
        self.bookItemWidgets.append(bookItemWidget)

    def onToolButtonRemoveBookClicked(self):
        bookItem = self.bookItemWidgets.pop()
        bookItem.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    QApplication.setOrganizationName("DevHyo")
    QApplication.setApplicationName("Gunpo UC Booker")

    widget = MainWidget()
    widget.loadConfig()
    widget.show()
    app.exec()
    sys.exit()
