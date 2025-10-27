<!--
MixedValueDropdown.svelte - Dropdown for handling mixed values in batch edit

Shows:
- Current state (all same, or mixed with values)
- Options: Keep as-is, Set all to X, Custom value

Usage:
<MixedValueDropdown
  label="Left Turn"
  values={[0, 1, 2, 3]} // 0-3 for turn amounts
  currentValues={new Set([1, 2, 3])} // Mixed values
  onChange={(value) => handleChange(value)}
/>
-->
<script lang="ts">
  // Props
  let {
    label = "",
    values = [],
    currentValues = new Set<number>(),
    selectedValue = $bindable(null),
    onChange,
  } = $props<{
    label: string;
    values: number[]; // Available values (e.g., [0, 1, 2, 3])
    currentValues: Set<number>; // Current values across selection
    selectedValue?: number | null;
    onChange?: (value: number | null) => void;
  }>();

  const isMixed = $derived(currentValues.size > 1);
  const singleValue = $derived(currentValues.size === 1 ? Array.from(currentValues)[0] : undefined);

  const displayText = $derived(() => {
    if (selectedValue !== null) {
      // User has made a selection
      return selectedValue.toString();
    }
    if (isMixed) {
      // @ts-ignore - Type inference issue with Set<number>
      return `Mixed (${Array.from(currentValues).sort((a: number, b: number) => a - b).join(', ')})`;
    }
    return singleValue !== undefined && singleValue !== null ? singleValue.toString() : '-';
  });

  const isEdited = $derived(selectedValue !== null);

  function handleChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const value = target.value;

    if (value === 'keep') {
      selectedValue = null;
      onChange?.(null);
    } else {
      const numValue = parseInt(value, 10);
      selectedValue = numValue;
      onChange?.(numValue);
    }
  }
</script>

<div class="mixed-value-dropdown">
  <label class="dropdown-label" class:edited={isEdited}>
    {label}
    {#if isEdited}
      <span class="edited-indicator">✓</span>
    {/if}
  </label>

  <div class="dropdown-info">
    <span class="current-value">
      Current: {isMixed ? 'Mixed' : singleValue}
    </span>
  </div>

  <select
    class="dropdown-select"
    class:mixed={isMixed}
    class:edited={isEdited}
    onchange={handleChange}
    value={selectedValue !== null ? selectedValue : 'keep'}
  >
    <option value="keep">
      {isMixed ? 'Keep mixed values' : 'No change'}
    </option>

    <optgroup label="Set all to:">
      {#each values as value}
        <option value={value}>
          {value} turn{value !== 1 ? 's' : ''}
          {#if currentValues.has(value)}
            (current)
          {/if}
        </option>
      {/each}
    </optgroup>
  </select>
</div>

<style>
  .mixed-value-dropdown {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
  }

  .dropdown-label {
    font-size: var(--font-size-md);
    font-weight: 500;
    color: hsl(var(--foreground));
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
  }

  .dropdown-label.edited {
    font-weight: 700;
    color: hsl(var(--primary));
  }

  .edited-indicator {
    font-size: 12px;
    color: hsl(var(--primary));
  }

  .dropdown-info {
    font-size: var(--font-size-sm);
    color: hsl(var(--muted-foreground));
  }

  .current-value {
    font-family: monospace;
  }

  .dropdown-select {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    background: hsl(var(--background));
    border: 1px solid hsl(var(--border));
    border-radius: 8px;
    font-size: var(--font-size-md);
    color: hsl(var(--foreground));
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .dropdown-select:hover {
    border-color: hsl(var(--primary) / 0.5);
  }

  .dropdown-select:focus {
    outline: none;
    border-color: hsl(var(--primary));
    box-shadow: 0 0 0 2px hsl(var(--primary) / 0.2);
  }

  .dropdown-select.mixed {
    font-style: italic;
    color: hsl(var(--muted-foreground));
  }

  .dropdown-select.edited {
    border-color: hsl(var(--primary));
    background: hsl(var(--primary) / 0.05);
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .dropdown-label {
      font-size: var(--font-size-sm);
    }

    .dropdown-select {
      padding: var(--spacing-xs) var(--spacing-sm);
      font-size: var(--font-size-sm);
    }
  }
</style>
