# TKA Schema Migration Strategy

## 🎯 Overview
This document outlines the strategy for migrating from desktop-first domain models to consistent cross-platform schemas.

## 🏗️ Architecture Flow
```
Python Domain Models → JSON Schemas → TypeScript Types
     (Source)            (Contract)     (Implementation)
```

## 📋 Schema Files Created

### Core Schemas
- `core-enums.json` - All enum types from Python models
- `motion-data-v2.json` - MotionData based on Python dataclass
- `glyph-data.json` - GlyphData for pictograph rendering
- `beat-data-v2.json` - BeatData with proper validation
- `sequence-data-v2.json` - SequenceData with metadata

### Generated Types
- `generated-types.ts` - TypeScript interfaces for web implementation

## 🔄 Sync Strategy

### 1. Desktop as Source of Truth
When Python domain models change:
1. Update the Python models in `src/desktop/modern/src/domain/models/`
2. Regenerate schemas from Python models
3. Update web TypeScript types from schemas
4. Test compatibility across platforms

### 2. Schema Validation Pipeline
```bash
# 1. Validate Python models produce valid JSON
python validate_domain_models.py

# 2. Validate schemas are well-formed
npx ajv-cli validate --schema schemas/*.json

# 3. Generate TypeScript types
npx json-schema-to-typescript schemas/generated-types.ts

# 4. Validate web implementation matches schemas
npm run test:schema-compliance
```

### 3. Version Management
- Use semantic versioning for schemas (v2.0.0)
- Python models include version metadata
- Web validates against schema version
- Graceful degradation for version mismatches

## 🚀 Implementation Steps

### Phase 1: Validate Desktop Models
- [ ] Ensure all Python models have proper `to_dict()` methods
- [ ] Add schema validation to Python serialization
- [ ] Create test data that validates against schemas

### Phase 2: Update Web Implementation
- [ ] Replace existing web types with schema-generated types
- [ ] Implement factory functions matching Python behavior
- [ ] Add runtime schema validation in web app
- [ ] Migrate existing web data to new format

### Phase 3: Cross-Platform Testing
- [ ] Create shared test data in schema format
- [ ] Validate Python → JSON → TypeScript roundtrip
- [ ] Performance testing for large sequences
- [ ] Error handling for schema violations

## 🛠️ Tools and Automation

### Schema Generation (Future)
```python
# Generate schemas from Python models
def generate_schema_from_dataclass(cls) -> dict:
    """Generate JSON schema from Python dataclass"""
    # Implementation to automatically generate schemas
```

### TypeScript Generation
```bash
# Automated type generation
npx json-schema-to-typescript \
  --input schemas/ \
  --output src/web/landing/src/lib/types/generated/
```

### Validation
```typescript
// Runtime schema validation in web app
import Ajv from 'ajv';
import beatSchema from 'schemas/beat-data-v2.json';

const ajv = new Ajv();
const validateBeat = ajv.compile(beatSchema);

export function validateBeatData(data: unknown): data is BeatData {
  return validateBeat(data);
}
```

## 🎯 Benefits

### Consistency
- Same data structures across platforms
- Guaranteed compatibility
- Single source of truth for business logic

### Type Safety
- Compile-time validation in TypeScript
- Runtime validation in both platforms
- Clear error messages for data issues

### Maintainability
- Changes in one place (Python models)
- Automated propagation to web
- Version-controlled schema evolution

## 📚 Next Steps

1. **Implement schema validation in Python domain models**
2. **Update web services to use new schemas**
3. **Create automated schema generation pipeline**
4. **Add comprehensive cross-platform tests**
5. **Document migration guide for existing data**

This approach ensures your sophisticated Python domain architecture becomes the foundation for a robust, type-safe, cross-platform system.
