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
        "cardName" : "The Fool",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_fool(0).jpg",
    },
    {
        "cardName" : "The Magician",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_magician(1).jpg",
    },
    {
        "cardName" : "The High Priestess",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_high_priestess(2).jpg",
    },
    {
        "cardName" : "The Empress",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_empress(3).jpg",
    },
    {
        "cardName" : "The Emperor",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_emperor(4).jpg",
    },
    {
        "cardName" : "The Hierophant",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_hierophant(5).jpg",
    },
    {
        "cardName" : "The Lovers",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_lovers(6).jpg",
    },
    {
        "cardName" : "The Chariot",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_chariot(7).jpg",
    },
    {
        "cardName" : "Strength",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/strength(8).jpg",
    },
    {
        "cardName" : "The Hermit",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the+_hermit(9).jpg",
    },
    {
        "cardName" : "Wheel of Fortune",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/wheel_of_fortune(10).jpg",
    },
    {
        "cardName" : "Justice",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/justice(11).jpg",
    },
    {
        "cardName" : "The Hanged Man",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_hanged_man(12).jpg",
    },
    {
        "cardName" : "Death",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/death(13).jpg",
    },
    {
        "cardName" : "Temperance",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/temperance(14).jpg",
    },
    {
        "cardName" : "The Devil",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_devil(15).jpg",
    },
    {
        "cardName" : "The Tower",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_tower(16).jpg",
    },
    {
        "cardName" : "The Star",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_star(17).jpg",
    },
    {
        "cardName" : "The Moon",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_moon(18).jpg",
    },
    {
        "cardName" : "The Sun",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_sun(19).jpg",
    },
    {
        "cardName" : "Judgment",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/judgement(20).jpg",
    },
    {
        "cardName" : "The World",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/the_world(21).jpg",
    },
    {
        "cardName" : "Ace of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ace_of_wands.jpg",
    },
    {
        "cardName" : "Two of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/II_of_Wands.jpg",
    },
    {
        "cardName" : "Three of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iii_of_wands.jpg",
    },
    {
        "cardName" : "Four of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iv_of_wands.jpg",
    },
    {
        "cardName" : "Five of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/v_of_wands.jpg",
    },
    {
        "cardName" : "Six of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vi_of_wands.jpg",
    },
    {
        "cardName" : "Seven of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vii_of_wands.jpg",
    },
    {
        "cardName" : "Eight of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/viii_of_wands.jpg",
    },
    {
        "cardName" : "Nine of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ix_of_wands.jpg",
    },
    {
        "cardName" : "Ten of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/x_of_wands.jpg",
    },
    {
        "cardName" : "Page of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/page_of_wands.jpg",
    },
    {
        "cardName" : "Knight of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/knight_of_wands.jpg",
    },
    {
        "cardName" : "Queen of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/queen_of_wands.jpg",
    },
    {
        "cardName" : "King of Wands",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/king_of_wands.jpg",
    },
    {
        "cardName" : "Ace of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ace_of_cups.jpg",
    },
    {
        "cardName" : "Two of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ii_of_cups.jpg",
    },
    {
        "cardName" : "Three of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iii_of_cups.jpg",
    },
    {
        "cardName" : "Four of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iv_of_cups.jpg",
    },
    {
        "cardName" : "Five of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/v_of_cups.jpg",
    },
    {
        "cardName" : "Six of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vi_of_cups.jpg",
    },
    {
        "cardName" : "Seven of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vii_of_cups.jpg",
    },
    {
        "cardName" : "Eight of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/viii_of_cups.jpg",
    },
    {
        "cardName" : "Nine of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ix_of_cups.jpg",
    },
    {
        "cardName" : "Ten of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/x_of_cups.jpg",
    },
    {
        "cardName" : "Page of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/page_of_cups.jpg",
    },
    {
        "cardName" : "Knight of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/knight_of_cups.jpg",
    },
    {
        "cardName" : "Queen of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/queen_of_cups.jpg",
    },
    {
        "cardName" : "King of Cups",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/king_of_cups.jpg",
    },
    {
        "cardName" : "Ace of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ace_of_swords.jpg",
    },
    {
        "cardName" : "Two of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ii_of_swords.jpg",
    },
    {
        "cardName" : "Three of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iii_of_swords.jpg",
    },
    {
        "cardName" : "Four of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iv_of_swords.jpg",
    },
    {
        "cardName" : "Five of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/v_of_swords.jpg",
    },
    {
        "cardName" : "Six of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vi_of_swords.jpg",
    },
    {
        "cardName" : "Seven of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vii_of_swords.jpg",
    },
    {
        "cardName" : "Eight of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/viii_of_swords.jpg",
    },
    {
        "cardName" : "Nine of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ix_of_swords.jpg",
    },
    {
        "cardName" : "Ten of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/x_of_swords.jpg",
    },
    {
        "cardName" : "Page of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/page_of_swords.jpg",
    },
    {
        "cardName" : "Knight of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/knight_of_swords.jpg",
    },
    {
        "cardName" : "Queen of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/queen_of_swords.jpg",
    },
    {
        "cardName" : "King of Swords",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/king_of_swords.jpg",
    },
    {
        "cardName" : "Ace of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ace_of_pentacles.jpg",
    },
    {
        "cardName" : "Two of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ii_of_pentacles.jpg",
    },
    {
        "cardName" : "Three of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iii_of_pentacles.jpg",
    },
    {
        "cardName" : "Four of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/iv_of_pentacles.jpg",
    },
    {
        "cardName" : "Five of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/v_of_pentacles.jpg",
    },
    {
        "cardName" : "Six of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vi_of_pentacles.jpg",
    },
    {
        "cardName" : "Seven of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/vii_of_pentacles.jpg",
    },
    {
        "cardName" : "Eight of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/viii_of_pentacles.jpg",
    },
    {
        "cardName" : "Nine of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/ix_of_pentacles.jpg",
    },
    {
        "cardName" : "Ten of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/x_of_pentacles.jpg",
    },
    {
        "cardName" : "Page of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/page_of_pentacles.jpg",
    },
    {
        "cardName" : "Knight of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/knight_of_pentacles.jpg",
    },
    {
        "cardName" : "Queen of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/queen_of_pentacles.jpg",
    },
    {
        "cardName" : "King of Pentacles",
        "cardImg" : "https://radiant-wise-spirit-tarot-deck.s3.eu-west-2.amazonaws.com/tarot-deck/Tarot-desk-resize/king_of_pentacles.jpg",
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
