import json

class Word:
    def __init__(self, text, definition='', example_text='', familiarity=0):
        self.text = text
        self.definition = definition
        self.example_text = example_text
        self.familiarity = familiarity

    def to_dict(self):
        return {
            'text': self.text,
            'definition': self.definition,
            'example_text': self.example_text,
            'familiarity': self.familiarity
        }

    @staticmethod
    def from_dict(data):
        """从字典创建Word对象。"""
        return Word(
            text=data['text'], 
            definition=data.get('definition', ''), 
            example_text=data.get('example_text', '') 
        )


class WordBook:
    """管理单词本的类。"""
    
    def __init__(self, file_path='wordbook.json'):
        self.file_path = file_path
        self.words = {}
        self.load_words()

    def add_word(self, word):
        """添加单词到单词本。"""
        if word.text not in self.words:
            self.words[word.text] = word
            self.save_words()
            return True
        return False
    
    def add_word_with_example(self, word_text, definition, example_text):
        """添加单词和生成的文本到单词本中。"""
        if word_text not in self.words:
            self.words[word_text] = Word(word_text, definition, example_text)
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

    def save_words(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # 转换self.words中的Word对象为字典
            words_dict = {text: word.to_dict() for text, word in self.words.items()}
            json.dump(words_dict, f, ensure_ascii=False, indent=4)

    def load_words(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                words_dict = json.load(f)
            # 从字典恢复Word对象
            self.words = {text: Word(**data) for text, data in words_dict.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.words = {}
