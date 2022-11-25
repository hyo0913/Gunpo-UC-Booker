# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget

from ui_BookItemForm import Ui_BookItemWidget

from enum import Enum

class Center(Enum):
    #GunpoGukminSportCenter = 0,
    #SiminSportSquare = 1
    SongJukSportCenter = 2
    #BukokSportCenter = 3

class Facility(Enum):
    # 송죽다목적체육관
    #SongJukMultiPurposeGym = 0
    DaeyamiFutsalStadium = 1

class Area(Enum):
    # 대야미 풋살장
    DaeyamiFutsalStadiumA = 0
    DaeyamiFutsalStadiumB = 1

class BookItemWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_BookItemWidget()
        self.ui.setupUi(self)

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
        pass

    def facility(self):
        return Facility.DaeyamiFutsalStadium.value

    def facilityText(self) -> str:
        return self.ui.comboBoxFacility.currentText()

    def setArea(self, area: int):
        match area:
            case Area.DaeyamiFutsalStadiumA.value:
                self.ui.comboBoxArea.setCurrentIndex(0)
            case Area.DaeyamiFutsalStadiumB.value:
                self.ui.comboBoxArea.setCurrentIndex(1)

    def area(self) -> int:
        index = self.ui.comboBoxArea.currentIndex()
        match index:
            case 0:
                return int(Area.DaeyamiFutsalStadiumA.value)
            case 1:
                return int(Area.DaeyamiFutsalStadiumB.value)
            case _:
                return 0

    def areaText(self) -> str:
        return self.ui.comboBoxArea.currentText()

    def setTime(self, time):
        self.ui.timeEditTime.setTime(time)

    def time(self):
        return self.ui.timeEditTime.time()
