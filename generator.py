# for language processing
import markovify
import os
import re
import spacy



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
class Character:
    def __init__(self):
        self.name = ""
        self.bio = ""

    def create_bio(self, name, bio):
        self.name = name
        self.bio = bio

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

    def speak_bio(self):
        print("-"*15)
        print(self.name)
        print(self.bio)
        print("-"*15)

    def speak_tweet(self):
        print(self.model.make_short_sentence(140))

    def return_tweet(self):
        return self.model.make_short_sentence(140)

class CharacterChooser:
    def __init__(self):
        self.models = []



lovecraft = Character()
lovecraft.create_bio("H.P. Lovecraft", "A xenophobic creepy writer.")
lovecraft.create_model_from_dir("character_texts/lovecraft")
lovecraft.speak_bio()

tweet = lovecraft.return_tweet()
print(tweet)
api.update_status(tweet)

gaiman = Character()
gaiman.create_bio("Neil Gaiman", "An excellent, empathetic man and writer.")
gaiman.create_model_from_dir("character_texts/gaiman")
gaiman.speak_bio()

tweet = gaiman.return_tweet()
print(tweet)
api.update_status(tweet)
