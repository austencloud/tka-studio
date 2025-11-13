import type { Meta, StoryObj } from "@storybook/svelte";
import ContentTypeSelector from "../../lib/shared/share/components/ContentTypeSelector.svelte";

type ContentType = "video" | "animation" | "image";

const meta = {
  title: "Create/Share/ContentTypeSelector",
  component: ContentTypeSelector as any,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
    backgrounds: {
      default: "dark",
      values: [
        { name: "dark", value: "#0f141e" },
        { name: "panel", value: "linear-gradient(135deg, rgba(20, 25, 35, 0.98) 0%, rgba(15, 20, 30, 0.95) 100%)" },
      ],
    },
  },
  argTypes: {
    onSelectionChange: { action: "selectionChange" },
  },
} satisfies Meta<ContentTypeSelector>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    selectedTypes: ["image"],
    onSelectionChange: (types: ContentType[]) => console.log("Selected:", types),
  },
};

export const MultipleSelected: Story = {
  args: {
    selectedTypes: ["animation", "image"],
    onSelectionChange: (types: ContentType[]) => console.log("Selected:", types),
  },
};

export const NoneSelected: Story = {
  args: {
    selectedTypes: [],
    onSelectionChange: (types: ContentType[]) => console.log("Selected:", types),
  },
};

export const AllSelected: Story = {
  args: {
    selectedTypes: ["video", "animation", "image"],
    onSelectionChange: (types: ContentType[]) => console.log("Selected:", types),
  },
};
