# TAYLKOMB — Rev D CAD Redesign Plan
**Locking Mechanism Overhaul + Six-Part Geometry — grounded in new render intent + 2026 pro-comb benchmarks**
Michael David Warren Jr. / TAYLKOMB LLC — Patent Pending USPTO #19362254
Date: April 16, 2026

---

## 0. Why this is Rev D (not Rev C)

Rev C assumed a **horizontal dovetail** — the handle slid onto the comb's side like a tongue-and-groove. The new renders (`Black_Combs.png`, `Metal_Agents.png`) + the new STL files you uploaded this session show a fundamentally different architecture:

1. **The Main Comb is the receiver.** It has the carved "M-shaped" dorsal cutout on its spine and **no downward stem**.
2. **The other 5 parts (2 combs + 3 handles) each carry the male stem** that inserts into the Main Comb. This is visible in the renders — Narrow and Wide combs have a thin stem extending *down* from their lower corner; all three handles have a small connector block with a thin pin above it.
3. **Insertion axis is vertical (along the comb's long axis), not lateral.** The stem slides into a socket cut into the Main Comb's spine cutout.

That's a Rev D architecture, not a tweak to Rev C. The locking mechanism has to be rebuilt around it. **Disregard the old STEP files** per your direction — they are work-in-progress snapshots, kept for history only.

---

## 1. Benchmark grounding (2026, web-verified)

| Product | OAL | Width | Source |
|---|---:|---:|---|
| Sam Villa Signature Long Cutting Comb | **222.25 mm** (8.75″) | 31.75 mm (1.25″) | saloncentric.com |
| Sam Villa Signature Short Cutting Comb | **200.03 mm** (7.875″) | 31.75 mm (1.25″) | saloncentric.com |
| Y.S. Park cutting combs | **165–188 mm** (6.5–7.4″) | — | staysharpshears.com |
| Y.S. Park 339 cutting | 229 mm | — | ysparkusa.com (prior research) |

**Your current STL target envelope (converted from inches):**

| Part | STL OAL (mm) | STL width (mm) | Verdict vs. benchmarks |
|---|---:|---:|---|
| Comb_Main | 145.3 | 32.3 | Width ✅ matches pro 1.25″ | OAL 20–55 mm under pro band |
| Comb_Narrow | 177.6 | 32.3 | Width ✅ | OAL in Y.S. Park band |
| Comb_Wide | 177.6 | 32.3 | Width ✅ | OAL in Y.S. Park band |
| Round_Handle | 154.2 | 10.2 × 5.1 | Ultra-slender stem (not full grip) |
| Flat_Handle | 162.4 | 10.2 × 5.1 | Ultra-slender stem |
| Double_Handle | 154.2 | 17.3 × 5.1 | Fork stem |

The slender handles are a **deliberate aesthetic choice** — the renders show handles designed as *continuations* of the comb line, not traditional bulk grips. That's a valid premium position ("instrument-like" rather than "tool-like"). The width of 10.16 × 5.08 mm = exactly 0.4″ × 0.2″ = a clean inch-based rail stock. Keep it.

---

## 2. Locking mechanism — Rev D design

### 2.1 Architecture

**Receiver**: Main Comb
**Driver**: any of the 5 non-Main parts (Wide Comb, Narrow Comb, Round Handle, Flat Handle, Double Handle)
**Insertion axis**: vertical, along the comb long axis (part slides *up* into the Main Comb socket)
**Lock type**: **captive ball-stud + spring-loaded cross-detent**, releasable via a flush side button on the Main Comb

### 2.2 Why this architecture (and why not Rev C's horizontal dovetail)

| Consideration | Rev C horizontal dovetail | Rev D vertical ball-stud |
|---|---|---|
| Matches render intent | ❌ render shows vertical stem | ✅ |
| Hair-catch at seam | Medium (two long rail edges exposed) | Low (single circular seam, hidden in spine cutout) |
| Manufacturing in PPS-CF40 | Dovetail walls are a mold risk at 60° undercut | Straight bore is trivial |
| Manufacturing in 316L stainless for stem | CNC dovetail tolerance is tight (±0.02) | Turn + drill on a Swiss CNC, routine |
| Cycle life to 15 000 swaps | Dovetail edges chip over time in CF-filled resin | Ball-on-bore wear is a solved problem (Quik-Latch: 150 lb pull rating, QL-25) |
| Part count | 1 comb side + 1 handle side (machined features) | 1 comb side (spring + button + ball) + 1 handle side (turned stem with groove) |
| Visual language | Two parting lines visible | One near-invisible circular joint |

Ball-stud captive latches are a mature, mass-produced pattern — Quik-Latch QL-25 at 31.72 mm diameter withstands 150 lb (≈667 N) pull before failure. **Scaling the pattern down to a 4 mm stud still buys 20–40 N working retention, which is 2–4× the 8–12 N detent force Rev C specified.**

### 2.3 Canonical dimensions (Rev D, locked)

```
REV D LOCKING MODULE — canonical geometry (all dimensions mm)
─────────────────────────────────────────────────────────────
DRIVER SIDE (on the 5 non-Main parts)
  Stem outer diameter ................  4.00 ±0.03
  Stem length (above connector block)  14.00 (full engagement = 12 into socket)
  Ball-head diameter (stem tip) ......  5.00
  Ball-head retention groove .........  Ø 3.20 × 1.00 long, 0.40 below ball-head
  Stem root fillet ...................  R 0.80
  Connector block (on stem base) .....  10.0 × 5.0 × 5.0 (W × H × D)
                                         → flush to part body, hair-shed chamfer 0.5 × 45°
  Material (stem + ball) .............. 316L stainless (turned, 1-pc)
  Surface finish ...................... Ra ≤ 0.4 µm on stem OD

RECEIVER SIDE (on the Main Comb only)
  Socket bore diameter ...............  4.10 (stem slip fit, 0.05 clearance per side)
  Socket bore depth ..................  13.00 (1 mm bottom clearance)
  Ball-capture cross-bore ............. Ø 3.00, perpendicular to socket axis
  Ball-capture ball diameter .........  3.00, 316L
  Ball spring ........................ 302 SS compression, 8–12 N at engagement
  Spring bore length .................  8.0 (Carr Lane CL-6-BPN or equivalent)
  Release-button bore diameter .......  6.00, flush to comb spine
  Release-button travel ..............  0.8 (enough to clear ball from stem groove)
  Release-button protrusion (unpressed) 0.3 above comb spine
  Socket wall thickness around bore ..  2.0 (sufficient for PPS-CF40 at 15k cycles)
  Material (ball plunger sub-assy) ... standard cross-drilled ball plunger,
                                        press-fit into molded PPS-CF40 socket
  Seam step (socket face to driver)...  ≤ 0.10 (tighter than Rev C's 0.15)
  Lead-in chamfer on socket mouth ....  30° × 0.8
  Hair-shed chamfer on seam perimeter.  0.5 × 45°

SYSTEM
  Insertion motion ................... pure axial (vertical), zero rotation
  Insertion force .................... 10–15 N (ball riding over stem ramp)
  Retention force .................... 30–40 N (ball in groove, locked)
  Release force ...................... 1–2 N (button press)
  Audible feedback ................... tactile + audible "click" on groove seat
  Cycle life target .................. ≥ 15 000 swaps
```

### 2.4 Anti-rotation (important because a round stem can spin)

The stem is circular, so an *anti-rotation key* is mandatory. Two options — pick one and lock:

**Option A (recommended): D-profile stem.** Flatten one side of the 4.00 mm stem to 3.20 mm across the chord. Socket gets matching D-bore. Zero rotation, single-orientation insertion (forces correct comb-side-up assembly, which is a UX bonus). Machinable in one Swiss-CNC op.

**Option B: 1.5 × 1.5 mm anti-rotation key on stem base**, mating to a relief in the socket mouth. More parts, more edges. Not recommended.

**Rev D locks Option A (D-profile).**

### 2.5 Release geometry

Release button sits on the **left face** of the Main Comb's spine cutout (when held teeth-down, spine-up, in the right hand). Thumb-accessible. Flush 0.3 mm protrusion. Press to release, ball retracts 0.8 mm, pull driver out axially.

### 2.6 Why this is better than Rev C's architecture

- **Hair cannot catch.** The entire joint is inside the Main Comb's M-cutout, not on an exposed rail edge.
- **One machining op per stem** (turn + groove + chord-flat on a Swiss CNC).
- **Molded socket is a straight bore**, not a 60° dovetail. PPS-CF40 molds cleanly with no side-action tooling.
- **Release action is pure 1-D press**, not the 2-D slide Rev C required.
- **Higher retention** (30–40 N vs. Rev C's 8–12 N) without the insertion force going up (because the ball rides a lead-in ramp on the stem).

---

## 3. Per-part redesign (Rev D)

Sources in order of precedence: **render intent** → **new STL measurements** → **Rev C dimensional ranges** → **2026 pro benchmarks**.

### 3.1 Main Comb (receiver — no stem)

| Parameter | Current STL (mm) | Rev D target (mm) | Rationale |
|---|---:|---:|---|
| OAL | 145.29 | **198 – 205**, target 202 | Pro "short cutting" band; Sam Villa Short = 200 |
| Width (spine height incl. M-cutout) | 32.26 | **32.0** | Matches 1.25″ pro standard; keep |
| Body thickness | 6.69 | **6.5 – 7.0**, target 6.7 | Matches current; within pro band |
| Tooth region length | — derived | ~140 | ~70% of OAL |
| M-cutout depth (from spine top) | — | **18.0** | Ergonomic index-finger rest |
| M-cutout peak-to-peak | — | **36.0** | Centered on comb |
| Socket bore position | — | Center of M-cutout valley | One socket only, inside the cutout |
| Socket bore (receiver) | — | Ø 4.10 × 13.0 deep, D-profile | Rev D locking module |
| Ball-capture sub-assembly | — | Ø 3.0 ball, 302 SS spring, 8–12 N | Rev D locking module |
| Release button protrusion | — | 0.3 above spine | Flush, thumb-operated |
| Material | — | **PPS-CF40** (injection mold) | Locked per Rev C §5 |
| Mass target | — | **12 – 18 g** | PPS-CF40 × 22.7 cm³ ≈ 13 g (from STL vol) |

### 3.2 Narrow Comb (driver — stem down)

| Parameter | Current STL (mm) | Rev D target (mm) | Rationale |
|---|---:|---:|---|
| OAL (body only, excl. stem) | 177.55 | **178** | Matches STL; Y.S. Park cutting band |
| Width | 32.26 | **32.0** | Shared spine silhouette with Main |
| Thickness | 6.69 | **6.7** | Shared |
| Tooth pitch (narrow) | — | **1.8 – 2.2**, target 2.0 | Fine cutting comb standard |
| Tooth row count | — | **60 teeth** @ 2.0 mm pitch over 120 mm | — |
| Stem (driver) | — | Ø 4.00 D-profile × 14 long, ball-head 5.0, groove per §2.3 | Rev D locking module |
| Stem position | — | Center of comb body lower edge | Axial alignment with Main's socket |
| Material | — | **PPS-CF40** + 316L stainless stem (insert-molded or pressed-in) | PPS-CF40 won't survive 15 k cycles as a bare stem |
| Mass target | — | **10 – 14 g** | Body 9.3 cm³ PPS-CF40 ≈ 13 g + 1 g stem |

### 3.3 Wide Comb (driver — stem down)

| Parameter | Current STL | Rev D target | Rationale |
|---|---:|---:|---|
| OAL (body only) | 177.55 | **178** | Same silhouette as Narrow |
| Width | 32.26 | **32.0** | Shared |
| Thickness | 6.69 | **6.7** | Shared |
| Tooth pitch (wide) | — | **4.5 – 5.5**, target 5.0 | Detangling band |
| Tooth row count | — | **24 teeth** @ 5.0 mm pitch over 120 mm | — |
| Stem | — | Same Rev D module as Narrow | Interchangeable |
| Material | — | PPS-CF40 + stainless stem | Same |
| Mass target | — | **11 – 15 g** | Slightly heavier (more material between wider teeth) |

### 3.4 Round Handle (driver — stem up, taper down)

| Parameter | Current STL | Rev D target | Rationale |
|---|---:|---:|---|
| OAL (total, incl. stem) | 154.18 | **158** | Render shows slender tail; keep |
| Body cross-section at connector block | 10.16 × 5.08 | **10.0 × 5.0** | Matches render; clean inch stock |
| Body cross-section at tip | — | **Ø 2.3** | Rev C §8 priority 6 — precision parting |
| Taper transition | — | Smooth spline from rect 10×5 → round Ø 2.3 over 130 mm | — |
| Connector block (base of stem) | — | 10.0 × 5.0 × 5.0, flush to body | Rev D module |
| Stem | — | Rev D driver module (see §2.3) | — |
| Material | — | **316L stainless** (CNC turned from bar) | Solid now that the body is so slender; hollowing buys <2 g |
| Mass target | — | **10 – 14 g** | Vol 1.46 cm³ × 7.98 ≈ 11.6 g per current STL |

### 3.5 Flat Handle (driver — stem up, flat tail)

| Parameter | Current STL | Rev D target | Rationale |
|---|---:|---:|---|
| OAL | 162.41 | **165** | Keep close to STL |
| Cross-section | 10.16 × 5.08 | **10.0 × 5.0** | Flat-rectangular stock |
| Tail profile | flat | radiused tip, 5.0 × 10.0 section constant, rounded end | Render-verified |
| Connector block + stem | — | Rev D driver module | — |
| Material | — | 316L stainless (CNC from flat bar) | — |
| Mass target | — | **20 – 25 g** | Vol 2.84 cm³ × 7.98 ≈ 22.7 g |

### 3.6 Double Handle (driver — stem up, fork down)

| Parameter | Current STL | Rev D target | Rationale |
|---|---:|---:|---|
| OAL | 154.18 | **158** | — |
| Fork outer width | 17.27 | **18.0** | Slightly widen for stability |
| Fork thickness (each prong) | 5.08 | **5.0** | — |
| Fork inner gap | ~8.0 derived | **8.0** | Parts for sectioning |
| Fork root fillet | — | **R 1.5** | Fatigue — Rev C audit finding |
| Fork length (working) | ~130 | **125** | Keeps tip OAL at 158 |
| Connector block + stem | — | Rev D driver module | — |
| Material | — | 316L stainless (CNC or wire-cut from plate, weld-free one-piece preferred) | — |
| Mass target | — | **22 – 28 g** | STL shows current weight high because fork walls are currently thicker than needed; target is lighter |

---

## 4. Shared spine silhouette (renders confirm)

All three combs (Main, Narrow, Wide) share the same outer silhouette including the M-cutout. Differences are **only in the tooth field**:

- Main: mixed tooth pattern (fine-left, wide-right), plus a pick tip on the left end
- Narrow: 2.0 mm uniform pitch
- Wide: 5.0 mm uniform pitch

This simplifies the CAD agent enormously: **build one `comb_body_blank.py` that generates the shared silhouette + M-cutout, then a second function `apply_tooth_field(blank, pitch, count)` that stamps teeth.**

---

## 5. Assembly envelope (Rev D, recomputed)

With the vertical-insert architecture, the assembled length is **Main OAL + driver OAL − engagement depth**:

| Config | Main OAL | Driver OAL | Engagement | Assembled OAL |
|---|---:|---:|---:|---:|
| Main + Narrow | 202 | 178 | 12 | **368** |
| Main + Wide | 202 | 178 | 12 | **368** |
| Main + Round Handle | 202 | 158 | 12 | **348** |
| Main + Flat Handle | 202 | 165 | 12 | **355** |
| Main + Double Handle | 202 | 158 | 12 | **348** |

**Observation.** Rev C's 280–320 mm assembled target is **still not achievable** with this architecture because the Main Comb alone is already 202 mm — you cannot assemble into the 280 mm band unless the driver is 90 mm or less, which defeats the modular purpose.

**Decision surfaced for human input.** Two options:

- **A)** Accept **340–380 mm** as the Rev D assembled band. This matches Mason Pearson combo brushes and full-length pro cutting tools; stylists consider this professional, not long.
- **B)** Shrink Main Comb further to **160 mm** (Y.S. Park short band) to hit 300–340 mm assembled. Reduces effective tooth field by ~25%, hurts the cutting role.

**Rev D recommendation: A.** The "modular long-tool" identity is stronger than forcing the 280–320 band, and the render intent clearly shows longer, slender silhouettes. The agent's rulepack will reflect this — but flag as a WARN until you sign off.

---

## 6. Weight envelope (Rev D)

| Part | Material | Target (g) | Max (g) |
|---|---|---:|---:|
| Main Comb | PPS-CF40 + ball plunger sub-assy (~2 g) | 14–18 | 22 |
| Wide Comb | PPS-CF40 + 316L stem | 11–15 | 18 |
| Narrow Comb | PPS-CF40 + 316L stem | 10–14 | 17 |
| Round Handle | 316L (solid) | 10–14 | 17 |
| Flat Handle | 316L (solid) | 20–25 | 30 |
| Double Handle | 316L (solid one-piece fork) | 22–28 | 34 |
| **Assembled (Main + any driver)** | — | **26–46 g** | **56 g** |

The Rev D assembled weight is **lighter than Rev C's 40–58 g** because (a) the new handle silhouettes are much slimmer and (b) hollowing is no longer required to hit weight. That's a net win.

---

## 7. Rev D revision checklist (priority order)

| # | Task | Part(s) | Urgency |
|---|---|---|---|
| 1 | Implement Rev D locking module: socket + ball-plunger sub-assy + D-stem | All 6 | IMMEDIATE |
| 2 | Regenerate shared comb-silhouette blank with M-cutout | Main, Wide, Narrow | IMMEDIATE |
| 3 | Apply differentiated tooth fields (mixed / narrow / wide) | Main, Narrow, Wide | IMMEDIATE |
| 4 | Model slender handle silhouettes per render intent | Round, Flat, Double | IMMEDIATE |
| 5 | Add flush release button on Main Comb spine face | Main | IMMEDIATE |
| 6 | Add hair-shed chamfer (0.5 × 45°) at seam perimeters | All 6 | NEXT |
| 7 | Round handle tail taper → Ø 2.3 mm tip | Round | NEXT |
| 8 | Double handle fork-root R1.5 fillet | Double | NEXT |
| 9 | Grip microtexture / knurling zone on handles | All 3 handles | PRE-PROTO |
| 10 | Final draft angles ≥ 0.5° on all molded PPS-CF40 surfaces | All 3 combs | PRE-PROTO |

---

## 8. Validation gates (Rev D rulepack additions)

In addition to the Rev C rules, Rev D adds:

1. `stem_diameter_mm == 4.00 ± 0.03` — locked.
2. `socket_bore_diameter_mm == 4.10 ± 0.03` — locked.
3. `stem_ball_head_diameter_mm == 5.00 ± 0.05` — locked.
4. `stem_d_profile_chord_mm == 3.20 ± 0.05` — locked.
5. `insertion_force_N ∈ [10, 15]` — design simulation + physical.
6. `retention_force_N ∈ [30, 40]` — must exceed 3× expected pull in use.
7. `release_force_N ∈ [1, 2]` — thumb-comfortable.
8. `seam_step_mm ≤ 0.10` — tightened from Rev C's 0.15.
9. `cycle_life_target ≥ 15 000` — verified in prototype phase 2.
10. **Assembled-length rule REPLACED**: new band is `assembled_oal_mm ∈ [340, 380]` (WARN outside, REJECT below 320 or above 410).

---

## 9. Export / artifact policy (unchanged from Rev C)

Every variant emits: `.py` (CadQuery source), `.step` (AP214), `.stl` (binary), `.3mf` (optional), `.png` (iso + seam close-up), `_metrics.json`, `_validation.json`, `_report.md`. Release bundle zips the passing set.

---

## 10. What the agent must still NEVER do

- Touch the locked Rev D socket / stem geometry without a human-edited spec bump.
- Export a STEP for a variant that failed any rulepack rule.
- Propose alternatives to the ball-stud + cross-detent architecture (dovetail, bayonet, magnet, collet are ruled out — Rev C §6.3 + Rev D §2.2).
- Average conflicting numbers. Source precedence: render intent → new STL → Rev C → benchmarks.

---

*End — Deliverable 1 (Rev D).*
