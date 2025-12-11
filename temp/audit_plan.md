# Audit Plan

## Objectives
- Validate every orbital and terrestrial economic calculation in `static/js/math.js`.
- Exercise the model with multiple non-default set points to probe sensitivity.
- Cross-check results against physics/industry heuristics (mass-to-orbit limits, NGCC performance, etc.).
- Produce a third-party audit log under `/audit` plus a variance report covering any discrepancies.

## Method
1. Map each calculation step in `calculateOrbital` and `calculateTerrestrial` to its physical/economic assumption.
2. Recompute baseline outputs using both the JS module (Node) and the parity script (`temp/check_numbers.py`).
3. Build a small harness to sweep alternative scenarios:
   - Optimistic Starship (cheap launch & higher specific power)
   - Pessimistic orbital (higher degradation + lower sun fraction)
   - High gas price terrestrial stress test
   - Low capacity factor terrestrial case
4. Compare outcomes to reference industry values and flag anything outside plausible ranges.
5. Summarize findings, sanity checks, and failed calculations (if any) in `/audit/third_party_audit.md`.
