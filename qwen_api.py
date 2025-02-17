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

    def generate_example(self, word):
        # 如果用户定义了prompt，使用用户定义的prompt；否则使用默认prompt
        if self.custom_prompt:
            formatted_prompt = self.default_prompt.format(word=word, user_input=self.custom_prompt)
        else:
            user_input = self.custom_prompt if self.custom_prompt else "用英文生成一个该单词的例句，40词以内，并提供中文翻译"
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


