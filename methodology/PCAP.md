# Prophetic Chronology Assignment Protocol (PCAP v1.2)

## Purpose
Provide a rigorous, falsifiable method for assigning each hadith to a chronological interval within the Sīra, with explicit uncertainty modeling and auditability.

## Temporal Representation

Each hadith receives:

- era_id (mandatory: E0/E1/E2/E3)
- sub_era_id (optional)
- event_window_id (optional)
- earliest_ah
- latest_ah
- anchor_before (list)
- anchor_after (list)

## Evidence Typing (Factual Validation)

| Type | Factual Basis |
|------|---------------|
| explicit_text | Date/place stated in hadith |
| explicit_event | Mentions known dated battle, treaty, migration |
| isnad_generation | Companion presence constrains date |
| sirah_alignment | Matches dated sīra episode |
| contextual_order | Before/after relation only |
| speculative | Weak or solitary inference |

## Certainty Model

For each depth (era, sub-era, event, date):

posterior_confidence ∈ [0,1]

Derived from:
- number of independent corroborations
- strength of isnād
- agreement of classical historians
- absence of contradiction with anchors

Reasoning must be listed, verifieable by scholars

## Logical Constraints

1. Non-contradiction with:
   - Hijrah (1 AH)
   - Badr (2 AH)
   - Uhud (3 AH)
   - Khandaq (5 AH)
   - Hudaybiyyah (6 AH)
   - Fath Makkah (8 AH)
   - Tabuk (9 AH)
   - Farewell Hajj (10 AH)
   - Death (11 AH)

2. Interval consistency (Allen relations):
   - before, after, overlaps, during, meets, equals

## Error Types & Factual Checks

| Potential Error | Factual Check |
|-----------------|---------------|
| Wrong era | Compare against anchor events |
| Anachronism | Verify companion age/location |
| Over-precision | Downgrade if only relative order |
| Sectarian dating | Require majority-sīra consensus |
| CE drift | Recompute from AH with lunar-solar offset |

## Revision Rule

Updates must:
- Increase posterior probability
- Or narrow interval
- Never violate anchor constraints

## Improvements over v1.0
1. Replaced single-score certainty with Bayesian-style posterior confidence per depth.
2. Formalized temporal logic (Allen interval relations) to prevent inconsistent ordering.
3. Added anchor-priority and contradiction-resolution rules.
4. Distinguished historical fact, scholarly consensus, and probabilistic inference.
5. Added machine-checkable constraints.
