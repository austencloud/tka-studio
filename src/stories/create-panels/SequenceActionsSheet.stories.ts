import type { Meta, StoryObj } from "@storybook/svelte";
import SequenceActionsSheetWrapper from "./SequenceActionsSheetWrapper.svelte";

const meta = {
  title: "Create/Panels/SequenceActionsSheet",
  component: SequenceActionsSheetWrapper as any,
  tags: ["autodocs"],
  parameters: {
    layout: "fullscreen",
    backgrounds: {
      default: "dark",
      values: [
        { name: "dark", value: "#0a0e14" },
      ],
    },
  },
} satisfies Meta<typeof SequenceActionsSheetWrapper>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};
