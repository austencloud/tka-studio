<script lang="ts">
  import { animationActions } from '../stores/animation.js';
  import type { SequenceData } from '../types.js';

  interface SequenceRecord {
    word: string;
    author: string;
    level: number;
    length: number;
    grid_mode: string;
    sequence: SequenceData[];
    thumbnail?: string;
    description?: string;
  }

  let selectedSequence: SequenceRecord | null = $state(null);
  let searchTerm = $state('');
  let sortBy = $state<'word' | 'author' | 'level' | 'length'>('word');
  let filterLevel = $state<number | 'all'>('all');
  let message = $state('');
  let messageType = $state<'success' | 'error' | ''>('');

  // Comprehensive sequence dictionary
  const SEQUENCE_DICTIONARY: SequenceRecord[] = [
    {
      word: 'ALFBBLFA',
      author: 'Austen Cloud',
      level: 3,
      length: 8,
      grid_mode: 'diamond',
      description: 'Classic 8-beat sequence with alternating pro/anti motions',
      sequence: [
        {
          word: 'ALFBBLFA',
          author: 'Austen Cloud',
          level: 3,
          prop_type: 'staff',
          grid_mode: 'diamond',
          is_circular: false
        },
        {
          beat: 0,
          letter: 'α',
          blue_attributes: { start_loc: 's', end_loc: 's', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 },
          red_attributes: { start_loc: 'n', end_loc: 'n', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 }
        },
        {
          beat: 1,
          letter: 'A',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 's', end_loc: 'w', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' }
        },
        {
          beat: 2,
          letter: 'L',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'w', end_loc: 'n', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'e', end_loc: 'n', turns: 0, end_ori: 'in' }
        },
        {
          beat: 3,
          letter: 'F',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'n', end_loc: 'w', turns: 0, end_ori: 'in' }
        },
        {
          beat: 4,
          letter: 'B',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'e', end_loc: 's', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'w', end_loc: 's', turns: 0, end_ori: 'in' }
        },
        {
          beat: 5,
          letter: 'B',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 's', end_loc: 'w', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 's', end_loc: 'e', turns: 0, end_ori: 'in' }
        },
        {
          beat: 6,
          letter: 'L',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'w', end_loc: 'n', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'e', end_loc: 'n', turns: 0, end_ori: 'in' }
        },
        {
          beat: 7,
          letter: 'F',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'n', end_loc: 'w', turns: 0, end_ori: 'in' }
        },
        {
          beat: 8,
          letter: 'A',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'e', end_loc: 's', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', prop_rot_dir: 'cw', start_loc: 'w', end_loc: 'n', turns: 0, end_ori: 'in' }
        }
      ]
    },
    {
      word: 'ABC',
      author: 'TKA',
      level: 1,
      length: 3,
      grid_mode: 'diamond',
      description: 'Simple 3-beat sequence for beginners',
      sequence: [
        {
          word: 'ABC',
          author: 'TKA',
          level: 1,
          prop_type: 'staff',
          grid_mode: 'diamond',
          is_circular: false
        },
        {
          beat: 0,
          letter: 'α',
          blue_attributes: { start_loc: 's', end_loc: 's', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 },
          red_attributes: { start_loc: 'n', end_loc: 'n', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 }
        },
        {
          beat: 1,
          letter: 'A',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'w', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' }
        },
        {
          beat: 2,
          letter: 'B',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'w', end_loc: 's', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'e', end_loc: 's', turns: 0, end_ori: 'in' }
        },
        {
          beat: 3,
          letter: 'C',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 's', end_loc: 'e', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'w', turns: 0, end_ori: 'in' }
        }
      ]
    },
    {
      word: 'ABCD',
      author: 'TKA',
      level: 2,
      length: 4,
      grid_mode: 'diamond',
      description: '4-beat sequence with mixed motions',
      sequence: [
        {
          word: 'ABCD',
          author: 'TKA',
          level: 2,
          prop_type: 'staff',
          grid_mode: 'diamond',
          is_circular: false
        },
        {
          beat: 0,
          letter: 'α',
          blue_attributes: { start_loc: 's', end_loc: 's', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 },
          red_attributes: { start_loc: 'n', end_loc: 'n', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 }
        },
        {
          beat: 1,
          letter: 'A',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'w', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' }
        },
        {
          beat: 2,
          letter: 'B',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'w', end_loc: 'n', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'e', end_loc: 'n', turns: 0, end_ori: 'in' }
        },
        {
          beat: 3,
          letter: 'C',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'n', end_loc: 'e', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 'w', turns: 0, end_ori: 'in' }
        },
        {
          beat: 4,
          letter: 'D',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'e', end_loc: 's', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'w', end_loc: 's', turns: 0, end_ori: 'in' }
        }
      ]
    },
    {
      word: 'TURNS_TEST',
      author: 'TKA',
      level: 4,
      length: 2,
      grid_mode: 'diamond',
      description: 'Test sequence with multiple turns',
      sequence: [
        {
          word: 'TURNS_TEST',
          author: 'TKA',
          level: 4,
          prop_type: 'staff',
          grid_mode: 'diamond',
          is_circular: false
        },
        {
          beat: 0,
          letter: 'α',
          blue_attributes: { start_loc: 's', end_loc: 's', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 },
          red_attributes: { start_loc: 'n', end_loc: 'n', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 }
        },
        {
          beat: 1,
          letter: 'T',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'e', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 'w', turns: 1, end_ori: 'in' }
        },
        {
          beat: 2,
          letter: 'T',
          blue_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'e', end_loc: 'n', turns: 1, end_ori: 'in' },
          red_attributes: { motion_type: 'anti', start_ori: 'in', start_loc: 'w', end_loc: 's', turns: 2, end_ori: 'in' }
        }
      ]
    },
    {
      word: 'SIMPLE',
      author: 'Beginner',
      level: 1,
      length: 2,
      grid_mode: 'diamond',
      description: 'Very simple 2-beat sequence',
      sequence: [
        {
          word: 'SIMPLE',
          author: 'Beginner',
          level: 1,
          prop_type: 'staff',
          grid_mode: 'diamond',
          is_circular: false
        },
        {
          beat: 0,
          letter: 'α',
          blue_attributes: { start_loc: 's', end_loc: 's', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 },
          red_attributes: { start_loc: 'n', end_loc: 'n', start_ori: 'in', end_ori: 'in', motion_type: 'static', turns: 0 }
        },
        {
          beat: 1,
          letter: 'S',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'n', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 's', turns: 0, end_ori: 'in' }
        },
        {
          beat: 2,
          letter: 'S',
          blue_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 'n', end_loc: 's', turns: 0, end_ori: 'in' },
          red_attributes: { motion_type: 'pro', start_ori: 'in', start_loc: 's', end_loc: 'n', turns: 0, end_ori: 'in' }
        }
      ]
    }
  ];

  // Computed filtered and sorted sequences
  const filteredSequences = $derived.by(() => {
    let filtered = SEQUENCE_DICTIONARY;

    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(seq =>
        seq.word.toLowerCase().includes(term) ||
        seq.author.toLowerCase().includes(term) ||
        seq.description?.toLowerCase().includes(term)
      );
    }

    // Filter by level
    if (filterLevel !== 'all') {
      filtered = filtered.filter(seq => seq.level === filterLevel);
    }

    // Sort sequences
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'word':
          return a.word.localeCompare(b.word);
        case 'author':
          return a.author.localeCompare(b.author);
        case 'level':
          return a.level - b.level;
        case 'length':
          return a.length - b.length;
        default:
          return 0;
      }
    });

    return filtered;
  });

  function selectSequence(sequence: SequenceRecord) {
    selectedSequence = sequence;
  }

  function loadSelectedSequence() {
    if (!selectedSequence) {
      showMessage('error', 'Please select a sequence first.');
      return;
    }

    animationActions.loadSequence(selectedSequence.sequence);
    showMessage('success', `Sequence "${selectedSequence.word}" loaded successfully.`);
  }

  function showMessage(type: 'success' | 'error', text: string) {
    message = text;
    messageType = type;

    setTimeout(() => {
      message = '';
      messageType = '';
    }, 3000);
  }

  function getLevelColor(level: number): string {
    switch (level) {
      case 1: return '#10b981'; // green
      case 2: return '#3b82f6'; // blue
      case 3: return '#f59e0b'; // amber
      case 4: return '#ef4444'; // red
      default: return '#6b7280'; // gray
    }
  }
</script>

<div class="sequence-dictionary">
  <div class="dictionary-header">
    <h3>Sequence Dictionary</h3>
    <div class="controls">
      <input
        type="text"
        placeholder="Search sequences..."
        bind:value={searchTerm}
        class="search-input"
      />

      <select bind:value={sortBy} class="sort-select">
        <option value="word">Sort by Word</option>
        <option value="author">Sort by Author</option>
        <option value="level">Sort by Level</option>
        <option value="length">Sort by Length</option>
      </select>

      <select bind:value={filterLevel} class="filter-select">
        <option value="all">All Levels</option>
        <option value={1}>Level 1</option>
        <option value={2}>Level 2</option>
        <option value={3}>Level 3</option>
        <option value={4}>Level 4</option>
      </select>
    </div>
  </div>

  <div class="dictionary-content">
    <div class="sequence-grid">
      {#each filteredSequences as sequence (sequence.word)}
        <div
          class="sequence-card"
          class:selected={selectedSequence?.word === sequence.word}
          onclick={() => selectSequence(sequence)}
          onkeydown={(e) => e.key === 'Enter' && selectSequence(sequence)}
          role="button"
          tabindex="0"
        >
          <div class="card-header">
            <h4 class="sequence-word">{sequence.word}</h4>
            <div
              class="level-badge"
              style="background-color: {getLevelColor(sequence.level)}"
            >
              L{sequence.level}
            </div>
          </div>

          <div class="card-body">
            <p class="author">by {sequence.author}</p>
            <p class="description">{sequence.description}</p>
            <div class="metadata">
              <span class="length">{sequence.length} beats</span>
              <span class="grid-mode">{sequence.grid_mode}</span>
            </div>
          </div>
        </div>
      {/each}
    </div>

    {#if filteredSequences.length === 0}
      <div class="no-results">
        <p>No sequences found matching your criteria.</p>
      </div>
    {/if}
  </div>

  <div class="dictionary-footer">
    {#if selectedSequence}
      <div class="selected-info">
        <strong>Selected:</strong> {selectedSequence.word} by {selectedSequence.author}
      </div>
    {/if}

    <button
      class="load-btn"
      onclick={loadSelectedSequence}
      disabled={!selectedSequence}
    >
      Load Selected Sequence
    </button>
  </div>

  {#if message}
    <div class="message" class:error={messageType === 'error'} class:success={messageType === 'success'}>
      {message}
    </div>
  {/if}
</div>

<style>
  .sequence-dictionary {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 100%;
  }

  .dictionary-header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .dictionary-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #374151;
  }

  .controls {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .search-input,
  .sort-select,
  .filter-select {
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    background: white;
  }

  .search-input {
    flex: 1;
    min-width: 200px;
  }

  .search-input:focus,
  .sort-select:focus,
  .filter-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
  }

  .dictionary-content {
    flex: 1;
    overflow-y: auto;
    min-height: 300px;
  }

  .sequence-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    padding: 0.5rem 0;
  }

  .sequence-card {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem;
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .sequence-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .sequence-card.selected {
    border-color: #3b82f6;
    background: #eff6ff;
    box-shadow: 0 0 0 1px #3b82f6;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .sequence-word {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #1f2937;
  }

  .level-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .card-body {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .author {
    margin: 0;
    font-size: 0.875rem;
    color: #6b7280;
    font-style: italic;
  }

  .description {
    margin: 0;
    font-size: 0.875rem;
    color: #4b5563;
    line-height: 1.4;
  }

  .metadata {
    display: flex;
    gap: 1rem;
    font-size: 0.75rem;
    color: #9ca3af;
  }

  .no-results {
    text-align: center;
    padding: 2rem;
    color: #6b7280;
  }

  .dictionary-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .selected-info {
    font-size: 0.875rem;
    color: #4b5563;
  }

  .load-btn {
    padding: 0.75rem 1.5rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  .load-btn:hover:not(:disabled) {
    background: #2563eb;
  }

  .load-btn:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }

  .message {
    padding: 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    text-align: center;
  }

  .message.error {
    color: #b91c1c;
    background: #fee2e2;
    border: 1px solid #fecaca;
  }

  .message.success {
    color: #047857;
    background: #d1fae5;
    border: 1px solid #a7f3d0;
  }

  @media (max-width: 768px) {
    .sequence-grid {
      grid-template-columns: 1fr;
    }

    .controls {
      flex-direction: column;
    }

    .dictionary-footer {
      flex-direction: column;
      align-items: stretch;
    }
  }
</style>
