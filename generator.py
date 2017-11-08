import os
import markovify
import markov_novel
import re
import spacy

nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

# Build the model.
combined_model = None
for (dirpath, _, filenames) in os.walk("texts"):
    for filename in filenames:
        with open(os.path.join(dirpath, filename)) as ind_file:
            ind_text = ind_file.read()
            model = markovify.Text(ind_text)
            if combined_model:
                combined_model = markovify.combine(models=[combined_model, model])
            else:
                combined_model = model

novel = markov_novel.Novel(combined_model, chapter_count=1)
novel.write(novel_title='my-novel', filetype='md')