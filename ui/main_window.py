import tkinter as tk
from tkinter import messagebox, ttk
import threading
import datetime
import sys
import random

from config import Config
from utils import load_words
from game import WordleGame
from solvers import BFSSolver, DFSSolver, UCSSolver, AStarSolver

# Import our new modular dialogs
from .dialogs import ResultsDialog, HintDialog, BenchmarkDialog

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle AI Project")
        self.root.geometry("1100x850") 
        self.root.minsize(900, 700)
        self.root.configure(bg=Config.COLOR_BG)
        
        # Protocol for clean exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.word_list = load_words()
        self.game = WordleGame(self.word_list)
        
        self.solvers = {
            "BFS": BFSSolver, 
            "DFS": DFSSolver, 
            "UCS": UCSSolver, 
            "A*": AStarSolver
        }
        # Default solver instance
        self.current_solver_instance = AStarSolver(self.game) 
        
        self.is_auto_playing = False
        self.key_map = {} 
        self.guesses = [] 
        
        self.setup_ui()
        self.start_new_game()

    def on_close(self):
        self.is_auto_playing = False
        self.root.destroy()
        sys.exit(0)

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(0, weight=1)

        # --- LEFT CONTAINER (GAME) ---
        left_container = tk.Frame(self.root, bg=Config.COLOR_BG)
        left_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        tk.Label(left_container, text="WORDLE AI PROJECT", font=Config.FONT_TITLE, 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT).pack(pady=(0, 10), fill="x")

        game_area = tk.Frame(left_container, bg=Config.COLOR_BG)
        game_area.pack(expand=True, fill="both")
        
        self.grid_frame = tk.Frame(game_area, bg=Config.COLOR_BG)
        self.grid_frame.place(relx=0.5, rely=0.5, anchor="center") 
        
        self.cells = []
        for row in range(6):
            row_cells = []
            for col in range(5):
                lbl = tk.Label(self.grid_frame, text="", width=4, height=2,
                               font=Config.FONT_GRID,
                               bg=Config.COLOR_BG, fg=Config.COLOR_TEXT,
                               relief="solid", borderwidth=2)
                lbl.config(highlightbackground=Config.COLOR_EMPTY, highlightthickness=1)
                lbl.config(bg=Config.COLOR_BG, fg=Config.COLOR_TEXT) 
                lbl.grid(row=row, column=col, padx=3, pady=3)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        # --- CONTROLS ---
        controls_area = tk.Frame(left_container, bg=Config.COLOR_BG)
        controls_area.pack(fill="x", pady=(10, 5))

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(controls_area, textvariable=self.status_var, 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT, font=("Arial", 11, "italic")).pack(pady=5)

        btn_row = tk.Frame(controls_area, bg=Config.COLOR_BG)
        btn_row.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(btn_row, textvariable=self.entry_var, font=("Arial", 14), 
                              width=8, justify="center", bg="white", fg="black", insertbackground="black")
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.process_player_guess())

        # FIXED: Assigning to self.btn_guess
        self.btn_guess = tk.Button(btn_row, text="GUESS", command=self.process_player_guess,
                                   bg=Config.COLOR_CORRECT, fg="white", font=("Arial", 10, "bold"))
        self.btn_guess.pack(side=tk.LEFT, padx=5)

        ttk.Separator(btn_row, orient='vertical').pack(side=tk.LEFT, fill='y', padx=10)

        self.algo_var = tk.StringVar(value="A*")
        for mode in ["BFS", "DFS", "UCS", "A*"]:
            tk.Radiobutton(btn_row, text=mode, variable=self.algo_var, value=mode,
                           bg=Config.COLOR_BG, fg=Config.COLOR_TEXT, selectcolor=Config.COLOR_BG,
                           activebackground=Config.COLOR_BG, activeforeground=Config.COLOR_TEXT,
                           font=("Arial", 10), command=self.switch_solver).pack(side=tk.LEFT, padx=2)

        # --- FIX IS HERE: Assigning to self.btn_solve ---
        self.btn_solve = tk.Button(btn_row, text="▶ Auto solve", command=self.start_auto_solve,
                                   bg=Config.COLOR_PRESENT, fg="white", font=("Arial", 10, "bold"))
        self.btn_solve.pack(side=tk.LEFT, padx=10)

        tk.Button(btn_row, text="💡 Hint", command=self.give_hint,
                  bg="#f1c40f", fg="black", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_row, text="📊 Algorithm assessment", command=self.open_benchmark_window,
                  bg="#d35400", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        ttk.Separator(left_container, orient='horizontal').pack(fill='x', pady=10)
        self.keyboard_frame = tk.Frame(left_container, bg=Config.COLOR_BG)
        self.keyboard_frame.pack(fill="x", pady=(0, 10))
        self.create_keyboard()

        # --- RIGHT CONTAINER (LOGS) ---
        right_container = tk.Frame(self.root, bg=Config.COLOR_LOG_BG, width=320)
        right_container.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=20)
        right_container.pack_propagate(False) 
        self.setup_log_area(right_container)

    def setup_log_area(self, parent_frame):
        tk.Label(parent_frame, text="GAME LOGS", font=("Arial", 11, "bold"), 
                 bg=Config.COLOR_LOG_BG, fg=Config.COLOR_LOG_TEXT, pady=10).pack(fill="x")
        
        text_frame = tk.Frame(parent_frame, bg=Config.COLOR_LOG_BG)
        text_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.log_text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set,
                                bg=Config.COLOR_LOG_BG, fg=Config.COLOR_LOG_TEXT,
                                font=Config.FONT_LOG, state="disabled", borderwidth=0)
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.log_text.tag_configure("green", foreground=Config.COLOR_LOG_GREEN, font=(Config.FONT_LOG[0], Config.FONT_LOG[1], "bold"))
        self.log_text.tag_configure("yellow", foreground=Config.COLOR_LOG_YELLOW, font=(Config.FONT_LOG[0], Config.FONT_LOG[1], "bold"))
        self.log_text.tag_configure("bold", font=(Config.FONT_LOG[0], Config.FONT_LOG[1], "bold"))
        self.log_text.tag_configure("hint", foreground="#d35400", font=(Config.FONT_LOG[0], Config.FONT_LOG[1], "bold"))

    def log_message(self, message, tags=None):
        self.log_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
        self.log_text.insert("end", timestamp)
        self.log_text.insert("end", message + "\n", tags)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def create_keyboard(self):
        container = tk.Frame(self.keyboard_frame, bg=Config.COLOR_BG)
        container.pack()
        keys = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        for row in keys:
            row_frame = tk.Frame(container, bg=Config.COLOR_BG)
            row_frame.pack(pady=4) 
            for char in row:
                lbl = tk.Label(row_frame, text=char.upper(), width=5, height=1, font=Config.FONT_KEY,
                               bg=Config.COLOR_KEY_DEFAULT, fg=Config.COLOR_TEXT, 
                               relief="raised", borderwidth=1)
                lbl.pack(side=tk.LEFT, padx=3, ipady=8) 
                self.key_map[char] = lbl

    def update_keyboard_color(self, char, status):
        if char not in self.key_map: return
        widget = self.key_map[char]
        current_bg = widget.cget("bg")
        
        new_color = Config.COLOR_KEY_DEFAULT
        text_color = Config.COLOR_TEXT 
        
        if status == 2: 
            new_color = Config.COLOR_CORRECT; text_color = "white"
        elif status == 1:
            if current_bg != Config.COLOR_CORRECT: 
                new_color = Config.COLOR_PRESENT; text_color = "white"
            else: new_color = current_bg; text_color = "white"
        elif status == 0:
            if current_bg not in [Config.COLOR_CORRECT, Config.COLOR_PRESENT]: 
                new_color = Config.COLOR_ABSENT; text_color = "white"
            else: new_color = current_bg; text_color = "white"
                
        widget.config(bg=new_color, fg=text_color)

    # --- GAMEPLAY ---
    def start_new_game(self):
        self.game.reset_game()
        self.current_row = 0
        self.guesses = []
        self.entry_var.set("")
        self.status_var.set("New Game Started")
        
        for row in range(6):
            for col in range(5):
                self.cells[row][col].config(text="", bg=Config.COLOR_EMPTY, fg=Config.COLOR_TEXT, highlightthickness=1)
        for char, widget in self.key_map.items(): 
            widget.config(bg=Config.COLOR_KEY_DEFAULT, fg=Config.COLOR_TEXT)
            
        self.log_text.config(state="normal"); self.log_text.delete(1.0, "end"); self.log_text.config(state="disabled")
        self.log_message("--- NEW GAME STARTED ---", "bold")
        self.is_auto_playing = False
        
        # Fix: btn_solve is now properly initialized
        self.entry.config(state="normal")
        self.btn_solve.config(state="normal")
        self.entry.focus_set()
        self.switch_solver()

    def switch_solver(self):
        algo_name = self.algo_var.get()
        self.current_solver_instance = self.solvers[algo_name](self.game)
        self.current_solver_instance.reset()

    def process_player_guess(self):
        if self.game.game_over or self.is_auto_playing: return
        guess = self.entry_var.get().strip().lower()
        if len(guess) != 5: return messagebox.showwarning("Invalid", "Word must be 5 letters.")
        if not self.game.is_valid_word(guess): return messagebox.showwarning("Invalid", "Not in dictionary.")
        
        self.log_message(f"Player guessed: {guess.upper()}")
        self.submit_guess(guess)
        self.entry_var.set("")

    def give_hint(self):
        if self.game.game_over: return
        target = self.game.secret_word
        hint_char, hint_idx = "", -1
        
        if not self.guesses:
            hint_idx = random.randint(0, 4)
            hint_char = target[hint_idx]
        else:
            last_guess = self.guesses[-1]
            feedback = self.game.check_guess(last_guess)
            yellow_indices = [i for i, s in enumerate(feedback) if s == 1]
            
            if yellow_indices:
                char = last_guess[random.choice(yellow_indices)]
                hint_idx = target.find(char)
                hint_char = char
            else:
                green_indices = [i for i, s in enumerate(feedback) if s == 2]
                hidden = [i for i in range(5) if i not in green_indices]
                if hidden:
                    hint_idx = random.choice(hidden)
                    hint_char = target[hint_idx]
        
        if hint_char: HintDialog(self.root, hint_char, hint_idx)

    def start_auto_solve(self):
        if self.game.game_over: return
        self.is_auto_playing = True
        self.entry.config(state="disabled")
        self.btn_solve.config(state="disabled")
        algo = self.algo_var.get()
        self.log_message(f"--- AI ({algo}) Taking Over ---", "bold")
        self.run_auto_step()

    def run_auto_step(self):
        try:
            if not self.root.winfo_exists(): return
        except tk.TclError: return
        if self.game.game_over: return 
        
        solver = self.current_solver_instance
        count = len(solver.candidates)
        self.log_message(f"AI thinking... ({count} candidates)")
        guess = solver.solve_step()
        
        if guess:
            self.log_message(f"AI guesses: {guess.upper()}", "bold")
            self.submit_guess(guess)
            if not self.game.game_over: self.root.after(1000, self.run_auto_step)
        else:
            self.log_message("AI Failed: No candidates.", "yellow")
            self.is_auto_playing = False; self.btn_solve.config(state="normal")

    def submit_guess(self, guess):
        self.guesses.append(guess)
        for i, char in enumerate(guess): self.cells[self.current_row][i].config(text=char.upper())
        feedback = self.game.check_guess(guess)
        log_fb = ["🟩" if s==2 else "🟨" if s==1 else "⬛" for s in feedback]
        self.log_message(f"Feedback: {''.join(log_fb)}")
        
        for i, status in enumerate(feedback):
            color = Config.COLOR_CORRECT if status==2 else Config.COLOR_PRESENT if status==1 else Config.COLOR_ABSENT
            self.cells[self.current_row][i].config(bg=color, fg="white", highlightthickness=0)
            self.update_keyboard_color(guess[i], status)
            
        self.current_solver_instance.filter_candidates(guess, feedback)
        
        if all(f == 2 for f in feedback):
            self.game.game_over = True; self.status_var.set("Victory!")
            self.log_message(">>> GAME WON! <<<", "green")
            self.root.after(500, lambda: self.show_results_popup(True))
        elif self.current_row >= 5:
            self.game.game_over = True; self.status_var.set("Game Over")
            self.log_message(f">>> GAME LOST. Word: {self.game.secret_word.upper()}", "yellow")
            self.root.after(500, lambda: self.show_results_popup(False))
        else: self.current_row += 1

    def show_results_popup(self, won):
        ResultsDialog(self.root, won, self.game.secret_word, self.start_new_game, self.on_close)

    def open_benchmark_window(self):
        BenchmarkDialog(self.root, self.word_list, self.solvers)