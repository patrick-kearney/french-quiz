# French Noun Quiz Program
Picks a French noun from a dictionary noun-list.txt and prompts the user with the English noun and article.
Checks if the user is correct and displays the IPA pronunciation of the noun.
Can be run in terminal with $python3 noun.py

## verb data
verbs.csv is a list of the (roughly 2000) most common verbs in French. It is derived from a list of the 10,000 most common French lemmas. I got the list from here: https://www.reddit.com/r/French/comments/140xl68/resource_free_top_10000_french_words_listgrouped/
It is based on the database at www.lexique.org, based on the most frequently used words in films. 
The point of this csv was to show, for each common verb, the model for it's conjugation (eg demander is conjugated like parler, devoir is conjugated like devoir) along with the participles and pronominal form if it exists. A quick analysis shows that about two-thirds of these verbs are conjugated like parler, although the most common verbs are all irregular.