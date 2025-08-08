<script lang="ts">
  import { animationActions } from '../stores/animation.js';
  import type { SequenceData } from '../types.js';
  import SequenceSelector from './SequenceSelector.svelte';
  import SequenceDictionary from './SequenceDictionary.svelte';

  let textareaValue = $state('');
  let message = $state('');
  let messageType = $state<'success' | 'error' | ''>('');
  let activeTab = $state<'dictionary' | 'select' | 'json'>('dictionary');

  // Default ALFBBLFA sequence from working HTML
  const DEFAULT_SEQUENCE: SequenceData[] = [
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
    },
    {
      beat: 4,
      letter: 'B',
      blue_attributes: {
        motion_type: 'pro',
        start_ori: 'in',
        prop_rot_dir: 'cw',
        start_loc: 'e',
        end_loc: 's',
        turns: 0,
        end_ori: 'in'
      },
      red_attributes: {
        motion_type: 'anti',
        start_ori: 'in',
        prop_rot_dir: 'cw',
        start_loc: 'w',
        end_loc: 's',
        turns: 0,
        end_ori: 'in'
      }
    },
    {
      beat: 5,
      letter: 'B',
      blue_attributes: {
        motion_type: 'anti',
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
        start_loc: 's',
        end_loc: 'e',
        turns: 0,
        end_ori: 'in'
      }
    },
    {
      beat: 6,
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
      beat: 7,
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
    },
    {
      beat: 8,
      letter: 'A',
      blue_attributes: {
        motion_type: 'pro',
        start_ori: 'in',
        prop_rot_dir: 'cw',
        start_loc: 'e',
        end_loc: 's',
        turns: 0,
        end_ori: 'in'
      },
      red_attributes: {
        motion_type: 'pro',
        start_ori: 'in',
        prop_rot_dir: 'cw',
        start_loc: 'w',
        end_loc: 'n',
        turns: 0,
        end_ori: 'in'
      }
    }
  ];

  function loadSequence() {
    const jsonString = textareaValue.trim();

    if (!jsonString) {
      showMessage('error', 'Textarea is empty.');
      return;
    }

    try {
      const parsedData = JSON.parse(jsonString) as SequenceData[];

      // Basic validation
      if (!Array.isArray(parsedData) || parsedData.length < 2) {
        throw new Error('Invalid sequence data: Must be an array with at least 2 elements.');
      }

      animationActions.loadSequence(parsedData);

      const metadata = parsedData[0] as any;
      showMessage('success', `Sequence "${metadata.word || 'Untitled'}" loaded successfully.`);
      textareaValue = ''; // Clear after successful load

    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : 'Unknown error';
      showMessage('error', `Error loading sequence: ${errorMessage}`);
    }
  }

  function loadDefaultSequence() {
    animationActions.loadSequence(DEFAULT_SEQUENCE);
    showMessage('success', 'Default ALFBBLFA sequence loaded.');
  }

  function showMessage(type: 'success' | 'error', text: string) {
    message = text;
    messageType = type;

    setTimeout(() => {
      message = '';
      messageType = '';
    }, 5000);
  }
</script>

<div class="sequence-input">
  <div class="input-header">
    <h3>Load Sequence</h3>
    <button class="load-default-btn" onclick={loadDefaultSequence}>
      Load Default (ALFBBLFA)
    </button>
  </div>

  <!-- Tab Navigation -->
  <div class="tab-nav">
    <button
      class="tab-btn"
      class:active={activeTab === 'dictionary'}
      onclick={() => activeTab = 'dictionary'}
    >
      📚 Dictionary Browser
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'select'}
      onclick={() => activeTab = 'select'}
    >
      📋 Quick Select
    </button>
    <button
      class="tab-btn"
      class:active={activeTab === 'json'}
      onclick={() => activeTab = 'json'}
    >
      📝 Paste JSON
    </button>
  </div>

  <!-- Tab Content -->
  <div class="tab-content">
    {#if activeTab === 'dictionary'}
      <SequenceDictionary />
    {:else if activeTab === 'select'}
      <SequenceSelector />
    {:else if activeTab === 'json'}
      <div class="json-input">
        <label for="sequence-textarea">Paste Sequence JSON:</label>
        <textarea
          id="sequence-textarea"
          bind:value={textareaValue}
          placeholder="Paste your sequence JSON array here..."
          rows="6"
        ></textarea>

        <div class="input-footer">
          <button class="load-btn" onclick={loadSequence}>
            Load Sequence
          </button>
        </div>
      </div>
    {/if}
  </div>

  {#if message}
    <div class="message" class:error={messageType === 'error'} class:success={messageType === 'success'}>
      {message}
    </div>
  {/if}
</div>

<style>
  .sequence-input {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .input-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #374151;
  }

  .load-default-btn {
    padding: 0.5rem 1rem;
    background: #6b7280;
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  .load-default-btn:hover {
    background: #4b5563;
  }

  .tab-nav {
    display: flex;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 1rem;
  }

  .tab-btn {
    padding: 0.75rem 1rem;
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    font-weight: 500;
    color: #6b7280;
    transition: all 0.2s;
  }

  .tab-btn:hover {
    color: #374151;
  }

  .tab-btn.active {
    color: #3b82f6;
    border-bottom-color: #3b82f6;
  }

  .tab-content {
    min-height: 200px;
  }

  .json-input {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #4b5563;
  }

  textarea {
    width: 100%;
    min-height: 120px;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    padding: 0.75rem;
    font-family: monospace;
    font-size: 0.875rem;
    resize: vertical;
  }

  textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
  }

  .input-footer {
    display: flex;
    justify-content: flex-end;
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

  .load-btn:hover {
    background: #2563eb;
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
