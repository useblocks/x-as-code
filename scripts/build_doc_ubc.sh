#!/bin/bash
# build_doc_ubc.sh - Build the documentation with ubCode (ubc), the counterpart of build_doc.sh

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

if ! command -v ubc &>/dev/null; then
    print_error "ubc (ubCode CLI) is not installed. See https://ubcode.useblocks.com"
    exit 1
fi

echo ""
echo "============================================"
echo "Building Documentation with ubCode"
echo "Project Root: ${PROJECT_ROOT}"
echo "============================================"
echo ""

cd "${PROJECT_ROOT}"

# Separate output directory, so the Sphinx build in docs/_build/html is not overwritten
print_info "Generating documentation..."
ubc build html docs -o docs/_build/ubc --fresh

echo ""
print_success "Documentation built successfully!"
echo "  Output: ${PROJECT_ROOT}/docs/_build/ubc/index.html"
