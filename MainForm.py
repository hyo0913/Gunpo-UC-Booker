# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QSettings, QDate, QTime

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from time import sleep

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
configKeyBookDate = "Book_date"
configKeyBookItemCount = "Book_item_count"
configGroupBookItem = "Book_item"
configKeyBookEnabled = "Enabled"
configKeyBookCenter = "Center"
configKeyBookFacility = "Facility"
configKeyBookArea = "Area"
configKeyBookTime = "Time"

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

class MainWidget(QWidget):
    driver: webdriver
    driverOptions: webdriver.ChromeOptions
    bookItemWidgets = []
    currentBookItemWidget: BookItemWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

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

        settings.beginGroup(configGroupBookItems)
        date = settings.value(configKeyBookDate)
        self.ui.calendarWidget.setSelectedDate(date)
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

        settings.beginGroup(configGroupBookItems)
        settings.setValue(configKeyBookDate, self.ui.calendarWidget.selectedDate())
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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_id"]')))
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

        return True

    def enquiryBookTime(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="center"]')))

        Select(self.driver.find_element(By.XPATH, '//*[@id="center"]')).select_by_value('GUNPO03') #"?????????????????????(???????????????)" ??????
        Select(self.driver.find_element(By.XPATH, '//*[@id="part"]')).select_by_value('07') #"??????????????????" ??????

        areaValue = ''
        match self.currentBookItemWidget.area():
            case Area.DaeyamiFutsalStadiumA.value:
                areaValue = '5'
            case Area.DaeyamiFutsalStadiumB.value:
                areaValue = '6'
            case _:
                return -2 #?????? ??????

        Select(self.driver.find_element(By.XPATH, '//*[@id="place"]')).select_by_value(areaValue) #"?????????A??????(?????????) ??????
        self.driver.find_element(By.XPATH, '//*[@id="search"]/fieldset/div/div/div/button').click() #?????? ?????? ??????

        if self.goToMonthPage():
            pass
        else:
            return -1

        dateElementSelector = '#date-' + self.ui.calendarWidget.selectedDate().toString('yyyyMMdd')
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, dateElementSelector)))
        element.click()

        while True:
            QApplication.processEvents()
            dateStateText = self.driver.find_element(By.CSS_SELECTOR, dateElementSelector + ' > span').text
            if (dateStateText == '????????????') or (dateStateText == '??????'):
                return 1
            elif dateStateText == '????????????':
                break
            elif dateStateText == '????????????':
                self.driver.find_element(By.XPATH, '//*[@id="search"]/fieldset/div/div/div/button').click() #?????? ?????? ??????
            else:
                return -1 #??? ??? ?????? ??????

        hour = self.currentBookItemWidget.time().hour()

        timeIndex = getTimeIndex(hour)
        if timeIndex < 0:
            return -3 #?????? ??????

        tableIndex = str(timeIndex + 1)
        feeTextXPath = '//*[@id="contents"]/article/div[1]/div/div[5]/div[2]/div/div/table/tbody/tr[' + tableIndex + ']/td[3]'

        feeText = self.driver.find_element(By.XPATH, feeTextXPath).text
        if (feeText == '????????????') or (feeText == '??????'):
            return 1
        elif feeText == '0': #????????????
            return 0
        else:
            return -1 #??? ??? ?????? ??????

    def applyBookDateTime(self):
        hour = self.currentBookItemWidget.time().hour()

        timeIndex = getTimeIndex(hour)
        checkBoxId = 'checkbox_time_' + str(timeIndex)
        self.driver.find_element(By.ID, checkBoxId).click()

        #recaptcha ??????
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[6]/div[1]/div/div/div/iframe')))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#recaptcha-anchor'))).click()
        WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element_attribute((By.CSS_SELECTOR, '#recaptcha-anchor'), 'aria-checked', 'true')) #????????? ???????????? ?????? ?????????
        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[6]/div[2]').click()

        return True

    def applyBookInfo(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="team_nm"]')))

        self.driver.find_element(By.XPATH, '//*[@id="team_nm"]').send_keys(self.ui.lineEditTeamName.text())
        self.driver.find_element(By.XPATH, '//*[@id="users"]').send_keys(self.ui.spinBoxPlayerCount.value())
        self.driver.find_element(By.XPATH, '//*[@id="mobile_tel"]').send_keys(self.ui.lineEditPhoneNumber.text())
        self.driver.find_element(By.XPATH, '//*[@id="purpose"]').send_keys(self.ui.lineEditPurposeOfUse.text())
        self.driver.find_element(By.CSS_SELECTOR, '#agree_use1').click()

        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="writeForm"]/fieldset/table[3]/tbody/tr/td/div/div/div/div/div/iframe')))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#recaptcha-anchor'))).click()
        WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element_attribute((By.CSS_SELECTOR, '#recaptcha-anchor'), 'aria-checked', 'true'))
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, '#chkrecapt_btn').click()

        resultElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/article/div[1]/div/div[1]')))
        if resultElement.text.endswith('????????????'):
            return True
        else:
            return False

    def onPushButtonExecuteClicked(self):
        self.ui.textEditLog.clear()
        message = '?????? ?????? ' + QTime.currentTime().toString();
        self.appendLogMessage(message)

        if self.initWebDriver():
            self.appendLogMessage("???????????? ??????")
        else:
            self.appendLogMessage("???????????? ?????? ??????")

        if self.login():
            self.appendLogMessage("????????? ??????")
        else:
            self.appendLogMessage("????????? ??????")

        if self.goToBookPage():
            self.appendLogMessage("?????? ??????")
        else:
            self.appendLogMessage("?????? ??????")

        for self.currentBookItemWidget in self.bookItemWidgets:
            message = '?????? ?????? ' + QTime.currentTime().toString();
            self.appendLogMessage(message)

            centerText = self.currentBookItemWidget.centerText()
            facilityText = self.currentBookItemWidget.facilityText()
            areaText = self.currentBookItemWidget.areaText()
            timeText = self.currentBookItemWidget.time().toString()
            message = centerText + ' > ' + facilityText + ' > ' + areaText + ' - ' + timeText
            self.appendLogMessage(message)

            status = self.enquiryBookTime()
            if status == 0:
                self.appendLogMessage("?????? ?????? ?????? ??????")
                if self.applyBookDateTime():
                    if self.applyBookInfo():
                        self.appendLogMessage("?????? ??????")
                    else:
                        self.appendLogMessage("?????? ??????")
                        continue
                else:
                    self.appendLogMessage("?????? ??????")
                    continue
            elif status > 0:
                self.appendLogMessage("?????? ??????")
                continue
            else:
                self.appendLogMessage("?????? ?????? ?????? ??????")
                continue

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
