# Islamic Knowledge Base - Processing Pipeline

Phase 2 implementation for applying IPKSA/PCAP/HMSTS methodologies to 50,884 hadiths using Large Language Models.

## Overview

This processing system enriches the raw hadith corpus with:
- **Temporal data** (PCAP): Chronological assignment with uncertainty modeling
- **Semantic data** (HMSTS): 5-layer multi-dimensional semantic tagging
- **Cross-references**: Abrogation chains, thematic links, pedagogical sequences
- **Validation**: Quality assurance and consistency checking

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Docker & Docker Compose
- 10GB+ available disk space
- Anthropic API key (Claude)

### 2. Installation

```bash
# Navigate to processing directory
cd /Users/ns/home/library/ctrl/db/processing

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

### 3. Start Infrastructure

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Wait for health checks
docker-compose ps

# Initialize database schema
python scripts/setup_db.py
```

### 4. Load Source Data

```bash
# Ingest hadiths and temporal markers
python scripts/ingest_data.py
```

### 5. Run Processing

```bash
# Process hadiths through PCAP (temporal assignment)
python scripts/process_hadiths.py --stage pcap

# Process hadiths through HMSTS (semantic tagging)
python scripts/process_hadiths.py --stage hmsts

# Run cross-linking
python scripts/process_hadiths.py --stage linking

# Run validation
python scripts/validate_outputs.py
```

## Architecture

```
processing/
├── config/               # Configuration & prompts
│   ├── settings.py      # Pydantic settings management
│   ├── prompts/         # LLM prompt templates
│   └── schemas/         # JSON schemas for validation
│
├── src/                  # Source code
│   ├── models/          # Pydantic data models
│   ├── ingestion/       # Data loading
│   ├── preprocessing/   # Text normalization
│   ├── llm/             # LLM integration & rate limiting
│   ├── processors/      # Core processing logic (PCAP, HMSTS)
│   ├── validation/      # Quality assurance
│   └── storage/         # Database operations
│
├── scripts/             # CLI tools
│   ├── setup_db.py      # Database initialization
│   ├── ingest_data.py   # Load source data
│   ├── process_hadiths.py  # Main processing script
│   └── validate_outputs.py # Validation runner
│
└── tests/               # Test suite
```

## Processing Pipeline

### Stage 1: Initialization
- Load configuration
- Initialize database connections
- Load temporal markers + methodology docs
- Check for checkpoints

### Stage 2: Ingestion
- Load 50,884 hadiths from JSON
- Store in PostgreSQL
- Create processing queue

### Stage 3: Preprocessing
- Normalize Arabic/English text
- Parse isnad (narrator chains)
- Extract explicit temporal markers

### Stage 4: PCAP Processing
- Batch: 100 hadiths, 5 parallel workers
- Temporal assignment using Claude
- Validate against anchor events
- Checkpoint every 500 hadiths
- **Estimated time:** 20-25 hours

### Stage 5: HMSTS Processing
- Batch: 50 hadiths, 5 parallel workers
- 5-layer semantic tagging using Claude
- Validate ontology compliance
- Checkpoint every 500 hadiths
- **Estimated time:** 20-25 hours

### Stage 6: Cross-Linking
- Abrogation detection
- Tension identification
- Thematic clustering

### Stage 7: Validation
- Temporal validation
- Semantic validation
- Consistency checks
- Quality scoring

### Stage 8: Export
- JSON, CSV, JSONLines formats
- Processing reports
- Version archive

## Configuration

See `.env.example` for all configuration options.

**Key Settings:**
- `ANTHROPIC_API_KEY`: Your Claude API key (required)
- `PCAP_BATCH_SIZE`: Hadiths per PCAP batch (default: 100)
- `HMSTS_BATCH_SIZE`: Hadiths per HMSTS batch (default: 50)
- `PARALLEL_WORKERS`: Async workers (default: 5)
- `CHECKPOINT_INTERVAL`: Save progress every N hadiths (default: 500)

## Cost Management

**Estimated LLM API Costs:**
- PCAP: ~$3,000
- HMSTS: ~$5,000
- With caching: **~$6,000-7,000 total**

**Cost Controls:**
- `COST_BUDGET_USD`: Hard limit on spending
- `COST_ALERT_THRESHOLD`: Alert percentage
- Automatic cost tracking and reporting

## Checkpoints & Resume

Processing automatically saves checkpoints every 500 hadiths. If interrupted:

```bash
# Automatically resume from latest checkpoint
python scripts/process_hadiths.py --stage pcap --resume

# Or specify checkpoint file
python scripts/process_hadiths.py --stage pcap --checkpoint checkpoints/pcap_checkpoint_15000.json
```

## Monitoring

### Progress Tracking
```bash
# View real-time progress
tail -f logs/processing.log

# Generate progress report
python scripts/generate_report.py --stage pcap
```

### Quality Metrics
```bash
# View validation results
python scripts/validate_outputs.py --report

# Quality dashboard (Jupyter)
jupyter notebook notebooks/quality_analysis.ipynb
```

## Database Access

### PostgreSQL
```bash
# Connect to database
docker exec -it islamic_kb_postgres psql -U ikb_user -d islamic_kb

# Or use PgAdmin (start with --profile tools)
docker-compose --profile tools up -d
# Access: http://localhost:5050
```

### Redis
```bash
# Connect to Redis
docker exec -it islamic_kb_redis redis-cli

# View cached items
redis-cli KEYS "pcap:*"
```

### Neo4j (Phase 2.5)
```bash
# Start Neo4j
docker-compose --profile phase2.5 up -d

# Access browser: http://localhost:7474
# Username: neo4j, Password: (from .env)
```

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_processors/test_pcap_processor.py
```

### Code Quality
```bash
# Format code
black src/ scripts/

# Lint code
ruff check src/ scripts/

# Type checking
mypy src/
```

### Prompt Engineering
```bash
# Test prompts in Jupyter
jupyter notebook notebooks/prompt_engineering.ipynb

# Save prompts for review
python scripts/process_hadiths.py --stage pcap --save-prompts --limit 10
```

## Troubleshooting

### Database Connection Issues
```bash
# Check containers
docker-compose ps

# View logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### LLM API Issues
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Test connection
python -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-3-5-sonnet-20241022', max_tokens=10, messages=[{'role':'user','content':'test'}]))"

# View rate limiting status
python scripts/check_rate_limits.py
```

### Out of Memory
```bash
# Reduce batch size in .env
PCAP_BATCH_SIZE=50
HMSTS_BATCH_SIZE=25

# Reduce parallel workers
PARALLEL_WORKERS=3
```

## Data Export

```bash
# Export processed hadiths to JSON
python scripts/export_data.py --format json --version v1.0

# Export to CSV for analysis
python scripts/export_data.py --format csv --version v1.0

# Export validation reports
python scripts/export_data.py --type validation --version v1.0
```

## Phase 3 Preparation

After Phase 2 completion, the processed data will be ready for:
- REST/GraphQL API development
- Semantic search implementation
- Moral commandments extraction
- AI reasoning interfaces

See Phase 3 documentation for next steps.

## Support

For issues or questions:
1. Check this README
2. Review CLAUDE.MD in parent directory
3. Check methodology docs in ../methodology/
4. Open issue on GitHub

## License

See parent repository for license information.

---

**Phase 2 Status:** In Development
**Version:** 1.0.0
**Last Updated:** 2026-01-19
