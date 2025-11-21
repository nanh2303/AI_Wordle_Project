# Handle various dialog popups in the application
import tkinter as tk
from tkinter import ttk
import threading
from config import Config
from benchmark import PerformanceBenchmark

# Matplotlib Check
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class BaseDialog(tk.Toplevel):
    """A base class for styled popups"""
    def __init__(self, parent, title, w=400, h=300):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=Config.COLOR_BG)
        
        # Center window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (w // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        
        self.transient(parent)
        self.grab_set()
        self.focus_set()

class ResultsDialog(BaseDialog):
    def __init__(self, parent, won, secret_word, restart_cb, exit_cb):
        super().__init__(parent, "Results", 400, 300)
        
        content = tk.Frame(self, bg=Config.COLOR_BG)
        content.pack(expand=True, fill="both", padx=20, pady=20)
        
        title_text = "VICTORY!" if won else "GAME OVER!"
        title_color = Config.COLOR_CORRECT if won else "#e74c3c"
        
        tk.Label(content, text=title_text, font=("Helvetica Neue", 28, "bold"), 
                 bg=Config.COLOR_BG, fg=title_color).pack(pady=(10, 10))
        
        tk.Label(content, text="The correct word was:", font=("Arial", 12), 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT).pack()
        
        tk.Label(content, text=secret_word.upper(), font=("Helvetica Neue", 24, "bold"), 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT).pack(pady=10)
        
        btn_frame = tk.Frame(content, bg=Config.COLOR_BG)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="PLAY AGAIN", command=lambda: [self.destroy(), restart_cb()],
                  bg=Config.COLOR_CORRECT, fg="white", font=("Arial", 11, "bold"), width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="EXIT", command=lambda: [self.destroy(), exit_cb()],
                  bg=Config.COLOR_ABSENT, fg="white", font=("Arial", 11, "bold"), width=10).pack(side=tk.LEFT, padx=10)

class HintDialog(BaseDialog):
    def __init__(self, parent, char, idx):
        super().__init__(parent, "Hint", 350, 180)
        
        tk.Label(self, text="HINT", font=("Helvetica Neue", 20, "bold"), 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT).pack(pady=(15, 10))
        
        block_frame = tk.Frame(self, bg=Config.COLOR_BG)
        block_frame.pack(pady=10)
        
        for i in range(5):
            if i == idx:
                bg_color = Config.COLOR_CORRECT
                text = char.upper()
                fg_color = "white"
            else:
                bg_color = Config.COLOR_EMPTY
                text = ""
                fg_color = Config.COLOR_TEXT
            
            lbl = tk.Label(block_frame, text=text, width=4, height=2,
                           font=Config.FONT_GRID, bg=bg_color, fg=fg_color,
                           relief="solid", borderwidth=1)
            lbl.pack(side=tk.LEFT, padx=2)
            
        tk.Label(self, text=f"Character '{char.upper()}' is at position {idx+1}", 
                 bg=Config.COLOR_BG, fg=Config.COLOR_TEXT, font=("Arial", 10, "italic")).pack(pady=5)

class BenchmarkDialog(tk.Toplevel):
    """Handles the complex Performance Dashboard"""
    def __init__(self, parent, word_list, solver_classes):
        super().__init__(parent)
        self.title("Search Algorithm Assessment")
        self.geometry("1100x900")
        self.configure(bg="white")
        self.word_list = word_list
        self.solver_classes = solver_classes
        
        if not HAS_MATPLOTLIB:
            tk.Label(self, text="Matplotlib not found!", fg="red").pack()
            return

        self.setup_ui()

    def setup_ui(self):
        ctrl_frame = tk.Frame(self, bg="white")
        ctrl_frame.pack(pady=10)
        
        tk.Label(ctrl_frame, text="Run 10 Games using:", bg="white", font=("Arial", 12)).pack(side=tk.LEFT)
        self.algo_combobox = ttk.Combobox(ctrl_frame, values=["BFS", "DFS", "UCS", "A*"], state="readonly")
        self.algo_combobox.set("A*")
        self.algo_combobox.pack(side=tk.LEFT, padx=10)
        
        tk.Button(ctrl_frame, text="Start Assessment", bg="#d35400", fg="white",
                  command=self.run_benchmark).pack(side=tk.LEFT)

        self.insight_frame = tk.LabelFrame(self, text="AI Insights", bg="white", font=("Arial", 10, "bold"))
        self.insight_frame.pack(fill="x", padx=20, pady=5)
        self.insight_lbl = tk.Label(self.insight_frame, text="Select an algorithm and run to see analytics.", 
                                    justify="left", bg="white", fg="#333")
        self.insight_lbl.pack(fill="x", padx=10, pady=10)

        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def run_benchmark(self):
        algo_name = self.algo_combobox.get()
        self.config(cursor="wait")
        self.insight_lbl.config(text=f"Running simulation for {algo_name}... Please wait...")
        self.update()
        
        solver_class = self.solver_classes[algo_name]
        bench = PerformanceBenchmark(self.word_list, solver_class, num_games=10)
        
        def task():
            stats = bench.run()
            if self.winfo_exists():
                self.after(0, lambda: self.show_results(algo_name, stats))
        
        threading.Thread(target=task, daemon=True).start()

    def show_results(self, algo_name, stats):
        self.config(cursor="")
        if not stats: return
        
        # Text Analytics
        insight = f"--- PERFORMANCE REPORT: {algo_name} ---\n"
        insight += f"TIME (µs): Avg {stats['avg_time']:.2f} | Peak {stats['max_time']:.2f}\n"
        insight += f"MEMORY (B): Avg {stats['avg_mem']:.2f} | Peak {stats['max_mem']:.2f}\n"
        insight += f"NODES: Avg {stats['avg_nodes']:.1f} | Peak {stats['max_nodes']}\n"
        insight += f"GUESSES: Avg {stats['avg_guesses']:.1f} | Peak {stats['max_guesses']}"
        self.insight_lbl.config(text=insight)

        # Charts
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        
        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        fig.suptitle(f'{algo_name} Metrics', fontsize=14)
        
        def draw(ax, title, avg, peak, unit, cols):
            ax.bar(['Avg', 'Peak'], [avg, peak], color=cols)
            ax.set_title(title); ax.set_ylabel(unit)
            for i, v in enumerate([avg, peak]): ax.text(i, v, f'{v:.1f}', ha='center', va='bottom')

        draw(axs[0,0], "Time", stats['avg_time'], stats['max_time'], "µs", ['#3498db', '#2980b9'])
        draw(axs[0,1], "Memory", stats['avg_mem'], stats['max_mem'], "Bytes", ['#9b59b6', '#8e44ad'])
        draw(axs[1,0], "Nodes", stats['avg_nodes'], stats['max_nodes'], "Count", ['#e67e22', '#d35400'])
        draw(axs[1,1], "Guesses", stats['avg_guesses'], stats['max_guesses'], "Count", ['#2ecc71', '#27ae60'])
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)