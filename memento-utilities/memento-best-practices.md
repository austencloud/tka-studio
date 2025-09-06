# Memento MCP Best Practices Guide
## Preventing Duplicate Relations

### ✅ ALWAYS DO THIS:

1. **Check Before Create Pattern:**
   ```javascript
   // Step 1: Read current graph state
   const graph = await mcp_memory_read_graph();
   
   // Step 2: Check if relation exists
   const existingRelation = graph.relations.find(r => 
     r.from === "Entity A" && 
     r.to === "Entity B" && 
     r.relationType === "relates_to"
   );
   
   // Step 3: Only create if missing
   if (!existingRelation) {
     await mcp_memory_create_relations([{
       from: "Entity A",
       to: "Entity B", 
       relationType: "relates_to"
     }]);
   }
   ```

2. **Use Update for Existing Relations:**
   ```javascript
   // For existing relations, use update instead of create
   await mcp_memory_update_relation({
     from: "Existing Entity",
     to: "Another Entity",
     relationType: "existing_relation",
     strength: 0.9,
     metadata: { updated: Date.now() }
   });
   ```

### 🚫 NEVER DO THIS:

```javascript
// ❌ DON'T: Create without checking
await mcp_memory_create_relations([{
  from: "Entity A",
  to: "Entity B",
  relationType: "relates_to"
}]);
```

### 🎯 CLAUDE DESKTOP SPECIFIC WORKFLOW:

1. **Before ANY relation creation:**
   - Call `mcp_memory_read_graph()` first
   - Search for existing relations
   - Document your reasoning

2. **When adding architecture connections:**
   - Check if entities already have relationships
   - Use specific, descriptive relation types
   - Add metadata for source tracking

3. **Neo4j Query Mode Optimization:**
   ```cypher
   // Get current entities only (no historical versions)
   MATCH (n) 
   WHERE NOT EXISTS {
     MATCH (newer) 
     WHERE newer.name = n.name 
     AND newer.validFrom > n.validFrom
   }
   RETURN n;
   
   // Get clean relationship view
   MATCH (a)-[r]->(b)
   RETURN DISTINCT a.name, type(r), b.name;
   ```

### 📋 CHECKLIST FOR CLAUDE AGENTS:

- [ ] Read graph state first
- [ ] Check for existing relations  
- [ ] Use updates for existing entity pairs
- [ ] Add descriptive metadata
- [ ] Document relation creation reasoning
- [ ] Verify no duplicates after creation

### 🔧 SYSTEM IMPROVEMENTS NEEDED:

1. **Memento MCP Enhancement Request:**
   - Use MERGE instead of CREATE internally
   - Add duplicate detection at API level
   - Implement automatic constraint creation

2. **Neo4j Configuration:**
   - Add relationship uniqueness constraints
   - Set up proper indexing for performance
   - Enable query optimization
