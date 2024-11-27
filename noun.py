import csv
import datetime
import random
# read the txt file in and print
# save words into a dictionary of dictionaries
# the top level key is the french noun
# the keys in the internal dictionary are for gender, english definition and an empty list to
# record when the word was tested and if it was recalled successfully or not
# note that ipa data is from: https://github.com/open-dict-data/ipa-dict/ (MIT licence)

# constructing the dictionary of words

class Run:
    def __init__(self):
        self.nouns = self.get_nouns()
        self.words_seen = set()
        self.run_over = False
        self.noun_list = list(self.nouns.keys())

    def get_nouns(self):
        ### should make this a default dictionary in case eg some nouns don't have all the features
        # should also have a skip if noun is already in the dictionary
        # eventually this will be in it's own file, making the dictionary will
        # essentially be a one off, this is just to get the program started
        # also should have a check here to see if word is correctly spelt (ie does it appear
        # in the IPA list)
        nouns = {}
        with open("noun-list.txt") as file:
            reader = csv.DictReader(file)
            for row in reader:
                nouns[row["french"].strip()] = {"gender": row["gender"], 
                    "english": row["english"].strip(),"seen":[], "ipa": '',
                    "countable": row["countable"]}
        
        # add the ipa data to the dictionary - there must be a faster way to do this.. (binary search?)
        # should only do it once and then put the saved dictionary into a pickle file?
        word_set = set(nouns.keys())
        with open("fr_FR.txt") as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if row['word'] in word_set:
                    nouns[row['word']]['ipa'] = row['ipa']
        return nouns

    def random_noun(self):
        ### returns a random noun from the list of nouns on this run
        return random.choice(self.noun_list)
    
    def create_question(self):
    #given a (french) noun and a dictionary of (french) nouns
    #generate a test question (the english noun with a definite or indefinite article)
    # and the correct answer (the french noun with the corresponding article)
        noun = self.random_noun()
        vowels = ('a', 'e', 'i', 'o', 'u')
        gender = self.nouns[noun]['gender']
        english = self.nouns[noun]['english']

        #if mass noun, type is definite, otherwise select at random
        # mass nouns cannot take an indefinite article
        if self.nouns[noun]["countable"] == "False": #mass noun
            type = 'definite'
            english_article = ''
        else:
            type = random.choice(['definite', 'indefinite'])
            # generate the correct article for english
            if type == "definite":
                english_article = "the "
            elif english.startswith(vowels):
                english_article = "an "
            else:
                english_article = 'a '    
        english = english_article + english

        # generate correct article for french noun based on the starting letter and article type
        h_muet = False
        if noun.startswith('h'):
                #check if the 'h' is muet (liasion allowed) or aspiré (liasion forbidden)
                if self.nouns[noun]['ipa'].startswith("/ʼ"):
                    # le h est aspiré, do nothing, this h behaves like a consonant
                    pass
                else:
                    h_muet = True
        
        if type == "definite":
            if noun.startswith(vowels) or h_muet:
                french_article = "l'"
            elif gender == "m":
                french_article = "le "
            else:
                french_article = "la "
        else:
            if gender == "m":
                french_article = "un "
            else:
                french_article = "une "
        french = french_article + noun
        ipa = self.nouns[noun]['ipa']
        gender = self.nouns[noun]['gender']
        return english, french, ipa, gender


def main():
    run = Run()
    counter = 0
    while run.run_over is False:
        now = datetime.datetime.now()
        english,french,ipa,gender = run.create_question()
        user_answer = input(f"translate: {english}\n").strip()

        ## this needs more error checking,
        ## screen for bad user inputs
        #  mass nouns cannot take an indefinite article
        ## the point is to test gender
        ## not whether they get the difference between definite and indefinite articles correct
        ## the testing code should be tidied into one function
        if user_answer.lower() in ('quit', 'q', 'stop'):
            break
        if user_answer == french:
            
            print("correct")
        else:
            print(f"the correct answer is: {french}.")
        print(f"the ipa pronounciation is {ipa}\n")

        if french.startswith("l'"):
                # need to check the user knows the gender
                user_gender = input("what is the gender of the noun (m or f)?:\n")
                if user_gender == gender:
                    print('correct\n')
                else:
                    print(f"incorrect, the gender is: {gender}\n")
              
        counter +=1
        if counter > 100:
            run.run_over = True
    



if __name__ == "__main__":
    main()