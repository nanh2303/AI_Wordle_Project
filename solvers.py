# solvers.py
import collections
import heapq
from config import Config

class WordleSolver:
    def __init__(self, game_instance):
        self.game = game_instance
        self.candidates = []
        self.nodes_expanded = 0 

    def reset(self):
        self.candidates = list(self.game.full_dictionary)
        self.nodes_expanded = 0

    def filter_candidates(self, last_guess, feedback):
        new_candidates = []
        for word in self.candidates:
            if self.is_consistent(word, last_guess, feedback):
                new_candidates.append(word)
        self.candidates = new_candidates

    def is_consistent(self, candidate, guess, feedback):
        temp_counts = collections.Counter(candidate)
        sim_feedback = [0] * 5
        
        for i in range(5):
            if guess[i] == candidate[i]:
                sim_feedback[i] = 2
                temp_counts[guess[i]] -= 1
        for i in range(5):
            if sim_feedback[i] == 0:
                if guess[i] in temp_counts and temp_counts[guess[i]] > 0:
                    sim_feedback[i] = 1
                    temp_counts[guess[i]] -= 1
        return sim_feedback == feedback

    def solve_step(self): 
        raise NotImplementedError

# --- Concrete Implementations ---

class BFSSolver(WordleSolver):
    def solve_step(self):
        queue = collections.deque(self.candidates)
        if queue:
            self.nodes_expanded += 1
            return queue.popleft()
        return None

class DFSSolver(WordleSolver):
    def solve_step(self):
        if self.candidates:
            self.nodes_expanded += 1
            return self.candidates[-1]
        return None

class UCSSolver(WordleSolver):
    def get_cost(self, word):
        score = 0; seen = set()
        for char in word:
            if char not in seen:
                score += Config.LETTER_FREQ.get(char, 0)
                seen.add(char)
        return 100 - score 
        
    def solve_step(self):
        pq = []
        for word in self.candidates: 
            heapq.heappush(pq, (self.get_cost(word), word))
        if pq:
            self.nodes_expanded += 1
            return heapq.heappop(pq)[1]
        return None

class AStarSolver(WordleSolver):
    def heuristic(self, word):
        score = 0
        for i, char in enumerate(word): 
            score += Config.LETTER_FREQ.get(char, 0)
        return -score
        
    def solve_step(self):
        pq = []; g_n = 1 
        for word in self.candidates: 
            heapq.heappush(pq, (g_n + self.heuristic(word), word))
        if pq:
            self.nodes_expanded += 1
            return heapq.heappop(pq)[1]
        return None