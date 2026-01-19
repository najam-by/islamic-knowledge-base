# Islamic Knowledge Base

A systematic, living knowledge base of Islamic primary sources with rigorous structuring methodologies for AI applications and scholarly research.

## Overview

This repository implements the **Integrated Prophetic Knowledge Structuring Architecture (IPKSA)** to create a verifiable, computationally-accessible knowledge system grounded in Islamic primary sources.

### Hierarchical Authority

1. **Quran** - Primary foundational source (immutable)
2. **Hadith** - Prophetic traditions (immutable source texts, interpretations allowed)
3. **Major Works** - Classical scholarly works for refinement and interpretation

## Quick Start

### For AI/ML Developers
- Read **[CLAUDE.MD](CLAUDE.MD)** for comprehensive project guide
- Review **[methodology/](methodology/)** for structuring protocols
- Access data: `1. quran/`, `2. hadith/`, `3. major works/`

### For Scholars
- **Primary Sources**: 50,884 hadiths from 17 authentic collections
- **Quranic Texts**: Including MASAQ morphological analysis
- **Chronological Framework**: 54 key events from Prophet's life
- **Methodology**: IPKSA v1.2, PCAP v1.2, HMSTS v1.1

### For Contributors
- **Original texts remain immutable**
- **Interpretations require provenance tracking**
- **All additions must maintain IPKSA compliance**
- See Contributing Guidelines in [CLAUDE.MD](CLAUDE.MD)

## Repository Structure

```
.
├── README.md                          # This file - quick overview
├── CLAUDE.MD                          # Comprehensive project guide for Claude/contributors
├── methodology/                       # IPKSA structuring protocols
│   ├── IPKSA.md                      # Architecture overview (v1.2)
│   ├── PCAP.md                       # Chronology assignment protocol (v1.2)
│   └── HMSTS.md                      # Semantic tagging system (v1.1)
├── Prophetic_era_markers__v1_.csv   # Temporal coordinate system
│
├── 1. quran/                         # Quranic texts (Priority 1)
├── 2. hadith/                        # Hadith corpus (Priority 2) - 50,884 hadiths
└── 3. major works/                   # Classical scholarship (Priority 3)
```

## Key Features

### Multi-Layer Semantic System
- **Layer 0**: Textual facts (speaker, addressee, modality)
- **Layer 1**: Ontological categories
- **Layer 2**: Functional roles
- **Layer 3**: Hermeneutic and spiritual dimensions
- **Layer 4**: Thematic vectors and objectives

### Chronological Anchoring
- Temporal mapping to Prophet's life with uncertainty modeling
- Evidence typing (explicit text, event references, chain analysis)
- Bayesian confidence scoring
- Logical consistency validation

### Quality Assurance
- Chronological contradiction detection
- Semantic distortion prevention
- Sectarian bias mitigation
- Over-inference prevention
- Concept drift tracking

## Data Statistics

- **Hadiths**: 50,884 from 17 authentic collections
- **Quranic Verses**: Complete text with morphological analysis
- **Temporal Markers**: 54 key events (570-632 CE / -53 to 11 AH)
- **Major Works**: Starting with Imam al-Ghazali's "Book of Knowledge"

## End Goals

1. **Semantic Knowledge Graph** for AI reasoning with proper context
2. **Moral Commandments Extraction** (obligations, prohibitions, recommendations)
3. **Living Database** with locked sources and tracked interpretations
4. **Verifiable Reasoning** with traceable inference chains

## Current Status

**Phase 1: Foundation** (In Progress)
- [x] Collect 50,884 hadiths from 17 collections
- [x] Obtain Quranic texts with morphological analysis
- [x] Create chronological marker system
- [x] Develop IPKSA/PCAP/HMSTS methodologies
- [x] Structure repository systematically
- [ ] Initialize version control

**Next Phases**: Hadith Processing → Quran Integration → Major Works → Semantic Extraction → AI Application Layer

## Technology Stack

**Current**: Node.js, TypeScript, Cheerio.js, Axios
**Future**: Graph database, Python/TypeScript NLP, REST/GraphQL API

## Documentation

- **[CLAUDE.MD](CLAUDE.MD)** - Comprehensive guide (architecture, schemas, workflows)
- **[methodology/IPKSA.md](methodology/IPKSA.md)** - System architecture
- **[methodology/PCAP.md](methodology/PCAP.md)** - Chronology protocol
- **[methodology/HMSTS.md](methodology/HMSTS.md)** - Semantic tagging
- **[2. hadith/README.md](2.%20hadith/README.md)** - Hadith database details

## License & Attribution

**Hadith Data**: [sunnah.com](https://sunnah.com/)
**Quranic Text**: Public domain for educational/research use
**MASAQ Dataset**: Check original licensing

Islamic religious texts are generally accessible for educational and research purposes.

## Version

**IPKSA v1.2** | **PCAP v1.2** | **HMSTS v1.1**
**Last Updated**: 2026-01-19

---

*May this work serve the pursuit of authentic knowledge and benefit all who seek it.*
