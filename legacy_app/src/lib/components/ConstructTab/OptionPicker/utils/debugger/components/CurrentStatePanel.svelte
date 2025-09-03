<!-- src/lib/components/OptionPicker/utils/debugger/components/CurrentStatePanel.svelte -->
<script lang="ts">
    import { activeLayoutRule } from '../../layoutUtils';
    import { get } from 'svelte/store';
    import CopyButton from './CopyButton.svelte';

    export let layoutContext: any;

    // Function to build the current state text for copying
    async function buildCurrentStateText(): Promise<string> {
      // Get active rule info
      const activeRule = get(activeLayoutRule);
      const ruleName = activeRule ? activeRule.description : 'No rule matched';

      // Get foldable info from context
      const foldableInfo = layoutContext.foldableInfo || {
        isFoldable: false,
        isUnfolded: false,
        foldableType: 'unknown',
        confidence: 0
      };

      // User agent info
      const ua = typeof navigator !== 'undefined' ? navigator.userAgent : 'Unknown';
      const uaShort = ua.substring(0, 80) + (ua.length > 80 ? '...' : '');

      return `Current State:
    - Active Rule: ${ruleName}
    - Columns: ${layoutContext.layoutConfig.gridColumns.match(/repeat\((\d+)\)/)?.[1] || 'unknown'}
    - Device: ${layoutContext.deviceType} (${layoutContext.isMobile ? 'mobile' : 'desktop'})
    - Foldable: ${foldableInfo?.isFoldable ? 'Yes' : 'No'}
  ${foldableInfo?.isFoldable ? `  - Type: ${foldableInfo.foldableType}\n  - Unfolded: ${foldableInfo.isUnfolded ? 'Yes' : 'No'}\n  - Detection: ${foldableInfo.detectionMethod || 'Unknown'}\n  - Confidence: ${foldableInfo.confidence || 'N/A'}` : ''}
    - Aspect: ${layoutContext.containerAspect}
    - Orientation: ${layoutContext.isPortrait ? 'portrait' : 'landscape'}
    - Size: ${layoutContext.containerWidth}×${layoutContext.containerHeight}
    - Pixel Ratio: ${typeof window !== 'undefined' ? window.devicePixelRatio : 'N/A'}
    - User Agent: ${uaShort}`;
    }
  </script>

  <div class="current-state">
    <div class="state-header">
      <span>Current State:</span>
      <CopyButton
        onClick={buildCurrentStateText}
        className="copy-current-state-button"
        iconOnly={true}
        smallIcon={true}
      />
    </div>

    <ul class="state-list">
      <li class="highlight-rule">
        <strong>Rule Applied:</strong>
        {$activeLayoutRule ? $activeLayoutRule.description : 'None matched'}
      </li>
      <li>
        <strong>Columns:</strong>
        {layoutContext.layoutConfig.gridColumns.match(/repeat\((\d+)\)/)?.[1] || 'unknown'}
      </li>
      <li>
        <strong>Device:</strong>
        {layoutContext.deviceType}
        {layoutContext.isMobile
          ? '(mobile)'
          : layoutContext.isTablet
            ? '(tablet)'
            : '(desktop)'}
      </li>

      <!-- Foldable Device Information -->
      {#if layoutContext.foldableInfo?.isFoldable}
        <li class="foldable-info highlight-foldable">
          <strong>Foldable:</strong> Yes
          <ul>
            <li>
              <strong>Type:</strong>
              {layoutContext.foldableInfo.foldableType}
            </li>
            <li>
              <strong>State:</strong>
              {layoutContext.foldableInfo.isUnfolded ? 'Unfolded' : 'Folded'}
            </li>
            {#if layoutContext.foldableInfo.detectionMethod}
              <li>
                <strong>Detection:</strong>
                {layoutContext.foldableInfo.detectionMethod}
              </li>
            {/if}
            {#if layoutContext.foldableInfo.confidence !== undefined}
              <li>
                <strong>Confidence:</strong>
                {(layoutContext.foldableInfo.confidence * 100).toFixed(0)}%
              </li>
            {/if}
          </ul>
        </li>
      {:else}
        <li><strong>Foldable:</strong> No</li>
      {/if}

      <li><strong>Aspect:</strong> {layoutContext.containerAspect}</li>
      <li>
        <strong>Orientation:</strong>
        {layoutContext.isPortrait ? 'Portrait' : 'Landscape'}
      </li>
      <li>
        <strong>Size:</strong>
        {layoutContext.containerWidth}×{layoutContext.containerHeight}
      </li>
      <li>
        <strong>Pixel Ratio:</strong>
        {typeof window !== 'undefined' ? window.devicePixelRatio : 'N/A'}
      </li>
      <li class="ua-info">
        <strong>UA:</strong>
        <div class="ua-details">
          {typeof navigator !== 'undefined'
            ? navigator.userAgent.substring(0, 80) +
              (navigator.userAgent.length > 80 ? '...' : '')
            : 'Unknown'}
        </div>
      </li>
    </ul>
  </div>

  <style>
    /* --- Current State --- */
    .current-state {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 4px;
      padding: 10px;
      margin-bottom: 12px;
      font-size: 11px;
      color: #cbd5e1;
    }

    .state-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      color: #7dd3fc;
      margin-bottom: 6px;
    }

    .state-header span {
      flex-grow: 1;
    }

    .current-state ul {
      margin: 4px 0 0 0;
      padding-left: 16px;
    }

    .current-state li {
      margin: 3px 0;
    }

    /* --- Specific styled elements --- */
    .state-list li {
      margin: 5px 0;
      line-height: 1.3;
    }

    .highlight-rule {
      background-color: #1e3a8a20;
      border-left: 3px solid #3b82f6;
      padding: 4px 8px;
      margin-left: -8px !important;
      margin-bottom: 8px !important;
    }

    .highlight-foldable {
      background-color: #065f4620;
      border-left: 3px solid #10b981;
      padding: 4px 8px;
      margin-left: -8px !important;
    }

    .foldable-info ul {
      margin-top: 3px !important;
      margin-bottom: 3px !important;
    }

    .foldable-info li {
      margin: 2px 0 !important;
    }

    .ua-info {
      margin-top: 8px !important;
      font-size: 9px;
      word-break: break-all;
    }

    .ua-details {
      max-height: 32px;
      overflow-y: auto;
      color: #94a3b8;
    }

    /* --- Copy button styles --- */
    :global(.copy-current-state-button) {
      background-color: transparent;
      color: #94a3b8;
      border: none;
      padding: 4px;
      border-radius: 4px;
      line-height: 1;
    }

    :global(.copy-current-state-button:not(:disabled):hover) {
      background-color: #334155;
      color: #e2e8f0;
      transform: none;
      box-shadow: none;
    }

    :global(.state-copy-error) {
      font-size: 9px;
      text-align: left;
      width: 100%;
      margin-bottom: 4px;
    }
  </style>
