<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { browser } from '$app/environment';
  import BackgroundSelector from './BackgroundSelector.svelte';
  
  interface Props {
    isOpen?: boolean;
    currentBackground?: string;
    onClose?: () => void;
    onBackgroundChange?: (background: string) => void;
  }
  
  let { isOpen = false, currentBackground = 'deepOcean', onClose, onBackgroundChange }: Props = $props();
  
  let modalElement = $state<HTMLDivElement>();
  let firstFocusableElement: HTMLElement;
  let lastFocusableElement: HTMLElement;
  let mounted = $state(false);
  
  // Only render on client to avoid hydration issues
  onMount(() => {
    mounted = true;
  });
  
  // Handle escape key and focus trapping
  onMount(() => {
    function handleKeydown(event: KeyboardEvent) {
      if (!isOpen) return;
      
      if (event.key === 'Escape') {
        onClose?.();
        return;
      }
      
      // Focus trapping
      if (event.key === 'Tab') {
        const focusableElements = modalElement?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements && focusableElements.length > 0) {
          firstFocusableElement = focusableElements[0] as HTMLElement;
          lastFocusableElement = focusableElements[focusableElements.length - 1] as HTMLElement;
          
          if (event.shiftKey) {
            if (document.activeElement === firstFocusableElement) {
              lastFocusableElement.focus();
              event.preventDefault();
            }
          } else {
            if (document.activeElement === lastFocusableElement) {
              firstFocusableElement.focus();
              event.preventDefault();
            }
          }
        }
      }
    }
    
    document.addEventListener('keydown', handleKeydown);
    
    return () => {
      document.removeEventListener('keydown', handleKeydown);
    };
  });
  
  // Focus first element when modal opens
  $effect(() => {
    if (isOpen && modalElement) {
      const focusableElements = modalElement.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusableElements.length > 0) {
        (focusableElements[0] as HTMLElement).focus();
      }
    }
  });
  
  function handleBackgroundChange(event: CustomEvent) {
    onBackgroundChange?.(event.detail);
  }
</script>

{#if mounted && isOpen}
  <!-- Modal backdrop -->
  <div 
    class="modal-backdrop" 
    role="dialog" 
    aria-modal="true" 
    aria-labelledby="settings-title"
  >
    <!-- Modal content -->
    <div class="modal-content" bind:this={modalElement}>
      <!-- Modal header -->
      <div class="modal-header">
        <h2 id="settings-title">Settings</h2>
        <button class="close-button" onclick={onClose} aria-label="Close settings">
          ✕
        </button>
      </div>
      
      <!-- Modal body -->
      <div class="modal-body">
        <BackgroundSelector 
          {currentBackground} 
          on:backgroundChange={handleBackgroundChange}
        />
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    
    /* Glassmorphism backdrop */
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    
    /* Center modal */
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    
    /* Smooth entrance animation */
    opacity: 0;
    animation: fadeIn 0.3s ease-out forwards;
  }
  
  @keyframes fadeIn {
    to {
      opacity: 1;
    }
  }
  
  .modal-content {
    /* Glassmorphism modal styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop-strong);
    -webkit-backdrop-filter: var(--glass-backdrop-strong);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass-hover);
    
    /* Layout */
    width: 100%;
    max-width: 500px;
    max-height: 80vh;
    overflow: hidden;
    
    /* Smooth entrance animation */
    transform: translateY(20px) scale(0.95);
    animation: modalSlideIn 0.3s ease-out forwards;
  }
  
  @keyframes modalSlideIn {
    to {
      transform: translateY(0) scale(1);
    }
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    border-bottom: var(--glass-border);
  }
  
  .modal-header h2 {
    margin: 0;
    color: var(--text-color);
    font-size: var(--font-size-xl);
    font-weight: 600;
  }
  
  .close-button {
    /* Glassmorphism close button */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius);
    padding: var(--spacing-sm);
    color: var(--text-color);
    cursor: pointer;
    font-size: var(--font-size-lg);
    transition: all var(--transition-normal);
    box-shadow: var(--shadow-glass);
    
    /* Center the X */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
  }
  
  .close-button:hover {
    background: var(--surface-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }
  
  .modal-body {
    padding: var(--spacing-lg);
    overflow-y: auto;
  }
  
  /* Mobile responsive */
  @media (max-width: 768px) {
    .modal-backdrop {
      padding: var(--spacing-md);
    }
    
    .modal-content {
      max-width: 100%;
      max-height: 90vh;
    }
    
    .modal-header,
    .modal-body {
      padding: var(--spacing-md);
    }
  }
  
  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .modal-backdrop,
    .modal-content {
      animation: none;
    }
    
    .modal-content {
      transform: none;
    }
  }
</style>
