# Phase 2 Implementation Plan: Islamic Knowledge Base - LLM Processing System

## Executive Summary

Design and implement a production-ready system to apply IPKSA/PCAP/HMSTS methodologies to 50,884 hadiths using Large Language Models. This creates the foundational infrastructure for Phase 3 applications (moral commandments extraction, semantic search, AI reasoning).

**Timeline:** 10 weeks (2.5 months)
**Estimated Cost:** $9,000 LLM APIs + infrastructure
**Output:** Fully enriched hadith corpus with temporal + semantic metadata

---

## 1. Technology Stack Decisions

### 1.1 Programming Languages

**Python 3.11+ (Primary)**
- Best ecosystem for LLM APIs (Anthropic, OpenAI SDKs)
- Rich data science libraries (pandas, pydantic)
- Excellent async support for parallel processing
- Strong NLP tools for Arabic text

**TypeScript/Node.js (Phase 3 API)**
- API layer for Phase 3
- Maintains consistency with existing hadith scraper code

### 1.2 Database Architecture (Hybrid)

**PostgreSQL with jsonb (Primary Storage)**
- Rationale: Flexible schema, ACID compliance, proven scalability
- Use: Processed hadiths, versions, validation results
- Cost: $0 (self-hosted) or $20/month (managed)

**Neo4j (Graph Layer - Phase 2.5)**
- Rationale: Native graph traversal for relationships
- Use: Abrogation chains, pedagogical sequences, thematic clustering
- Implementation: Sync from PostgreSQL after enrichment

**Redis (Caching & Queue)**
- Rationale: Fast in-memory operations
- Use: LLM response caching, processing queue, rate limiting

### 1.3 LLM Strategy

**Claude 3.5 Sonnet (Primary)**
- 200k context window (full methodology + examples)
- Superior reasoning for temporal logic & semantic analysis
- Structured output support
- Cost: ~$3k PCAP + ~$5k HMSTS = **$8k total**

**GPT-4o (Secondary/Validation)**
- Cross-validation for critical assignments
- Fallback for rate limits

**Local LLM (Phase 2.5 - Optional)**
- Llama 3.1 70B for cost reduction on re-processing

---

## 2. System Architecture

```
INPUT LAYER (Phase 1 - Complete)
├─ 50,884 hadiths (JSON)
├─ Temporal markers CSV (54 events)
└─ Methodology docs (IPKSA, PCAP, HMSTS)

PROCESSING PIPELINE (Phase 2)
├─ Ingestion → Load hadiths into PostgreSQL
├─ Preprocessing → Normalize text, parse isnad
├─ LLM Orchestrator → Rate limiting, caching, retry
│   ├─ PCAP Processor → Temporal assignment
│   └─ HMSTS Processor → Semantic tagging (5 layers)
├─ Validation → Temporal, semantic, consistency checks
└─ Cross-linking → Abrogation, tensions, themes

STORAGE LAYER
├─ PostgreSQL → Versioned processed data
├─ Redis → Cache + queue
└─ Neo4j → Graph relationships (Phase 2.5)

OUTPUT LAYER (Phase 3)
├─ REST/GraphQL API
├─ Semantic search
└─ Reasoning interface
```

---

## 3. Directory Structure

```
/Users/ns/home/library/ctrl/db/
├── processing/                        # NEW - Phase 2 codebase
│   ├── requirements.txt              # Python dependencies
│   ├── docker-compose.yml            # Infrastructure (PostgreSQL, Redis, Neo4j)
│   ├── .env.example                  # Config template
│   │
│   ├── config/
│   │   ├── settings.py              # Pydantic settings
│   │   ├── prompts/
│   │   │   ├── pcap_system.txt     # PCAP methodology prompt
│   │   │   ├── pcap_examples.yaml  # Few-shot examples
│   │   │   ├── hmsts_system.txt    # HMSTS 5-layer prompt
│   │   │   └── hmsts_examples.yaml
│   │   └── schemas/
│   │       ├── hadith_ipksa.json   # Extended schema
│   │       ├── pcap_output.json
│   │       └── hmsts_output.json
│   │
│   ├── src/
│   │   ├── models/                  # Pydantic data models
│   │   │   ├── hadith.py
│   │   │   ├── temporal.py         # PCAP models
│   │   │   └── semantic.py         # HMSTS models
│   │   │
│   │   ├── ingestion/              # Data loading
│   │   │   ├── hadith_loader.py
│   │   │   └── marker_loader.py
│   │   │
│   │   ├── preprocessing/
│   │   │   ├── arabic_normalizer.py
│   │   │   └── isnad_parser.py
│   │   │
│   │   ├── llm/                    # LLM integration
│   │   │   ├── claude.py
│   │   │   ├── rate_limiter.py
│   │   │   ├── cache.py
│   │   │   ├── cost_tracker.py
│   │   │   └── prompt_builder.py   # CRITICAL
│   │   │
│   │   ├── processors/             # Core logic
│   │   │   ├── pcap_processor.py   # CRITICAL
│   │   │   ├── hmsts_processor.py  # CRITICAL
│   │   │   └── orchestrator.py
│   │   │
│   │   ├── validation/
│   │   │   ├── temporal_validator.py # CRITICAL
│   │   │   ├── semantic_validator.py
│   │   │   └── consistency_checker.py
│   │   │
│   │   └── storage/
│   │       ├── postgres.py         # CRITICAL
│   │       └── neo4j_sync.py
│   │
│   ├── scripts/                    # CLI tools
│   │   ├── setup_db.py
│   │   ├── process_hadiths.py
│   │   └── generate_report.py
│   │
│   └── tests/
│
├── processed/                       # NEW - Outputs
│   ├── versions/v1.0/
│   │   ├── hadiths_ipksa/
│   │   └── validation_reports/
│   ├── exports/
│   └── checkpoints/
```

---

## 4. Processing Pipeline Design

### 4.1 Pipeline Stages

**Stage 1: INITIALIZATION**
- Load configuration & credentials
- Initialize database connections
- Load temporal markers + methodology docs
- Check for existing checkpoints

**Stage 2: INGESTION**
- Load all 50,884 hadiths from JSON
- Store in PostgreSQL (raw_hadiths table)
- Create processing queue
- Checkpoint saved

**Stage 3: PREPROCESSING**
- Normalize Arabic text
- Parse isnad (narrator chains)
- Extract explicit temporal markers from text
- Checkpoint saved

**Stage 4: PCAP PROCESSING (Temporal Assignment)**
- Batch: 100 hadiths per batch, 5 parallel workers
- For each hadith:
  - Build PCAP prompt (methodology + markers + 3-5 examples)
  - Call Claude API with structured output
  - Validate temporal constraints
  - Calculate confidence score
  - Store temporal data
- Checkpoint every 500 hadiths
- **Estimated time:** 20-25 hours with parallelization

**Stage 5: HMSTS PROCESSING (Semantic Tagging)**
- Batch: 50 hadiths per batch, 5 parallel workers
- For each hadith:
  - Build HMSTS prompt (5 layers + vocabularies + 5-7 examples)
  - Call Claude API with structured output
  - Validate semantic consistency
  - Cross-check against classical taxonomy
  - Store semantic data
- Checkpoint every 500 hadiths
- **Estimated time:** 20-25 hours with parallelization

**Stage 6: CROSS-LINKING**
- Abrogation detection (nasikh/mansukh)
- Tension identification
- Thematic clustering
- Pedagogical sequencing

**Stage 7: VALIDATION**
- Temporal: Anchor consistency, Allen interval logic, companion verification
- Semantic: Ontology compliance, layer coherence
- Consistency: Chronological contradictions, semantic distortions
- Quality scoring with confidence aggregation

**Stage 8: GRAPH CONSTRUCTION (Phase 2.5)**
- Export to Neo4j
- Create nodes + relationships
- Index for queries

**Stage 9: EXPORT**
- JSON, CSV, JSONLines formats
- Processing reports
- Version archive

### 4.2 Batch Processing Strategy

```python
PCAP_BATCH_SIZE = 100
HMSTS_BATCH_SIZE = 50
PARALLEL_WORKERS = 5
CHECKPOINT_INTERVAL = 500
```

**Resume Capability:**
- Checkpoint file tracks last processed ID
- On restart, skip completed hadiths
- Merge with existing data

---

## 5. LLM Integration Strategy

### 5.1 Prompt Engineering

**PCAP Prompt Structure (~14k tokens input, ~1k output):**
```
SYSTEM PROMPT (~8k tokens):
- Full PCAP methodology from PCAP.md
- Temporal marker reference table
- Evidence typing definitions
- Certainty scoring guidelines
- JSON output schema

USER PROMPT (~2k tokens per hadith):
- Hadith text (Arabic + English)
- Isnad information
- Detected temporal markers

FEW-SHOT EXAMPLES (~4k tokens):
- 3-5 diverse examples with reasoning
- Explicit text evidence
- Uncertain timing handling
- Isnad-based dating
```

**Cost per hadith:** ~$0.06
**Total PCAP cost:** 50,884 × $0.06 = **~$3,053**

**HMSTS Prompt Structure (~22k tokens input, ~2k output):**
```
SYSTEM PROMPT (~12k tokens):
- Full HMSTS methodology (5 layers)
- Controlled vocabularies
- Interpretive principles
- JSON output schema

USER PROMPT (~2.5k tokens per hadith):
- Hadith text + temporal context
- Era/date information

FEW-SHOT EXAMPLES (~8k tokens):
- 5-7 examples covering all layer types
- Normative, descriptive, spiritual
- Multi-dimensional analysis
```

**Cost per hadith:** ~$0.10
**Total HMSTS cost:** 50,884 × $0.10 = **~$5,088**

**TOTAL ESTIMATED LLM COST: $8,000-10,000**

### 5.2 Structured Output & Validation

**Claude JSON Mode:**
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    temperature=0.1,  # Low for consistency
    system=pcap_system_prompt,
    messages=[{"role": "user", "content": user_prompt}],
    response_format={"type": "json_object"}
)
```

**Pydantic Validation:**
```python
class PCAPOutput(BaseModel):
    era_id: str = Field(..., regex="^E[0-3]$")
    earliest_ah: float
    latest_ah: float
    evidence_type: Literal['explicit_text', 'explicit_event',
                          'isnad_generation', 'sirah_alignment',
                          'contextual_order', 'speculative']
    posterior_confidence: float = Field(..., ge=0, le=1)
    reasoning: str = Field(..., min_length=50)
```

### 5.3 Rate Limiting & Retry

**Rate Limiter:**
- Claude tier 2: 5,000 RPM, 400k tokens/minute
- Track request times and token usage
- Auto-throttle when approaching limits

**Retry Strategy (tenacity):**
```python
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
async def call_llm_with_retry(prompt: str) -> dict:
    # Exponential backoff on rate limits
```

### 5.4 Cost Optimization

- **Prompt caching:** Cache system prompts
- **Response caching:** Cache identical hadiths
- **Batch similar:** Group by chapter/theme
- **Expected savings:** 20-30% → **$6k-7k actual cost**

---

## 6. Data Storage Strategy

### 6.1 PostgreSQL Schema

**Key Tables:**
```sql
-- Immutable source data
CREATE TABLE raw_hadiths (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    arabic TEXT,
    english_text TEXT,
    ...
);

-- PCAP temporal assignments
CREATE TABLE pcap_assignments (
    hadith_id INTEGER REFERENCES raw_hadiths(id),
    version VARCHAR(20),
    era_id VARCHAR(10),
    earliest_ah FLOAT,
    latest_ah FLOAT,
    evidence_type VARCHAR(50),
    posterior_confidence FLOAT,
    reasoning TEXT,
    ...
    UNIQUE(hadith_id, version)
);

-- HMSTS semantic tags
CREATE TABLE hmsts_tags (
    hadith_id INTEGER REFERENCES raw_hadiths(id),
    version VARCHAR(20),
    layer0_speaker VARCHAR(255),
    layer0_modality VARCHAR(50),
    layer1_categories TEXT[],
    layer2_role VARCHAR(50),
    layer3_axis_a JSONB,
    layer4_vectors JSONB,
    ...
    UNIQUE(hadith_id, version)
);

-- Cross-references
CREATE TABLE hadith_links (
    hadith_id INTEGER,
    related_hadith_id INTEGER,
    link_type VARCHAR(50),  -- 'abrogation', 'tension', 'theme'
    confidence FLOAT,
    ...
);

-- Validation results
CREATE TABLE validation_results (
    hadith_id INTEGER,
    validation_type VARCHAR(50),
    status VARCHAR(20),  -- 'pass', 'warning', 'fail'
    issues JSONB,
    quality_score FLOAT
);
```

**Versioning:**
- Each processing run versioned (v1.0, v1.1)
- Allows reprocessing without data loss
- A/B comparison of methodologies

### 6.2 Neo4j Graph Schema (Phase 2.5)

**Nodes:** Hadith, Era, Event, Theme, Concept
**Relationships:** TEMPORAL_BEFORE, ABROGATES, RELATES_TO, NARRATED_BY

---

## 7. Validation Framework

### 7.1 Temporal Validation

**Anchor Event Consistency:**
```python
def validate_anchor_consistency(pcap: PCAPOutput) -> ValidationResult:
    # Check anchor_before constraints
    # Check anchor_after constraints
    # Allen interval logic validation
    # Return pass/warning/fail with issues
```

**Companion Presence Verification:**
- Check narrator birth/death years
- Verify location consistency
- Flag anachronisms

### 7.2 Semantic Validation

**Ontology Compliance:**
- Validate against controlled vocabularies
- Check layer coherence (literal foundation required)
- Detect mystification without base

**Quality Scoring:**
```python
overall_score = (
    0.35 * temporal_confidence +
    0.25 * evidence_strength +
    0.25 * validation_pass_rate +
    0.15 * semantic_completeness
)
```

### 7.3 Consistency Validation

- Detect chronological contradictions (temporal cycles)
- Detect semantic distortions (over-categorization)
- Cross-check confidence vs evidence type

---

## 8. Implementation Sequence (10 Weeks)

### Phase 2.1: Foundation (Week 1-2)
- [ ] Set up PostgreSQL, Redis (Docker)
- [ ] Create database schema + migrations
- [ ] Define Pydantic models
- [ ] Load hadiths + temporal markers into DB

### Phase 2.2: Preprocessing (Week 3)
- [ ] Implement text normalization
- [ ] Build isnad parser
- [ ] Implement LLM integration (Claude, rate limiter, cache)

### Phase 2.3: PCAP Processing (Week 4-5)
- [ ] Engineer PCAP prompts + examples
- [ ] Build PCAP processor with batching
- [ ] Implement temporal validator
- [ ] Process full corpus (50,884 hadiths)
- [ ] Generate PCAP report

### Phase 2.4: HMSTS Processing (Week 6-7)
- [ ] Engineer HMSTS prompts (5 layers)
- [ ] Build HMSTS processor
- [ ] Implement semantic validator
- [ ] Process full corpus
- [ ] Generate HMSTS report

### Phase 2.5: Cross-Linking & Validation (Week 8)
- [ ] Build linking processor (abrogation, themes)
- [ ] Run comprehensive validation
- [ ] Calculate quality scores
- [ ] Review low-confidence hadiths

### Phase 2.6: Graph & Export (Week 9)
- [ ] Set up Neo4j, build sync
- [ ] Export processed data (JSON, CSV)
- [ ] Generate processing reports

### Phase 2.7: Testing & Documentation (Week 10)
- [ ] Write test suite
- [ ] Optimize performance
- [ ] Complete documentation
- [ ] Prepare Phase 3 handoff

---

## 9. Phase 3 Extensibility

### 9.1 API Layer (Future)

**REST Endpoints:**
```
GET  /api/v1/hadiths?era={era}&theme={theme}
GET  /api/v1/hadiths/{id}
GET  /api/v1/hadiths/{id}/abrogation
GET  /api/v1/commandments/obligations
POST /api/v1/query (semantic search)
POST /api/v1/reasoning (AI reasoning with sources)
```

### 9.2 Query Interface

**Semantic Search Engine:**
- Search by theme, modality, spiritual layer
- Filter by confidence score
- Pedagogical sequence queries

**Reasoning Engine:**
- Derive rulings with source hierarchy (Quran > Hadith)
- Explain contradictions (temporal/semantic context)
- Trace concept evolution through Prophetic era

### 9.3 Moral Commandments Extraction

```python
class CommandmentExtractor:
    def extract_obligations(self) -> List[MoralCommandment]:
        return query_db(modality='obligatory',
                       functional_role='Normative',
                       min_confidence=0.75)

    def extract_prohibitions(self) -> List[MoralCommandment]:
        return query_db(modality='forbidden',
                       functional_role='Normative',
                       min_confidence=0.75)
```

**Output Schema:**
```python
class MoralCommandment(BaseModel):
    type: Literal['wajib', 'haram', 'mustahabb', 'makruh', 'mubah']
    text: str
    sources: List[int]  # Hadith IDs
    scope: Literal['individual', 'communal', 'universal']
    certainty: Literal['qatʿī', 'ẓannī']
    conditions: Optional[List[str]]
    temporal_context: TemporalData
```

---

## 10. Risk Mitigation

### Technical Risks
- **API rate limits:** Multi-provider support, rate limiter
- **Cost overruns:** Set caps, progressive processing, caching (20-30% savings)
- **Low LLM quality:** Validation framework, human review, reprocessing
- **Data loss:** Checkpoint system every 500 hadiths

### Scholarly Risks
- **Sectarian bias:** Majority-position weighting, classical validation
- **Over-interpretation:** Layer coherence checks, literal foundation requirement
- **Chronological errors:** Anchor event constraints, companion verification
- **Concept drift:** Controlled vocabularies, ontology versioning

### Contingency Plans
- If costs exceed budget: Optimize prompts, use local LLM, phase processing
- If quality insufficient: Refine prompts, use Claude Opus, human-in-loop
- If timeline exceeds: Prioritize critical collections (Bukhari, Muslim)

---

## 11. Cost Summary

**LLM API Costs:**
- PCAP: $3,053
- HMSTS: $5,088
- Validation/reprocessing: $1,000
- **Total (with caching savings): $6,000-7,000**

**Infrastructure:**
- PostgreSQL: $0-20/month
- Redis: $0-10/month
- Neo4j: $0-65/month
- **Total: $0-95/month**

**Development Time:**
- 10 weeks (2.5 months)
- Senior Python/ML engineer: $20k-40k (if hiring)

**TOTAL PHASE 2 INVESTMENT: $26,000-47,000**

---

## 12. Critical Files for Implementation

1. **processing/src/processors/pcap_processor.py** - Temporal assignment core logic
2. **processing/src/processors/hmsts_processor.py** - Semantic tagging (5 layers)
3. **processing/src/llm/prompt_builder.py** - Dynamic prompt construction
4. **processing/src/validation/temporal_validator.py** - Chronological consistency
5. **processing/src/storage/postgres.py** - Database operations
6. **processing/config/prompts/pcap_system.txt** - PCAP methodology prompt
7. **processing/config/prompts/hmsts_system.txt** - HMSTS 5-layer prompt
8. **processing/src/models/hadith.py** - Pydantic IPKSA schema

---

## Success Metrics

**Phase 2 Completion Criteria:**
- [ ] 50,884 hadiths processed through PCAP (temporal assignment)
- [ ] 50,884 hadiths processed through HMSTS (semantic tagging)
- [ ] Average quality score ≥ 0.70
- [ ] <5% validation failures requiring manual review
- [ ] Complete processing reports + statistics
- [ ] Versioned exports (JSON, CSV) ready for Phase 3
- [ ] Neo4j graph with relationships populated
- [ ] Documentation complete for Phase 3 handoff

**Quality Targets:**
- Temporal confidence (avg): ≥ 0.75
- Validation pass rate: ≥ 95%
- API response time (Phase 3): < 200ms
- Cost within budget: $6k-7k LLM costs

---

## Next Steps After Approval

1. **Set up development environment** (Docker, Python, databases)
2. **Initialize processing/ directory structure**
3. **Install dependencies** (Anthropic SDK, PostgreSQL, Redis clients)
4. **Create database schema** (Alembic migrations)
5. **Load source data** (hadiths, temporal markers)
6. **Begin PCAP prompt engineering** (critical for quality)
7. **Implement core processors** (PCAP → HMSTS → Validation)
8. **Start incremental processing** (checkpoint-based)

**Ready to proceed with Phase 2 implementation upon approval.**
