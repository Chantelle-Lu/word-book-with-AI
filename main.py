import os
from wordbook import WordBook
from user_interface import UserInterface
from youdao_api import YoudaoAPI
from qwen_api import QwenAPI
from dotenv import load_dotenv

load_dotenv()

# 获取环境变量
youdao_app_key = os.getenv('YOUDAO_APP_KEY')
youdao_app_secret = os.getenv('YOUDAO_APP_SECRET')
tongyi_api_key = os.getenv('TONGYI_API_KEY')

class MainApp:
    def __init__(self):
        self.wordbook = WordBook()  # 使用默认的JSON文件路径
        self.youdao_api = YoudaoAPI(os.getenv('YOUDAO_APP_KEY'), os.getenv('YOUDAO_APP_SECRET'))
        self.qwen_api = QwenAPI(os.getenv('TONGYI_API_KEY'))
        self.ui = UserInterface(self)
        self.setup_close_event()

    def run(self):
        # 启动用户界面
        self.ui.run()

    def setup_close_event(self):
        self.ui.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.wordbook.save_words()  # 保存单词本状态
        self.ui.window.destroy()  # 关闭窗口

if __name__ == "__main__":
    app = MainApp()
    app.run()
