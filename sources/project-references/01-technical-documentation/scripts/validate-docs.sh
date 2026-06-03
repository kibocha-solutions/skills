#!/usr/bin/env bash
#
# Unified Documentation Validation Script
# Validates all documentation types according to their canons
#
# Usage:
#   ./scripts/validate-docs.sh              # Validate all
#   ./scripts/validate-docs.sh --rest       # Validate only reST files
#   ./scripts/validate-docs.sh --openapi    # Validate only OpenAPI specs
#   ./scripts/validate-docs.sh --pre-commit # Quick validation for pre-commit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

# Functions
print_header() {
    echo -e "\n${GREEN}=== $1 ===${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    ((WARNINGS++))
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Validate reStructuredText files
validate_rest() {
    print_header "Validating reStructuredText Files"
    
    if ! command_exists rstcheck; then
        print_warning "rstcheck not installed. Install: pip install rstcheck"
        return
    fi
    
    if [ -d "docs/source" ]; then
        find docs/source -name "*.rst" -type f | while read -r file; do
            if rstcheck "$file" 2>&1 | grep -q "ERROR"; then
                print_error "reST validation failed: $file"
            else
                print_success "reST valid: $file"
            fi
        done
    else
        print_warning "No docs/source directory found"
    fi
}

# Validate OpenAPI specifications
validate_openapi() {
    print_header "Validating OpenAPI Specifications"
    
    if ! command_exists swagger-cli; then
        print_warning "swagger-cli not installed. Install: npm install -g @apidevtools/swagger-cli"
        return
    fi
    
    if [ -d "api-specs" ]; then
        find api-specs -name "*.yaml" -o -name "*.yml" | while read -r file; do
            if swagger-cli validate "$file" 2>&1 | grep -q "is valid"; then
                print_success "OpenAPI valid: $file"
            else
                print_error "OpenAPI validation failed: $file"
            fi
        done
    else
        print_warning "No api-specs directory found"
    fi
}

# Validate GraphQL schemas
validate_graphql() {
    print_header "Validating GraphQL Schemas"
    
    if ! command_exists graphql; then
        print_warning "graphql not installed. Install: npm install -g graphql"
        return
    fi
    
    if [ -d "graphql" ]; then
        find graphql -name "*.graphql" -o -name "*.gql" | while read -r file; do
            if node -e "const fs = require('fs'); const { buildSchema } = require('graphql'); try { buildSchema(fs.readFileSync('$file', 'utf8')); console.log('valid'); } catch(e) { console.error(e.message); process.exit(1); }" 2>&1 | grep -q "valid"; then
                print_success "GraphQL valid: $file"
            else
                print_error "GraphQL validation failed: $file"
            fi
        done
    else
        print_warning "No graphql directory found"
    fi
}

# Validate Protocol Buffers
validate_proto() {
    print_header "Validating Protocol Buffers"
    
    if ! command_exists protoc; then
        print_warning "protoc not installed. Install: https://grpc.io/docs/protoc-installation/"
        return
    fi
    
    if [ -d "proto" ]; then
        find proto -name "*.proto" | while read -r file; do
            if protoc --proto_path=proto --descriptor_set_out=/dev/null "$file" 2>&1; then
                print_success "Proto valid: $file"
            else
                print_error "Proto validation failed: $file"
            fi
        done
    else
        print_warning "No proto directory found"
    fi
}

# Validate Markdown files
validate_markdown() {
    print_header "Validating Markdown Files"
    
    if ! command_exists markdownlint; then
        print_warning "markdownlint not installed. Install: npm install -g markdownlint-cli"
        return
    fi
    
    # Validate CHANGELOG
    if [ -f "CHANGELOG.md" ]; then
        if markdownlint CHANGELOG.md 2>&1; then
            print_success "Markdown valid: CHANGELOG.md"
        else
            print_error "Markdown validation failed: CHANGELOG.md"
        fi
    fi
    
    # Validate ADRs
    if [ -d "docs/decisions" ]; then
        find docs/decisions -name "*.md" | while read -r file; do
            if markdownlint "$file" 2>&1; then
                print_success "Markdown valid: $file"
            else
                print_error "Markdown validation failed: $file"
            fi
        done
    fi
}

# Validate Sphinx build
validate_sphinx() {
    print_header "Validating Sphinx Build"
    
    if ! command_exists sphinx-build; then
        print_warning "sphinx-build not installed. Install: pip install sphinx"
        return
    fi
    
    if [ -d "docs/source" ] && [ -f "docs/source/conf.py" ]; then
        if sphinx-build -W -b html docs/source docs/build 2>&1 | grep -q "build succeeded"; then
            print_success "Sphinx build succeeded"
        else
            print_error "Sphinx build failed"
        fi
    else
        print_warning "No Sphinx configuration found"
    fi
}

# Check access level warnings
check_access_levels() {
    print_header "Checking Access Level Warnings"
    
    # Check reST files for access level warnings
    if [ -d "docs/source" ]; then
        find docs/source -name "*.rst" -type f | while read -r file; do
            if ! grep -q "DOCUMENTATION - Level" "$file"; then
                print_warning "Missing access level warning: $file"
            fi
        done
    fi
}

# Validate no emojis or emdashes
check_formatting_rules() {
    print_header "Checking Formatting Rules (No Emojis, No Emdashes)"
    
    # Check for emojis (basic check for common emoji patterns)
    if [ -d "docs" ]; then
        if grep -r "😀\|😁\|😂\|🎉\|✅\|❌\|⚠️" docs/ 2>/dev/null; then
            print_error "Emojis found in documentation (violates core canon)"
        else
            print_success "No emojis found"
        fi
        
        # Check for emdashes (—)
        if grep -r "—" docs/ 2>/dev/null; then
            print_error "Emdashes (—) found in documentation (violates core canon)"
        else
            print_success "No emdashes found"
        fi
    fi
}

# Main execution
main() {
    echo "Documentation Validation Script"
    echo "================================"
    
    case "${1:-all}" in
        --rest)
            validate_rest
            ;;
        --openapi)
            validate_openapi
            ;;
        --graphql)
            validate_graphql
            ;;
        --proto)
            validate_proto
            ;;
        --markdown)
            validate_markdown
            ;;
        --sphinx)
            validate_sphinx
            ;;
        --pre-commit)
            # Quick validation for pre-commit (only changed files)
            validate_markdown
            check_formatting_rules
            ;;
        --all|*)
            validate_rest
            validate_openapi
            validate_graphql
            validate_proto
            validate_markdown
            validate_sphinx
            check_access_levels
            check_formatting_rules
            ;;
    esac
    
    # Summary
    echo -e "\n${GREEN}=== Validation Summary ===${NC}"
    echo "Errors: $ERRORS"
    echo "Warnings: $WARNINGS"
    
    if [ $ERRORS -gt 0 ]; then
        echo -e "${RED}Validation FAILED${NC}"
        exit 1
    elif [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}Validation PASSED with warnings${NC}"
        exit 0
    else
        echo -e "${GREEN}Validation PASSED${NC}"
        exit 0
    fi
}

main "$@"
