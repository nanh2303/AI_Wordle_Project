# benchmark.py
import time
import tracemalloc
import statistics
from game import WordleGame

class PerformanceBenchmark:
    def __init__(self, word_list, algo_class, num_games=10):
        self.word_list = word_list
        self.algo_class = algo_class
        self.num_games = num_games
        self.results = {
            "times": [],
            "memory": [],
            "nodes": [],
            "guesses": [],
            "wins": 0
        }

    def run(self, progress_callback=None):
        for i in range(self.num_games):
            game = WordleGame(self.word_list)
            solver = self.algo_class(game)
            
            tracemalloc.start()
            start_time = time.perf_counter()
            
            attempts = 0
            won = False
            
            while attempts < 6:
                guess = solver.solve_step()
                if not guess: break
                attempts += 1
                
                feedback = game.check_guess(guess)
                solver.filter_candidates(guess, feedback)
                
                if all(f == 2 for f in feedback):
                    won = True
                    break
            
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # Record Data
            self.results["times"].append((end_time - start_time) * 1_000_000) # Microseconds
            self.results["memory"].append(peak) # Bytes
            self.results["nodes"].append(solver.nodes_expanded)
            self.results["guesses"].append(attempts)
            if won: self.results["wins"] += 1
            
            if progress_callback: 
                progress_callback(i + 1, self.num_games)

        return self.calculate_stats()

    def calculate_stats(self):
        r = self.results
        if not r["times"]: return {}
        
        return {
            "avg_time": statistics.mean(r["times"]),
            "max_time": max(r["times"]),
            
            "avg_mem": statistics.mean(r["memory"]),
            "max_mem": max(r["memory"]),
            
            "avg_nodes": statistics.mean(r["nodes"]),
            "max_nodes": max(r["nodes"]),
            
            "avg_guesses": statistics.mean(r["guesses"]),
            "max_guesses": max(r["guesses"]),
            
            "win_rate": (r["wins"] / self.num_games) * 100
        }