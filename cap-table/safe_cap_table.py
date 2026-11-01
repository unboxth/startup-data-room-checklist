#!/usr/bin/env python3
"""Post-money SAFE conversion + priced round cap table (no dependencies).

Implements the conversion described in Y Combinator's Post-Money SAFE User Guide:
  * Company Capitalization = all issued shares + outstanding and promised options
    + the existing unissued pool + the SAFE conversion shares. It EXCLUDES the new
    money and the option pool increase adopted in the priced round.
  * Safe Price      = Post-Money Valuation Cap / Company Capitalization
  * Discount Price  = round price per share x (1 - discount)
  * Each SAFE converts at the lower of the prices that apply to it.
The priced round is solved so that new investors own investment / post-money and
the unissued pool equals the target % of the post-round fully diluted total.

Shares are rounded down to whole shares, as YC does in its worked examples.
This is a model for planning, not legal advice. Your lawyer's closing cap table wins.

Usage:
    python3 safe_cap_table.py examples/yc-example-1.json
    python3 safe_cap_table.py examples/yc-example-1.json --csv out.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field


@dataclass
class Safe:
    name: str
    amount: float
    cap: float | None = None        # post-money valuation cap (None = uncapped)
    discount: float = 0.0           # e.g. 0.20 for 20%; YC uncapped = discount form


@dataclass
class Inputs:
    holders: dict[str, int]                         # issued shares + options by name
    unissued_pool: int
    safes: list[Safe] = field(default_factory=list)
    pre_money: float | None = None                   # priced round, optional
    investment: float = 0.0
    pool_target_post: float = 0.0                    # e.g. 0.10 for 10% after the round


def _round_solve(cap_base_excl_pool_increase: float, unissued: float, pre: float, inv: float, target: float):
    """Return (pool_increase, new_shares, price, post_total) for the priced round.

    C = company capitalization incl. SAFE shares (before pool increase/new money).
    New money fraction f = inv / (pre + inv). Unknowns: total T, pool increase dP.
      (1 - f) T = C + dP      (pre-money shares include the pool increase)
      U + dP    = target T
    """
    C, U = cap_base_excl_pool_increase, unissued
    f = inv / (pre + inv)
    T = (C - U) / (1 - f - target) if target > 0 else C / (1 - f)
    dP = target * T - U
    if dP < 0:  # existing pool already big enough
        dP = 0.0
        T = C / (1 - f)
    new_shares = f * T
    price = pre / (C + dP)
    return dP, new_shares, price, T


def solve(inp: Inputs, max_iter: int = 200):
    base = sum(inp.holders.values()) + inp.unissued_pool
    # Start with every capped SAFE converting at its cap (closed form).
    capped = [s for s in inp.safes if s.cap]
    sold = sum(s.amount / s.cap for s in capped)
    if sold >= 1:
        raise ValueError("SAFEs sell 100% or more of the company: check amounts and caps")
    C = base / (1 - sold)
    shares = {s.name: (s.amount / s.cap) * C if s.cap else 0.0 for s in inp.safes}
    price = None
    how = {s.name: "cap" for s in inp.safes}
    if inp.pre_money:
        for _ in range(max_iter):
            C = base + sum(shares.values())
            dP, new_sh, price, T = _round_solve(C, inp.unissued_pool, inp.pre_money, inp.investment, inp.pool_target_post)
            new = {}
            for s in inp.safes:
                options = []
                if s.cap:
                    options.append((s.cap / C, "cap"))
                options.append((price * (1 - s.discount), "discount" if s.discount else "round price"))
                p, label = min(options, key=lambda x: x[0])
                new[s.name] = s.amount / p
                how[s.name] = label
            if all(abs(new[k] - shares[k]) < 1e-6 for k in new):
                shares = new
                break
            shares = new
        else:
            raise RuntimeError("conversion did not converge")
    elif any(not s.cap for s in inp.safes):
        raise ValueError("uncapped SAFEs need a priced round (pre_money) to convert")

    floor = {k: math.floor(v + 1e-6) for k, v in shares.items()}
    C_exact = base + sum(shares.values())
    rows = [(k, v) for k, v in inp.holders.items()]
    rows += [(f"{k} (SAFE, {how[k]})", floor[k]) for k in floor]
    result = {"company_capitalization": math.floor(C_exact + 1e-6),
              "safe_prices": {s.name: (s.cap / C_exact if s.cap else None) for s in inp.safes},
              "conversion": how}
    before = rows + [("Unissued option pool", inp.unissued_pool)]
    if inp.pre_money:
        dP, new_sh, price, T = _round_solve(C_exact, inp.unissued_pool, inp.pre_money, inp.investment, inp.pool_target_post)
        after = rows + [("New investors (priced round)", math.floor(new_sh + 1e-6)),
                        ("Unissued option pool (old + increase)", math.floor(inp.unissued_pool + dP + 1e-6))]
        result.update(round_price=price, pool_increase=dP, post_money=inp.pre_money + inp.investment)
    else:
        after = None
    result["before_round"] = before
    result["after_round"] = after
    return result


def _table(rows):
    total = sum(v for _, v in rows)
    return [(k, v, v / total * 100) for k, v in rows] + [("Total fully diluted", total, 100.0)]


def load(path: str) -> Inputs:
    with open(path) as fh:
        d = json.load(fh)
    return Inputs(holders=d["holders"], unissued_pool=d.get("unissued_pool", 0),
                  safes=[Safe(**s) for s in d.get("safes", [])],
                  pre_money=d.get("pre_money"), investment=d.get("investment", 0.0),
                  pool_target_post=d.get("pool_target_post", 0.0))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", help="JSON file, see examples/")
    ap.add_argument("--csv", help="write the post-round (or post-SAFE) table to this CSV")
    a = ap.parse_args(argv)
    r = solve(load(a.inputs))
    print(f"Company capitalization (SAFE conversion): {r['company_capitalization']:,}")
    for k, p in r["safe_prices"].items():
        print(f"  {k}: safe price {('$%.4f' % p) if p else 'n/a (uncapped)'}, converts at {r['conversion'][k]}")
    if r.get("round_price"):
        print(f"Round price per share: ${r['round_price']:.4f}   pool increase: {r['pool_increase']:,.0f}   post-money: ${r['post_money']:,.0f}")
    for title, rows in (("As converted, just before the round", r["before_round"]), ("After the round", r["after_round"])):
        if not rows:
            continue
        print(f"\n{title}")
        for k, v, pct in _table(rows):
            print(f"  {k:<48}{v:>14,}{pct:>9.2f}%")
    if a.csv:
        rows = _table(r["after_round"] or r["before_round"])
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Holder", "Shares", "Fully diluted %"])
            for k, v, pct in rows:
                w.writerow([k, v, f"{pct:.2f}%"])
        print(f"\nWrote {a.csv}")


if __name__ == "__main__":
    sys.exit(main())
