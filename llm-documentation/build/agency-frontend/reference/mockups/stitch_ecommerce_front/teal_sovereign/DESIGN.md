---
name: Teal Sovereign
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadad9'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f3'
  surface-container: '#eeeeed'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#3d4947'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f0'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#006a61'
  on-primary: '#ffffff'
  primary-container: '#49c5b6'
  on-primary-container: '#004e47'
  inverse-primary: '#61daca'
  secondary: '#276860'
  on-secondary: '#ffffff'
  secondary-container: '#aeefe4'
  on-secondary-container: '#2e6f66'
  tertiary: '#5b5f5f'
  on-tertiary: '#ffffff'
  tertiary-container: '#b0b3b3'
  on-tertiary-container: '#414546'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#7ff6e6'
  primary-fixed-dim: '#61daca'
  on-primary-fixed: '#00201c'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#aeefe4'
  secondary-fixed-dim: '#93d3c8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#015048'
  tertiary-fixed: '#e0e3e3'
  tertiary-fixed-dim: '#c4c7c7'
  on-tertiary-fixed: '#181c1d'
  on-tertiary-fixed-variant: '#434748'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style
The design system is engineered for high-volume B2B commerce, prioritizing efficiency, reliability, and institutional trust. The brand personality is professional and industrious, removing visual friction to facilitate rapid bulk ordering and account management.

The design style follows a **Corporate / Modern** aesthetic. It utilizes a refined grid, generous whitespace to manage data density, and a focused color palette that signals stability. Every interface element is designed to feel intentional and durable, moving away from consumer-oriented "fluff" toward a utilitarian yet sophisticated tool for procurement professionals.

## Colors
The color strategy centers on a "Teal Stack" to establish brand authority while maintaining professional sobriety.

- **Primary (#49C5B6):** Used for primary actions, progress indicators, and active states. It provides a modern, energetic contrast to the darker tones.
- **Secondary (#015048):** Reserved for deep-level navigation, headers, and high-impact brand moments. It anchors the UI and provides the "High-Trust" foundation.
- **Tertiary (#F4F7F7):** A soft, cool-grey teal used for surface backgrounds and subtle sectioning to prevent eye fatigue during long sessions.
- **Neutral (#1A1C1C):** A near-black for maximum legibility in typography and iconography.

## Typography
This design system utilizes **Inter** for all roles to ensure maximum readability across data-dense tables and complex forms. The hierarchy is strictly enforced to help users scan large catalogs quickly.

- **Headlines:** Use a tighter letter-spacing and heavier weights to create a sense of importance and structure.
- **Body:** Standardized at 16px for primary reading to accommodate professional users on desktop monitors.
- **Labels:** Utilized for table headers and metadata, often paired with a subtle uppercase treatment to distinguish from interactive text.

## Layout & Spacing
The layout follows a **Fluid Grid** logic with a maximum container width of 1440px to ensure the UI doesn't become over-extended on ultra-wide monitors common in office environments.

- **Desktop (1024px+):** 12-column grid with 24px gutters. Sidebars for filtering and account navigation are typically fixed at 280px.
- **Tablet (768px - 1023px):** 8-column grid with 16px gutters. Sidebars collapse into drawers.
- **Mobile (<767px):** 4-column grid with 16px margins. Product cards transition to a single-column list view for better detail visibility.

A strict 8px base unit governs all padding and margin decisions, ensuring visual harmony across diverse dashboard layouts.

## Elevation & Depth
To maintain a professional and "flat" corporate feel, depth is communicated through **Tonal Layers** and **Low-Contrast Outlines** rather than heavy shadows.

- **Level 0 (Background):** Primary background (#FFFFFF) or Tertiary (#F4F7F7) for page-level sectioning.
- **Level 1 (Cards/Surface):** White surfaces with a 1px border (#E2E8E8). No shadow.
- **Level 2 (Interaction):** When a user hovers over an element, a very soft, ambient shadow (0px 4px 12px rgba(0,0,0,0.05)) is applied to indicate lift.
- **Level 3 (Modals/Overlays):** Used for bulk-edit menus or quick-view modals, utilizing a semi-transparent backdrop blur (8px) to maintain context.

## Shapes
The shape language is **Soft**, utilizing small radii to maintain a crisp, efficient look without appearing overly "bubbly" or consumer-grade.

- **Standard Elements (Buttons, Inputs):** 0.25rem (4px) corner radius.
- **Containers (Cards, Modals):** 0.5rem (8px) corner radius.
- **Badges/Status Indicators:** 1rem (16px) or fully pill-shaped to differentiate them from interactive buttons.

## Components
Consistent component styling ensures the platform feels like a cohesive tool.

- **Buttons:** Primary buttons use #49C5B6 with white text. Secondary buttons use a #015048 outline. Height is standardized at 40px for desktop to accommodate fast clicking.
- **Product Cards:** Minimalist design focusing on SKU, stock availability, and a "Quick Add" quantity selector. Use a 1px border; do not use shadows unless hovered.
- **Structured Forms:** Labels are always top-aligned. Required fields are marked with a subtle primary-colored dot rather than a red asterisk to keep the UI clean.
- **Data Tables:** High-density rows (48px height) with zebra-striping using the Tertiary color. The header row is always pinned (sticky) and uses a `label-md` font style.
- **Progress Indicators:** Linear bars for order tracking and circular "steppers" for multi-step checkout processes, utilizing the Primary teal for completed states.
- **Chips:** Used for order status (e.g., "Shipped", "Pending"). Backgrounds should be low-opacity versions of the status color (Green/Yellow/Blue) with high-contrast text.