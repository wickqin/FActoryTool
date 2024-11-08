import os
import subprocess

from PyQt5.QtCore import QTimer, pyqtSlot, Qt, QSize
from PyQt5.QtGui import QStandardItem, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QAction, QShortcut, QWidget, QMessageBox, QDialog, \
    QHBoxLayout, QListWidgetItem, QLabel, QSizePolicy, QStyledItemDelegate
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
    INIT_DATA = {}

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_test_index = 0
        self.test_commands = [
            {"name": "Scan SN", "command": "./ScanSN.sh", "result": True, "cont": 0},
            {"name": "SN Check", "command": "./CheckSN.sh", "result": True, "cont": 0},
            {"name": "CPU Check", "command": "./cpu.sh", "result": True, "cont": 0},
            {"name": "DIMM Check", "command": "./DDRchk.sh", "result": True, "cont": 0},
            {"name": "BIOS Check", "command": "./BIOSchk.sh", "result": True, "cont": 0},
            {"name": "Touchpad Test", "command": "./touchpad.sh", "result": True, "cont": 0},
            {"name": "Check EC Test", "command": "cd ./sp41x6g-fw-ver3.0&&./CheckEC.sh", "result": True, "cont": 0},
            {"name": "Check PD_FW Test", "command": "cd ./sp41x6g-fw-ver3.0&&./CheckPD_FW.sh", "result": True,
             "cont": 0},
            {"name": "Check Fan Test", "command": "./CheckFan.sh", "result": True, "cont": 0},
            {"name": "BlueTooth Test", "command": "./BlueTooth.sh", "result": True, "cont": 0},
            {"name": "WIFI Test", "command": "./WIFITest.sh", "result": True, "cont": 0},
            {"name": "Keyboard Test", "command": "cd ./KBTest&&./kb.sh", "result": True, "cont": 0},
            {"name": "Battery Test", "command": "./Battery.sh", "result": True, "cont": 0},
            {"name": "SDCard Test", "command": "./CardTest.sh", "result": True, "cont": 0},
            {"name": "Camera Test", "command": "./CameraTest.sh", "result": True, "cont": 0},
            {"name": "HDMI Test", "command": "./color.py", "result": True, "cont": 0},
            {"name": "WIFI Test", "command": "./wifitest.sh", "result": True, "cont": 0}
        ]

        self.init_info(MainWindow.FILE_NAME)

        self.top = SettingWindow(MainWindow.INIT_DATA, MainWindow.FILE_NAME)

        self.ui.reset_test_button.clicked.connect(self.run_selected_test)
        self.ui.start_test_button.clicked.connect(self.start_all_tests)
        self.bind('F10', self.on_setting)
        self.update_ui()
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
            self.top = SettingWindow(MainWindow.INIT_DATA, MainWindow.FILE_NAME)
        self.show_or_hide_window(self.top)

    def show_or_hide_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.setWindowModality(Qt.WindowModal)
            self.init_info(MainWindow.FILE_NAME)
            window.update_settings(MainWindow.INIT_DATA)
            window.show()

    def init_info(self, file_name):
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as file:
                    for line in file:
                        key_value = line.strip().split(':')
                        if len(key_value) == 2:
                            key, value = map(str.strip, key_value)
                            MainWindow.INIT_DATA[key] = value
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            MainWindow.INIT_DATA = MainWindow.INIT_DATA_TEMPLATE.copy()
            self.save_info_to_file(file_name)

    def save_info_to_file(self, file_name):
        try:
            with open(file_name, 'w') as file:
                for key, value in MainWindow.INIT_DATA.items():
                    file.write(f"{key}:{value}\n")
        except Exception as e:
            print(f"Error saving file: {e}")

    def update_ui(self):
        self.ui.psLabel.setText(f'工号：{MainWindow.INIT_DATA.get("Personal ID", "")}')
        self.ui.lineLabel.setText(f'线别：{MainWindow.INIT_DATA.get("Line", "")}')
        self.ui.fxLabel.setText(f'站位：{MainWindow.INIT_DATA.get("Fixture ID", "")}')
        self.ui.pnLabel.setText(f'料号：{MainWindow.INIT_DATA.get("PN", "")}')

    def update_listview_item(self, test_name, passed):
        for index in range(self.ui.test_listView.count()):
            item = self.ui.test_listView.item(index)
            if item.text() == test_name:
                if passed:
                    item.setBackground(QtGui.QColor("green"))
                else:
                    item.setBackground(QtGui.QColor("red"))
                break

    def item_wight(self, item):
        name = item['name']
        command = item['command']
        cont = str(item['cont'])
        result = 'Pass' if item['result'] else 'Fail'

        parent_item = QStandardItem()
        parent_item.setSizeHint(QSize(400, 30))

        name_item = QStandardItem()
        name_item.setTextAlignment(Qt.AlignCenter)
        name_item.setText(name)
        name_item.setBackground(Qt.GlobalColor.black)
        command_item = QStandardItem()
        command_item.setTextAlignment(Qt.AlignCenter)
        command_item.setText(command)
        cont_item = QStandardItem()
        cont_item.setTextAlignment(Qt.AlignCenter)
        cont_item.setText(cont)
        result_item = QStandardItem()
        result_item.setTextAlignment(Qt.AlignCenter)
        result_item.setText(result)

        parent_item.appendRow(name_item)
        parent_item.appendRow(command_item)
        parent_item.appendRow(cont_item)
        parent_item.appendRow(result_item)

        return parent_item

    def update_test_list(self):
        model = QtGui.QStandardItemModel()
        for test in self.test_commands:
            item = self.item_wight(test)
            item.setEditable(False)
            item.setFont(QFont("Arial", 10))
            model.appendRow(item)
        self.ui.test_listView.setSpacing(2)

        self.ui.test_listView.setStyleSheet("""
            QListView::item {
                border: 1px solid lightgray;
                padding: 2px;
            }
            QListView::item:selected {
                background-color: lightblue;
            }
        """)

        self.ui.test_listView.setModel(model)

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
        sn = self.ui.snEdit.text().strip().upper()
        if sn != "" and len(sn) == 15:
            self.ui.snEdit.setDisabled(True)
            self.ui.test_progressBar.setValue(0)
            self.current_test_index = 0
            self.timer.timeout.connect(self.run_next_test)
            self.timer.start(100)
        else:
            alert("Warning", "请检查SN输入")

    @pyqtSlot()
    def run_next_test(self):
        if self.current_test_index < len(self.test_commands):
            test = self.test_commands[self.current_test_index]
            self.run_test(test)
            self.current_test_index += 1
            progress = (self.current_test_index / len(self.test_commands)) * 100
            self.ui.test_progressBar.setValue(progress)
        else:
            self.timer.stop()

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
        self.update_ui()

    def update_settings(self, new_data):
        self.initData = new_data
        self.update_ui()

    def update_ui(self):
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
                MainWindow.INIT_DATA = self.initData
                mainWindow.update_ui()
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
