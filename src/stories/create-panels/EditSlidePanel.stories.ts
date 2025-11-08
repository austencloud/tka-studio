import type { Meta, StoryObj } from "@storybook/svelte";
import EditSlidePanelWrapper from "./EditSlidePanelWrapper.svelte";

const meta = {
  title: "Create/Panels/EditSlidePanel",
  component: EditSlidePanelWrapper as any,
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
} satisfies Meta<typeof EditSlidePanelWrapper>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};
