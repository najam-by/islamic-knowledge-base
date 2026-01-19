# Hadith Multi-Layer Semantic Tagging System (HMSTS v1.1)

## Purpose
Extract structured, multi-dimensional meaning from each hadith in a way consistent with classical usūl, tafsīr, and taṣawwuf, while remaining machine-operable.

## Improvements over v1.0
1. Separated semantic facts from interpretive layers.
2. Added provenance and school-of-thought fields.
3. Added contradiction and abrogation detection.
4. Added polarity and scope logic.
5. Added ontology validation.

## Layer 0 — Textual Fact Layer
- speaker
- addressee
- verb_type (command, prohibition, report, supplication)
- modality (obligatory, recommended, permitted, discouraged, forbidden, informative)

## Layer 1 — Ontological Category
Controlled vocabulary, validated against fiqh and aqīdah taxonomies.
Multi-select controlled vocabulary, e.g.:

- Event  
- Legislation  
- Sunnah (action)  
- Sunnah (speech)  
- Ethics  
- Mercy  
- Warning  
- Cosmology  
- Eschatology  
- Social Order  
- Governance  
- Worship  
- Warfare  
- Family  
- Trade  
- Spiritual State  

---

## Layer 2 — Functional Role

| Role            | Description            |
|-----------------|------------------------|
| Normative       | Establishes rule      |
| Descriptive     | Reports occurrence    |
| Explanatory     | Clarifies principle   |
| Corrective      | Rectifies error       |
| Exemplary       | Models conduct        |
| Prophetic State | Reveals inner condition |
| Divine Address  | Quoted revelation     |
| Divine Attribute| Attribute of Allah    |

## Layer 3 — Four Meaning Axes

### Axis A (Hermeneutic)
1. Literal (ẓāhir)
2. Indicative (ishāra)
3. Moral (akhlaq)
4. Metaphysical (ḥaqīqa)

### Axis B (Spiritual Ascent)
1. Outward (ʿamal)
2. Inward (niyya)
3. Limit (ḥadd)
4. Ascent (maʿrifa)

Each axis stores:
- proposition
- scope (individual, communal, universal)
- certainty (qatʿī, ẓannī, ishārī)
- conditionality (absolute / contextual)

## Layer 4 — Thematic Vectors
- Divine attribute manifested
- Human faculty addressed (body / intellect / heart / spirit)
- Maqām / ḥāl (if spiritual)
- Legal cause (ʿilla)
- Objective (maqṣad)
- Value promoted
- Vice restrained

## Error Detection

| Error | Verification |
|-------|-------------|
| Category drift | Compare with classical sharḥ |
| Over-mystification | Check against literal layer |
| Legal misclassification | Cross-check with fiqh usūl |
| Symbol inflation | Require isnād of interpretation |

## Cross-Hadith Linking
- Abrogation candidate (nasikh/mansukh)
- Apparent tension group
- Thematic cluster
- Pedagogical sequence
