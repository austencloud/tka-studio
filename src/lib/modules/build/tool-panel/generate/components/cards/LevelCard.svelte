<!--
LevelCard.svelte - Card for selecting difficulty level
Uses stepper pattern for space-efficient level selection
-->
<script lang="ts">
  import { DifficultyLevel } from "../../shared/domain";
  import StepperCard from "./StepperCard.svelte";

  let {
    currentLevel,
    onLevelChange,
    gridColumnSpan = 2,
    cardIndex = 0,
    headerFontSize = "9px"
  } = $props<{
    currentLevel: DifficultyLevel;
    onLevelChange: (level: DifficultyLevel) => void;
    gridColumnSpan?: number;
    cardIndex?: number;
    headerFontSize?: string;
  }>();

  // 🎨 ENHANCED: Level display data with PRONOUNCED gradient colors for visibility
  const levelData: Record<DifficultyLevel, { name: string; number: number; color: string; textColor: string }> = {
    [DifficultyLevel.BEGINNER]: {
      name: "No Turns",
      number: 1,
      // 🌟 ENHANCED: Bright sky blue gradient with radial depth
      color: `radial-gradient(ellipse at top left,
        rgb(186, 230, 253) 0%,
        rgb(125, 211, 252) 30%,
        rgb(56, 189, 248) 70%,
        rgb(14, 165, 233) 100%)`,
      textColor: "black"
    },
    [DifficultyLevel.INTERMEDIATE]: {
      name: "Whole Turns",
      number: 2,
      // 🌟 ENHANCED: Metallic silver gradient with strong contrast
      color: `radial-gradient(ellipse at top left,
        rgb(226, 232, 240) 0%,
        rgb(148, 163, 184) 30%,
        rgb(100, 116, 139) 70%,
        rgb(71, 85, 105) 100%)`,
      textColor: "white"
    },
    [DifficultyLevel.ADVANCED]: {
      name: "Half Turns",
      number: 3,
      // 🌟 ENHANCED: Rich gold gradient with warm depth
      color: `radial-gradient(ellipse at top left,
        rgb(254, 240, 138) 0%,
        rgb(253, 224, 71) 20%,
        rgb(250, 204, 21) 40%,
        rgb(234, 179, 8) 60%,
        rgb(202, 138, 4) 80%,
        rgb(161, 98, 7) 100%)`,
      textColor: "black"
    }
  };

  // Convert DifficultyLevel to numeric value for stepper
  const levelToNumber: Record<DifficultyLevel, number> = {
    [DifficultyLevel.BEGINNER]: 1,
    [DifficultyLevel.INTERMEDIATE]: 2,
    [DifficultyLevel.ADVANCED]: 3
  };

  const numberToLevel: Record<number, DifficultyLevel> = {
    1: DifficultyLevel.BEGINNER,
    2: DifficultyLevel.INTERMEDIATE,
    3: DifficultyLevel.ADVANCED
  };

  const currentLevelNumber = $derived(levelToNumber[currentLevel as DifficultyLevel]);

  function handleIncrement() {
    const newLevel = Math.min(currentLevelNumber + 1, 3);
    onLevelChange(numberToLevel[newLevel]);
  }

  function handleDecrement() {
    const newLevel = Math.max(currentLevelNumber - 1, 1);
    onLevelChange(numberToLevel[newLevel]);
  }

  function formatValue(value: number): string {
    return value.toString();
  }

  function getDescription(value: number): string {
    const level = numberToLevel[value];
    const data = levelData[level];
    return data.name;
  }

  function getColor(value: number): string {
    const level = numberToLevel[value];
    const data = levelData[level];
    return data.color;
  }

  function getTextColor(value: number): string {
    const level = numberToLevel[value];
    const data = levelData[level];
    return data.textColor;
  }

  const description = $derived(getDescription(currentLevelNumber));
  const color = $derived(getColor(currentLevelNumber));
  const textColor = $derived(getTextColor(currentLevelNumber));
</script>

<StepperCard
  title="Level"
  icon="🎯"
  currentValue={currentLevelNumber}
  minValue={1}
  maxValue={3}
  step={1}
  onIncrement={handleIncrement}
  onDecrement={handleDecrement}
  {formatValue}
  {description}
  {color}
  {textColor}
  shadowColor="0deg 0% 0%"
  {gridColumnSpan}
  {cardIndex}
  {headerFontSize}
/>
