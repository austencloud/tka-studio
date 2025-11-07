import type { Meta, StoryObj } from "@storybook/svelte";
import SequenceCard from "../lib/modules/explore/display/components/SequenceCard/SequenceCard.svelte";
import type { SequenceData } from "$shared";

const demoSequence: SequenceData = {
  id: "seq-001",
  name: "Aurora Wave",
  word: "Aurora Wave",
  beats: [],
  thumbnails: [],
  isFavorite: false,
  isCircular: false,
  tags: [],
  metadata: {},
  difficultyLevel: "intermediate",
  sequenceLength: 8,
};

const meta = {
  title: "Explore/SequenceCard",
  component: SequenceCard,
  tags: ["autodocs"],
  args: {
    sequence: demoSequence,
    coverUrl:
      "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&auto=format&fit=crop",
    badges: ["Featured", "New"],
  },
} satisfies Meta<SequenceCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Favorited: Story = {
  args: {
    isFavorite: true,
  },
};

export const NoImage: Story = {
  args: {
    coverUrl: "",
  },
};
