"""
Rock Paper Scissors - Professional Edition
A GUI game built with tkinter.
"""

import os
import tkinter as tk
from tkinter import messagebox
import random
import winsound
from PIL import Image, ImageTk


# ---------- Sound Effects ----------
def play_sound(result):
    """Play a beep sound based on the round result."""
    if result == "win":
        winsound.Beep(1000, 300)   # happy high beep
    elif result == "lose":
        winsound.Beep(300, 400)    # sad low beep
    else:
        winsound.Beep(600, 200)    # neutral beep for draw


# ---------- Game Constants ----------
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo", "image.jpg")
CHOICES = ["Rock", "Paper", "Scissors"]
ICONS = {"Rock": "\u270A", "Paper": "\u270B", "Scissors": "\u270C"}
WIN_RULES = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper",
}
COLORS = {
    "bg": "#1e1e2e",
    "panel": "#313244",
    "accent": "#89b4fa",
    "win": "#a6e3a1",
    "lose": "#f38ba8",
    "draw": "#f9e2af",
    "text": "#cdd6f4",
}


# ---------- Game Logic ----------
class GameLogic:
    """Decides who wins a round. Pure logic, no GUI."""

    @staticmethod
    def decide(player, computer):
        if player == computer:
            return "draw"
        if WIN_RULES[player] == computer:
            return "win"
        return "lose"

    @staticmethod
    def computer_choice():
        return random.choice(CHOICES)


# ---------- Main Application ----------
class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("640x780")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        # Load and set the window icon (shown in the title bar / taskbar)
        self._set_window_icon()

        # Score state
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 0
        self.history = []

        self._build_ui()

    # ----- UI Construction -----
    def _build_ui(self):
        self._build_logo()
        self._build_header()
        self._build_scoreboard()
        self._build_arena()
        self._build_buttons()
        self._build_history()
        self._build_footer()

    def _set_window_icon(self):
        """Set the logo as the window's title-bar / taskbar icon."""
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((64, 64))
            self.window_icon = ImageTk.PhotoImage(img)
            self.root.iconphoto(True, self.window_icon)
        except Exception:
            pass

    def _build_logo(self):
        """Show the logo image at the top of the window."""
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((220, 124))
            self.logo_image = ImageTk.PhotoImage(img)
            tk.Label(
                self.root, image=self.logo_image, bg=COLORS["bg"]
            ).pack(pady=(15, 5))
        except Exception:
            pass

    def _build_header(self):
        header = tk.Label(
            self.root,
            text="ROCK  PAPER  SCISSORS",
            font=("Helvetica", 22, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["accent"],
        )
        header.pack(pady=(20, 5))

        sub = tk.Label(
            self.root,
            text="Choose your weapon and beat the computer!",
            font=("Helvetica", 11),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        sub.pack(pady=(0, 10))

    def _build_scoreboard(self):
        frame = tk.Frame(self.root, bg=COLORS["panel"], bd=0, relief="flat")
        frame.pack(fill="x", padx=40, pady=5)

        self.round_label = tk.Label(
            frame, text="Round: 0", font=("Helvetica", 12, "bold"),
            bg=COLORS["panel"], fg=COLORS["text"]
        )
        self.round_label.pack(side="left", padx=20, pady=10)

        self.score_label = tk.Label(
            frame, text="You 0  -  0 CPU", font=("Helvetica", 12, "bold"),
            bg=COLORS["panel"], fg=COLORS["accent"]
        )
        self.score_label.pack(side="right", padx=20, pady=10)

    def _build_arena(self):
        arena = tk.Frame(self.root, bg=COLORS["panel"], bd=0, relief="flat")
        arena.pack(fill="x", padx=40, pady=10)

        # Player side
        self.player_icon = tk.Label(
            arena, text="\u270A", font=("Helvetica", 60),
            bg=COLORS["panel"], fg=COLORS["accent"]
        )
        self.player_icon.pack(side="left", padx=40, pady=20)

        # VS / Result
        self.result_label = tk.Label(
            arena, text="VS", font=("Helvetica", 18, "bold"),
            bg=COLORS["panel"], fg=COLORS["text"]
        )
        self.result_label.pack(side="left", padx=20)

        # Computer side
        self.computer_icon = tk.Label(
            arena, text="\u270A", font=("Helvetica", 60),
            bg=COLORS["panel"], fg=COLORS["lose"]
        )
        self.computer_icon.pack(side="right", padx=40, pady=20)

    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=COLORS["bg"])
        btn_frame.pack(pady=10)

        for choice in CHOICES:
            b = tk.Button(
                btn_frame,
                text=f"{ICONS[choice]}  {choice}",
                font=("Helvetica", 13, "bold"),
                width=10,
                bg=COLORS["accent"],
                fg=COLORS["bg"],
                activebackground=COLORS["panel"],
                activeforeground=COLORS["accent"],
                bd=0,
                relief="flat",
                command=lambda c=choice: self.play_round(c),
            )
            b.pack(side="left", padx=8, pady=5)

    def _build_history(self):
        hist_frame = tk.Frame(self.root, bg=COLORS["bg"])
        hist_frame.pack(fill="both", expand=True, padx=40, pady=10)

        tk.Label(
            hist_frame, text="Match History",
            font=("Helvetica", 12, "bold"),
            bg=COLORS["bg"], fg=COLORS["text"]
        ).pack(anchor="w")

        self.history_box = tk.Listbox(
            hist_frame,
            height=6,
            font=("Consolas", 10),
            bg=COLORS["panel"],
            fg=COLORS["text"],
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        self.history_box.pack(fill="both", expand=True, pady=(5, 0))

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=COLORS["bg"])
        footer.pack(side="bottom", fill="x", padx=40, pady=10)

        tk.Button(
            footer, text="Reset", font=("Helvetica", 11, "bold"),
            bg=COLORS["panel"], fg=COLORS["text"], bd=0, relief="flat",
            command=self.reset_game
        ).pack(side="left", padx=5)

        tk.Button(
            footer, text="Quit", font=("Helvetica", 11, "bold"),
            bg=COLORS["lose"], fg=COLORS["bg"], bd=0, relief="flat",
            command=self.root.quit
        ).pack(side="right", padx=5)

    # ----- Game Actions -----
    def play_round(self, player_choice):
        computer_choice = GameLogic.computer_choice()
        outcome = GameLogic.decide(player_choice, computer_choice)
        play_sound(outcome)

        self.round_number += 1
        self.player_icon.config(text=ICONS[player_choice])
        self.computer_icon.config(text=ICONS[computer_choice])

        if outcome == "win":
            self.player_score += 1
            self.result_label.config(text="YOU WIN!", fg=COLORS["win"])
            result_text = "WIN"
        elif outcome == "lose":
            self.computer_score += 1
            self.result_label.config(text="YOU LOSE", fg=COLORS["lose"])
            result_text = "LOSE"
        else:
            self.result_label.config(text="DRAW", fg=COLORS["draw"])
            result_text = "DRAW"

        self._update_scoreboard()
        self._add_history(self.round_number, player_choice, computer_choice, result_text)

        if self.player_score == 5:
            self._declare_winner("You")
        elif self.computer_score == 5:
            self._declare_winner("Computer")

    def _update_scoreboard(self):
        self.round_label.config(text=f"Round: {self.round_number}")
        self.score_label.config(
            text=f"You {self.player_score}  -  {self.computer_score} CPU"
        )

    def _add_history(self, rnd, p, c, result):
        entry = f"R{rnd:>2} | You: {p:<9} | CPU: {c:<9} | {result}"
        self.history.insert(0, entry)
        self.history_box.insert(0, entry)
        if len(self.history) > 50:
            self.history.pop()
            self.history_box.delete(50, tk.END)

    def _declare_winner(self, winner):
        messagebox.showinfo(
            "Game Over",
            f"{winner} won the match!\n\nFinal Score:\nYou {self.player_score} - {self.computer_score} CPU",
        )
        self.reset_game()

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 0
        self.history.clear()
        self.history_box.delete(0, tk.END)
        self.player_icon.config(text="\u270A")
        self.computer_icon.config(text="\u270A")
        self.result_label.config(text="VS", fg=COLORS["text"])
        self._update_scoreboard()


# ---------- Entry Point -----
def main():
    root = tk.Tk()
    RockPaperScissorsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()