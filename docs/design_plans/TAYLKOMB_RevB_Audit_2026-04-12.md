# TAYLKOMB — Deep Research-Backed Engineering & Market Audit (Rev B Prep)
**Date:** 2026-04-12  
**Basis:** 6 uploaded drawing PDFs + market/ergonomic/material references listed in Section 10.  
**Important:** Where direct benchmark data was unavailable, I explicitly mark conclusions as **Engineering inference**.

## SECTION 1 — Executive Verdict
- **Biggest size issue:** the system is currently too long as a family (many parts in the 242–256 mm class), which can over-leverage wrist control and raise fatigue in detail work.  
- **Biggest ergonomic issue:** grip cross-sections appear inconsistent across attachments, so hand-feel and balance likely shift too much between swaps.  
- **Biggest structural issue:** thin transition zones near connector + long cantilever sections (especially round-tail and double handle fork neck) are likely high-cycle failure points.  
- **Biggest opportunity:** standardize a **single connector datum stack + seam blending geometry** and tune each attachment around use-case-specific balance windows.  
- **Closest to working now:** Main Comb / Wide / Narrow body-length class (~208 mm working body) aligns with professional long-cutting comb territory.  
- **Most urgent redesign:** connector architecture and seam-zone geometry before tooth/tail micro-optimization.

---

## SECTION 2 — Part-by-Part Audit

### 2.1 Main Comb
**Current draft dimensions (from drawing extraction):** overall ~228.81 mm, body ~208.01 mm, body height class ~50.8 mm.  

**What works**
- Working length is in-range with long pro cutting combs (e.g., Y.S. Park 331 at 229 mm).  
- Height class supports mixed control (detangle + smoothing).

**What does not work / likely unrealistic**
- At current total length, if paired with long handle modules, assembled tool becomes too long for fast sectioning and near-head maneuvering.

**Ergonomic concerns**
- If connector adds rear mass, center of mass may drift behind desired control point for detail parting.

**Structural concerns**
- Tooth-root transition and connector-neck blending need thicker local section than aesthetic minimum.

**Recommended target dimensions/ranges**
- Overall assembled comb section (without extra handle): **220 mm target**, 212–228 acceptable, <205 too short, >232 too long.
- Active toothed length: **198–206 target**, 192–210 acceptable.
- Body max height: **47–51 target**, 44–53 acceptable.
- Spine thickness (non-tooth zone): **3.0–3.8 target**, 2.6–4.2 acceptable.
- Tooth root thickness: **1.25–1.6 target**, <1.1 risky, >1.8 draggy.

**Confidence level:** Medium-High (geometry known; tooth micro-geometry still needs prototype confirmation).

---

### 2.2 Round Comb Handle (rat-tail style)
**Current draft dimensions:** overall ~242.65 mm; long tapered section ~187.2 mm; tip noted around 3.11 mm in prompt, but drawing extraction indicates a finer terminal value appears closer to ~1.3 mm (needs drawing confirmation in CAD).  

**What works**
- Overall concept aligns with pro tail-comb length class (Y.S. Park 106 listed 245 mm).

**What does not work / unrealistic**
- If true tip is ~3.11 mm, this is too blunt for precision parting; if true tip ~1.3 mm, better for sectioning but may be fragile if transition not reinforced.

**Ergonomic concerns**
- Long taper can induce “whip feel” and less precise indexing if connector interface has any play.

**Structural concerns**
- Highest risk area is tip-to-mid taper and neck at connector transition.

**Recommended target dimensions/ranges**
- Overall: **235 mm target**, 225–245 acceptable, <220 too short, >250 too long.
- Effective tail length: **170–182 target**, 160–188 acceptable.
- Tip diameter: **1.2 target**, 0.9–1.5 acceptable, <0.8 break risk, >1.8 poor parting.
- Tail diameter at 25 mm from tip: **1.8–2.3 target**.
- Tail base diameter at connector-side taper start: **4.2–5.5 target**.

**Confidence level:** Medium (tip dimension conflict requires CAD check).

---

### 2.3 Flat Handle
**Current draft dimensions:** overall by chain ~255.6 mm class; long body section ~204.95 mm.  

**What works**
- Provides leverage and broad hand support for smoothing/twisting motions.

**What does not work / unrealistic**
- 255+ mm class is likely overlong for repeated salon workflows; causes handle collisions and slower repositioning.

**Ergonomic concerns**
- Over-length increases wrist moment; risk of forearm fatigue in all-day use.

**Structural concerns**
- Long unsupported flat sections can feel springy unless thickness and rib logic are tuned.

**Recommended target dimensions/ranges**
- Overall: **235 target**, 225–242 acceptable, <218 too short, >248 too long.
- Functional grip length: **105–120 target**, 95–130 acceptable.
- Max grip width: **22–26 target**, 20–28 acceptable.
- Grip thickness: **7–10 target**, 6–11 acceptable.
- Neck thickness at connector transition: **4.0–5.2 target**.

**Confidence level:** Medium-High.

---

### 2.4 Double Handle
**Current draft dimensions:** overall ~242.8 mm; working/fork length ~192 mm; outer width ~27.2 mm.  

**What works**
- Width class can support stable dual-finger indexing.

**What does not work / unrealistic**
- Current fork length likely excessive for precision control and may flex during twisting/sectioning.

**Ergonomic concerns**
- Distal-heavy perception if fork arms are long and thin.

**Structural concerns**
- Fork root is a fatigue hotspot; needs radius + local thickening.

**Recommended target dimensions/ranges**
- Overall: **228 target**, 220–238 acceptable, <214 too short, >244 too long.
- Fork functional length: **150–168 target**, 140–176 acceptable.
- Outer width: **24–28 target**, 22–30 acceptable.
- Inner gap: **10–14 target**.
- Fork arm thickness: **3.5–4.8 target**, <3.2 risky.

**Confidence level:** Medium.

---

### 2.5 Wide Comb
**Current draft dimensions:** overall ~223.23 mm; body ~208.01 mm.  

**What works**
- Strongly aligned with pro long-comb envelope.
- Good candidate for detangling/smoothing primary head.

**What does not work / unrealistic**
- Risk of overbuilt tooth thickness if tuned for strength only; would increase drag.

**Ergonomic concerns**
- Needs tooth pitch gradient tuned to prevent snagging in dense/curly sections.

**Structural concerns**
- Wide-tooth roots must avoid stress risers at spine.

**Recommended target dimensions/ranges**
- Overall: **220 target**, 212–228 acceptable.
- Active toothed length: **196–204 target**.
- Wide-tooth pitch: **3.8–5.2 target**.
- Tooth tip thickness: **0.9–1.3 target**.
- Tooth root thickness: **1.4–1.9 target**.
- Tooth length: **25–34 target**.

**Confidence level:** High for envelope, medium for tooth micro-geometry.

---

### 2.6 Narrow Comb
**Current draft dimensions:** overall ~223.67 mm; body ~208.01 mm.  

**What works**
- Envelope suits precision smoothing/sectioning analogs.

**What does not work / unrealistic**
- If narrow teeth are too fine at root, breakage risk rises under detangle misuse.

**Ergonomic concerns**
- Needs clear visual/tactile distinction from wide comb to justify modular swap in-speed.

**Structural concerns**
- Fine tooth root and first 10 mm from root are key risk zones.

**Recommended target dimensions/ranges**
- Overall: **220 target**, 212–228 acceptable.
- Active toothed length: **196–204 target**.
- Fine-tooth pitch: **1.8–2.6 target**.
- Tooth tip thickness: **0.6–0.95 target**.
- Tooth root thickness: **1.0–1.35 target**, <0.9 risky.
- Tooth length: **20–28 target**.

**Confidence level:** Medium-High.

---

## SECTION 3 — Master Sizing Table

| Part | Current draft size | Recommended target | Acceptable range | Too small threshold | Too large threshold | CAD notes |
|---|---|---|---|---|---|---|
| Main Comb | 228.81 OAL / 208.01 body | 220 OAL | 212–228 | <205 | >232 | Keep body family, reduce rear overhang |
| Round Handle | 242.65 OAL / 187.2 tail | 235 OAL, tip 1.2 | 225–245, tip 0.9–1.5 | <220, tip <0.8 | >250, tip >1.8 | confirm terminal tip dimension in CAD |
| Flat Handle | ~255.6 OAL class | 235 OAL | 225–242 | <218 | >248 | shorten + re-balance |
| Double Handle | 242.8 OAL / 192 fork | 228 OAL / 160 fork | 220–238 / 140–176 | <214 / <140 | >244 / >176 | reinforce fork root transition |
| Wide Comb | 223.23 OAL / 208.01 body | 220 OAL | 212–228 | <205 | >232 | tune wide tooth pitch gradient |
| Narrow Comb | 223.67 OAL / 208.01 body | 220 OAL | 212–228 | <205 | >232 | protect fine tooth roots |

---

## SECTION 4 — Weight & Ergonomics Table

| Part | Target weight | Max suggested weight | Balance notes | Grip type | Fatigue risk |
|---|---:|---:|---|---|---|
| Main Comb core | 12–18 g | 22 g | COM at 45–52% from tooth-leading end | precision / pinch | Low if balanced |
| Round Handle module | 6–11 g | 14 g | keep COM near connector to reduce whip | precision parting | Medium if tail too flexible |
| Flat Handle module | 10–16 g | 20 g | COM at 35–45% from connector | power+precision hybrid | Medium at >18 g |
| Double Handle module | 11–17 g | 21 g | COM centered at fork root zone | indexed power grip | Medium-High if distal-heavy |
| Wide Comb module | 10–15 g | 18 g | slightly forward-biased for detangle | power to precision shift | Low-Medium |
| Narrow Comb module | 8–13 g | 16 g | neutral/near-center for sectioning | precision | Low-Medium |

**Assembled guidance (Main Comb + module):**
- With round handle: **18–28 g target**, >32 g fatigue risk.
- With flat handle: **22–34 g target**, >38 g fatigue risk.
- With double handle: **23–35 g target**, >40 g fatigue risk.
- With wide/narrow modules: **20–31 g target**, >35 g fatigue risk.

**Ergonomic reference anchor:** precision handle diameters and power-handle diameters from CA DOSH hand-tool ergonomics checklist (1/4–1/2 in precision, 1.25–2 in high-force tools) are used as boundary logic, then scaled down for salon-comb force profile (**Engineering inference**).

---

## SECTION 5 — Connector Recommendation

### Recommended architecture
**Hybrid rail-and-slide + spring detent + hard-stop shoulder + anti-rotation key**.

### Why this is best for TAYLKOMB
- Better anti-wobble potential than pure snap-fit.
- Better repeat-cycle retention than high-deflection latch-only concepts.
- Cleaner seam control than twist-lock threads in hair-contact zones.

### 10,000+ swap cycle strategy
- Use sliding primary load path (rails), with detent for retention rather than primary structural load.
- Add replaceable/wear-optimized detent element or low-strain compliant arm.
- Keep insertion chamfers polished and radiused.

### Target interface geometry (Rev B start points)
- Engagement length: **18–24 mm target** (min 16, max 28).
- Rail bearing land width: **1.8–2.8 mm each side**.
- Diametral/side clearance in molded condition: **0.04–0.10 mm per side functional target** (tooling capability dependent).
- Anti-rotation key depth: **0.8–1.4 mm**.
- Lead-in chamfer: **20–35°** with 0.4–0.8 mm entry radius.
- Seam step mismatch (post-assembly): target **<=0.10 mm**, reject >0.20 mm on hair-contact edge.

### Interface options comparison (summary)
- **Snap-fit only:** simple, low cost, but wear/creep risk at high cycles.
- **Detent-only peg:** fast UX, poor torsional stiffness.
- **Rail-and-slide:** excellent alignment and wobble control.
- **Twist-lock:** strong retention; can trap hair/debris and slow swaps.
- **Interference-fit:** good initial stiffness, poor long-term repeatability.
- **Hybrid (recommended):** best all-around for salon repeated swaps.

---

## SECTION 6 — Materials Recommendation

### Part-by-part recommendation
- **Teeth-critical comb elements (wide/narrow/main):** high-stiffness, fatigue-tolerant engineering resin; shortlist **POM (acetal)** and **PEI/Ultem-class** depending heat/chemical target and cost.
- **Connector-bearing elements:** wear-stable pair strategy (e.g., POM/PPSU or PBT/POM pairing) to reduce galling and looseness growth.
- **High-touch handles:** optional overmold (TPE 45–65A) only away from seam/cleaning trap zones.

### Chemical/heat rationale
- Y.S. Park and Sam Villa references emphasize high heat resistance (around 220–232°C claims on specific combs).
- Barbicide uses quaternary ammonium compounds; compatibility against disinfectant chemistry must be validated with soak cycles.
- PBT families can be strong but may have alkaline sensitivity limits.
- PPSU has strong disinfectant/sterilization reputation and high heat stability but higher cost and density.

### Recommended production strategy
**Hybrid material strategy (preferred):**
- Comb/tooth bodies: tuned for flex + edge durability.
- Connector substructure: tuned for wear + dimensional stability.
- Optional grip skin only where needed for control.

### Do-not-assume items
- Final bleach/Barbicide/heat resistance cannot be locked from generic datasheets alone; must run your own exposure + cycle testing.

---

## SECTION 7 — CAD Revision Plan

### Change now
1. Normalize family OAL around 220–235 mm depending attachment function.
2. Standardize connector datums across all 5 interchangeable pieces.
3. Add seam blending fillets and hard-stop shoulder.
4. Increase fork-root and neck transition radii.
5. Rework round-tail taper curve for strength near tip.

### Keep for now
- Main comb body-length class (~208 mm).
- Wide/narrow comb overall envelope class (~223 mm current, trimmed slightly).

### Prototype before locking
- Tip diameter final value.
- Tooth pitch gradients (wide and narrow).
- Final handle thickness and grip contour.
- Rail clearance and detent force curve.

### Top 10 CAD revisions (priority order)
1. Connector architecture conversion to hybrid rail+detent.  
2. Seam-zone flush condition redesign.  
3. Round-tail tip-to-base taper recalibration.  
4. Fork-root local section thickening + radii.  
5. Flat-handle overall length reduction.  
6. Standardized engagement length (18–24 mm).  
7. Tooth-root reinforcement logic standardization.  
8. Weight balancing via local pocketing/ribbing.  
9. Surface edge-break standard (anti-snag).  
10. Datum stack simplification for mold repeatability.

**High-risk list:** connector wear wobble, round-tail breakage, fork-root fatigue, seam snagging.  
**Do-not-lock-yet list:** detent geometry, final clearances, final tooth tip thicknesses, final overmold usage.

---

## SECTION 8 — Prototype Validation Plan

1. **Comfort test:** 2-hour repeated grip protocol across at least 12 stylists; capture subjective control and hotspot mapping.  
2. **Fatigue test:** 6-hour simulated salon cycle (detangle/section/smooth/twist repeats), RPE scoring every 30 min.  
3. **Repeated swap test:** automated/manual 10k cycle target; measure insertion force, extraction force, angular play growth.  
4. **Detangling performance test:** standardized wet/dry hair tress pull-force and snag incident count by comb variant.  
5. **Snag test (seam):** seam-first pass over mixed-texture tresses; count catches per 100 strokes.  
6. **Heat/chemical exposure:** disinfectant soak cycles (including quats and dilute bleach), then dimensional and strength checks.  
7. **Drop/breakage:** multiple drops from 1.2 m onto hard floor; inspect teeth, connector function, retained straightness.  
8. **Stylist field-use test:** 2–4 week in-salon beta, instrumented log of preferred module combinations and failure events.

Lock geometry only after passing thresholds on swap durability + snag + fatigue.

---

## SECTION 9 — Parametric Appendix

### 9.1 Coordinate-style reference logic
- **Global datum A:** connector center plane.  
- **Datum B:** primary rail mid-plane.  
- **Datum C:** tooth-root neutral axis.  
- Measure all module offsets from A/B/C to ensure cross-compatibility.

### 9.2 Core parametric relationships
- `OAL_part = L_connector_zone + L_active_zone + L_terminal_feature`
- `L_engagement = k1 * T_connector_block` where `k1` start range 3.0–4.5.
- `t_root_to_tip_ratio` target: wide teeth 1.5–2.0; narrow teeth 1.6–2.2.

### 9.3 Taper rules
- Round tail taper: piecewise linear + blended spline.  
  - Segment 1 (base stability): shallow taper.  
  - Segment 2 (functional precision): steeper taper.  
  - Segment 3 (tip safety): micro-taper with radius cap.

### 9.4 Tooth-array spacing logic
- Use GDP-style progression (decreasing pitch) on at least one zone for tension control.  
- Suggested form: `pitch(i)=p0 - i*delta`, bounded by manufacturing minimum and snag criteria.

### 9.5 Connector datum logic
- All modules must share: engagement start plane, anti-rotation key position, detent centerline, and hard-stop shoulder depth.

### 9.6 Section transition rules
- Minimum transition radius in high-cycle load paths: **R >= 0.8 mm**, preferred 1.2–1.8 mm.
- No abrupt section jump >35% without intermediate blend.

---

## SECTION 10 — Sources & Evidence (used + translated)

### Professional comb benchmarks / product geometry
1. Y.S. Park 339 product page (length, material/heat claims, GDP pitch language): https://ysparkusa.com/products/ys-park-cutting-comb-339  
2. Y.S. Park 106 tail comb (245 mm class): https://ysparkusa.com/products/ys-park-tail-comb-106  
3. Y.S. Park 331 long cutting comb (229 mm class): https://ysparkusa.com/products/ys-park-cutting-comb-331  
4. Sam Villa Signature Series Long Cutting Comb (8.75 in dimensions, heat resistance claim): https://www.samvilla.com/products/long-cutting-comb  
5. Sam Villa Artist Series Detail Comb (6.875 in class): https://www.samvilla.com/products/detail-comb  
6. Hercules Sagemann product descriptions (ebonite material, hand-polished teeth, pro positioning): https://uk.lorealpartnershop.com/default/brush-et-comb-sets/hercules-s%C3%A4gemann-special-trimmer-comb-with-handle/M4000165476005.html  

### Ergonomics references
7. California DOSH hand-tool selection (handle diameter guidance): https://www.dir.ca.gov/dosh/dosh_publications/handtools6.html  
8. California DOSH selection guidance (high-force handle length): https://www.dir.ca.gov/dosh/dosh_publications/handtools5.html  
9. CDC/NIOSH ergonomics program reference baseline: https://www.cdc.gov/niosh/ergonomics/ergo-programs/index.html  

### Materials / connector design references
10. DuPont/Celanese Delrin engineering design principles (snap-fit design guidance context): https://www.delrin.com/wp-content/uploads/2023/10/General-Design-Principles-for-Engineering-Polymers.pdf  
11. BASF Ultradur brochure (chemical behavior and limitations context): https://download.basf.com/p1/8a8081c57fd4b609017fdf6cfd252296/en/Ultradur%C2%AE_Product_Brochure_Brochure_English.pdf  
12. Solvay sulfone polymer chemical resistance document: https://www.solvay.com/sites/g/files/srpend221/files/2018-07/Sulfone-Polymers-Chemical-Resistance_EN.pdf  
13. Solvay healthcare chemical resistance comparison including bleach examples: https://www.solvay.com/sites/g/files/srpend221/files/2018-08/Healthcare-Chemical-Resistance-of-SP-for-Medical-Equipment-Housings_EN_v1.1_0.pdf  
14. BARBICIDE label chemistry (quaternary ammonium active): https://barbicide.com/wp-content/uploads/2020/06/BARBICIDE-Spray-Bottle-Label-1.pdf

### Notes on evidence quality
- Official manufacturer pages were prioritized for dimensions/claims.  
- Some Hercules data are distributor-channel descriptions where official dimensional tables are sparse.  
- Where exact tooth pitch/weights were missing, recommendations are marked as engineering inference and bounded as ranges.
