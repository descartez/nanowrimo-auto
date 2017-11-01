# for language processing
import markovify
import os
import re
import spacy
import random



class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

#------------------------------------------
# AUTHOR/CHARACTER CLASS
#------------------------------------------

# Creates a "character" class, that can load in mulitple files.
class Text:
    def __init__(self):
        self.prompt_sizes = [140, 280, 420]

    def create_model(self, file):
        with open(file) as f:
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
        self.model = combined_model

    def create_prompt(self):
        return self.model.make_short_sentence(self.prompt_sizes)

    def write_file(self, name):
        prompt = self.create_prompt()
        operating_file = open(("texts/original/" + name), "w")
        operating_file.write("PROMPT: \"" + str(prompt) + "\"")
        operating_file.close()


prompt_sizes = [140, 280, 420]

text = Text()
text.create_model_from_dir("texts")
text.write_file("text_2.txt")

