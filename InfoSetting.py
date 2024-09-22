import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from setting import Ui_Form


def entryIsEmpty(lineEdit):
    if lineEdit.text().strip() == "":
        return False
    else:
        return True


def alert(msg_type, msg):
    QMessageBox.warning(None, msg_type, msg)


def cancel():
    sys.exit(1)


class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setting_ui = Ui_Form()
        self.setting_ui.setupUi(self)
        self.setTabOrder(self.setting_ui.psEdit, self.setting_ui.lineEdit)
        self.setTabOrder(self.setting_ui.lineEdit, self.setting_ui.fxEdit)
        self.setTabOrder(self.setting_ui.fxEdit, self.setting_ui.pnEdit)
        self.setTabOrder(self.setting_ui.pnEdit, self.setting_ui.okButton)
        self.file_name = "TestInfo.dat"
        self.initData = {}
        self.setting_ui.okButton.clicked.connect(self.saveGeometry)
        self.setting_ui.cancelButton.clicked.connect(self.close)
        self.init_info(self.file_name)

        self.setting_ui.psEdit.setText(self.initData.get("Personal ID", ""))
        self.setting_ui.lineEdit.setText(self.initData.get("Line", ""))
        self.setting_ui.fxEdit.setText(self.initData.get("Fixture ID", ""))
        self.setting_ui.pnEdit.setText(self.initData.get("PN", ""))

    def saveGeometry(self):
        controls_to_check = [
            (self.setting_ui.psEdit, "Personal ID"),
            (self.setting_ui.lineEdit, "Line"),
            (self.setting_ui.fxEdit, "Fixture ID"),
            (self.setting_ui.pnEdit, "PN")
        ]
        for line_edit, key in controls_to_check:
            if entryIsEmpty(line_edit):
                value = line_edit.text().strip()
                self.initData[key] = value.upper()
            else:
                alert("Warning", f"请输入{key}")
                line_edit.setFocus()
                return
        try:
            with open(self.file_name, 'w') as f:
                for key, value in self.initData.items():
                    f.write(f"{key}:{value}\n")
            self.close()
        except Exception as e:
            alert("Error", f"文件写入失败: {e}")

    def init_info(self, file_name):
        try:
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    for line in file:
                        key_value = line.strip().split(':')
                        if len(key_value) == 2:
                            key = key_value[0].strip()
                            value = key_value[1].strip()
                            self.initData[key] = value
            else:
                with open(file_name, 'w') as f:
                    self.initData = {
                        "Personal ID": "",
                        "Line": "",
                        "Fixture ID": "",
                        "PN": ""
                    }
                    for key, value in self.initData.items():
                        f.write(f"{key}:{value}\n")
        except Exception as e:
            print(f"Error reading file: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SettingWindow = SettingWindow()
    SettingWindow.show()
    sys.exit(app.exec_())
