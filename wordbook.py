import json

class Word:
    """代表单词的类，包含单词的各种属性。"""
    
    def __init__(self, text, definition='', example='', memory_hint=''):
        self.text = text
        self.definition = definition
        self.example = example
        self.memory_hint = memory_hint
        self.familiarity = 0  # 熟悉度，默认为0

    def to_dict(self):
        """将Word对象转换为字典，便于保存。"""
        return {
            'text': self.text,
            'definition': self.definition,
            'example': self.example,
            'memory_hint': self.memory_hint,
            'familiarity': self.familiarity
        }

    @staticmethod
    def from_dict(data):
        """从字典创建Word对象。"""
        # 确保调用时传递所有需要的参数
        return Word(data['text'], data.get('definition', ''), data.get('example', ''), data.get('memory_hint', ''))


class WordBook:
    """管理单词本的类。"""
    
    def __init__(self, file_path='wordbook.json'):
        self.file_path = file_path
        self.words = self.load_words()

    def add_word(self, word):
        """添加单词到单词本。"""
        if word.text not in self.words:
            self.words[word.text] = word
            self.save_words()
            return True
        return False
    
    def add_word_with_story(self, word_text, definition, story):
        """添加单词和相关的故事到单词本中。"""
        if word_text not in self.words:
            self.words[word_text] = Word(word_text, definition, memory_hint=story)
            self.save_words()
            return True
        return False

    def delete_word(self, word_text):
        """从单词本删除单词。"""
        if word_text in self.words:
            del self.words[word_text]
            self.save_words()
            return True
        return False

    def query_word(self, word_text):
        """查询单词详细信息。"""
        return self.words.get(word_text)

    def load_words(self):
        """从文件加载单词本。"""
        try:
            with open(self.file_path, 'r') as file:
                word_dicts = json.load(file)
            return {text: Word.from_dict(data) for text, data in word_dicts.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_words(self):
        """将单词本保存到文件。"""
        with open(self.file_path, 'w') as file:
            json.dump({text: word.to_dict() for text, word in self.words.items()}, file, ensure_ascii=False, indent=4)
