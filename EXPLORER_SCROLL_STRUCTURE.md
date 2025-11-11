# Explorer Module Structure Analysis for Scroll-Based Hide/Show

## 1. OVERALL MODULE STRUCTURE

The Explorer module (src/lib/modules/explore/) is organized as:
- display/ - Sequence grid display and cards
- navigation/ - Navigation sidebar and controls  
- filtering/ - Filter and sort UI
- shared/ - Shared state and components (ExploreTab, ExploreLayout)
- collections/, users/, search/, spotlight/ - Additional features

## 2. PRIMARY SCROLLABLE CONTAINER

SequenceDisplayPanel.svelte (src/lib/modules/explore/display/components/)

Structure:
- div.sequence-display-panel (height: 100%, overflow: hidden)
  - div.display-content (flex: 1, overflow-y: auto) ← MAIN SCROLL HERE
    - ExploreGrid (renders sequences)

CSS:
.display-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg);
  container-type: inline-size;
}

## 3. LAYOUT HIERARCHY FOR HIDING

ExploreTab (main coordinator)
└── ExploreLayout (responsive layout)
    ├── div.top-section (60px height, HIDE CANDIDATE)
    │   └── CompactFilterPanel (sort dropdown + view mode)
    ├── div.horizontal-navigation (70px, portrait mobile only, HIDE CANDIDATE)
    │   └── SimpleNavigationSidebar (horizontal layout)
    └── div.main-content
        ├── SimpleNavigationSidebar (vertical, non-portrait, OPTIONAL HIDE)
        └── div.center-panel
            └── SequenceDisplayPanel
                └── div.display-content (overflow-y: auto) ← LISTEN HERE

## 4. HEADER ELEMENTS TO HIDE

1. div.top-section
   - Contains: CompactFilterPanel with sort dropdown and view toggle
   - Height: ~60px
   - Position: Top, always in layout
   - Hide trigger: Scroll down >100px

2. div.horizontal-navigation
   - Contains: SimpleNavigationSidebar with letter/level buttons
   - Height: ~70px
   - Visible: Only on portrait mobile (isPortraitMobile = true)
   - Hide trigger: Scroll down >100px (mobile only)

3. SimpleNavigationSidebar (vertical)
   - Width: 80-160px
   - Visible: Only on non-portrait screens
   - Can fade or collapse on scroll

## 5. STATE MANAGEMENT

Explore State (src/lib/modules/explore/shared/state/explore-state-factory.svelte.ts):

Key variables:
- displayedSequences[] - Filtered sequences to show
- currentSortMethod - How sequences are sorted
- availableNavigationSections[] - Section titles for navigation
- sequenceSections[] - Organized sequences by section

Uses Svelte 5 runes: $state, $derived, $effect

## 6. RESPONSIVE DETECTION

Already implemented:
const isPortraitMobile = $derived(
  responsiveSettings?.isMobile &&
  responsiveSettings?.orientation === "portrait"
);

This controls whether:
- Horizontal navigation shows (portrait only)
- Vertical sidebar shows (non-portrait only)

## 7. COMPONENT COMMUNICATION

ExploreTab passes:
- sequences to SequenceDisplayPanel
- sections to ExploreGrid
- sortMethod to SimpleNavigationSidebar
- visibility state to ExploreLayout

Scroll state would flow:
SequenceDisplayPanel (detects scroll)
→ ExploreTab (stores scroll state)
→ ExploreLayout (applies hiding via props)

## 8. KEY FILES TO MODIFY

1. SequenceDisplayPanel.svelte
   - Add scroll listener to .display-content
   - Track scroll position and direction
   - Emit scroll state

2. ExploreLayout.svelte
   - Receive scroll state prop
   - Apply display: none/flex to .top-section
   - Apply display: none/flex to .horizontal-navigation
   - Use CSS transitions

3. ExploreTab.svelte
   - Create scroll state management
   - Pass to ExploreLayout

4. SimpleNavigationSidebar.svelte (optional)
   - Add visibility prop
   - Toggle opacity or transform

## 9. IMPLEMENTATION PATTERN

Add to SequenceDisplayPanel:
let scrollPosition = $state(0);
let scrollDirection = $state("down");
let isHeaderHidden = $state(false);

$effect(() => {
  scrollContainer?.addEventListener('scroll', handleScroll);
});

function handleScroll() {
  const newPosition = scrollContainer.scrollTop;
  if (newPosition > lastScrollPosition) {
    scrollDirection = "down";
    if (newPosition > 100) isHeaderHidden = true;
  } else {
    scrollDirection = "up";
    isHeaderHidden = false;
  }
}

Pass to ExploreLayout:
<ExploreLayout 
  headerHidden={isHeaderHidden}
  navigationHidden={isHeaderHidden && isPortraitMobile}
>

## 10. CSS TRANSITIONS

.top-section {
  transition: transform 0.3s ease, opacity 0.3s ease;
  transform: translateY(0);
}

.top-section.hidden {
  transform: translateY(-100%);
  opacity: 0;
  pointer-events: none;
}

Same for .horizontal-navigation

## 11. SCROLL THRESHOLD CONSIDERATIONS

- Threshold: 100px (hide after scrolling down 100px)
- Show threshold: Scroll up to top 50px
- Debounce: 200-300ms to prevent flashing
- Animation duration: 300ms for smooth transition

## 12. RESPONSIVE CONSIDERATIONS

Mobile (portrait):
- Hide both top-section and horizontal-navigation
- Full screen for sequences

Tablet/Desktop (landscape):
- Hide top-section
- Keep vertical sidebar visible
- Show more columns

Desktop (wide):
- Hide top-section
- Keep vertical sidebar
- 4-column grid

