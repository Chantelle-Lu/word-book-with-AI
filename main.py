
from wordbook import WordBook, Word
from user_interface import UserInterface
from youdao_api import YoudaoAPI
from qwen_api import QwenAPI
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

YOUDAO_APP_KEY = '7a46ca68f52ee337'
YOUDAO_APP_SECRET = '0kSGGZYEbxUXi9q4gGvCNZcZZTSMnyVX'
TONGYI_API_KEY = 'sk-3b736ed70cc74c90b1aec671161ea43f'

class MainApp:
    """程序的主控制类，处理用户输入和导航。"""
    
    def __init__(self):
        self.wordbook = WordBook()  # 使用默认的JSON文件路径
        self.youdao_api = YoudaoAPI(YOUDAO_APP_KEY, YOUDAO_APP_SECRET)
        self.qwen_api = QwenAPI(TONGYI_API_KEY)
        # 传递自身到UserInterface，以便在UI中调用MainApp的方法
        self.ui = UserInterface(self)

    def query_word(self):
        word = self.ui.prompt_for_word()
        definition = self.youdao_api.query_word(word)
        story_text = self.qwen_api.generate_story_text(word)
        print(f"单词释义: {definition}")
        print(f"趣味故事: {story_text}")

    def manage_wordbook(self):
        # 仅保留删除单词的逻辑
        del_word = simpledialog.askstring("删除单词", "请输入要删除的单词：")
        if del_word:
            if self.wordbook.delete_word(del_word):
                messagebox.showinfo("成功", "单词删除成功。")
            else:
                messagebox.showinfo("失败", "找不到单词 {del_word}")

    def run(self):
            # 启动用户界面
            self.ui.run()

if __name__ == "__main__":
    app = MainApp()
    app.run()





