# PostgreSQL Database Schema
**Islamic Knowledge Base - IPKSA Processing System**

## Overview

This database stores 50,884 hadiths with PCAP (temporal) and HMSTS (semantic) enrichment metadata. The schema supports versioning, JSONB for flexible semantic data, and efficient querying.

## Schema Design

### Seven Core Tables

1. **raw_hadiths** (50,884 rows) - Immutable source data from JSON files
2. **preprocessed_hadiths** (50,884 rows) - Normalized text, parsed isnad
3. **temporal_markers** (54 rows) - Prophetic era events reference
4. **pcap_assignments** (~50k per version) - PCAP temporal assignments
5. **hmsts_tags** (~50k per version) - HMSTS semantic tags (5 layers)
6. **hadith_links** (~100k estimated) - Cross-references between hadiths
7. **validation_results** (~200k estimated) - Validation outcomes

### Key Design Decisions

**Versioning**: Single `version VARCHAR(20)` column in enriched tables
- Query across versions or filter by specific version
- No dynamic table creation needed
- Storage efficient with partial indexes

**JSONB Columns**: Used for layer3_axis_a, layer3_axis_b, layer4_vectors
- Preserves nested structure from LLM JSON output
- Queryable with GIN indexes
- Flexible schema evolution

**Index Strategy**:
- B-Tree: Primary keys, foreign keys, equality/range queries
- GIN: JSONB columns, TEXT[] arrays, full-text search
- Partial: Sparse data (e.g., explicit dates only)
- Composite: Common query patterns (book_id, chapter_id, version)

## Table Details

### 1. raw_hadiths

**Purpose**: Immutable source data from sunnah.com JSON files

**Schema**:
```sql
CREATE TABLE raw_hadiths (
    id INTEGER PRIMARY KEY,
    id_in_book INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    chapter_id INTEGER NOT NULL,
    arabic TEXT NOT NULL,
    english_narrator TEXT,
    english_text TEXT,
    book_name_arabic VARCHAR(255),
    book_name_english VARCHAR(255),
    chapter_name_arabic TEXT,
    chapter_name_english TEXT,
    source_file VARCHAR(500),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (book_id, id_in_book)
);
```

**Indexes**:
- `idx_raw_hadiths_book` - B-Tree on book_id
- `idx_raw_hadiths_chapter` - B-Tree on chapter_id
- `idx_raw_hadiths_book_chapter` - Composite (book_id, chapter_id)
- `idx_raw_hadiths_arabic_fts` - GIN full-text search (Arabic)
- `idx_raw_hadiths_english_fts` - GIN full-text search (English)

**Constraints**:
- PRIMARY KEY on id
- UNIQUE (book_id, id_in_book) prevents duplicates

### 2. preprocessed_hadiths

**Purpose**: Normalized text and parsed isnad chains

**Schema**:
```sql
CREATE TABLE preprocessed_hadiths (
    hadith_id INTEGER PRIMARY KEY REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    arabic_normalized TEXT,
    english_normalized TEXT,
    isnad_chain TEXT[],
    isnad_generation INTEGER,
    explicit_temporal_references TEXT[],
    explicit_person_references TEXT[],
    text_length_arabic INTEGER,
    text_length_english INTEGER,
    has_explicit_date BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preprocessing_version VARCHAR(20) DEFAULT '1.0'
);
```

**Indexes**:
- `idx_preprocessed_generation` - B-Tree on isnad_generation
- `idx_preprocessed_has_date` - Partial index WHERE has_explicit_date = TRUE

### 3. temporal_markers

**Purpose**: Reference table for Prophetic era events (54 events)

**Schema**:
```sql
CREATE TABLE temporal_markers (
    event_id VARCHAR(20) PRIMARY KEY,
    parent_event_id VARCHAR(20) REFERENCES temporal_markers(event_id),
    depth INTEGER NOT NULL,
    era_category VARCHAR(10),
    ce_start DATE,
    ce_end DATE,
    ah_value VARCHAR(50),
    event_name_english VARCHAR(255) NOT NULL,
    event_name_arabic VARCHAR(255),
    location VARCHAR(255),
    significance TEXT,
    certainty_date VARCHAR(10),
    certainty_event VARCHAR(10),
    source_tradition VARCHAR(255),
    notes TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- `idx_temporal_era` - B-Tree on era_category
- `idx_temporal_dates` - Composite (ce_start, ce_end)

**Hierarchical Structure**: Self-referencing foreign key for parent-child relationships

### 4. pcap_assignments

**Purpose**: PCAP temporal assignments with versioning

**Schema**:
```sql
CREATE TABLE pcap_assignments (
    id SERIAL PRIMARY KEY,
    hadith_id INTEGER NOT NULL REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    -- Temporal assignment
    era_id VARCHAR(20) NOT NULL,
    sub_era_id VARCHAR(20),
    event_window_id VARCHAR(20),
    earliest_ah DECIMAL(6,2) NOT NULL,
    latest_ah DECIMAL(6,2) NOT NULL,
    earliest_ce DATE,
    latest_ce DATE,
    anchor_before TEXT[],
    anchor_after TEXT[],
    -- Evidence and confidence
    evidence_type VARCHAR(50) NOT NULL,
    posterior_confidence DECIMAL(4,3) NOT NULL,
    reasoning TEXT NOT NULL,
    -- Metadata
    llm_model VARCHAR(100),
    llm_cost_usd DECIMAL(8,6),
    processing_duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (hadith_id, version),
    CHECK (earliest_ah <= latest_ah),
    CHECK (posterior_confidence >= 0 AND posterior_confidence <= 1),
    CHECK (evidence_type IN ('explicit_text', 'explicit_event', 'isnad_generation',
                             'sirah_alignment', 'contextual_order', 'speculative'))
);
```

**Indexes**:
- `idx_pcap_hadith_version` - Composite (hadith_id, version)
- `idx_pcap_era` - Composite (era_id, version)
- `idx_pcap_confidence` - Composite (posterior_confidence, version)
- `idx_pcap_date_range` - Composite (earliest_ah, latest_ah, version)
- `idx_pcap_anchors` - GIN (anchor_before, anchor_after)

**Key Features**:
- DECIMAL(6,2) for AH dates supports fractional years: -53.00 to 9999.99
- TEXT[] arrays for anchor relationships
- CHECK constraints enforce data validity

### 5. hmsts_tags

**Purpose**: HMSTS semantic tags (5 layers) with versioning

**Schema**:
```sql
CREATE TABLE hmsts_tags (
    id SERIAL PRIMARY KEY,
    hadith_id INTEGER NOT NULL REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    -- Layer 0: Textual Fact
    layer0_speaker VARCHAR(255),
    layer0_addressee VARCHAR(255),
    layer0_verb_type VARCHAR(100),
    layer0_modality VARCHAR(50),
    -- Layer 1: Ontological Category
    layer1_categories TEXT[] NOT NULL,
    -- Layer 2: Functional Role
    layer2_role VARCHAR(50) NOT NULL,
    -- Layer 3: Four Meaning Axes (JSONB)
    layer3_axis_a JSONB,
    layer3_axis_b JSONB,
    -- Layer 4: Thematic Vectors (JSONB)
    layer4_vectors JSONB,
    -- Metadata
    llm_model VARCHAR(100),
    llm_cost_usd DECIMAL(8,6),
    processing_duration_ms INTEGER,
    semantic_completeness_score DECIMAL(4,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (hadith_id, version),
    CHECK (layer0_modality IN ('obligatory', 'recommended', 'permitted',
                                'discouraged', 'forbidden', 'informative')),
    CHECK (layer2_role IN ('Normative', 'Descriptive', 'Explanatory', 'Corrective',
                          'Exemplary', 'Prophetic State', 'Divine Address', 'Divine Attribute'))
);
```

**Indexes**:
- `idx_hmsts_hadith_version` - Composite (hadith_id, version)
- `idx_hmsts_modality` - Composite (layer0_modality, version)
- `idx_hmsts_role` - Composite (layer2_role, version)
- `idx_hmsts_categories` - GIN (layer1_categories)
- `idx_hmsts_layer3_a` - GIN (layer3_axis_a)
- `idx_hmsts_layer3_b` - GIN (layer3_axis_b)
- `idx_hmsts_layer4` - GIN (layer4_vectors)

**JSONB Structure Examples**:

Layer 3 Axis A (Hermeneutic):
```json
{
  "zahir": {
    "proposition": "Prayer is obligatory five times daily",
    "scope": "universal",
    "certainty": "qatʿī",
    "conditionality": "absolute"
  },
  "ishara": null,
  "akhlaq": null,
  "haqiqa": null
}
```

Layer 4 Vectors (Thematic):
```json
{
  "divine_attributes": ["Al-Rahman", "Al-Hakim"],
  "faculties_addressed": ["intellect", "will"],
  "maqam_hal": "tawakkul",
  "legal_cause": "protection of life",
  "objective": "social cohesion",
  "values": ["justice", "mercy"],
  "vices": ["arrogance"]
}
```

### 6. hadith_links

**Purpose**: Cross-references between hadiths (abrogation, themes, etc.)

**Schema**:
```sql
CREATE TABLE hadith_links (
    id SERIAL PRIMARY KEY,
    hadith_id INTEGER NOT NULL REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    related_hadith_id INTEGER NOT NULL REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    link_type VARCHAR(50) NOT NULL,
    link_subtype VARCHAR(100),
    confidence DECIMAL(4,3),
    reasoning TEXT,
    theme_label VARCHAR(255),
    pedagogical_sequence INTEGER,
    is_bidirectional BOOLEAN DEFAULT FALSE,
    detected_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (hadith_id != related_hadith_id),
    CHECK (link_type IN ('abrogation', 'tension', 'theme', 'pedagogical', 'corroboration'))
);
```

**Indexes**:
- `idx_links_hadith` - Composite (hadith_id, version)
- `idx_links_related` - Composite (related_hadith_id, version)
- `idx_links_type` - Composite (link_type, version)
- `idx_unique_link` - Unique index on normalized pair WHERE is_bidirectional = TRUE

**Unique Bidirectional Links**: Uses LEAST/GREATEST to prevent duplicate A→B and B→A entries

### 7. validation_results

**Purpose**: Validation outcomes and quality scores

**Schema**:
```sql
CREATE TABLE validation_results (
    id SERIAL PRIMARY KEY,
    hadith_id INTEGER NOT NULL REFERENCES raw_hadiths(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL DEFAULT 'v1.0',
    validation_type VARCHAR(100) NOT NULL,
    validation_category VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    issues JSONB,
    quality_score DECIMAL(4,3),
    temporal_confidence DECIMAL(4,3),
    semantic_completeness DECIMAL(4,3),
    validation_pass_rate DECIMAL(4,3),
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validator_version VARCHAR(20),
    CHECK (status IN ('pass', 'warning', 'fail')),
    CHECK (validation_category IN ('temporal', 'semantic', 'consistency', 'overall'))
);
```

**Indexes**:
- `idx_validation_hadith_version` - Composite (hadith_id, version)
- `idx_validation_status` - Composite (status, version)
- `idx_validation_issues` - GIN (issues)

## Common Queries

### Get Latest PCAP Assignment
```sql
SELECT * FROM pcap_assignments
WHERE hadith_id = 1
ORDER BY version DESC LIMIT 1;
```

### Find Hadiths by Era
```sql
SELECT h.id, h.arabic, p.era_id, p.posterior_confidence
FROM raw_hadiths h
JOIN pcap_assignments p ON h.id = p.hadith_id
WHERE p.era_id = 'E2' AND p.version = 'v1.0'
ORDER BY p.earliest_ah;
```

### Search JSONB Values
```sql
-- Find hadiths with "justice" value
SELECT * FROM hmsts_tags
WHERE layer4_vectors @> '{"values": ["justice"]}'::jsonb
AND version = 'v1.0';
```

### Compare Versions
```sql
SELECT
    v1.hadith_id,
    v1.era_id as era_v1,
    v2.era_id as era_v2,
    v1.posterior_confidence as conf_v1,
    v2.posterior_confidence as conf_v2
FROM pcap_assignments v1
JOIN pcap_assignments v2 USING (hadith_id)
WHERE v1.version = 'v1.0' AND v2.version = 'v1.1'
AND v1.era_id != v2.era_id;
```

### Get Validation Summary
```sql
SELECT
    validation_category,
    status,
    COUNT(*) as count,
    AVG(quality_score) as avg_quality
FROM validation_results
WHERE version = 'v1.0'
GROUP BY validation_category, status
ORDER BY validation_category, status;
```

## Performance Expectations

For 50,884 hadiths:
- Single hadith retrieval: <10ms
- Batch queries (1000 rows): <100ms
- Full table scan: <1 second
- JSONB containment queries: <50ms with GIN index

## Migration Management

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Last Migration
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

### Current Database Version
```bash
alembic current
```

## Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://ikb_user:changeme123@localhost:5432/islamic_kb",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

## Setup Instructions

1. **Start PostgreSQL**:
   ```bash
   docker-compose up -d postgres
   ```

2. **Run setup script**:
   ```bash
   cd processing
   ./scripts/setup_database.sh
   ```

3. **Verify schema**:
   ```bash
   psql -h localhost -U ikb_user -d islamic_kb
   \dt  -- List tables
   \d raw_hadiths  -- Describe table
   ```

## Next Steps

After schema creation:
1. Define Pydantic models (src/models/)
2. Implement data ingestion (src/ingestion/)
3. Load 50,884 hadiths into database
4. Begin Phase 2.2: Preprocessing
