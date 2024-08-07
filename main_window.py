import subprocess

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets
from main_ui import Ui_MainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_test_index = 0
        self.test_commands = [
            {"name": "Scan SN", "command": "./settime.sh", "result": True, "TestCont": 0},
            {"name": "CPU Check", "command": "./cpu.sh"},
            {"name": "DIMM Check", "command": "./DDRchk.sh"},
            {"name": "BIOS Check", "command": "./BIOSchk.sh"},
            {"name": "Touchpad Test", "command": "./touchpad.sh"},
            {"name": "Check EC Test", "command": "cd ./sp41x6g-fw-ver3.0&&./CheckEC.sh"},
            {"name": "Check PD_FW Test", "command": "cd ./sp41x6g-fw-ver3.0&&./CheckPD_FW.sh"},
            {"name": "Check Fan Test", "command": "./CheckFan.sh"},
            {"name": "BlueTooth Test", "command": "./BlueTooth.sh"},
            {"name": "WIFI Test", "command": "./WIFITest.sh"},
            {"name": "Battery Test", "command": "./Battery.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            {"name": "WIFI Test", "command": "./wifitest.sh"},
            # Add more tests here
        ]
        self.timer = QTimer(self)
        self.ui.reset_test_button.clicked.connect(self.run_selected_test)
        self.ui.start_test_button.clicked.connect(self.start_all_tests)
        self.update_test_list()
        

    def update_test_list(self):
        model = QtGui.QStandardItemModel()
        for test in self.test_commands:
            item = QtGui.QStandardItem(test["name"])
            item.setEditable(False)
            model.appendRow(item)
        (self.ui.test_listView.setModel(model))

    def run_selected_test(self):
        selected_indexes = self.ui.test_listView.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0].row()
            test = self.test_commands[selected_index]
            self.run_test(test)

    def run_test(self, test):
        self.log(f"Starting {test['name']}...")
        success = self.run_command(test['command'])
        self.log(f"{test['name']} {'PASSED' if success else 'FAILED'}")

    def log(self, message):
        self.ui.textBrowser.append(message)

    def start_all_tests(self):
        self.ui.test_progressBar.setValue(0)
        self.current_test_index = 0
        self.timer.timeout.connect(self.run_next_test)
        self.timer.start(100)

    @pyqtSlot()
    def run_next_test(self):
        if self.current_test_index < len(self.test_commands):
            test = self.test_commands[self.current_test_index]
            self.run_test(test)
            self.current_test_index += 1
            progress = (self.current_test_index / len(self.test_commands)) * 100
            print(f"progress---------{progress}")
            self.ui.test_progressBar.setValue(progress)
            #QtCore.QTimer.singleShot(100, self.run_next_test)  # Run the next test after 100 ms
        else:
            self.timer.stop()
            # QtWidgets.QMessageBox.information(None, "Test Complete", "All tests are complete.")

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"{command} PASSED")
                return True
            else:
                self.log(f"{command} FAILED\n{result.stderr}")
                return False
        except Exception as e:
            self.log(f"Error running {command}: {e}")
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
