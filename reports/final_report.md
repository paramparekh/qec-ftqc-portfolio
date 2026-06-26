# Final Technical Report — Draft
# Circuit-Level Evaluation and Fault-Tolerant Gadget Simulation for Surface and Bivariate Bicycle Codes

**Status:** In Progress — populate during Phases 2–7  
**Target:** 6–10 pages, publication-style write-up

---

## 1. Introduction
*To be written in Phase 7.*
- Why fault-tolerant QEC matters
- What this project implements and why it matters for industry

## 2. Background
*To be written in Phase 7, drawing on each phase's implementation.*
- Stabilizer / CSS codes
- Decoding and detector error models
- BB / qLDPC motivation

## 3. Methods
*Populated as each phase is completed.*
- Code construction (GF(2) linear algebra, CSS, BB polynomial construction)
- Circuit generation (syndrome extraction, memory experiments)
- Noise models (phenomenological vs circuit-level)
- Decoders (MWPM, BP-OSD)
- Verification (GF(2) rank, MILP distance)

## 4. Experiments & Results
*Tables and plots added as phases complete.*

### 4.1 Surface Code Baseline (Phase 2)
- LER vs physical error rate for d=3, 5, 7
- Pseudo-threshold estimate

### 4.2 Bivariate Bicycle / qLDPC Reproduction (Phase 3)
- Parameter tables: n, k, d, FOM
- Decoder comparison

### 4.3 Circuit-Level Simulations (Phase 4)
- Phenomenological vs circuit-level noise gap
- Hook-error sensitivity

### 4.4 FT Gadget Demonstrations (Phase 5)
- Logical state preparation
- Logical measurement
- Magic-state resource estimator

### 4.5 Resource Estimation (Phase 6)
- Toy algorithm mapped to logical budget
- Surface vs BB/qLDPC comparison table

## 5. Limitations
- Circuit scheduling simplifications
- Decoder assumptions
- Finite-size effects
- Hardware connectivity assumptions

## 6. Future Work
- Code surgery and lattice surgery
- Magic-state factories at scale
- qLDPC compilation for real hardware
- Hardware execution (IBM/Google backends)

## References
*(To be completed — see execution plan reading list)*
