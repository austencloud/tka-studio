// Resource Guide Types
// Type definitions for resource modal functionality

export interface TableOfContentsItem {
  id: string;
  label: string;
}

export interface RelatedResource {
  name: string;
  url: string;
  description: string;
  type: "internal" | "external";
}

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
  tableOfContents: TableOfContentsItem[];
  relatedResources: RelatedResource[];
  heroGradient: string;
  creatorColor: string;
}

export interface ModalState {
  isOpen: boolean;
  resourceName: string | null;
  modalData: ResourceModalData | null;
}
