<!--
ProAntiSelectionModal.svelte - Modal for selecting Pro or Anti motion type

Appears when user moves away from float motion and needs to choose
between Pro (natural) or Anti (reverse) circular motion direction.
-->
<script lang="ts">
  import { MotionType } from "$domain";
  import "$lib/styles/modal-animations.css";
  import { onMount } from "svelte";

  interface Props {
    onMotionTypeSelect: (motionType: MotionType) => void;
    onClose: () => void;
    color: string;
    triggerElement?: HTMLElement; // The element that triggered the modal
  }

  let { onMotionTypeSelect, onClose, color, triggerElement }: Props = $props();

  let mounted = $state(false);

  onMount(() => {
    mounted = true;
    if (triggerElement) {
      // Find the prop panel container (should be the closest .prop-section)
      const propPanel = triggerElement.closest(".prop-section") as HTMLElement;
      if (propPanel) {
        renderModalOverPropPanel(propPanel);
      }
    }

    return () => {
      if (modalElement && modalElement.parentNode) {
        modalElement.parentNode.removeChild(modalElement);
      }
    };
  });

  let modalElement: HTMLElement;

  function renderModalOverPropPanel(propPanel: HTMLElement) {
    // Create modal element as a child of the prop panel
    modalElement = document.createElement("div");
    modalElement.style.cssText = `
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			z-index: 1000;
			pointer-events: auto;
		`;

    // Ensure the prop panel has relative positioning
    const currentPosition = window.getComputedStyle(propPanel).position;
    if (currentPosition === "static") {
      propPanel.style.position = "relative";
    }

    propPanel.appendChild(modalElement);
    renderModalContent();
  }

  function renderModalContent() {
    if (!modalElement) return;

    const backdrop = document.createElement("div");
    backdrop.className = "modal-backdrop";
    backdrop.style.cssText = `
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0, 0, 0, 0.4);
			backdrop-filter: blur(2px);
			z-index: 1000;
			display: flex;
			align-items: center;
			justify-content: center;
		`;

    const content = document.createElement("div");
    content.className = "modal-content";
    content.style.cssText = `
			position: relative;
			background: rgba(20, 20, 30, 0.95);
			border: 1px solid rgba(255, 255, 255, 0.2);
			border-radius: 12px;
			box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
			backdrop-filter: blur(10px);
			min-width: 240px;
			max-width: 280px;
			animation: modalAppear 0.2s ease-out;
			z-index: 10000;
		`;

    // Add modal content HTML
    content.innerHTML = `
			<div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
				<span class="modal-title" style="font-size: 13px; font-weight: 600; color: rgba(255, 255, 255, 0.9); text-transform: uppercase; letter-spacing: 0.5px;">Select Turn Direction</span>
				<button class="close-btn" style="background: none; border: none; color: rgba(255, 255, 255, 0.6); font-size: 18px; font-weight: 700; cursor: pointer; padding: 0; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; border-radius: 4px;">×</button>
			</div>
			<div class="motion-grid" style="display: grid; grid-template-columns: 1fr; gap: 12px; padding: 20px;">
				<button class="motion-option pro-option" 
					data-motion="pro"
					style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 16px 12px; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; background: rgba(255, 255, 255, 0.05); color: rgba(255, 255, 255, 0.7); cursor: pointer; min-height: 70px; transition: all 0.2s ease;">
					<span style="font-size: 20px; line-height: 1;">↻</span>
					<span style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1;">Pro</span>
					<span style="font-size: 10px; color: rgba(255, 255, 255, 0.5); text-align: center; line-height: 1.2;">Natural circular motion</span>
				</button>
				<button class="motion-option anti-option" 
					data-motion="anti"
					style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 16px 12px; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; background: rgba(255, 255, 255, 0.05); color: rgba(255, 255, 255, 0.7); cursor: pointer; min-height: 70px; transition: all 0.2s ease;">
					<span style="font-size: 20px; line-height: 1;">↺</span>
					<span style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1;">Anti</span>
					<span style="font-size: 10px; color: rgba(255, 255, 255, 0.5); text-align: center; line-height: 1.2;">Reverse circular motion</span>
				</button>
			</div>
		`;

    // Add event listeners
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) onClose();
    });

    content.querySelector(".close-btn")?.addEventListener("click", onClose);

    content.querySelectorAll(".motion-option").forEach((button) => {
      const htmlButton = button as HTMLElement;
      htmlButton.addEventListener("click", () => {
        const motionType = htmlButton.getAttribute("data-motion");
        if (motionType === "pro") {
          onMotionTypeSelect(MotionType.PRO);
        } else if (motionType === "anti") {
          onMotionTypeSelect(MotionType.ANTI);
        }
        onClose();
      });

      // Add hover effects
      htmlButton.addEventListener("mouseenter", () => {
        htmlButton.style.background = `rgba(${color}, 0.2)`;
        htmlButton.style.borderColor = `rgba(${color}, 0.4)`;
        htmlButton.style.color = "white";
      });

      htmlButton.addEventListener("mouseleave", () => {
        htmlButton.style.background = "rgba(255, 255, 255, 0.05)";
        htmlButton.style.borderColor = "rgba(255, 255, 255, 0.15)";
        htmlButton.style.color = "rgba(255, 255, 255, 0.7)";
      });
    });

    backdrop.appendChild(content);
    modalElement.appendChild(backdrop);
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      onClose();
    }
  }
</script>

<svelte:window onkeydown={handleKeyDown} />

<!-- Modal is rendered via DOM manipulation into prop panel -->
