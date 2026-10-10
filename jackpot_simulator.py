#!/usr/bin/env python3
"""A graphical jackpot simulator with an optional command-line batch mode."""

from __future__ import annotations

import argparse
import random
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk


@dataclass
class Game:
    jackpot: int = 1_000
    jackpot_odds: int = 10_000
    stake: int = 1
    rng: random.Random | None = None

    def __post_init__(self) -> None:
        if self.jackpot < 0:
            raise ValueError("jackpot must be non-negative")
        if self.jackpot_odds < 1:
            raise ValueError("odds must be at least 1")
        if self.stake < 1:
            raise ValueError("stake must be at least 1")
        if self.rng is None:
            self.rng = random.Random()

    def play(self) -> tuple[bool, int]:
        assert self.rng is not None
        won = self.rng.randrange(self.jackpot_odds) == 0
        return won, self.jackpot if won else 0


def simulate(plays: int, game: Game) -> dict[str, int | float]:
    if plays < 0:
        raise ValueError("plays must be non-negative")
    wins = total_paid = 0
    for _ in range(plays):
        won, payout = game.play()
        wins += int(won)
        total_paid += payout
    spent = plays * game.stake
    return {"plays": plays, "wins": wins, "spent": spent, "paid_out": total_paid,
            "net": total_paid - spent, "win_rate": wins / plays if plays else 0.0}


class JackpotApp:
    BG = "#101522"
    PANEL = "#1b2435"
    GOLD = "#ffd166"
    WHITE = "#f4f7fb"
    MUTED = "#aab4c5"

    def __init__(self, root: tk.Tk, jackpot: int, odds: int, stake: int, credits: int, seed: int | None):
        self.root = root
        self.root.title("Jackpot Simulator")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)
        self.game = Game(jackpot, odds, stake, random.Random(seed))
        self.starting_credits = credits
        self.credits = credits
        self.plays = 0
        self.wins = 0
        self.total_paid = 0
        self._build_ui()
        self._update_stats()

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TEntry", fieldbackground="#f4f7fb", foreground="#172033", padding=6)
        outer = tk.Frame(self.root, bg=self.BG, padx=28, pady=24)
        outer.pack()
        tk.Label(outer, text="LUCKY JACKPOT", bg=self.BG, fg=self.GOLD,
                 font=("Helvetica", 12, "bold")).pack()
        tk.Label(outer, text="Jackpot Simulator", bg=self.BG, fg=self.WHITE,
                 font=("Helvetica", 25, "bold")).pack(pady=(3, 18))

        slot = tk.Frame(outer, bg=self.PANEL, padx=18, pady=14)
        slot.pack(fill="x")
        self.reels = []
        for _ in range(3):
            reel = tk.Label(slot, text="🍒", bg="#f4f7fb", fg="#172033", width=3,
                            font=("Apple Color Emoji", 38), padx=8, pady=4)
            reel.pack(side="left", padx=6)
            self.reels.append(reel)

        self.message = tk.Label(outer, text="Press SPIN to try your luck", bg=self.BG,
                                fg=self.MUTED, font=("Helvetica", 12))
        self.message.pack(pady=12)
        self.spin_button = tk.Button(outer, text="SPIN", command=self.spin,
                                     bg=self.GOLD, fg="#172033", activebackground="#ffe29a",
                                     activeforeground="#172033", relief="flat", cursor="hand2",
                                     font=("Helvetica", 15, "bold"), padx=35, pady=10)
        self.spin_button.pack()

        stats = tk.Frame(outer, bg=self.PANEL, padx=15, pady=12)
        stats.pack(fill="x", pady=(18, 12))
        self.credit_label = tk.Label(stats, bg=self.PANEL, fg=self.WHITE, font=("Helvetica", 15, "bold"))
        self.credit_label.grid(row=0, column=0, sticky="w", padx=(0, 36))
        self.jackpot_label = tk.Label(stats, bg=self.PANEL, fg=self.GOLD, font=("Helvetica", 15, "bold"))
        self.jackpot_label.grid(row=0, column=1, sticky="e")
        self.stats_label = tk.Label(stats, bg=self.PANEL, fg=self.MUTED, font=("Helvetica", 10))
        self.stats_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(7, 0))
        stats.grid_columnconfigure(1, weight=1)

        settings = tk.Frame(outer, bg=self.BG)
        settings.pack(fill="x", pady=(2, 0))
        self.settings_vars = []
        for label, value in (("Jackpot", self.game.jackpot), ("Odds (1 in)", self.game.jackpot_odds),
                             ("Stake", self.game.stake), ("Starting credits", self.starting_credits)):
            field = tk.Frame(settings, bg=self.BG)
            field.pack(side="left", expand=True, padx=3)
            tk.Label(field, text=label, bg=self.BG, fg=self.MUTED, font=("Helvetica", 9)).pack(anchor="w")
            var = tk.StringVar(value=str(value))
            ttk.Entry(field, textvariable=var, width=13).pack(fill="x", pady=(3, 0))
            self.settings_vars.append(var)
        tk.Button(outer, text="Apply settings / reset", command=self.reset,
                  bg="#344258", fg=self.WHITE, activebackground="#455873", activeforeground=self.WHITE,
                  relief="flat", cursor="hand2", font=("Helvetica", 10), padx=12, pady=7).pack(pady=(12, 0))
        tk.Label(outer, text="For entertainment only · No real money", bg=self.BG, fg="#7f8ba0",
                 font=("Helvetica", 9)).pack(pady=(12, 0))

    def _update_stats(self) -> None:
        self.credit_label.config(text=f"CREDITS  {self.credits:,}")
        self.jackpot_label.config(text=f"JACKPOT  {self.game.jackpot:,}")
        rate = f"{self.wins / self.plays:.2%}" if self.plays else "—"
        self.stats_label.config(text=f"Plays: {self.plays}     Jackpots: {self.wins}     Paid out: {self.total_paid:,}     Win rate: {rate}")
        self.spin_button.config(state="normal" if self.credits >= self.game.stake else "disabled")

    def spin(self) -> None:
        self.credits -= self.game.stake
        self.plays += 1
        won, payout = self.game.play()
        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣", "🍀"]
        result = ["7️⃣"] * 3 if won else [self.game.rng.choice(symbols) for _ in range(3)]  # type: ignore[union-attr]
        for reel, symbol in zip(self.reels, result):
            reel.config(text=symbol)
        if won:
            self.credits += payout
            self.wins += 1
            self.total_paid += payout
            self.message.config(text=f"JACKPOT! You won {payout:,} credits!", fg=self.GOLD)
        else:
            self.message.config(text=f"No win this time. {self.game.stake} credit(s) played.", fg=self.MUTED)
        self._update_stats()

    def reset(self) -> None:
        try:
            jackpot, odds, stake, credits = (int(v.get()) for v in self.settings_vars)
            if jackpot < 0 or odds < 1 or stake < 1 or credits < 0:
                raise ValueError
            self.game = Game(jackpot, odds, stake, random.Random())
        except ValueError:
            messagebox.showerror("Invalid settings", "Use whole numbers. Jackpot and credits must be 0 or more; odds and stake must be at least 1.")
            return
        self.starting_credits = credits
        self.credits = credits
        self.plays = self.wins = self.total_paid = 0
        for reel in self.reels:
            reel.config(text="🍒")
        self.message.config(text="Settings applied. Press SPIN to play!", fg=self.MUTED)
        self._update_stats()


def main() -> None:
    parser = argparse.ArgumentParser(description="Graphical jackpot simulator; use --plays for a batch simulation.")
    parser.add_argument("--jackpot", type=int, default=1_000)
    parser.add_argument("--odds", type=int, default=10_000, help="denominator; 1 means every play wins")
    parser.add_argument("--stake", type=int, default=1)
    parser.add_argument("--credits", type=int, default=100)
    parser.add_argument("--seed", type=int, help="random seed (also makes the GUI sequence repeatable)")
    parser.add_argument("--plays", type=int, help="run a batch simulation in the terminal")
    args = parser.parse_args()
    try:
        game = Game(args.jackpot, args.odds, args.stake, random.Random(args.seed))
        if args.credits < 0:
            raise ValueError("credits must be non-negative")
        if args.plays is not None:
            result = simulate(args.plays, game)
            print(f"Plays: {result['plays']} | Jackpots: {result['wins']} | Spent: {result['spent']} | Paid out: {result['paid_out']} | Net: {result['net']} | Win rate: {result['win_rate']:.4%}")
            return
    except ValueError as exc:
        parser.error(str(exc))
    root = tk.Tk()
    JackpotApp(root, args.jackpot, args.odds, args.stake, args.credits, args.seed)
    root.mainloop()


if __name__ == "__main__":
    main()
