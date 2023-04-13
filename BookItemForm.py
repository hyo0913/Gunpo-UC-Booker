# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget

from ui_BookItemForm import Ui_BookItemWidget

from enum import Enum

class Center(Enum):
    #GunpoGukminSportCenter = 0
    #SiminSportSquare = 1
    SongJukSportCenter = 2
    #BukokSportCenter = 3

class Facility(Enum):
    # 송죽다목적체육관
    #SongJukMultiPurposeGym = 0
    DaeyamiFutsalStadium = 1
    HanwoomulFutsalStadium = 2

class Area(Enum):
    # 대야미 풋살장
    DaeyamiFutsalStadiumA = 0
    DaeyamiFutsalStadiumB = 1
    HanwoomulFutsalStadium = 2

def centerToString(center):
    match center:
        case Center.SongJukSportCenter.value:
            return '송죽다목적체육관/소규모체육시설'

    return ''

def centerFromString(center):
    match center:
        case '송죽다목적체육관/소규모체육시설':
            return Center.SongJukSportCenter.value

    return 0

def facilityToString(facility):
    match facility:
        case Facility.DaeyamiFutsalStadium.value:
            return '대야미풋살장'
        case Facility.HanwoomulFutsalStadium.value:
            return '한우물풋살장'

    return ''

def facilityFromString(facility):
    match facility:
        case '대야미풋살장':
            return Facility.DaeyamiFutsalStadium.value
        case '한우물풋살장':
            return Facility.HanwoomulFutsalStadium.value

    return 0

def areaToString(area):
    match area:
        case Area.DaeyamiFutsalStadiumA.value:
            return '대야미A구장(전철쪽)'
        case Area.DaeyamiFutsalStadiumB.value:
            return '대야미B구장(차도쪽)'
        case Area.HanwoomulFutsalStadium.value:
            return '한우물풋살장'

    return ''

def areaFromString(area):
    match area:
        case '대야미A구장(전철쪽)':
            return Area.DaeyamiFutsalStadiumA.value
        case '대야미B구장(차도쪽)':
            return Area.DaeyamiFutsalStadiumB.value
        case '한우물풋살장':
            return Area.HanwoomulFutsalStadium.value

    return 0

class BookItemWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_BookItemWidget()
        self.ui.setupUi(self)

        self.ui.comboBoxCenter.clear()
        self.ui.comboBoxFacility.clear()
        self.ui.comboBoxArea.clear()

        self.ui.comboBoxCenter.currentIndexChanged.connect(self.onComboBoxCenterCurrentIndexChanged)
        self.ui.comboBoxFacility.currentIndexChanged.connect(self.onComboBoxFacilityCurrentIndexChanged)

        self.ui.comboBoxCenter.addItem(centerToString(Center.SongJukSportCenter.value))

    def setEnabled(self, enabled: bool):
        self.ui.checkBoxEnable.setChecked(enabled)

    def isEnabled(self) -> bool:
        return self.ui.checkBoxEnable.isChecked()

    def setCenter(self, center: int):
        pass

    def center(self) -> int:
        return Center.SongJukSportCenter.value

    def centerText(self) -> str:
        return self.ui.comboBoxCenter.currentText()

    def setFacility(self, facility: int):
        text = facilityToString(facility)
        index = self.ui.comboBoxFacility.findText(text)
        self.ui.comboBoxFacility.setCurrentIndex(index)
        pass

    def facility(self):
        text = self.ui.comboBoxFacility.currentText()
        return facilityFromString(text)

    def facilityText(self) -> str:
        return self.ui.comboBoxFacility.currentText()

    def setArea(self, area: int):
        text = areaToString(area)
        index = self.ui.comboBoxArea.findText(text)
        self.ui.comboBoxArea.setCurrentIndex(index)

    def area(self) -> int:
        text = self.ui.comboBoxArea.currentText()
        return areaFromString(text)

    def areaText(self) -> str:
        return self.ui.comboBoxArea.currentText()

    def setTime(self, time):
        self.ui.timeEditTime.setTime(time)

    def time(self):
        return self.ui.timeEditTime.time()

    def onComboBoxCenterCurrentIndexChanged(self, index):
        centerText = self.ui.comboBoxCenter.currentText()
        center = centerFromString(centerText)

        self.ui.comboBoxFacility.clear()

        match center:
            case Center.SongJukSportCenter.value:
                self.ui.comboBoxFacility.addItem(facilityToString(Facility.DaeyamiFutsalStadium.value))
                self.ui.comboBoxFacility.addItem(facilityToString(Facility.HanwoomulFutsalStadium.value))

    def onComboBoxFacilityCurrentIndexChanged(self, index):
        facilityText = self.ui.comboBoxFacility.currentText()
        facility = facilityFromString(facilityText)

        self.ui.comboBoxArea.clear()

        match facility:
            case Facility.DaeyamiFutsalStadium.value:
                self.ui.comboBoxArea.addItem(areaToString(Area.DaeyamiFutsalStadiumA.value))
                self.ui.comboBoxArea.addItem(areaToString(Area.DaeyamiFutsalStadiumB.value))
            case Facility.HanwoomulFutsalStadium.value:
                self.ui.comboBoxArea.addItem(areaToString(Area.HanwoomulFutsalStadium.value))
