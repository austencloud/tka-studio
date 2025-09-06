/**
 * Memento MCP Relation Deduplicator
 * Prevents duplicate relations by checking before creating
 */

class RelationDeduplicator {
  constructor(mementoApi) {
    this.api = mementoApi;
    this.knownRelations = new Set();
  }

  // Create unique key for relation comparison
  createRelationKey(from, to, relationType) {
    return `${from}|${relationType}|${to}`;
  }

  // Load existing relations into memory
  async loadExistingRelations() {
    const graph = await this.api.readGraph();
    this.knownRelations.clear();

    graph.relations.forEach((rel) => {
      const key = this.createRelationKey(rel.from, rel.to, rel.relationType);
      this.knownRelations.add(key);
    });

    console.log(`Loaded ${this.knownRelations.size} existing relations`);
  }

  // Check if relation already exists
  relationExists(from, to, relationType) {
    const key = this.createRelationKey(from, to, relationType);
    return this.knownRelations.has(key);
  }

  // Safe relation creation with duplicate prevention
  async createRelationSafely(relationData) {
    await this.loadExistingRelations();

    const { from, to, relationType } = relationData;

    if (this.relationExists(from, to, relationType)) {
      console.log(`Relation already exists: ${from} → ${to} (${relationType})`);
      return { action: "skipped", reason: "duplicate_prevented" };
    }

    // Create the relation since it doesn't exist
    await this.api.createRelations([relationData]);

    // Update our known relations cache
    const key = this.createRelationKey(from, to, relationType);
    this.knownRelations.add(key);

    console.log(`Created new relation: ${from} → ${to} (${relationType})`);
    return { action: "created", relation: relationData };
  }

  // Batch create relations with deduplication
  async createRelationsBatch(relations) {
    await this.loadExistingRelations();

    const results = [];
    const newRelations = [];

    for (const rel of relations) {
      if (this.relationExists(rel.from, rel.to, rel.relationType)) {
        results.push({ ...rel, action: "skipped", reason: "duplicate" });
      } else {
        newRelations.push(rel);
        results.push({ ...rel, action: "will_create" });
      }
    }

    if (newRelations.length > 0) {
      await this.api.createRelations(newRelations);
      console.log(
        `Created ${newRelations.length} new relations, skipped ${relations.length - newRelations.length} duplicates`
      );
    }

    return results;
  }
}

module.exports = { RelationDeduplicator };
