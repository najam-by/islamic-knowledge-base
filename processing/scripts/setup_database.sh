#!/bin/bash
# Database Setup Script for Islamic Knowledge Base
# Phase 2.1: PostgreSQL Schema Creation

set -e  # Exit on error

echo "=============================================="
echo "Islamic Knowledge Base - Database Setup"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "alembic.ini" ]; then
    echo -e "${RED}Error: alembic.ini not found. Please run from processing/ directory${NC}"
    exit 1
fi

# Step 1: Check Docker
echo -e "${YELLOW}Step 1: Checking Docker...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Step 2: Install Python dependencies
echo -e "${YELLOW}Step 2: Setting up Python environment...${NC}"

# Detect Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Detected Python version: $PYTHON_VERSION"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies (this may take a few minutes)..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}Error: Failed to install dependencies${NC}"
    echo "Try manually: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi
echo ""

# Step 3: Start PostgreSQL
echo -e "${YELLOW}Step 3: Starting PostgreSQL container...${NC}"
docker-compose up -d postgres
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is ready (using docker exec instead of psql)
for i in {1..30}; do
    if docker exec islamic_kb_postgres pg_isready -U ikb_user > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: PostgreSQL failed to start${NC}"
        exit 1
    fi
    sleep 1
done
echo ""

# Step 4: Run Alembic migrations
echo -e "${YELLOW}Step 4: Running database migrations...${NC}"
alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database schema created${NC}"
else
    echo -e "${RED}Error: Migration failed${NC}"
    exit 1
fi
echo ""

# Step 5: Verify schema
echo -e "${YELLOW}Step 5: Verifying database schema...${NC}"
TABLE_COUNT=$(docker exec islamic_kb_postgres psql -U ikb_user -d islamic_kb -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name != 'alembic_version'")
echo "Application tables created: $TABLE_COUNT (excluding alembic_version)"

if [ "$TABLE_COUNT" -eq "7" ]; then
    echo -e "${GREEN}✓ All 7 tables created successfully${NC}"
    echo ""
    echo "Tables:"
    docker exec islamic_kb_postgres psql -U ikb_user -d islamic_kb -c "\dt"
    echo ""
    echo "Verifying table structure:"
    docker exec islamic_kb_postgres psql -U ikb_user -d islamic_kb -c "SELECT table_name, (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count FROM information_schema.tables t WHERE table_schema='public' AND table_name != 'alembic_version' ORDER BY table_name;"
else
    echo -e "${RED}Error: Expected 7 tables, found $TABLE_COUNT${NC}"
    exit 1
fi
echo ""

# Success message
echo "=============================================="
echo -e "${GREEN}✅ Database setup complete!${NC}"
echo "=============================================="
echo ""
echo "Virtual environment: $(pwd)/venv"
echo "To activate: source venv/bin/activate"
echo ""
echo "Database connection:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: islamic_kb"
echo "  User: ikb_user"
echo "  Password: changeme123"
echo ""
echo "To connect via Docker:"
echo "  docker exec -it islamic_kb_postgres psql -U ikb_user -d islamic_kb"
echo ""
echo "To view tables:"
echo "  docker exec islamic_kb_postgres psql -U ikb_user -d islamic_kb -c '\\dt'"
echo ""
echo "Next steps:"
echo "1. Implement Pydantic models (src/models/)"
echo "2. Implement data ingestion (src/ingestion/)"
echo "3. Load 50,884 hadiths into database"
echo ""
