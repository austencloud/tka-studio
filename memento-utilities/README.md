# Memento MCP Utilities

This directory contains utilities and documentation for managing the Memento MCP knowledge graph memory system.

## Files

- **`memento-relation-deduplicator.js`** - JavaScript utility to prevent duplicate relations
- **`memento-best-practices.md`** - Comprehensive guide for Claude agents to use Memento MCP properly
- **`README.md`** - This file

## Purpose

These utilities exist to solve the duplicate relation problem that occurs when multiple Claude Desktop sessions create identical relationships in the Neo4j knowledge graph, causing visual clutter in query mode.

## Usage

These files serve as reference documentation and utility code for:
- Claude agents working with Memento MCP
- System administrators managing Neo4j instances  
- Developers building on top of the Memento MCP system

## Location Rationale

Located at `C:\TKA\memento-utilities\` because:
- ✅ Separate from specific project code (not in `/web`)
- ✅ Part of the TKA ecosystem but not TKA-specific
- ✅ Accessible to all projects that use Memento MCP
- ✅ Clear organizational structure for memory system tools