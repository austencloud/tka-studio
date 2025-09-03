<!-- src/lib/components/OptionPicker/utils/debugger/components/ActiveRulePanel.svelte -->
<script lang="ts">
    export let activeRule: any;
  </script>

  <h3>Active Layout Rule:</h3>
  {#if activeRule}
    <div class="rule-info">
      <span class="rule-desc">{activeRule.description}</span>
      <div class="rule-details">
        <div class="columns">Columns: <b>{activeRule.columns}</b></div>
        {#if activeRule.maxColumns}<div class="max-cols">
            (Max: {activeRule.maxColumns})
          </div>{/if}
      </div>
      <div class="conditions">
        Conditions:
        <ul>
          {#if activeRule.when.count !== undefined}<li>
              Count: {activeRule.when.count}
            </li>{/if}
          {#if activeRule.when.minCount !== undefined}<li>
              Min Count: {activeRule.when.minCount}
            </li>{/if}
          {#if activeRule.when.maxCount !== undefined}<li>
              Max Count: {activeRule.when.maxCount}
            </li>{/if}
          {#if activeRule.when.device}<li>
              Device: {activeRule.when.device}
            </li>{/if}
          {#if activeRule.when.aspect}<li>
              Aspect: {activeRule.when.aspect}
            </li>{/if}
          {#if activeRule.when.aspects}<li>
              Aspects: {activeRule.when.aspects.join(', ')}
            </li>{/if}
          {#if activeRule.when.orientation}<li>
              Orientation: {activeRule.when.orientation}
            </li>{/if}
          {#if activeRule.when.extraCheck}<li>Has extra check condition</li>{/if}
        </ul>
      </div>
    </div>
  {:else}
    <div class="no-rule">No layout rule currently matched.</div>
  {/if}

  <style>
    h3 {
      margin: 0 0 10px 0;
      font-size: 14px;
      font-weight: 600;
      color: #7dd3fc;
      border-bottom: 1px solid #334155;
      padding-bottom: 6px;
    }

    /* --- Rule Info & Conditions --- */
    .rule-info {
      margin-bottom: 14px;
    }

    .rule-desc {
      display: block;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 8px;
      font-style: italic;
    }

    .rule-details {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      font-weight: 500;
    }

    .columns b {
      color: #e2e8f0;
    }

    .columns {
      color: #7dd3fc;
    }

    .max-cols {
      color: #94a3b8;
      font-size: 11px;
    }

    .conditions {
      font-size: 11px;
      margin-top: 8px;
      color: #cbd5e1;
    }

    .conditions ul {
      margin: 4px 0 0 0;
      padding-left: 16px;
    }

    .conditions li {
      margin: 3px 0;
    }

    .no-rule {
      padding: 10px 0;
      color: #fb7185;
      font-style: italic;
    }
  </style>
