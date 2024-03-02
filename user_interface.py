import tkinter as tk
from tkinter import simpledialog, messagebox
from youdao_api import YoudaoAPI
from qwen_api import QwenAPI
import random

class UserInterface:
    def __init__(self, main_app):
        self.main_app = main_app
        self.custom_prompt = None

        self.youdao_api = main_app.youdao_api
        self.qwen_api = main_app.qwen_api

        self.last_generated_story = None
        
        self.window = tk.Tk()
        self.window.title("背单词程序")
        
        self.setup_ui()
        self.create_menus()  # 创建菜单

        
    def setup_ui(self):
        self.word_entry = tk.Entry(self.window, width=50)
        self.word_entry.pack(pady=10)

        # 输出区域
        self.output_text = tk.Text(self.window, height=10, width=50)
        self.output_text.pack(pady=10)
        self.word_entry.focus_set()
        
    
    def create_menus(self):
        # 创建一个顶级菜单
        # 创建顶级菜单
        self.menubar = tk.Menu(self.window)
        # 查词
        self.menubar.add_command(label="查词", command=self.query_word)
        # AI功能
        self.menubar.add_command(label="千问AI", command=self.generate_story)
        # 修改prompt
        self.menubar.add_command(label="Prompt", command=self.update_prompt)
        # 添加单词到单词本
        self.menubar.add_command(label="添加单词到单词本", command=self.add_word_to_wordbook)
        # 背词菜单
        review_menu = tk.Menu(self.menubar, tearoff=0)
        review_menu.add_command(label="记忆模式", command=self.memory_mode)
        review_menu.add_command(label="拼写模式", command=self.spelling_mode)
        self.menubar.add_cascade(label="背词", menu=review_menu)
        # 创建单词本管理菜单及其子菜单项
        wordbook_menu = tk.Menu(self.menubar, tearoff=0)
        wordbook_menu.add_command(label="生词本", command=self.show_new_words)
        wordbook_menu.add_command(label="记忆中", command=self.show_learning_words)
        wordbook_menu.add_command(label="熟词本", command=self.show_known_words)
        wordbook_menu.add_command(label="删除单词", command=self.delete_word)
        self.menubar.add_cascade(label="单词本管理", menu=wordbook_menu)

        # 配置窗口使用这个菜单
        self.window.config(menu=self.menubar)

        
    def query_word(self):
        word = self.word_entry.get()
        if word:
            result = self.youdao_api.connect(word)  # 假设这是调用API的方法
            self.output_text.delete(1.0, tk.END)  # 清空文本框
            
            if 'errorCode' in result and result['errorCode'] != '0':
                # 如果有错误码且不为0，显示错误信息
                error_msg = f"错误：{result.get('errorMessage', '未知错误')}"
                self.output_text.insert(tk.END, error_msg)
            elif 'basic' in result:
                # 格式化输出，将释义每个条目换行显示
                explains = result['basic'].get('explains', [])
                if explains:
                    formatted_text = "\n".join(explains)
                else:
                    formatted_text = "没有找到释义。"
                self.output_text.insert(tk.END, formatted_text)
            else:
                self.output_text.insert(tk.END, "没有找到释义。")
        else:
            messagebox.showinfo("提示", "请输入单词")
        

    def generate_story(self):
        word = self.word_entry.get()
        if word:
            # 调用 QwenAPI 实例的 generate_story 方法生成故事
            story_text = self.qwen_api.generate_story(word)
            if story_text:
                self.last_generated_story = story_text  # 保存最后一次生成的故事
                self.output_text.delete(1.0, tk.END)  # 清空输出区域
                self.output_text.insert(tk.END, story_text)  # 显示故事
            else:
                # 如果没有生成故事，可能是因为API调用失败
                messagebox.showinfo("提示", "无法生成故事，请重试。")
        else:
            messagebox.showinfo("提示", "请输入单词来生成故事")


    def show_wordbook(self):
        # 调用MainApp类中的view_wordbook方法
        self.main_app.view_wordbook()

    def view_wordbook(self):
        # 查看单词本
        new_words = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity == 0}
        learning_words = {word: info for word, info in self.main_app.wordbook.words.items() if 0 < info.familiarity < 10}
        known_words = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity == 10}
        
        message = "生词本:\n" + "\n".join(new_words.keys()) + "\n\n"
        message += "记忆中:\n" + "\n".join(learning_words.keys()) + "\n\n"
        message += "熟词本:\n" + "\n".join(known_words.keys())
        
        messagebox.showinfo("单词本", message)

    def generate_story(self):
        word = self.word_entry.get()  # 获取用户输入的单词
        if word:
            content = self.main_app.qwen_api.generate_story(word)  # 这里传递单词作为参数
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, content)
        else:
            messagebox.showinfo("提示", "请输入单词来生成内容")


    def add_word_to_wordbook(self):
        word = self.word_entry.get().strip()
        if word:
            # 使用YoudaoAPI类的connect方法查询单词
            word_info = self.youdao_api.connect(word)
            # 检查是否成功获取到词条信息
            if word_info and 'basic' in word_info:
                # 提取词性和释义部分
                explains = "\n".join(word_info['basic'].get('explains', []))
                # 如果有最后一次生成的故事，包括故事
                story = self.last_generated_story if self.last_generated_story else ""
                # 调用WordBook的方法添加单词和故事（如果有）到单词本
                if self.main_app.wordbook.add_word_with_story(word, explains, story):
                    messagebox.showinfo("成功", "单词已成功添加到单词本")
                    self.last_generated_story = None  # 重置最后一次生成的故事
                else:
                    messagebox.showinfo("失败", "该单词已存在于单词本中")
            else:
                messagebox.showinfo("失败", "无法找到该单词的详细信息")
        else:
            messagebox.showinfo("提示", "请输入单词")


    def delete_word(self):
        # 从单词本删除单词
        word_to_delete = simpledialog.askstring("删除单词", "请输入要删除的单词：")
        if word_to_delete:
            if self.main_app.wordbook.delete_word(word_to_delete):
                messagebox.showinfo("成功", f"单词 {word_to_delete} 已从单词本中删除")
            else:
                messagebox.showinfo("失败", f"找不到单词 {word_to_delete}")


    def display_words(self, title, words):
        """展示单词本中的单词列表，仅展示单词和第一个释义"""
        if words:
            # 对于每个单词，只选择第一个释义来展示
            words_list = "\n".join([f"{word}: {info.definition.split(';')[0]}" for word, info in words.items()])
            messagebox.showinfo(title, words_list)
        else:
            messagebox.showinfo(title, f"{title}是空的。")

    def show_new_words(self):
        new_words = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity == 0}
        self.display_words("生词本", new_words)

    def show_learning_words(self):
        learning_words = {word: info for word, info in self.main_app.wordbook.words.items() if 0 < info.familiarity < 10}
        self.display_words("记忆中", learning_words)

    def show_known_words(self):
        known_words = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity == 10}
        self.display_words("熟词本", known_words)

    def memory_mode(self):
        words_to_review = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity < 10}
        if not words_to_review:
            messagebox.showinfo("提示", "没有单词需要记忆啦")
            return

        def review_next_word():
            nonlocal words_to_review
            if not words_to_review:
                messagebox.showinfo("完成", "已经复习完所有单词！")
                return

            word, info = random.choice(list(words_to_review.items()))
            answer = messagebox.askquestion("记忆模式", f"你记得单词 '{word}' 的意思吗？", type='yesno')

            if answer == 'yes':
                info.familiarity += 1  # 熟悉度+1
                message = f"{word}: {info.definition.split(';')[0]}"  # 只显示第一个释义
                if info.memory_hint:
                    message += f"\n小故事：{info.memory_hint}"  # 如果有小故事也展示
                message += "\n\n点击【确定】继续下一个单词，【取消】退出复习。"
                words_to_review.pop(word)  # 从复习列表中移除
                if messagebox.askokcancel("记得", message):
                    review_next_word()

        review_next_word()
        self.main_app.wordbook.save_words()

    def spelling_mode(self):
        words_to_review = {word: info for word, info in self.main_app.wordbook.words.items() if info.familiarity < 10}
        if not words_to_review:
            messagebox.showinfo("提示", "没有单词需要记忆啦")
            return

        def review_next_word():
            nonlocal words_to_review
            if not words_to_review:
                messagebox.showinfo("完成", "已经复习完所有单词！")
                return

            word, info = random.choice(list(words_to_review.items()))
            user_spelling = simpledialog.askstring("拼写模式", f"释义为：'{info.definition.split(';')[0]}'\n请输入单词的拼写：")

            if user_spelling is None:  # 用户取消输入
                return

            if user_spelling.lower() == word.lower():
                info.familiarity += 1  # 熟悉度+1
                message = f"拼写正确！\n{word}: {info.definition.split(';')[0]}"
                if info.memory_hint:
                    message += f"\n小故事：{info.memory_hint}"  # 展示小故事
                message += "\n\n点击【确定】继续下一个单词，【取消】退出复习。"
                words_to_review.pop(word)  # 从复习列表中移除
                if messagebox.askokcancel("正确", message):
                    review_next_word()
            else:
                message = f"拼写错误。正确答案是：{word}\n{info.definition.split(';')[0]}"
                if messagebox.askokcancel("错误", message):
                    review_next_word()

        review_next_word()
        self.main_app.wordbook.save_words()


    def update_prompt(self):
        # 弹出对话框让用户输入新的prompt
        new_prompt = simpledialog.askstring("更新Prompt", "请输入新的Prompt：")
        if new_prompt:
            # 更新QwenAPI实例的prompt
            self.qwen_api.update_prompt(new_prompt)
            messagebox.showinfo("提示", "Prompt更新成功！")
        else:
            messagebox.showinfo("提示", "Prompt未更新。")



    def run(self):
        self.window.mainloop()
