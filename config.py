# config.py

class Config:
    WORD_LENGTH = 5
    
    # --- THEME: LIGHT YELLOW (LEMON) ---
    COLOR_BG = "#FFF9C4"        # Light Yellow Background
    COLOR_EMPTY = "#FFFFFF"     # Darker Yellow for empty tile borders/fill
    
    COLOR_CORRECT = "#6aaa64"   # Standard Green
    COLOR_PRESENT = "#c9b458"   # Standard Yellow
    COLOR_ABSENT = "#787c7e"    # Standard Gray
    
    COLOR_KEY_DEFAULT = "#d3d6da" # Light Gray for keyboard keys
    COLOR_TEXT = "#000000"      # BLACK text (Essential for light background)
    
    # Log Colors
    COLOR_LOG_BG = "#FFF59D"    # Slightly deeper yellow for log area
    COLOR_LOG_TEXT = "#333333"  # Dark gray text for logs
    COLOR_LOG_GREEN = "#2e7d32" # Darker green for text readability
    COLOR_LOG_YELLOW = "#f57f17" # Darker orange-yellow for text readability
    
    # Fonts
    FONT_TITLE = ("Helvetica Neue", 24, "bold")
    FONT_GRID = ("Helvetica Neue", 18, "bold") 
    FONT_KEY = ("Helvetica Neue", 12, "bold")   
    FONT_LOG = ("Consolas", 10) 
    
    # Letter Frequencies for Heuristics
    LETTER_FREQ = {
        'e': 11.16, 'a': 8.50, 'r': 7.58, 'i': 7.54, 'o': 7.16, 't': 6.95,
        'n': 6.65, 's': 5.74, 'l': 5.49, 'c': 4.54, 'u': 3.63, 'd': 3.38,
        'p': 3.17, 'm': 3.01, 'h': 3.00, 'g': 2.47, 'b': 2.07, 'f': 1.81,
        'y': 1.78, 'w': 1.29, 'k': 1.10, 'v': 1.01, 'x': 0.29, 'z': 0.27,
        'j': 0.20, 'q': 0.20
    }