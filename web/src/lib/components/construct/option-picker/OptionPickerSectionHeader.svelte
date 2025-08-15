<!--
OptionPickerSectionHeader.svelte - Section header with colored type button

Matches the desktop version exactly:
- Centered colored button showing type name and description
- Uses LetterType colors and styling
- Clickable to toggle section (like desktop)
-->
<script lang="ts">
  // Props
  const { letterType, onToggle = () => {} } = $props<{
    letterType: string;
    onToggle?: () => void;
  }>();

  // Get type info (simplified to avoid LetterType class issues)
  const typeInfo = $derived.by(() => {
    const typeDescriptions = {
      Type1: { description: "Dual-Shift", typeName: "Type1" },
      Type2: { description: "Shift", typeName: "Type2" },
      Type3: { description: "Cross-Shift", typeName: "Type3" },
      Type4: { description: "Dash", typeName: "Type4" },
      Type5: { description: "Dual-Dash", typeName: "Type5" },
      Type6: { description: "Static", typeName: "Type6" },
    };
    return (
      typeDescriptions[letterType as keyof typeof typeDescriptions] || {
        description: "Unknown",
        typeName: "Type ?",
      }
    );
  });

  const colorPairs = $derived.by(() => {
    const colorPairs = {
      Type1: { primary: "#36c3ff", secondary: "#6F2DA8" },
      Type2: { primary: "#6F2DA8", secondary: "#6F2DA8" },
      Type3: { primary: "#26e600", secondary: "#6F2DA8" },
      Type4: { primary: "#26e600", secondary: "#26e600" },
      Type5: { primary: "#00b3ff", secondary: "#26e600" },
      Type6: { primary: "#eb7d00", secondary: "#eb7d00" },
    };
    return (
      colorPairs[letterType as keyof typeof colorPairs] || {
        primary: "#666666",
        secondary: "#666666",
      }
    );
  });

  // Generate button text like desktop
  const buttonText = $derived(`${typeInfo.typeName}: ${typeInfo.description}`);
</script>

<div class="section-header">
  <div class="header-layout">
    <!-- Stretch before button -->
    <div class="stretch"></div>

    <!-- Type button (matches desktop exactly) -->
    <button
      class="type-button"
      style:border-color={colorPairs.primary}
      style:background-color={`${colorPairs.primary}15`}
      onclick={onToggle}
      title={`Toggle ${buttonText} section`}
    >
      <span class="button-label">
        {buttonText}
      </span>
    </button>

    <!-- Stretch after button -->
    <div class="stretch"></div>
  </div>
</div>

<style>
  .section-header {
    width: 100%;
    margin-bottom: 8px;
  }

  .header-layout {
    display: flex;
    align-items: center;
    width: 100%;
  }

  .stretch {
    flex: 1;
  }

  .type-button {
    /* Match desktop button styling exactly */
    padding: 8px 16px;
    border: 2px solid;
    border-radius: 6px;
    background: transparent;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;

    /* Center the button */
    flex-shrink: 0;

    /* Text styling */
    color: var(--foreground, #000000);
    text-align: center;
    white-space: nowrap;
  }

  .type-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    opacity: 0.9;
  }

  .type-button:active {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  }

  .button-label {
    display: inline-block;
    line-height: 1.2;
  }

  /* Ensure colored text in button label is visible */
  .button-label :global(span) {
    font-weight: inherit;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .type-button {
      padding: 6px 12px;
      font-size: 13px;
    }
  }

  @media (max-width: 480px) {
    .type-button {
      padding: 4px 8px;
      font-size: 12px;
    }
  }
</style>
