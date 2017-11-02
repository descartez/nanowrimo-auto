
import markovify
import markov_novel
import os
import re
import spacy

# nlp = spacy.load("en")

# class POSifiedText(markovify.Text):
#     def word_split(self, sentence):
#         return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

#     def word_join(self, words):
#         sentence = " ".join(word.split("::")[0] for word in words)
#         return sentence

class Text:
    def create_model(self, filename):
        with open(filename) as f:
            text = f.read()
        self.model = markovify.Text(text)

    def create_model_from_dir(self, dir_path):
        combined_model = None
        for (dirpath, _, filenames) in os.walk(dir_path):
            for filename in filenames:
                with open(os.path.join(dirpath, filename)) as f:
                    model = markovify.Text(f, retain_original=False)
                    if combined_model:
                        combined_model = markovify.combine(models=[combined_model, model])
                    else:
                        combined_model = model
        self.model = markovify.Text(combined_model)

    def create_prompt(self):
        return self.model.make_short_sentence(self.prompt_sizes)

    def write_file_with_text(self, name):
        novel = markov_novel.Novel(self.model, chapter_count=1)
        novel.write(novel_title=str(name), filetype='md')

text = Text()
text.create_model_from_dir("texts/gaiman/")
