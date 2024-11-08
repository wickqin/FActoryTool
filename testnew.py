import subprocess

def get_ec_version():
    try:
        # 尝试执行命令获取系统信息
        result = subprocess.run(['systeminfo'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if "BIOS 版本" in line:
                return line.split(":")[1].strip()
        return "无法获取 EC 版本信息"
    except subprocess.CalledProcessError as e:
        return f"发生错误: {e}"

# 调用函数并打印结果
ec_version = get_ec_version()
print(f"EC 版本: {ec_version}")