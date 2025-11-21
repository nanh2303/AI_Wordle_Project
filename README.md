# Wordle AI Project 🧩🤖

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

A fully functional, professional recreation of the popular **Wordle** game, built with Python. This project goes beyond a simple game clone by integrating an **Artificial Intelligence Testbed**, allowing users to visualize, benchmark, and compare different search algorithms (BFS, DFS, UCS, A*) in real-time.

## 📸 Screenshots

| **Main Game Interface** | **Performance Analytics** |
|:-----------------------:|:-------------------------:|
| ![Main Game Interface](screenshots/main_game.png) | ![Analytics Dashboard](screenshots/analytics.png) |
> *Note: The interface features a custom "Lemon Mode" light theme for better readability.*

---

## 📂 Project Structure

The source code is modularized to ensure maintainability, scalability, and clean separation of concerns (MVC Architecture).

```text
WordleProject/
│
├── main.py              # 🚀 Entry Point: Run this file to launch the application.
├── config.py            # ⚙️ Configuration: Stores constants, colors (Lemon Theme), and fonts.
├── game.py              # 🎮 Model: Handles core game logic, validation, and state management.
├── solvers.py           # 🧠 AI Logic: Implementation of BFS, DFS, UCS, and A* algorithms.
├── benchmark.py         # 📊 Analytics: Engine for running background simulations and gathering stats.
├── utils.py             # 🛠️ Utilities: Helper functions (e.g., loading the dictionary).
├── words.txt            # 📖 Dictionary: A database of valid 5-letter words.
│
└── ui/                  # 🎨 User Interface Package
    ├── __init__.py      # Package initialization.
    ├── main_window.py   # The main GUI controller and layout manager.
    └── dialogs.py       # Modular popup windows (Results, Hints, Benchmark Dashboard).
```

---

## 🚀 Installation & Setup

### Prerequisites
* **Python 3.x** installed on your system.
* **Matplotlib** library (required for generating performance charts).

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/wordle-ai-project.git](https://github.com/your-username/wordle-ai-project.git)
    cd wordle-ai-project
    ```

2.  **Install dependencies:**
    ```bash
    pip install matplotlib
    ```

3.  **Run the Game:**
    ```bash
    python main.py
    ```

---

## 🎮 Game Rules

1.  **Objective:** Guess the hidden **5-letter word** within **6 attempts**.
2.  **Color Feedback:**
    * 🟩 **Green:** The letter is correct and in the correct position.
    * 🟨 **Yellow:** The letter is in the word but in the wrong position.
    * ⬜ **Gray:** The letter is not in the word at all.
3.  **Winning:** Guess the word correctly to see the Victory screen!

---

## ✨ Features

### For Players
* **Interactive GUI:** A responsive, resizeable window with a clean "Lemon" light theme.
* **Smart Hints:** Stuck? Click the `💡 Hint` button.
    * *Logic:* If you have misplaced letters, it reveals their true position. If not, it reveals a new letter entirely.
* **Visual Keyboard:** The on-screen keyboard updates keys (Green/Yellow/Gray) in real-time to track used letters.
* **Game Logs:** A side panel records every move, hint, and AI decision for review.

### For Developers & Researchers
* **Auto-Solve:** Watch the AI play the game by clicking `▶ Auto`.
* **Algorithm Selection:** Choose between 4 distinct search strategies.
* **Performance Dashboard:** Click `📊 Performance` to run a 10-game simulation in the background.
    * **Metrics:** Search Time (µs), Memory Usage (Bytes), Expanded Nodes, and Average Guesses.
    * **Visuals:** Matplotlib charts comparing Average vs. Peak performance.

---

## 🧠 AI Algorithms Implemented

This project serves as a comparative study of Search Algorithms in a constraint satisfaction problem (Wordle).

### 1. Breadth-First Search (BFS)
* **Strategy:** Explores the search tree level by level. It blindly tries the first valid word available in the filtered list.
* **Pros/Cons:** Finds a solution, but inefficient. Expands many nodes without "thinking" ahead.

### 2. Depth-First Search (DFS)
* **Strategy:** Explores as deep as possible along each branch. It picks the *last* available word in the list.
* **Pros/Cons:** Extremely fast execution time but often makes terrible guesses, leading to a low win rate or high guess count.

### 3. Uniform Cost Search (UCS)
* **Cost Function:** Based on **Letter Frequency**.
* **Strategy:** Prioritizes words containing high-frequency English letters (e.g., E, A, R) to maximize information gain.
* **Pros/Cons:** Better than BFS/DFS, but slower than A* because it lacks a goal-oriented heuristic.

### 4. A* Search (A-Star) 🌟
* **Heuristic:** Positional Letter Frequency + Information Entropy.
* **Strategy:** Calculates a score for every candidate word based on how likely it is to prune the remaining search space.
* **Pros/Cons:** The optimal solver. It typically solves the game in 3-4 guesses with minimal search overhead.

---

## 🔮 Future Improvements

* **Hard Mode:** Enforce a rule where revealed hints *must* be used in subsequent guesses.
* **Entropy Heuristic:** Upgrade the A* heuristic to use Shannon Entropy calculation ($E = - \sum p \log p$) for mathematically optimal guesses.
* **Save/Load:** Ability to save game statistics and history to a local file.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).