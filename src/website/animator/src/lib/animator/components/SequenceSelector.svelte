<script lang="ts">
  import { animationActions } from '../stores/animation.js';
  import type { SequenceData } from '../types.js';

  let selectedSequence = $state('');
  let message = $state('');
  let messageType = $state<'success' | 'error' | ''>('');

  // Predefined sequences for selection
  const PREDEFINED_SEQUENCES: Record<string, SequenceData[]> = {
    'ALFBBLFA': [
      {
        word: 'ALFBBLFA',
        author: 'Austen Cloud',
        level: 0,
        prop_type: 'staff',
        grid_mode: 'diamond',
        is_circular: false
      },
      {
        beat: 0,
        letter: 'α',
        blue_attributes: {
          start_loc: 's',
          end_loc: 's',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        },
        red_attributes: {
          start_loc: 'n',
          end_loc: 'n',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        }
      },
      {
        beat: 1,
        letter: 'A',
        blue_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 's',
          end_loc: 'w',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 'n',
          end_loc: 'e',
          turns: 0,
          end_ori: 'in'
        }
      },
      {
        beat: 2,
        letter: 'L',
        blue_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 'w',
          end_loc: 'n',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 'e',
          end_loc: 'n',
          turns: 0,
          end_ori: 'in'
        }
      },
      {
        beat: 3,
        letter: 'F',
        blue_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 'n',
          end_loc: 'e',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          prop_rot_dir: 'cw',
          start_loc: 'n',
          end_loc: 'w',
          turns: 0,
          end_ori: 'in'
        }
      }
    ],
    'ABC': [
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
        blue_attributes: {
          start_loc: 's',
          end_loc: 's',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        },
        red_attributes: {
          start_loc: 'n',
          end_loc: 'n',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        }
      },
      {
        beat: 1,
        letter: 'A',
        blue_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 's',
          end_loc: 'w',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 'n',
          end_loc: 'e',
          turns: 0,
          end_ori: 'in'
        }
      },
      {
        beat: 2,
        letter: 'B',
        blue_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 'w',
          end_loc: 's',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          start_loc: 'e',
          end_loc: 's',
          turns: 0,
          end_ori: 'in'
        }
      },
      {
        beat: 3,
        letter: 'C',
        blue_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          start_loc: 's',
          end_loc: 'e',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 's',
          end_loc: 'w',
          turns: 0,
          end_ori: 'in'
        }
      }
    ],
    'TURNS_TEST': [
      {
        word: 'TURNS_TEST',
        author: 'TKA',
        level: 2,
        prop_type: 'staff',
        grid_mode: 'diamond',
        is_circular: false
      },
      {
        beat: 0,
        letter: 'α',
        blue_attributes: {
          start_loc: 's',
          end_loc: 's',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        },
        red_attributes: {
          start_loc: 'n',
          end_loc: 'n',
          start_ori: 'in',
          end_ori: 'in',
          motion_type: 'static',
          turns: 0
        }
      },
      {
        beat: 1,
        letter: 'T',
        blue_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 's',
          end_loc: 'e',
          turns: 0,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'pro',
          start_ori: 'in',
          start_loc: 'n',
          end_loc: 'w',
          turns: 1,
          end_ori: 'in'
        }
      },
      {
        beat: 2,
        letter: 'T',
        blue_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          start_loc: 'e',
          end_loc: 'n',
          turns: 1,
          end_ori: 'in'
        },
        red_attributes: {
          motion_type: 'anti',
          start_ori: 'in',
          start_loc: 'w',
          end_loc: 's',
          turns: 2,
          end_ori: 'in'
        }
      }
    ]
  };

  function loadSelectedSequence() {
    if (!selectedSequence) {
      showMessage('error', 'Please select a sequence.');
      return;
    }

    const sequence = PREDEFINED_SEQUENCES[selectedSequence];
    if (!sequence) {
      showMessage('error', 'Selected sequence not found.');
      return;
    }

    animationActions.loadSequence(sequence);
    showMessage('success', `Sequence "${selectedSequence}" loaded successfully.`);
  }

  function showMessage(type: 'success' | 'error', text: string) {
    message = text;
    messageType = type;

    setTimeout(() => {
      message = '';
      messageType = '';
    }, 3000);
  }
</script>

<div class="sequence-selector">
  <div class="selector-header">
    <h3>Select Sequence</h3>
  </div>

  <div class="selector-controls">
    <label for="sequence-dropdown">Choose a sequence:</label>
    <select id="sequence-dropdown" bind:value={selectedSequence}>
      <option value="">-- Select a sequence --</option>
      {#each Object.keys(PREDEFINED_SEQUENCES) as sequenceName}
        <option value={sequenceName}>{sequenceName}</option>
      {/each}
    </select>

    <button
      class="load-btn"
      onclick={loadSelectedSequence}
      disabled={!selectedSequence}
    >
      Load Sequence
    </button>
  </div>

  {#if message}
    <div class="message" class:error={messageType === 'error'} class:success={messageType === 'success'}>
      {message}
    </div>
  {/if}
</div>

<style>
  .sequence-selector {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .selector-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #374151;
  }

  .selector-controls {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #4b5563;
  }

  select {
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    background: white;
    cursor: pointer;
  }

  select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
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
</style>
