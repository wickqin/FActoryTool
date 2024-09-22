import os
import subprocess

from PyQt5.QtCore import QTimer, pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QAction, QShortcut, QWidget, QMessageBox, QDialog
from PyQt5 import QtGui
from main_ui import Ui_MainWindow
from setting import Ui_Form
import sys


class MainWindow(QMainWindow):
    FILE_NAME = "./TestInfo.dat"
    INIT_DATA_TEMPLATE = {
        "Personal ID": "",
        "Line": "",
        "Fixture ID": "",
        "PN": ""
    }

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initData = {}
        self.current_test_index = 0
        self.test_commands = [
            {"name": "Scan SN", "command": "./ScanSN.sh", "result": True, "TestCont": 0},
            {"name": "SN Check", "command": "./CheckSN.sh"},
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
            {"name": "SDCard Test", "command": "./CardTest.sh"},
            {"name": "Camera Test", "command": "./CameraTest.sh"},
            {"name": "HDMI Test", "command": "./color.py"},
            {"name": "WIFI Test", "command": "./wifitest.sh"}
        ]

        self.init_info(MainWindow.FILE_NAME)

        self.top = SettingWindow(self.initData, MainWindow.FILE_NAME)

        self.ui.reset_test_button.clicked.connect(self.run_selected_test)
        self.ui.start_test_button.clicked.connect(self.start_all_tests)
        self.bind('F10', self.on_setting)

        self.timer = QTimer(self)
        self.update_test_list()

    def bind(self, key, func):
        shortcut = QShortcut(QtGui.QKeySequence(key), self)
        shortcut.activated.connect(func)

    def on_setting(self):
        if not os.path.exists(MainWindow.FILE_NAME):
            print("文件名为空或非法")
            return

        if not hasattr(self, 'top') or self.top is None:
            self.top = SettingWindow(self.initData, MainWindow.FILE_NAME)
        self.show_or_hide_window(self.top)

    def show_or_hide_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.setWindowModality(Qt.WindowModal)
            self.init_info(MainWindow.FILE_NAME)
            window.show()

    def init_info(self, file_name):
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as file:
                    for line in file:
                        key_value = line.strip().split(':')
                        if len(key_value) == 2:
                            key, value = map(str.strip, key_value)
                            self.initData[key] = value
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            self.initData = MainWindow.INIT_DATA_TEMPLATE.copy()
            self.save_info_to_file(file_name)

    def save_info_to_file(self, file_name):
        try:
            with open(file_name, 'w') as file:
                for key, value in self.initData.items():
                    file.write(f"{key}:{value}\n")
        except Exception as e:
            print(f"Error saving file: {e}")

    def update_listview_item(self, test_name, passed):
        for index in range(self.ui.test_listView.count()):
            item = self.ui.test_listView.item(index)
            if item.text() == test_name:
                if passed:
                    item.setBackground(QtGui.QColor("green"))
                else:
                    item.setBackground(QtGui.QColor("red"))
                break

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
        else:
            print(selected_indexes)
            pass

    def run_test(self, test):
        self.log(f"Starting {test['name']}...")
        success = self.run_command(test['command'])
        self.log(f"{test['name']} {'PASSED' if success else 'FAILED'}")
        self.update_listview_item(test['name'], success)

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
            # QtCore.QTimer.singleShot(100, self.run_next_test)  # Run the next test after 100 ms
        else:
            self.timer.stop()
            # QtWidgets.QMessageBox.information(None, "Test Complete", "All tests are complete.")

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                # self.ui.test_listView.itemDelegateForRow()
                self.log(f"{command} PASSED")
                return True
            else:
                self.log(f"{command} FAILED\n{result.stderr}")
                return False
        except Exception as e:
            self.log(f"Error running {command}: {e}")
            return False


def entryIsEmpty(lineEdit):
    if lineEdit.text().strip() == "":
        return False
    else:
        return True


def alert(msg_type, msg):
    QMessageBox.warning(None, msg_type, msg)


def check_input_length(line_edit, key, expected_length):
    value = line_edit.text().strip()
    if len(value) != expected_length:
        alert("Warning", f"请检查{key}输入")
        line_edit.setFocus()
        return False
    return True


class SettingWindow(QDialog):
    def __init__(self, initData, file_name):
        super().__init__()
        self.setting_ui = Ui_Form()
        self.setting_ui.setupUi(self)
        self.initData = initData
        self.file_name = file_name
        self.setting_ui.okButton.clicked.connect(self.saveGeometry)
        self.setting_ui.cancelButton.clicked.connect(self.close)
        self.setting_ui.psEdit.setText(self.initData.get("Personal ID", ""))
        self.setting_ui.lineEdit.setText(self.initData.get("Line", ""))
        self.setting_ui.fxEdit.setText(self.initData.get("Fixture ID", ""))
        self.setting_ui.pnEdit.setText(self.initData.get("PN", ""))

    def saveGeometry(self):
        controls_to_check = [
            (self.setting_ui.psEdit, "Personal ID", 7),
            (self.setting_ui.lineEdit, "Line", 6),
            (self.setting_ui.fxEdit, "Fixture ID", 10),
            (self.setting_ui.pnEdit, "PN", 13)
        ]
        for line_edit, key, length in controls_to_check:
            if entryIsEmpty(line_edit):
                if not check_input_length(line_edit, key, length):
                    return
                self.initData[key] = line_edit.text().strip().upper()
        try:
            with open(self.file_name, 'w') as f:
                for key, value in self.initData.items():
                    f.write(f"{key}:{value}\n")
            self.close()
        except Exception as e:
            alert("Error", f"文件写入失败: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
