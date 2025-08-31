<!--
OrientationModal.svelte - Mini modal for orientation selection

A small popup modal that appears when clicking the orientation button,
positioned over the specific prop panel that triggered it.
-->
<script lang="ts">
  import type { Orientation } from "$domain";
  import "$lib/styles/modal-animations.css";
  import { onMount } from "svelte";

  interface Props {
    selectedOrientation: Orientation;
    onOrientationChange: (orientation: Orientation) => void;
    onClose: () => void;
    color: string;
    triggerElement?: HTMLElement; // The button that triggered the modal
  }

  let {
    selectedOrientation,
    onOrientationChange,
    onClose,
    color,
    triggerElement,
  }: Props = $props();

  let modalElement: HTMLElement;
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
			min-width: 200px;
			max-width: 250px;
			animation: modalAppear 0.2s ease-out;
			z-index: 10000;
		`;

    // Add modal content HTML
    content.innerHTML = `
			<div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
				<span class="modal-title" style="font-size: 12px; font-weight: 600; color: rgba(255, 255, 255, 0.9); text-transform: uppercase; letter-spacing: 0.5px;">Select Orientation</span>
				<button class="close-btn" style="background: none; border: none; color: rgba(255, 255, 255, 0.6); font-size: 18px; font-weight: 700; cursor: pointer; padding: 0; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; border-radius: 4px;">×</button>
			</div>
			<div class="orientation-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; padding: 16px;">
				${orientations
          .map(
            (orientation) => `
					<button class="orientation-option ${selectedOrientation === orientation.id ? "selected" : ""}"
						data-orientation="${orientation.id}"
						style="display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 12px 8px; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; background: ${selectedOrientation === orientation.id ? `rgba(${color}, 0.2)` : "rgba(255, 255, 255, 0.05)"}; color: ${selectedOrientation === orientation.id ? "white" : "rgba(255, 255, 255, 0.7)"}; cursor: pointer; min-height: 60px;">
						<span style="font-size: 18px; line-height: 1;">${orientation.icon}</span>
						<span style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1;">${orientation.label}</span>
					</button>
				`
          )
          .join("")}
			</div>
		`;

    // Add event listeners
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) onClose();
    });

    content.querySelector(".close-btn")?.addEventListener("click", onClose);

    content.querySelectorAll(".orientation-option").forEach((button) => {
      button.addEventListener("click", () => {
        const orientation = button.getAttribute(
          "data-orientation"
        ) as Orientation;
        onOrientationChange(orientation);
        onClose();
      });
    });

    backdrop.appendChild(content);
    modalElement.appendChild(backdrop);
  }

  const orientations: {
    id: Orientation;
    label: string;
    icon: string;
    description: string;
  }[] = [
    {
      id: "in" as Orientation,
      label: "In",
      icon: "↑",
      description: "Inward orientation",
    },
    {
      id: "out" as Orientation,
      label: "Out",
      icon: "↓",
      description: "Outward orientation",
    },
    {
      id: "clock" as Orientation,
      label: "Clock",
      icon: "↻",
      description: "Clockwise orientation",
    },
    {
      id: "counter" as Orientation,
      label: "Counter",
      icon: "↺",
      description: "Counter-clockwise orientation",
    },
  ];

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      onClose();
    }
  }
</script>

<svelte:window onkeydown={handleKeyDown} />

<!-- Modal is rendered via DOM manipulation into document.body -->
