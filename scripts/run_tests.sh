#!/bin/bash
# Financial Agent - Test Runner Script

set -e  # Exit on error

echo "🧪 Financial Agent - Running Tests"
echo "=================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "Run: source venv/bin/activate"
    exit 1
fi

# Run unit tests
echo ""
echo "1️⃣  Running Unit Tests..."
pytest src/ -v -m unit --cov=src/financial_agent --cov-report=term-missing

# Run integration tests (if requested)
if [[ "$1" == "--integration" ]]; then
    echo ""
    echo "2️⃣  Running Integration Tests..."
    pytest tests/integration/ -v -m integration
fi

# Run type checking
if command -v mypy &> /dev/null; then
    echo ""
    echo "3️⃣  Running Type Checks..."
    mypy src/financial_agent
fi

# Run linting
if command -v flake8 &> /dev/null; then
    echo ""
    echo "4️⃣  Running Linting..."
    flake8 src/financial_agent --max-line-length=100
fi

echo ""
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "📊 Coverage report: htmlcov/index.html"
