import sys


def change_color(text, color):
    if sys.platform == 'win32':
        # 对于Windows系统，使用colorama库
        from colorama import init, Fore, Back, Style
        init()
        if color == 'red':
            return Fore.RED + text + Style.RESET_ALL  # 设置文本为红色，并恢复默认颜色
        elif color == 'green':
            return Fore.GREEN + text + Style.RESET_ALL  # 设置文本为绿色，并恢复默认颜色
        elif color == 'blue':
            return Fore.BLUE + text + Style.RESET_ALL  # 设置文本为蓝色，并恢复默认颜色
        else:
            return text
    else:
        # 对于其他操作系统，直接使用ANSI转义序列
        if color == 'red':
            return '\033[91m' + text + '\033[0m'  # 设置文本为红色，并恢复默认颜色
        elif color == 'green':
            return '\033[92m' + text + '\033[0m'  # 设置文本为绿色，并恢复默认颜色
        elif color == 'blue':
            return '\033[94m' + text + '\033[0m'  # 设置文本为蓝色，并恢复默认颜色
        else:
            return text
