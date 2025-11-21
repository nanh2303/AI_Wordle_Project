# utils.py

def load_words(filename="words.txt"):
    """Loads valid 5-letter words from a text file."""
    try:
        with open(filename, "r") as f:
            print("loaded words.txt")
            return [w.strip().lower() for w in f.readlines() if len(w.strip()) == 5 and w.strip().isalpha()]
    except FileNotFoundError:
        # Default fallback list
        print("cannot load words.txt")
        return [
            "apple", "beach", "brain", "bread", "brush", "chair", "chest", "chord", 
            "click", "clock", "cloud", "dance", "diary", "drive", "drone", "eagle", 
            "earth", "feast", "field", "flame", "fruit", "glass", "grape", "green", 
            "ghost", "heart", "house", "juice", "light", "lemon", "melon", "money", 
            "music", "night", "ocean", "party", "piano", "pilot", "plane", "plant", 
            "plate", "phone", "power", "quiet", "radio", "river", "robot", "sheep", 
            "shirt", "shoes", "smile", "snake", "space", "spoon", "storm", "sugar", 
            "table", "tiger", "toast", "touch", "train", "truck", "voice", "watch", 
            "water", "whale", "white", "woman", "world", "write", "youth", "zebra", 
            "adieu", "tears", "alone", "arise", "stare", "hello", "media", "audit"
        ]