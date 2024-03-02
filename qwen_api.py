import random
from http import HTTPStatus
import dashscope
from dashscope import get_tokenizer
import tkinter.messagebox as messagebox


class QwenAPI:
    def __init__(self, api_key, default_prompt="请根据以下要求生成关于{word}的文本：{user_input}"):
        self.api_key = api_key
        self.default_prompt = default_prompt  # 保存默认prompt
        self.custom_prompt = None  # 用于保存用户通过Prompt菜单输入的文本
        dashscope.api_key = self.api_key  # 设置API密钥

    def generate_story(self, word):
        # 如果用户定义了prompt，使用用户定义的prompt；否则使用默认prompt
        if self.custom_prompt:
            formatted_prompt = self.custom_prompt.format(word=word)  # 确保用户的prompt中可以使用{word}来插入单词
        else:
            user_input = self.custom_prompt if self.custom_prompt else "编一个有关这个单词的小故事"
            formatted_prompt = self.default_prompt.format(word=word, user_input=user_input)

        try:
            response = dashscope.Generation.call(
                model=dashscope.Generation.Models.qwen_turbo,
                prompt=formatted_prompt,
                seed=random.randint(1, 10000),
            )

            if response.status_code == HTTPStatus.OK:
                return response.output.text
            else:
                error_info = response.json()
                error_message = error_info.get('message', '未知错误')
                messagebox.showerror("生成内容失败", f"状态码: {response.status_code}, 错误信息: {error_message}")
                return None
        except Exception as e:
            messagebox.showerror("生成内容异常", str(e))
            return None

    def update_prompt(self, new_prompt):
        """更新用户输入的prompt部分。"""
        self.custom_prompt = new_prompt


# 示例使用
if __name__ == '__main__':
    API_KEY = 'sk-3b736ed70cc74c90b1aec671161ea43f'
    qwen_api = QwenAPI(API_KEY)
    word = 'amaze'  # 示例单词
    story = qwen_api.generate_story(word)
    if story:
        print("趣味小故事:", story)
    else:
        print("未能生成小故事。")

