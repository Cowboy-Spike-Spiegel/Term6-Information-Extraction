import os
import window
from extraction import Module


if __name__ == '__main__':
    folder_path = os.getcwd()+'\\data'

    # 初始化提取module
    module = Module()

    # 创建UIApp实例并运行
    window = window.UIApp(folder_path, module)
    window.run()