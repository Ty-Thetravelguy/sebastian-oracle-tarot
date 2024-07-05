import os
from pymongo import MongoClient

if os.path.exists("env.py"):
    import env


mongo_uri = os.environ.get("MONGO_URI")
mongo_dbname = os.environ.get("MONGO_DBNAME")


client = MongoClient(mongo_uri)
db = client[mongo_dbname]


tarotCards = [
    {
        "cardName" : "Judgment",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/judgement(20).jpg",
    },
    {
        "cardName" : "The World",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/the_world(21).jpg",
    },
    {
        "cardName" : "Ace of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ace_of_wands.jpg",
    },
    {
        "cardName" : "Two of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/II_of_Wands.jpg",
    },
    {
        "cardName" : "Three of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iii_of_wands.jpg",
    },
    {
        "cardName" : "Four of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iv_of_wands.jpg",
    },
    {
        "cardName" : "Five of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/v_of_wands.jpg",
    },
    {
        "cardName" : "Six of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vi_of_wands.jpg",
    },
    {
        "cardName" : "Seven of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vii_of_wands.jpg",
    },
    {
        "cardName" : "Eight of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/viii_of_wands.jpg",
    },
    {
        "cardName" : "Nine of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ix_of_wands.jpg",
    },
    {
        "cardName" : "Ten of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/x_of_wands.jpg",
    },
    {
        "cardName" : "Page of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/page_of_wands.jpg",
    },
    {
        "cardName" : "Knight of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/knight_of_wands.jpg",
    },
    {
        "cardName" : "Queen of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/queen_of_wands.jpg",
    },
    {
        "cardName" : "King of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/king_of_wands.jpg",
    },
    {
        "cardName" : "Ace of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ace_of_cups.jpg",
    },
    {
        "cardName" : "Two of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ii_of_cups.jpg",
    },
    {
        "cardName" : "Three of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iii_of_cups.jpg",
    },
    {
        "cardName" : "Four of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iv_of_cups.jpg",
    },
    {
        "cardName" : "Five of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/v_of_cups.jpg",
    },
    {
        "cardName" : "Six of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vi_of_cups.jpg",
    },
    {
        "cardName" : "Seven of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vii_of_cups.jpg",
    },
    {
        "cardName" : "Eight of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/viii_of_cups.jpg",
    },
    {
        "cardName" : "Nine of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ix_of_cups.jpg",
    },
    {
        "cardName" : "Ten of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/x_of_cups.jpg",
    },
    {
        "cardName" : "Page of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/page_of_cups.jpg",
    },
    {
        "cardName" : "Knight of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/knight_of_cups.jpg",
    },
    {
        "cardName" : "Queen of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/queen_of_cups.jpg",
    },
    {
        "cardName" : "King of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/king_of_cups.jpg",
    },
    {
        "cardName" : "Ace of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ace_of_swords.jpg",
    },
    {
        "cardName" : "Two of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ii_of_swords.jpg",
    },
    {
        "cardName" : "Three of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iii_of_swords.jpg",
    },
    {
        "cardName" : "Four of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iv_of_swords.jpg",
    },
    {
        "cardName" : "Five of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/v_of_swords.jpg",
    },
    {
        "cardName" : "Six of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vi_of_swords.jpg",
    },
    {
        "cardName" : "Seven of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vii_of_swords.jpg",
    },
    {
        "cardName" : "Eight of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/viii_of_swords.jpg",
    },
    {
        "cardName" : "Nine of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ix_of_swords.jpg",
    },
    {
        "cardName" : "Ten of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/x_of_swords.jpg",
    },
    {
        "cardName" : "Page of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/page_of_swords.jpg",
    },
    {
        "cardName" : "Knight of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/knight_of_swords.jpg",
    },
    {
        "cardName" : "Queen of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/queen_of_swords.jpg",
    },
    {
        "cardName" : "King of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/king_of_swords.jpg",
    },
    {
        "cardName" : "Ace of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ace_of_pentacles.jpg",
    },
    {
        "cardName" : "Two of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ii_of_pentacles.jpg",
    },
    {
        "cardName" : "Three of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iii_of_pentacles.jpg",
    },
    {
        "cardName" : "Four of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/iv_of_pentacles.jpg",
    },
    {
        "cardName" : "Five of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/v_of_pentacles.jpg",
    },
    {
        "cardName" : "Six of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vi_of_pentacles.jpg",
    },
    {
        "cardName" : "Seven of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/vii_of_pentacles.jpg",
    },
    {
        "cardName" : "Eight of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/viii_of_pentacles.jpg",
    },
    {
        "cardName" : "Nine of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/ix_of_pentacles.jpg",
    },
    {
        "cardName" : "Ten of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/x_of_pentacles.jpg",
    },
    {
        "cardName" : "Page of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/page_of_pentacles.jpg",
    },
    {
        "cardName" : "Knight of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/knight_of_pentacles.jpg",
    },
    {
        "cardName" : "Queen of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/queen_of_pentacles.jpg",
    },
    {
        "cardName" : "King of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/king_of_pentacles.jpg",
    },
]

# Insert the tarot cards into the collection
try:
    result = db.tarotCards.insert_many(tarotCards)
    print(f"Inserted {len(result.inserted_ids)} cards into the collection.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
