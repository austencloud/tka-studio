import type { Meta, StoryObj } from "@storybook/svelte";
import ImageOptionsMenu from "../../lib/shared/share/components/ImageOptionsMenu.svelte";
import type { ShareOptions } from "../../lib/shared/share/domain";

const meta = {
  title: "Create/Share/ImageOptionsMenu",
  component: ImageOptionsMenu as any,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
    backgrounds: {
      default: "dark",
      values: [
        { name: "dark", value: "#0f141e" },
      ],
    },
  },
  argTypes: {
    onOptionsChange: { action: "optionsChange" },
  },
} satisfies Meta<ImageOptionsMenu>;

export default meta;
type Story = StoryObj<typeof meta>;

const defaultOptions = {
  addWord: true,
  addBeatNumbers: false,
  addUserInfo: false,
  addDifficultyLevel: true,
  includeStartPosition: true,
  userName: "",
  notes: "",
  format: "PNG" as const,
  quality: 1.0,
};

export const Collapsed: Story = {
  args: {
    options: defaultOptions,
    isExpanded: false,
    onOptionsChange: (opts: Partial<ShareOptions>) => console.log("Options:", opts),
  },
};

export const Expanded: Story = {
  args: {
    options: defaultOptions,
    isExpanded: true,
    onOptionsChange: (opts: Partial<ShareOptions>) => console.log("Options:", opts),
  },
};

export const WithUserInfo: Story = {
  args: {
    options: {
      ...defaultOptions,
      addUserInfo: true,
      userName: "John Doe",
      notes: "Practice sequence",
    },
    isExpanded: true,
    onOptionsChange: (opts: Partial<ShareOptions>) => console.log("Options:", opts),
  },
};
