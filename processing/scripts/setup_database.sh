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
echo -e "${YELLOW}Step 2: Installing Python dependencies...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 3: Start PostgreSQL
echo -e "${YELLOW}Step 3: Starting PostgreSQL container...${NC}"
docker-compose up -d postgres
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is ready
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U ikb_user > /dev/null 2>&1; then
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
echo -e "${GREEN}✓ Database schema created${NC}"
echo ""

# Step 5: Verify schema
echo -e "${YELLOW}Step 5: Verifying database schema...${NC}"
TABLE_COUNT=$(docker-compose exec -T postgres psql -U ikb_user -d islamic_kb -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
echo "Tables created: $TABLE_COUNT"

if [ "$TABLE_COUNT" -eq "7" ]; then
    echo -e "${GREEN}✓ All 7 tables created successfully${NC}"
    echo ""
    echo "Tables:"
    docker-compose exec -T postgres psql -U ikb_user -d islamic_kb -c "\dt"
else
    echo -e "${RED}Error: Expected 7 tables, found $TABLE_COUNT${NC}"
    exit 1
fi
echo ""

# Success message
echo "=============================================="
echo -e "${GREEN}Database setup complete!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Review the schema: psql -h localhost -U ikb_user -d islamic_kb"
echo "2. Proceed with Pydantic models implementation"
echo "3. Implement data ingestion scripts"
echo ""
echo "Database connection:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: islamic_kb"
echo "  User: ikb_user"
echo "  Password: changeme123"
echo ""
