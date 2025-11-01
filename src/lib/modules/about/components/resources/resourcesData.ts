// resourcesData.ts - Resources data separated from component
export interface Resource {
  id?: string;
  name: string;
  description: string;
  url: string;
  category: string;
  level: string;
  value: string;
  hasLandingPage?: boolean;
  landingPageUrl?: string;
  status: "active" | "historical" | "vendor";
  lastUpdated?: string;
  foundingYear?: number;
  specialties?: string[];
  companyLocation?: string;
  modalType?: "educational" | "vendor" | "archive";
}

export const resources: Resource[] = [
  // ACTIVE LEARNING RESOURCES
  {
    name: "Vulcan Tech Gospel (VTG)",
    description:
      "📚 HISTORICAL FOUNDATION - Poi theory developed by Noel Yee that TKA was built from. NOTE: TKA adapted VTG concepts for STATIC PROPS (staff, fans, etc.) - poi itself is NOT supported.",
    url: "https://noelyee.com/instruction/vulcan-tech-gospel/",
    category: "active-learning",
    level: "intermediate",
    value:
      "The theoretical framework for poi spinning that inspired TKA's movement classification system.",
    status: "active",
    lastUpdated: "2023",
    hasLandingPage: true,
    landingPageUrl: "/links/vulcan-tech-gospel",
    modalType: "educational",
  },
  {
    name: "Charlie Cushing's 9 Square Theory",
    description:
      "📚 POI THEORY REFERENCE - Advanced framework for connecting unit circles in technical poi, developed by former helicopter pilot Charlie Cushing. NOTE: TKA is a STATIC PROP system and does NOT support poi.",
    url: "https://www.spinmorepoi.com/advanced/",
    category: "active-learning",
    level: "advanced",
    value:
      "Advanced poi theory building on VTG concepts (related to TKA's theoretical foundations).",
    status: "active",
    lastUpdated: "2023",
    hasLandingPage: true,
    landingPageUrl: "/links/charlie-cushing-9-square-theory",
    modalType: "educational",
  },
  {
    name: "Flow Arts Institute",
    description:
      "Educational platform exploring the phenomena of flow arts and providing comprehensive learning resources.",
    url: "https://flowartsinstitute.com/",
    category: "active-learning",
    level: "all",
    value:
      "Academic approach to understanding flow state and movement theory in flow arts.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },
  {
    name: "Playpoi",
    description:
      "Community-driven platform with extensive tutorials, courses, and educational content for poi spinning.",
    url: "https://playpoi.com/",
    category: "active-learning",
    level: "all",
    value:
      "Long-standing pillar of the poi community with comprehensive learning materials.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },
  {
    name: "The Kinetic Alphabet",
    description:
      "Revolutionary choreography notation system providing a systematic framework for flow arts movement documentation and sharing.",
    url: "/",
    category: "active-learning",
    level: "all",
    value:
      "Innovative approach to documenting and sharing flow arts choreography with structured notation - the core offering of this website.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },

  // ACTIVE COMMUNITY PLATFORMS
  {
    name: "Reddit Flow Arts Community",
    description:
      "Active discussion platform covering poi, staff, fans, hoops, and all flow arts disciplines.",
    url: "https://www.reddit.com/r/flowarts/",
    category: "active-community",
    level: "all",
    value:
      "Vibrant community for sharing videos, asking questions, and connecting with flow artists worldwide.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },
  {
    name: "Facebook Flow Arts Groups",
    description:
      "Various active Facebook groups for different flow arts communities and regional scenes.",
    url: "https://www.facebook.com/",
    category: "active-community",
    level: "all",
    value:
      "Regional and discipline-specific communities for local connections and sharing.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },
  {
    name: "Discord Communities",
    description:
      "Real-time chat communities for flow artists, including general flow arts and specialized servers.",
    url: "https://discord.com/",
    category: "active-community",
    level: "all",
    value:
      "Live discussion and community interaction with fellow flow artists.",
    status: "active",
    lastUpdated: "2024",
    modalType: "educational",
  },

  // FLOW ARTS VENDORS & EQUIPMENT
  {
    name: "Flowtoys",
    description:
      "Premium LED flow props including poi, staffs, clubs, and hoops with innovative technology.",
    url: "https://flowtoys.com/",
    category: "vendors",
    level: "all",
    value:
      "Industry leader in LED flow props with exceptional build quality and customer service.",
    status: "vendor",
    foundingYear: 2005,
    lastUpdated: "2024",
    specialties: [
      "LED Poi",
      "LED Staffs",
      "LED Clubs",
      "LED Hoops",
      "Capsule Handles",
    ],
    companyLocation: "USA",
    modalType: "vendor",
  },
  {
    name: "Lanternsmith",
    description:
      "Premium practice poi and fire poi crafted by Charlie Cushing, creator of 9 Square Theory.",
    url: "https://www.lanternsmith.com/",
    category: "vendors",
    level: "all",
    value:
      "Exceptional quality poi designed by a master practitioner with deep understanding of poi mechanics.",
    status: "vendor",
    foundingYear: 2008,
    lastUpdated: "2024",
    specialties: ["Practice Poi", "Fire Poi", "Custom Poi", "Poi Chains"],
    companyLocation: "USA",
    modalType: "vendor",
  },
  {
    name: "Cathedral Firetoys",
    description:
      "UK-based supplier of flow arts equipment, fire performance gear, and juggling props.",
    url: "https://www.cathedralfiretoys.co.uk/",
    category: "vendors",
    level: "all",
    value:
      "Reliable European supplier with extensive catalog and good shipping options.",
    status: "vendor",
    foundingYear: 2001,
    lastUpdated: "2024",
    specialties: ["Fire Props", "Practice Props", "Safety Gear", "Juggling"],
    companyLocation: "UK",
    modalType: "vendor",
  },
  {
    name: "Home of Poi",
    description:
      "Australian flow arts retailer specializing in poi, staffs, and performance accessories.",
    url: "https://www.homeofpoi.com/",
    category: "vendors",
    level: "all",
    value:
      "Long-established supplier with good selection and community connections.",
    status: "vendor",
    foundingYear: 2000,
    lastUpdated: "2024",
    specialties: ["Poi", "Staffs", "Fire Safety", "Performance Gear"],
    companyLocation: "Australia",
    modalType: "vendor",
  },

  // HISTORICAL ARCHIVES
  {
    name: "The Poi Page (Archive)",
    description:
      "Historical archive of Malcolm's original poi instruction site, one of the foundational resources of the online poi community.",
    url: "https://web.archive.org/web/20050404064746/http://www.poipage.com/",
    category: "historical-archives",
    level: "all",
    value:
      "Historical significance as one of the first comprehensive online poi instruction resources.",
    status: "historical",
    lastUpdated: "2005",
    modalType: "archive",
  },
  {
    name: "Original Glowsticking.com Archive",
    description:
      "Archive of the influential glowsticking community site that documented rave culture flow arts.",
    url: "https://web.archive.org/web/20041010000000*/glowsticking.com",
    category: "historical-archives",
    level: "all",
    value:
      "Important documentation of rave scene flow arts culture and early LED flow props.",
    status: "historical",
    lastUpdated: "2004",
    modalType: "archive",
  },
  {
    name: "Spinning.org Archive",
    description:
      "Historical poi community forum and resource archive from the early 2000s.",
    url: "https://web.archive.org/web/20050301000000*/spinning.org",
    category: "historical-archives",
    level: "all",
    value:
      "Archive of early poi community discussions and tutorial development.",
    status: "historical",
    lastUpdated: "2005",
    modalType: "archive",
  },
];

export const categories = [
  { value: "all", label: "All Resources" },
  { value: "active-learning", label: "Learning Resources" },
  { value: "active-community", label: "Community" },
  { value: "vendors", label: "Equipment & Vendors" },
  { value: "historical-archives", label: "Historical Archives" },
];

export const levels = [
  { value: "all", label: "All Levels" },
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "advanced", label: "Advanced" },
];

export function getCategoryDisplayName(category: string): string {
  const categoryMap: Record<string, string> = {
    "active-learning": "Active Learning Resources",
    "active-community": "Active Community Platforms",
    vendors: "Flow Arts Vendors & Equipment",
    "historical-archives": "Historical Archives",
  };
  return categoryMap[category] || category;
}

export function getLevelDisplayName(level: string): string {
  const levelMap: Record<string, string> = {
    beginner: "Beginner",
    intermediate: "Intermediate to Advanced",
    advanced: "Advanced",
    all: "All Levels",
  };
  return levelMap[level] || level;
}

export function getKeywordsForResource(resourceName: string): string {
  switch (resourceName) {
    case "vulcan-tech-gospel":
      return "Vulcan Tech Gospel, VTG, poi theory, Noel Yee, poi flowers, transition theory, technical poi, flow arts theory, EXTERNAL REFERENCE, NOT TKA";
    case "charlie-cushing-9-square-theory":
      return "9 square theory, Charlie Cushing, poi theory, unit circles, technical poi, helicopter pilot, LanternSmith, advanced poi, spatial relationships, EXTERNAL REFERENCE, NOT TKA";
    default:
      return "flow arts, theory, tutorial";
  }
}

export function getTableOfContentsForResource(
  resourceName: string
): Array<{ id: string; label: string }> {
  switch (resourceName) {
    case "vulcan-tech-gospel":
      return [
        { id: "overview", label: "Overview" },
        { id: "key-concepts", label: "Key Concepts" },
        { id: "getting-started", label: "Getting Started" },
        { id: "advanced-applications", label: "Advanced Applications" },
        { id: "community-impact", label: "Community Impact" },
        { id: "official-resources", label: "Official Resources" },
      ];
    case "charlie-cushing-9-square-theory":
      return [
        { id: "overview", label: "Overview" },
        { id: "creator-background", label: "Creator Background" },
        { id: "key-concepts", label: "Key Concepts" },
        { id: "getting-started", label: "Getting Started" },
        { id: "advanced-applications", label: "Advanced Applications" },
        { id: "community-resources", label: "Community Resources" },
      ];
    default:
      return [
        { id: "overview", label: "Overview" },
        { id: "getting-started", label: "Getting Started" },
        { id: "resources", label: "Additional Resources" },
      ];
  }
}
