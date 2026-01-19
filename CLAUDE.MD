# Islamic Knowledge Base - Claude Guide

## Vision & Mission

This repository is a **systematic, living Islamic knowledge base** designed to be a foundational datasource for AI applications and scholarly research. The system integrates primary Islamic sources with rigorous structuring methodologies to enable semantic reasoning while maintaining scholarly authenticity.

### Primary Objective

Create a verifiable, computationally-accessible knowledge system grounded in Islamic primary sources with explicit hierarchical authority:

1. **Quran** - Primary foundational source (immutable)
2. **Hadith** - Prophetic traditions (immutable source texts, interpretations allowed)
3. **Major Works** - Classical scholarly works for refinement and interpretation

### End Goals

1. **Semantic Knowledge Graph**: Enable AI systems to reason about Islamic knowledge with proper context, chronology, and interpretive layers
2. **Moral Commandments Extraction**: Derive comprehensive rule sets of Islamic ethics and jurisprudence:
   - Obligations (wajib)
   - Prohibitions (haram)
   - Recommendations (mustahabb)
   - Discouragements (makruh)
   - Permissibles (mubah)
3. **Living Database System**: Original sources remain locked; variations, interpretations, and scholarly refinements can be added with provenance tracking
4. **Verifiable Reasoning**: All semantic conclusions must be traceable back to primary sources with explicit inference chains

### Target Audience

- AI/ML researchers building Islamic applications
- Islamic scholars conducting computational research
- Developers creating ethics-aware systems
- Educators designing curriculum materials
- Students studying Islamic texts systematically

## Architectural Framework: IPKSA v1.2

**Integrated Prophetic Knowledge Structuring Architecture** provides the foundational methodology for organizing the entire corpus.

### Core Design Principles

1. **Chronology as Skeleton** - Temporal ordering provides structural foundation
2. **Meaning as Multi-Layer Field** - Multiple interpretive dimensions preserved simultaneously
3. **Certainty as First-Class Data** - Explicit epistemic confidence at every level
4. **Inference as Explicit, Never Hidden** - All reasoning chains must be auditable
5. **Hierarchy Before Interpretation** - Source authority determines interpretive priority
6. **Structure Before Insight** - Systematic organization precedes analytical extraction

### Three-Pillar Methodology

#### 1. PCAP - Prophetic Chronology Assignment Protocol (v1.2)

**Purpose**: Rigorously map each hadith to chronological intervals within the Prophet's life with explicit uncertainty modeling.

**File**: `PCAP.md`

**Key Features**:
- Temporal representation using era hierarchies (E0/E1/E2/E3)
- Evidence typing (explicit text, event references, isnad generation, sirah alignment)
- Bayesian-style posterior confidence scoring
- Allen interval logic for temporal consistency
- Anchor event constraints (Hijrah, Badr, Uhud, Khandaq, Hudaybiyyah, Fath Makkah, Tabuk, Farewell Hajj)

**Outputs**: Each hadith receives:
- `era_id`, `sub_era_id`, `event_window_id`
- `earliest_ah`, `latest_ah`
- `anchor_before`, `anchor_after` relations
- `posterior_confidence` score with reasoning

#### 2. HMSTS - Hadith Multi-Layer Semantic Tagging System (v1.1)

**Purpose**: Extract structured, multi-dimensional meaning consistent with classical usul, tafsir, and tasawwuf.

**File**: `HMSTS.md`

**Semantic Layers**:

**Layer 0 - Textual Fact Layer**:
- Speaker, addressee identification
- Verb type (command, prohibition, report, supplication)
- Modality (obligatory, recommended, permitted, discouraged, forbidden, informative)

**Layer 1 - Ontological Category**:
- Controlled vocabulary: Event, Legislation, Sunnah, Ethics, Mercy, Warning, Cosmology, Eschatology, Social Order, Governance, Worship, Warfare, Family, Trade, Spiritual State

**Layer 2 - Functional Role**:
- Normative, Descriptive, Explanatory, Corrective, Exemplary, Prophetic State, Divine Address, Divine Attribute

**Layer 3 - Four Meaning Axes**:
- **Axis A (Hermeneutic)**: Literal (zahir), Indicative (ishara), Moral (akhlaq), Metaphysical (haqiqa)
- **Axis B (Spiritual Ascent)**: Outward (amal), Inward (niyya), Limit (hadd), Ascent (ma'rifa)

Each includes: proposition, scope, certainty, conditionality

**Layer 4 - Thematic Vectors**:
- Divine attributes, human faculties addressed, spiritual stations, legal causes, objectives, values, vices

**Cross-Hadith Linking**:
- Abrogation detection (nasikh/mansukh)
- Apparent tension resolution
- Thematic clustering
- Pedagogical sequencing

#### 3. IPKSA - Integrated Architecture (v1.2)

**Purpose**: Unified system architecture integrating chronology, semantics, and quality control.

**File**: `IPKSA.md`

**Processing Pipeline**:
1. Ingest hadith + isnad
2. Normalize text
3. Temporal anchoring via PCAP
4. Certainty scoring
5. Semantic decomposition via HMSTS
6. Cross-linking (abrogation, pedagogy, theme)
7. Consistency validation
8. Knowledge graph construction
9. Query & reasoning layer

**Quality Control Framework**:
- Chronological contradiction detection
- Semantic distortion prevention via classical commentary cross-check
- Sectarian bias mitigation through majority-position weighting
- Over-inference prevention via probabilistic labeling
- Concept drift tracking through ontology versioning

## Scholarly Context

### What are Hadiths?

Hadiths are the recorded sayings, actions, and approvals of Prophet Muhammad (PBUH). They constitute the second source of Islamic law after the Quran. Each hadith consists of:

- **Matn**: The actual text or content of the hadith
- **Isnad**: The chain of narration tracing back to the Prophet
- **Narrator information**: The people who transmitted the hadith

**Hadith Classifications**:
- **Sahih** (Authentic): Highest level of authenticity with unbroken chain of reliable narrators
- **Hasan** (Good): Acceptable but slightly weaker than Sahih
- **Daif** (Weak): Contains weaknesses in the chain or text
- **Mawdu** (Fabricated): Considered fabricated or forged

### The 17 Included Hadith Collections

This database includes 50,884 hadiths from 17 authoritative collections:

**The Six Major Books (Kutub al-Sittah)**:
1. **Sahih al-Bukhari** - Most authentic collection, compiled by Imam al-Bukhari (d. 870 CE)
2. **Sahih Muslim** - Second most authentic, compiled by Imam Muslim (d. 875 CE)
3. **Sunan Abi Dawud** - Focus on legal hadiths
4. **Jami` at-Tirmidhi** - Includes authentication grades for each hadith
5. **Sunan an-Nasa'i** - Rigorous authentication standards
6. **Sunan Ibn Majah** - Completes the six major collections

**Additional Major Collections**:
7. **Muwatta Malik** - Earliest hadith collection, includes legal opinions
8. **Musnad Ahmad** - Comprehensive collection by Imam Ahmad ibn Hanbal
9. **Sunan ad-Darimi** - Early comprehensive collection

**Specialized Collections**:
10. **Riyad as-Salihin** - Compilation focusing on righteous conduct
11. **Shamail al-Muhammadiyah** - Descriptions of the Prophet's character and appearance
12. **Bulugh al-Maram** - Hadiths related to Islamic jurisprudence
13. **Al-Adab Al-Mufrad** - Collection focusing on manners and conduct
14. **Mishkat al-Masabih** - Expanded version of Masabih al-Sunnah

**The Forty Hadith Collections**:
15. **Al-Nawawi's Forty Hadith** - 42 essential hadiths covering Islamic principles
16. **Forty Hadith Qudsi** - Sacred hadiths directly from Allah
17. **Shah Waliullah's Forty Hadith** - Selection emphasizing spiritual and moral themes

### Quranic Structure

The Quran is divided into:
- **Surahs** (Chapters): 114 chapters of varying lengths
- **Ayahs** (Verses): Individual verses within each surah
- **Juz** (Parts): 30 equal divisions for reading throughout the month
- **Morphological Analysis**: Linguistic breakdown of Arabic grammar, roots, and meanings for computational analysis

### Historical Context

Prophet Muhammad (PBUH) lived from approximately 570-632 CE in the Arabian Peninsula. The temporal coordinate system uses:
- **AH (After Hijrah)**: Islamic calendar starting from migration to Medina (622 CE = 1 AH)
- **Major Anchor Events**: Hijrah (1 AH), Badr (2 AH), Uhud (3 AH), Khandaq (5 AH), Hudaybiyyah (6 AH), Fath Makkah (8 AH), Tabuk (9 AH), Farewell Hajj (10 AH), Death (11 AH)

The `Prophetic_era_markers__v1_.csv` file provides the foundational chronological tree for temporal anchoring.

## Repository Structure

```
/Users/ns/home/library/ctrl/db/
│
├── CLAUDE.MD                          # This file - comprehensive project guide
├── IPKSA.md                          # Architecture overview (v1.2)
├── PCAP.md                           # Chronology assignment protocol (v1.2)
├── HMSTS.md                          # Semantic tagging system (v1.1)
├── Prophetic_era_markers__v1_.csv   # Temporal coordinate system (54 events)
│
├── 1. quran/                         # Quranic texts (Primary Source - Priority 1)
│   ├── quran-simple.txt             # Plain text Quran
│   ├── quran-simple-clean.txt       # Cleaned version
│   └── MASAQ.../                    # Morphologically-analyzed dataset
│
├── 2. hadith/                        # Hadith corpus (Primary Source - Priority 2)
│   ├── README.md                    # Hadith database documentation (v1.2.0)
│   ├── by_book/                     # Hadiths organized by complete books
│   │   ├── the_9_books/            # Six major + three additional
│   │   ├── forties/                # Three "Forty Hadith" collections
│   │   └── other_books/            # Specialized collections
│   ├── by_chapter/                  # Hadiths organized by chapter/section
│   │   ├── the_9_books/
│   │   ├── forties/
│   │   └── other_books/
│   └── [future: processed/]         # IPKSA-processed hadiths (to be added)
│
├── 3. major works/                   # Classical Islamic scholarship (Priority 3)
│   └── TheBookOfKnowledgeByGhazali/ # First book of "Revival of Religious Sciences"
│       └── [EPUB, PDF formats]
│
└── archive/                          # Original compressed datasets
    ├── hadith-json-main.zip
    └── MASAQ...zip
```

## Data Schemas & Usage

### Hadith JSON Structure (Current)

```typescript
interface Hadith {
  id: number;              // Unique hadith identifier
  chapterId: number;       // Chapter/section ID
  bookId: number;          // Book collection ID
  arabic: string;          // Arabic text of the hadith
  english: {
    narrator: string;      // Chain of narration (isnad) in English
    text: string;          // Hadith text translated to English
  };
}
```

### Hadith Extended Structure (IPKSA Target)

```typescript
interface HadithIPKSA extends Hadith {
  // PCAP Temporal Data
  temporal: {
    era_id: string;                    // E0/E1/E2/E3
    sub_era_id?: string;
    event_window_id?: string;
    earliest_ah: number;
    latest_ah: number;
    anchor_before: string[];
    anchor_after: string[];
    evidence_type: 'explicit_text' | 'explicit_event' | 'isnad_generation' |
                   'sirah_alignment' | 'contextual_order' | 'speculative';
    posterior_confidence: number;      // [0,1]
    reasoning: string;
  };

  // HMSTS Semantic Data
  semantic: {
    layer0: {
      speaker: string;
      addressee: string;
      verb_type: string;
      modality: string;
    };
    layer1: {
      ontological_categories: string[];
    };
    layer2: {
      functional_role: string;
    };
    layer3: {
      axis_a: InterpretiveLayer;     // Hermeneutic
      axis_b: InterpretiveLayer;     // Spiritual Ascent
    };
    layer4: {
      divine_attributes: string[];
      faculties_addressed: string[];
      maqam_hal?: string;
      legal_cause?: string;
      objective?: string;
      values: string[];
      vices: string[];
    };
  };

  // Cross-References
  links: {
    abrogation?: { type: 'nasikh' | 'mansukh'; related_ids: number[] };
    tensions?: number[];
    themes: string[];
    pedagogical_sequence?: number;
  };
}

interface InterpretiveLayer {
  proposition: string;
  scope: 'individual' | 'communal' | 'universal';
  certainty: 'qatʿī' | 'ẓannī' | 'ishārī';
  conditionality: 'absolute' | 'contextual';
}
```

### Quranic Data Formats

**Simple Format** (`quran-simple.txt`, `quran-simple-clean.txt`):
- Plain text verses
- Organized by Surah and Ayah
- UTF-8 encoded with Arabic diacriticals

**MASAQ Morphologically-Analyzed Dataset**:
- Word-by-word grammatical analysis
- Root identification
- Part of speech tagging
- Morphological features
- Suitable for linguistic AI applications

### Temporal Markers CSV Schema

```csv
Event_ID, Era, Date_AH, Date_CE, Event_Name, Location, Significance, Notes
```

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Collect 50,884 hadiths from 17 collections
- [x] Obtain Quranic texts with morphological analysis
- [x] Create chronological marker system
- [x] Develop IPKSA/PCAP/HMSTS methodologies
- [ ] Structure repository systematically

### Phase 2: Hadith Processing
- [ ] Implement PCAP temporal assignment for all hadiths
- [ ] Apply HMSTS semantic tagging
- [ ] Build cross-reference linkages
- [ ] Validate consistency
- [ ] Create knowledge graph

### Phase 3: Quran Integration
- [ ] Structure Quranic verses with full morphological data
- [ ] Link hadiths to Quranic verses (tafsir connections)
- [ ] Establish Quran-Hadith semantic relationships
- [ ] Priority hierarchy enforcement in reasoning chains

### Phase 4: Major Works Integration
- [ ] Digitize and structure classical commentaries
- [ ] Link scholarly interpretations to primary sources
- [ ] Track provenance and school-of-thought attribution
- [ ] Validate interpretations against primary sources

### Phase 5: Semantic Extraction
- [ ] Extract moral commandments (obligations, prohibitions, recommendations)
- [ ] Build legal rule sets with source attribution
- [ ] Create ethical decision frameworks
- [ ] Develop query and reasoning APIs

### Phase 6: AI Application Layer
- [ ] Build semantic search capabilities
- [ ] Develop context-aware reasoning engines
- [ ] Create verification and validation tools
- [ ] Establish API endpoints for applications

## Working with This Repository

### Epistemic Priority Hierarchy

When reasoning or extracting conclusions, always follow this authority hierarchy:

1. **Quran** - Absolute authority, immutable
2. **Mutawatir Hadith** - Mass-transmitted, near-certain
3. **Sahih Hadith** - Authenticated, highly reliable
4. **Hasan Hadith** - Good, acceptable
5. **Classical Consensus (Ijma)** - Scholarly agreement
6. **Major Works** - Interpretive guidance
7. **Probabilistic Inference** - Explicitly labeled as such

### File Navigation Best Practices

1. **For Hadith Access by Book**: Use `2. hadith/by_book/`
2. **For Hadith Access by Chapter**: Use `2. hadith/by_chapter/`
3. **For Quranic Text**: Start with `1. quran/quran-simple-clean.txt`
4. **For Morphological Analysis**: Use `1. quran/MASAQ.../`
5. **For Chronology**: Reference `Prophetic_era_markers__v1_.csv`
6. **For Methodology**: Consult IPKSA.md, PCAP.md, HMSTS.md

### Character Encoding

**Critical**: All files use UTF-8 encoding for Arabic text support.

```javascript
// Node.js example
const fs = require('fs');
const data = fs.readFileSync('path/to/file.json', 'utf8');
```

### Querying Best Practices

1. **Source Verification**: Always trace conclusions back to primary sources
2. **Certainty Tracking**: Maintain epistemic confidence scores
3. **Context Preservation**: Keep temporal and semantic context with extracted data
4. **Cross-Validation**: Verify important findings across multiple hadiths/sources
5. **Explicit Inference**: Label all reasoning steps and inference types
6. **Chronological Awareness**: Consider temporal ordering for pedagogical understanding
7. **Multi-Layer Semantics**: Preserve multiple interpretive dimensions simultaneously

## Quality Assurance

### Validation Mechanisms

| Risk | Mitigation Strategy |
|------|-------------------|
| Chronological contradiction | Anchor-event constraints in PCAP |
| Semantic distortion | Classical commentary cross-check |
| Sectarian bias | Majority-position weighting |
| Over-inference | Probabilistic labeling required |
| Concept drift | Ontology versioning |
| Anachronism | Companion age/location verification |
| Context loss | Multi-layer semantic preservation |

### Error Detection

**Factual Errors**:
- Compare temporal assignments against anchor events
- Verify companion presence and ages
- Cross-check with multiple sirah sources

**Semantic Errors**:
- Validate categories against classical sharh (commentaries)
- Check literal layer before mystical interpretation
- Verify legal classifications against fiqh usul

**Inference Errors**:
- Require explicit reasoning chains
- Label confidence levels
- Track provenance of interpretations

## Technology Stack

**Current Data Processing**:
- Node.js runtime
- TypeScript language
- Cheerio.js (HTML parsing)
- Axios (HTTP requests)
- cli-progress (progress bars)

**Future Stack** (to be determined):
- Graph database (Neo4j, ArangoDB, or similar)
- Python/TypeScript for semantic processing
- NLP libraries for Arabic text analysis
- REST/GraphQL API layer

## Tips for Claude

When assisting with this repository:

1. **Maintain Source Hierarchy**: Always prioritize Quran > Hadith > Major Works
2. **Explicit Uncertainty**: Never state uncertain interpretations as facts
3. **Temporal Awareness**: Consider chronological context for pedagogical understanding
4. **Multi-Layer Thinking**: Preserve multiple interpretive dimensions simultaneously
5. **Provenance Tracking**: Always cite sources with proper attribution
6. **Classical Validation**: Cross-reference with traditional scholarship
7. **Sectarian Neutrality**: Represent majority positions; note variations
8. **Inference Labeling**: Clearly distinguish fact from interpretation
9. **Context Preservation**: Maintain isnad, temporal, and semantic context
10. **Scholarly Respect**: Use proper Islamic terminology and conventions

## Contributing Guidelines

### Data Addition
- Original Quranic and Hadith texts are immutable
- Interpretations must include provenance and confidence levels
- All additions must maintain IPKSA architectural compliance
- New major works must be vetted for scholarly authenticity

### Methodology Updates
- PCAP, HMSTS, and IPKSA documents are versioned
- Changes require validation against existing processed data
- Breaking changes require migration paths
- All updates must maintain auditability

### Quality Standards
- Factual accuracy over volume
- Explicit uncertainty over false confidence
- Structural consistency over convenience
- Classical compatibility over innovation

## License & Attribution

**Hadith Data**: Sourced from [sunnah.com](https://sunnah.com/) - verify usage terms
**Quranic Text**: Generally public domain for educational/research use
**MASAQ Dataset**: Check original licensing terms
**Major Works**: Verify copyright status per work

Islamic religious texts are generally considered accessible for educational and research purposes. For commercial applications, verify attribution requirements and licensing.

## Plan Management & Systematic Workflow

### Active Plan Documents

**Phase 2 Implementation Plan**: [PHASE_2_PLAN.md](PHASE_2_PLAN.md)
- Comprehensive 10-week implementation plan for LLM processing pipeline
- Technology stack, architecture, cost estimates, risk mitigation
- Detailed week-by-week implementation sequence

**Plan Status Tracking**: [PLAN_STATUS.md](PLAN_STATUS.md)
- Active progress tracking against PHASE_2_PLAN.md
- Checklist of completed, in-progress, and pending tasks
- Critical files status
- Session management notes
- Deviation log

### Systematic Work Protocol

**CRITICAL: All implementation work MUST follow the plan sequence**

1. **Before Starting Any Work**:
   - Read PHASE_2_PLAN.md section 8 (Implementation Sequence)
   - Check PLAN_STATUS.md for current progress
   - Identify the next pending task in sequence

2. **During Work**:
   - Follow the plan's specified approach and architecture
   - Update PLAN_STATUS.md with progress
   - Document any deviations with reasoning

3. **If Deviation Needed**:
   - Document reason in PLAN_STATUS.md "Deviations" section
   - Update PHASE_2_PLAN.md if fundamental change required
   - Commit changes with clear explanation

4. **Context Management**:
   - Monitor token usage (target: <180k before new session)
   - New session recommended at phase boundaries
   - Always reference PLAN_STATUS.md when resuming

### Anti-Slop Measures

**Problem**: AI can create incomplete implementations or deviate from plans

**Solution**:
- **Versioned Plans**: PHASE_2_PLAN.md in git, never just in ephemeral context
- **Status Tracking**: PLAN_STATUS.md shows what's ACTUALLY done vs planned
- **Explicit Checkpoints**: Each phase has completion criteria
- **Review Gate**: Compare deliverables against plan before marking complete

**For Claude**:
- ALWAYS check PLAN_STATUS.md before suggesting next steps
- NEVER deviate from PHASE_2_PLAN.md without explicit user approval
- UPDATE PLAN_STATUS.md after completing ANY task
- COMMIT progress frequently with detailed messages

### Session Continuity

**Starting New Session**:
```markdown
1. Read CLAUDE.MD (this file) - understand project
2. Read PHASE_2_PLAN.md - understand implementation plan
3. Read PLAN_STATUS.md - see current progress
4. Find "Next Immediate Steps" section
5. Continue from there
```

**Token Budget Management**:
- Sessions have 200k token context window
- Aim to start new session at phase boundaries
- Or when approaching 180k tokens
- Current phase completion is natural breakpoint

## Future Directions

1. **Tafsir Integration**: Connect classical Quranic commentaries
2. **Fiqh Rulings Database**: Systematic jurisprudential positions
3. **Seerah Reconstruction**: Comprehensive biographical timeline
4. **Aqidah Ontology**: Theological concept graph
5. **Tasawwuf Pathways**: Spiritual pedagogy mapping
6. **Arabic NLP Pipeline**: Automated semantic extraction tools
7. **Verification Dashboard**: Real-time quality monitoring
8. **Public API**: Semantic search and reasoning endpoints

---

*This repository aims to preserve and make accessible the foundational knowledge of Islam through systematic, verifiable, and computationally-enabled methods. May it serve the pursuit of authentic knowledge.*

**Current Version**: IPKSA v1.2 | PCAP v1.2 | HMSTS v1.1
**Last Updated**: 2026-01-19
