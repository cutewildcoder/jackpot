        # Jackpot Simulator

A small Python slot-machine style jackpot simulator with a graphical interface. Spin the reels, track your credits and session stats, and adjust the jackpot, odds, stake, and starting balance. This is for entertainment only; no real money is involved.

## Requirements

- Python 3.10 or newer
- Tkinter, which is included with many Python installations

## Run the graphical app

From the project directory, run:

```bash
python jackpot_simulator.py
```

Click **SPIN** to play. Each spin costs the configured stake. A jackpot win pays the configured jackpot amount. Use the fields at the bottom and click **Apply settings / reset** to start a fresh session with new values.

## Settings

| Setting | Meaning | Default |
| --- | --- | ---: |
| Jackpot | Credits awarded for a jackpot | 1,000 |
| Odds (1 in) | One chance in this many per spin | 10,000 |
| Stake | Credits spent per spin | 1 |
| Starting credits | Credits at the beginning of a session | 100 |

Set odds to `1` to make every spin a jackpot, which can be useful for trying out the win display.

## Batch simulation

You can also simulate a number of spins in the terminal and print a summary:

```bash
python jackpot_simulator.py --plays 100000
```

Optional command-line settings:

```bash
python jackpot_simulator.py --plays 50000 --jackpot 2500 --odds 5000 --stake 2 --seed 42
```

- `--jackpot`: payout in credits
- `--odds`: denominator for the jackpot odds
- `--stake`: cost per spin
- `--credits`: starting credits for the graphical session
- `--seed`: set a random seed for a repeatable sequence
- `--plays`: run a batch simulation instead of opening the graphical interface

For example, to open the app with 250 credits and 1-in-500 odds:

```bash
python jackpot_simulator.py --credits 250 --odds 500
```

## Notes

The batch simulation reports total plays, jackpot wins, credits spent, credits paid out, net result, and observed win rate. Results are random unless a seed is provided.
