<script lang="ts">
  /**
   * Daily Challenge Scheduler
   * 
   * Admin tool for scheduling daily challenges
   */
  
  import { onMount } from "svelte";
  import type { IAdminChallengeService } from "../services/contracts";
  import type { ChallengeScheduleEntry, ChallengeFormData } from "../domain/models";
  import type { SequenceData } from "$shared";
  import ChallengeCalendar from "./ChallengeCalendar.svelte";
  import SequenceBrowser from "./SequenceBrowser.svelte";
  
  // Props
  let { adminChallengeService }: { adminChallengeService: IAdminChallengeService } = $props();
  
  // State
  let isLoading = $state(true);
  let scheduleEntries = $state<ChallengeScheduleEntry[]>([]);
  let userSequences = $state<SequenceData[]>([]);
  let selectedDate = $state<string | null>(null);
  let selectedSequence = $state<SequenceData | null>(null);
  let showSequenceBrowser = $state(false);

  // Customization state
  let customTitle = $state("");
  let customDescription = $state("");
  let customDifficulty = $state<"beginner" | "intermediate" | "advanced">("intermediate");
  let customXP = $state(50);
  
  // Date range (show 2 weeks: 1 week past, 1 week future)
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 7);
  const endDate = new Date();
  endDate.setDate(endDate.getDate() + 7);
  
  onMount(async () => {
    await loadData();
  });
  
  async function loadData() {
    isLoading = true;
    try {
      const [entries, sequences] = await Promise.all([
        adminChallengeService.getScheduledChallenges(startDate, endDate),
        adminChallengeService.getUserSequences(),
      ]);
      
      scheduleEntries = entries;
      userSequences = sequences;
    } catch (error) {
      console.error("❌ Failed to load scheduler data:", error);
    } finally {
      isLoading = false;
    }
  }
  
  function handleDateSelect(date: string) {
    selectedDate = date;
    showSequenceBrowser = true;
  }
  
  function handleSequenceSelect(sequence: SequenceData) {
    selectedSequence = sequence;
    // Auto-populate title and description when sequence is selected
    if (!customTitle) {
      customTitle = `Daily Challenge: ${sequence.name}`;
    }
    if (!customDescription) {
      customDescription = `Complete this sequence to earn XP!`;
    }
  }
  
  async function handleScheduleChallenge() {
    if (!selectedDate || !selectedSequence) return;

    try {
      const formData: ChallengeFormData = {
        date: selectedDate,
        sequenceId: selectedSequence.id,
        title: customTitle || `Daily Challenge: ${selectedSequence.name}`,
        description: customDescription || `Complete this sequence to earn XP!`,
        difficulty: customDifficulty === "beginner" ? "beginner" : customDifficulty === "advanced" ? "advanced" : "intermediate",
        xpReward: customXP,
        type: "build_sequence",
        target: 1,
        metadata: {
          sequenceId: selectedSequence.id,
          sequenceName: selectedSequence.name,
        },
      };

      await adminChallengeService.createChallenge(formData);

      // Reload data
      await loadData();

      // Reset selection and customization
      selectedDate = null;
      selectedSequence = null;
      showSequenceBrowser = false;
      customTitle = "";
      customDescription = "";
      customDifficulty = "intermediate";
      customXP = 50;

      console.log("✅ Challenge scheduled successfully!");
    } catch (error) {
      console.error("❌ Failed to schedule challenge:", error);
      alert("Failed to schedule challenge. Please try again.");
    }
  }
  
  function handleCancel() {
    selectedDate = null;
    selectedSequence = null;
    showSequenceBrowser = false;
    customTitle = "";
    customDescription = "";
    customDifficulty = "intermediate";
    customXP = 50;
  }

  async function handleDeleteChallenge(challengeId: string) {
    try {
      await adminChallengeService.deleteChallenge(challengeId);

      // Reload data
      await loadData();

      console.log("✅ Challenge deleted successfully!");
    } catch (error) {
      console.error("❌ Failed to delete challenge:", error);
      alert("Failed to delete challenge. Please try again.");
    }
  }
</script>

<div class="scheduler">
  {#if isLoading}
    <div class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      <p>Loading schedule...</p>
    </div>
  {:else}
    <div class="scheduler-content">
      <ChallengeCalendar
        {scheduleEntries}
        onDateSelect={handleDateSelect}
        onDeleteChallenge={handleDeleteChallenge}
      />
      
      {#if showSequenceBrowser}
        <div class="sequence-selection">
          <div class="selection-header">
            <h3>Select Sequence for {selectedDate}</h3>
            <button class="close-button" onclick={handleCancel}>
              <i class="fas fa-times"></i>
            </button>
          </div>
          
          <SequenceBrowser
            sequences={userSequences}
            selectedSequence={selectedSequence}
            onSequenceSelect={handleSequenceSelect}
          />

          {#if selectedSequence}
            <div class="customization-form">
              <h4>Customize Challenge</h4>

              <div class="form-group">
                <label for="challenge-title">Title</label>
                <input
                  id="challenge-title"
                  type="text"
                  bind:value={customTitle}
                  placeholder="Daily Challenge: Sequence Name"
                />
              </div>

              <div class="form-group">
                <label for="challenge-description">Description</label>
                <textarea
                  id="challenge-description"
                  bind:value={customDescription}
                  placeholder="Complete this sequence to earn XP!"
                  rows="2"
                ></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="challenge-difficulty">Difficulty</label>
                  <select id="challenge-difficulty" bind:value={customDifficulty}>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="challenge-xp">XP Reward</label>
                  <input
                    id="challenge-xp"
                    type="number"
                    bind:value={customXP}
                    min="10"
                    max="500"
                    step="10"
                  />
                </div>
              </div>
            </div>
          {/if}

          <div class="selection-actions">
            <button class="cancel-button" onclick={handleCancel}>
              Cancel
            </button>
            <button
              class="schedule-button"
              onclick={handleScheduleChallenge}
              disabled={!selectedSequence}
            >
              <i class="fas fa-check"></i>
              Schedule Challenge
            </button>
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .scheduler {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1.5rem;
    overflow-y: auto;
  }

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 400px;
    gap: 1rem;
    opacity: 0.6;
  }

  .loading i {
    font-size: 2.5rem;
  }

  .scheduler-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .sequence-selection {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    animation: slideIn 0.3s ease;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .selection-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .selection-header h3 {
    margin: 0;
    font-size: 1.4rem;
  }

  .close-button {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--text-color, #ffffff);
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: rotate(90deg);
  }

  /* Customization Form */
  .customization-form {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 1.25rem;
    margin-top: 1.5rem;
  }

  .customization-form h4 {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .form-group label {
    font-size: 0.9rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.8);
  }

  .form-group input,
  .form-group textarea,
  .form-group select {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 0.65rem 0.85rem;
    color: var(--text-color, #ffffff);
    font-size: 0.95rem;
    transition: all 0.2s ease;
  }

  .form-group input:focus,
  .form-group textarea:focus,
  .form-group select:focus {
    outline: none;
    border-color: rgba(102, 126, 234, 0.6);
    background: rgba(255, 255, 255, 0.12);
  }

  .form-group textarea {
    resize: vertical;
    min-height: 60px;
    font-family: inherit;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .selection-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .cancel-button,
  .schedule-button {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }

  .cancel-button {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-color, #ffffff);
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.15);
  }

  .schedule-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .schedule-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .schedule-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .scheduler {
      padding: 1rem;
    }

    .sequence-selection {
      padding: 1rem;
    }

    .form-row {
      grid-template-columns: 1fr;
    }

    .selection-actions {
      flex-direction: column;
    }

    .cancel-button,
    .schedule-button {
      width: 100%;
    }
  }
</style>

