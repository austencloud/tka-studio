// Resource Guide Types
// Type definitions for resource modal functionality

export interface ResourceModalData {
  title: string;
  subtitle: string;
  creator: string;
  category: string;
  level: string;
  description: string;
  keywords: string;
  url: string;
  resourceName: string;
  tableOfContents: Array<{ id: string; label: string }>;
  relatedResources: Array<{
    name: string;
    url: string;
    description: string;
    type: "internal" | "external";
  }>;
  heroGradient: string;
  creatorColor: string;
}

export interface ModalState {
  isOpen: boolean;
  resourceName: string | null;
  modalData: ResourceModalData | null;
}
