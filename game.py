# game.py
import random
import collections

class WordleGame:
    def __init__(self, word_list):
        self.full_dictionary = word_list
        self.secret_word = ""
        self.game_over = False
        self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.full_dictionary)
        self.game_over = False

    def is_valid_word(self, word):
        return word in self.full_dictionary

    def check_guess(self, guess):
        """
        Returns a list of status codes:
        2 = Green (Correct)
        1 = Yellow (Present)
        0 = Gray (Absent)
        """
        guess = guess.lower()
        target = list(self.secret_word)
        result = [0] * 5
        target_counts = collections.Counter(target)
        
        # 1. Green Pass
        for i in range(5):
            if guess[i] == target[i]:
                result[i] = 2
                target_counts[guess[i]] -= 1
                
        # 2. Yellow Pass
        for i in range(5):
            if result[i] == 0: 
                if guess[i] in target_counts and target_counts[guess[i]] > 0:
                    result[i] = 1
                    target_counts[guess[i]] -= 1
        return result