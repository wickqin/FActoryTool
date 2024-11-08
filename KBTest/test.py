import os
import shutil
import time
import tkinter as tk
from tkinter import ttk, DISABLED, NORMAL, font, END


def read_config_file(filename):
    config_file = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                key_value = line.strip().split(':')
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    config_file[key] = value
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    return config_file


def read_and_parse_file(filename):
    config_dict = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                key_value = line.strip().split(':')
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    if not key.endswith('Path'):
                        config_dict[key] = value
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    return config_dict


def read_path(filename):
    config_path = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                key_value = line.strip().split(':')
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    if key.endswith('Path'):
                        config_path[key] = value
    except FileNotFoundError as e:
        print(f"File {filename} not found.{e}")
        return {}
    return config_path


def is_valid_error_code(error_code):
    # 检查Error Code是否以'EFT10'开头
    if error_code.startswith('EFT10'):
        # 检查Error Code的长度是否为7
        if len(error_code) == 7:
            return True
    return False


def is_valid_sn(sn):
    if len(sn) == 15:
        return True
    return False


def remove_all(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.top = None
        self.result_label = None
        self.sn_entry = None
        self.error_code_entry = None
        self.label_font = font.Font(family='Helvetica', size=14)
        self.label_frame = tk.Frame(self)
        self.label_frame.pack()
        self.error_frame = tk.Frame(self)
        self.title("VGA Card Upload By LesliesChen v1.6")
        self.geometry("550x650")
        self.resizable(False, False)

        self.result = tk.StringVar()
        self.filename = 'VGACARDDCN.ini'
        self.config_dict = read_and_parse_file(self.filename)
        self.config_path = read_path(self.filename)
        self.bind('<F10>', self.on_setting)

        if self.config_dict and self.config_path:
            for widget in self.label_frame.winfo_children():
                widget.destroy()
            self.init_ui(self.config_dict)
            self.error_frame.pack(side=tk.TOP, fill=tk.X)
            error_code_label = tk.Label(self.error_frame, text="Error Code:", anchor=tk.W, font=self.label_font)
            error_code_label.pack(side=tk.LEFT, padx=5, pady=10)
            error_code_label.config(width=15)
            self.error_code_entry = tk.Entry(self.error_frame, font=self.label_font)
            self.error_code_entry.pack(side=tk.LEFT, fill=tk.X, pady=10, padx=5)
            self.error_code_entry.config(width=50)
            self.error_code_entry.focus_set()

            sn_frame = tk.Frame(self)
            sn_frame.pack(side=tk.TOP, fill=tk.X)
            sn_label = tk.Label(sn_frame, text="SN:", anchor=tk.W, font=self.label_font)
            sn_label.pack(side=tk.LEFT, padx=5, pady=10)
            sn_label.config(width=15)
            self.sn_entry = tk.Entry(sn_frame, font=self.label_font)
            self.sn_entry.pack(side=tk.LEFT, fill=tk.X, pady=10, padx=5)
            self.sn_entry.config(width=50)
            self.result_label = tk.Label(self, textvariable=self.result, wraplength=550,
                                         font=font.Font(family='Helvetica', size=24))
            self.result_label.configure(width=30, height=10, bg="green")
            self.result_label.pack(side=tk.LEFT, padx=5, pady=5, expand=1)
            self.error_code_entry.bind("<Return>", self.focus_error_entry)
            self.sn_entry.bind("<Return>", self.focus_sn_entry)
        else:
            print(f'No {self.filename} found in the file.')

    def on_setting(self, event=None):
        if not self.top or not self.top.winfo_exists():
            self.top = settingDialog(self)

    def refresh_ui(self, config_dict):
        for widget in self.label_frame.winfo_children():
            widget.destroy()
        self.init_ui(config_dict)

    def init_ui(self, config_dict):
        y_position = 20
        max_label_width = 0
        for key, value in config_dict.items():
            config_frame = tk.Frame(self.label_frame)
            config_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
            text_width = font.Font().measure(f"{value}")
            max_label_width = max(max_label_width, text_width)

            label_key = tk.Label(config_frame, text=f"{key}: ", font=self.label_font, anchor=tk.W,
                                 justify=tk.LEFT)
            label_key.config(width=15)
            label_key.pack(side=tk.LEFT, fill=tk.X, pady=5, padx=5)
            y_position += label_key.winfo_reqheight() + 5

            label_value = tk.Label(config_frame, text=f"{value}", font=self.label_font, anchor=tk.W,
                                   justify=tk.LEFT)
            label_value.config(width=max_label_width // 5)
            label_value.pack(side=tk.LEFT, fill=tk.X, pady=5, padx=5)
            y_position += label_value.winfo_reqheight() + 5

    def focus_error_entry(self, event=None):
        error_code = self.error_code_entry.get()
        if is_valid_error_code(error_code):
            self.sn_entry.focus_set()
            self.result.set('')
            self.result_label.configure(bg='green')
        else:
            self.result.set("请检查Error Code输入是否有误")
            self.result_label.configure(bg='red')

    def focus_sn_entry(self, event=None):
        error_code = self.error_code_entry.get()
        sn = self.sn_entry.get()
        if is_valid_sn(sn) and is_valid_error_code(error_code):
            self.config_dict = read_and_parse_file(self.filename)
            self.config_path = read_path(self.filename)
            asusFileName = self.error_code_match(error_code, sn)
            with open(asusFileName, 'w') as f:
                f.write('')
            self.upload_file(asusFileName, self.config_path.get('Asus Log Path'))
            self.error_code_entry.focus_set()
            self.get_values(error_code, sn)
        else:
            self.result.set("请检查SN输入是否有误")
            self.result_label.configure(bg='red')

    def error_code_match(self, error_code, sn):
        NameStart = f"{self.config_dict.get('Factory')}_{self.config_dict.get('Test station')}_{self.config_dict.get('Model name')}_{self.config_dict.get('Asus PN')}_{sn}_"
        NameEnd = f"{self.config_dict.get('Fixture ID')}_{time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))}"
        match error_code:
            case 'EFT1011':
                asusFileName = f"{NameStart}FAIL_HANG_{NameEnd}.log"
            case 'EFT1012':
                asusFileName = f"{NameStart}FAIL_BROKEN DISPLAY_{NameEnd}.log"
            case 'EFT1013':
                asusFileName = f"{NameStart}FAIL_NO DISPLAY_{NameEnd}.log"
            case 'EFT1014':
                asusFileName = f"{NameStart}FAIL_NO POWER_{NameEnd}.log"
            case 'EFT1015':
                asusFileName = f"{NameStart}FAIL_LED&FAN_NG_{NameEnd}.log"
            case 'EFT1016':
                asusFileName = f"{NameStart}FAIL_OTHER DEFICIENT_{NameEnd}.log"
            case _:
                asusFileName = f"{NameStart}FAIL_{error_code}_{NameEnd}.log"
        return asusFileName

    def get_values(self, error_code, sn):
        if is_valid_error_code(error_code) and is_valid_sn(sn):
            with open(f"{sn}.dat", 'w') as f:
                for index, (name, item) in enumerate(self.config_dict.items()):
                    if index < 4:
                        f.write(f"{name}:{item}\n")
                f.write(f"Error Code:{error_code}\n")
                f.write(f"SN:{sn}\n")
                f.write(f"TIME:{time.strftime('%Y-%m-%d %X', time.localtime(time.time()))}\n")
            if os.path.exists(f"{sn}.dat"):
                self.result.set("正在上传")
                os.chmod(os.path.abspath(f"{sn}.dat"), 0o644)
                self.upload_files_sfis(f"{sn}.dat", self.config_path.get('ECS SFIS ReadPath'),
                                       self.config_path.get('ECS SFIS ReturnPath'))
        else:
            self.result.set("请检查Error Code或SN输入是否有误")
            self.result_label.configure(bg='red')

    def upload_file(self, filename, target_path):
        try:
            dat_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.log') and filename in f]
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            # 复制文件
            for file in dat_files:
                source_file = os.path.join(os.getcwd(), file)
                target_file = os.path.join(target_path, file)
                shutil.copy(source_file, target_file)
            if os.path.exists(filename):
                os.remove(filename)
        except FileNotFoundError:
            self.result.set(f'无法连接SFIS网络,ASUS LOG上传Fail!')
            self.result_label.configure(bg="red")

    def upload_files_sfis(self, filename, target_path, result_path):
        try:
            dat_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.dat') and self.sn_entry.get() in f]
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            # 复制文件
            for file in dat_files:
                source_file1 = os.path.join(os.getcwd(), file)
                target_file1 = os.path.join(target_path, file)
                shutil.copyfile(source_file1, target_file1, follow_symlinks=False)
                shutil.copy(source_file1, os.path.join(self.config_path.get('ECS Log SFIS Path'), file),
                            follow_symlinks=False)
                if os.path.exists(file):
                    os.remove(file)
            self.result.set(str("检查返回值"))
            time.sleep(6)
            if os.path.exists(f'{result_path}/{filename}'):
                self.check_result(filename, result_path)
            else:
                self.result.set(f'未检测到SFIS返回值,SFIS上传Fail!')
                self.result_label.configure(bg="red")
        except FileNotFoundError:
            self.result.set(f'无法连接SFIS网络,ECS LOG上传Fail!')
            self.result_label.configure(bg="red")

    def check_result(self, filename, result_path):
        try:
            with open(f'{result_path}/{filename}', 'r') as f:
                line = f.readline()
                if len(line) != 0:
                    self.result_label.configure(bg="green")
                    self.reset_values()
                    self.result.set(line)
                else:
                    self.result.set('未检测到SFIS返回值,SFIS上传Fail!')
                    self.result_label.configure(bg="red")
        except FileNotFoundError as e:
            print(f'文件{filename}未找到，e:{e}')

    def reset_values(self):
        self.error_code_entry.delete(0, END)
        self.sn_entry.delete(0, END)


class settingDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.config_file = {}
        self.title('设置')
        self.geometry('650x420')
        self.resizable(False, False)
        self.config_file = read_config_file('VGACARDDCN.ini')
        label_font = font.Font(family='Helvetica', size=12)
        self.entries = {}
        y_position = 0
        for key, value in self.config_file.items():
            tk.Label(self, text=f"{key}:", anchor='w', padx=5, pady=5, font=label_font).grid(row=y_position, column=0,
                                                                                             sticky='w')
            if key == 'Test station':
                entry = ttk.Combobox(self, values=('NLDF1', 'ALBigdataDF1'), width=47, font=label_font)
                entry.current(0)
            elif key == 'Terminal Name':
                entry = ttk.Combobox(self, values=('F4Test01', 'F1Test01'), width=47, font=label_font)
                entry.current(0)
            else:
                state = DISABLED if key in ['Fixture ID', 'Factory'] else tk.NORMAL
                entry = tk.Entry(self, width=50, state=NORMAL, font=label_font)
                entry.insert(0, value)
                entry['state'] = state

            entry.grid(row=y_position, column=1)
            self.entries[key] = entry
            y_position += 1

        tk.Button(self, text="保存", command=self.save_settings).grid(row=y_position, column=0, columnspan=2, pady=10)

    def save_settings(self):
        for key, entry in self.entries.items():
            self.config_file[key] = entry.get()
        with open('VGACARDDCN.ini', 'w') as file:
            for key, value in self.config_file.items():
                file.write(f"{key}: {value}\n")
        updated_config_dict = read_and_parse_file('VGACARDDCN.ini')
        self.master.refresh_ui(updated_config_dict)
        self.destroy()


if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()
