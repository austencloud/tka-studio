import type { Meta, StoryObj } from "@storybook/svelte";
import SequenceCard from "../lib/modules/explore/display/components/SequenceCard/SequenceCard.svelte";
import { createSequenceData } from "$shared";

const baseSequence = createSequenceData({
  id: "seq-001",
  name: "Aurora Wave",
  word: "Aurora Wave",
  beats: [],
  thumbnails: [],
  isFavorite: false,
  isCircular: false,
  tags: [],
  metadata: {},
  sequenceLength: 8,
  author: "TKA Studio",
  dateAdded: new Date(),
  level: 1,
  difficultyLevel: "beginner",
});

const coverUrl =
  "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&auto=format&fit=crop";

const meta = {
  title: "Explore/SequenceCard",
  component: SequenceCard as any,
  tags: ["autodocs"],
  args: {
    sequence: baseSequence,
    coverUrl,
  },
  parameters: {
    layout: "centered",
  },
} satisfies Meta<SequenceCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Beginner: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "beginner",
      level: 1,
    }),
  },
};

export const Intermediate: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "intermediate",
      level: 2,
    }),
  },
};

export const Advanced: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "advanced",
      level: 3,
    }),
  },
};

export const Mythic: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "mythic",
      level: 4,
      word: "Inferno Arc",
    }),
  },
};

export const Legendary: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "legendary",
      level: 5,
      word: "Celestial Nova",
    }),
  },
};

export const Favorited: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "advanced",
      level: 3,
    }),
    isFavorite: true,
  },
};

export const NoImage: Story = {
  args: {
    sequence: createSequenceData({
      ...baseSequence,
      difficultyLevel: "intermediate",
      level: 2,
    }),
    coverUrl: "",
  },
};
