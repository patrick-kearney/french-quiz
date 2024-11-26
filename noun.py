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
nouns = {}
with open("noun-list.txt") as file:
    reader = csv.DictReader(file)
    for row in reader:
        nouns[row["french"].strip()] = {"gender": row["gender"], 
            "english": row["english"].strip(),"seen":[], "ipa": '',
            "count_or_mass": row["count_or_mass"]}

# add the ipa data to the dictionary - there must be a faster way to do this.. (binary search?)
# should only do it once and then put the saved dictionary into a pickle file?

word_set = set(nouns.keys())
with open("fr_FR.txt") as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        if row['word'] in word_set:
            nouns[row['word']]['ipa'] = row['ipa']

print(nouns)

def main():
    play_flag = True
    noun_list = list(nouns.keys())
    counter = 0
    while play_flag:
        now = datetime.datetime.now()
        noun = random.choice(noun_list)
        english_test, french_test = create_question(noun,nouns)
        user_answer = input(f"translate: {english_test}\n").strip()
        # print(f"the user input is: {user_answer}.")
        # print(f"the correct answer is: {french_test}.")

        ## this needs more error checking,
        ## screen for bad user inputs
        #  mass nouns cannot take an indefinite article
        ## the point is to test gender
        ## not whether they get the difference between definite and indefinite articles correct
        ## the testing code should be tidied into one function
        if user_answer == french_test:
            
            print("correct")
        else:
            print(f"the correct answer is: {french_test}.")
        print(f"the ipa pronounciation is {nouns[noun]['ipa']}\n")

        if french_test.startswith("l'"):
                # need to check the user knows the gender
                user_gender = input("what is the gender of the noun (m or f)?:\n")
                if user_gender == nouns[noun]['gender']:
                    print('correct\n')
                else:
                    print(f"incorrect, the gender is: {nouns[noun][gender]}\n")
        
        
        counter +=1
        if counter > 10:
            play_flag = False
    

def create_question(noun,nouns):
    #given a (french) noun and a dictionary of (french) nouns
    #generate a test question (the english noun with a definite or indefinite article)
    # and the correct answer (the french noun with the corresponding article)
    vowels = ('a', 'e', 'i', 'o', 'u')
    gender = nouns[noun]['gender']
    english = nouns[noun]['english']
    type = random.choice(['definite', 'indefinite'])

    # mass nouns cannot take an indefinite article
    mass_noun = (nouns[noun]["count_or_mass"] == "mass")
    if mass_noun:
        type = "definite"
        english_article = ''
    else:
    # generate the correct article for english
        if type == "definite":
            english_article = "the "
        elif english.startswith(vowels):
            english_article = "an "
        else:
            english_article = 'a '
    english_test = english_article + english


    # generate correct article for french noun based on the starting letter and article type
    h_muet = False
    if noun.startswith('h'):
            #check if the 'h' is muet (liasion allowed) or aspiré (liasion forbidden)
            if nouns[noun]['ipa'].startswith("/ʼ"):
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
    french_test = french_article + noun

    return english_test, french_test

if __name__ == "__main__":
    main()