---
name: Precision & Growth
colors:
  surface: '#f5fbf8'
  surface-dim: '#d5dbd9'
  surface-bright: '#f5fbf8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff5f2'
  surface-container: '#e9efed'
  surface-container-high: '#e4e9e7'
  surface-container-highest: '#dee4e1'
  on-surface: '#171d1c'
  on-surface-variant: '#3d4947'
  inverse-surface: '#2c3230'
  inverse-on-surface: '#ecf2f0'
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
  tertiary: '#984629'
  on-tertiary: '#ffffff'
  tertiary-container: '#ff9774'
  on-tertiary-container: '#772e13'
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
  tertiary-fixed: '#ffdbd0'
  tertiary-fixed-dim: '#ffb59d'
  on-tertiary-fixed: '#390c00'
  on-tertiary-fixed-variant: '#7a3015'
  background: '#f5fbf8'
  on-background: '#171d1c'
  surface-variant: '#dee4e1'
typography:
  display-phase:
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
  step-indicator:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.05em
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
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 0.5rem
  sm: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  gutter: 24px
  container-max: 1280px
---

## Brand & Style

The design system is engineered for a high-performance B2B sales environment, emphasizing clarity, efficiency, and professional trust. The brand personality is authoritative yet approachable, positioning the agency as an expert extension of a client's sales team.

The visual style follows a **Modern Minimalist** approach with a focus on structured information density. By utilizing a light-mode foundation with strategic "Teal" accents, the UI directs focus toward conversion metrics and pipeline progression. Layouts are strictly card-based to containerize complex sales data, utilizing ample whitespace to prevent cognitive overload during the 22-step sales journey.

## Colors

The palette is anchored by a professional "Teal" hierarchy. 

- **Primary (#49C5B6):** Used for primary actions, progress indicators, and active states. It represents growth and movement.
- **Secondary (#015048):** Used for deep accents, sidebar backgrounds, or high-level headings to provide grounded authority.
- **Neutral Scale:** A range of cool grays (from #F9FAFB backgrounds to #111827 text) ensures high legibility and a clean, "SaaS-like" aesthetic.
- **Status Colors:** Standardized success (Emerald), warning (Amber), and error (Rose) colors should be used sparingly for pipeline health indicators.

## Typography

This design system utilizes **Inter** for its systematic, utilitarian aesthetic and exceptional legibility at small sizes. 

- **Phase Headers:** Use `display-phase` for the four major sales phases (Qualification, Discovery, etc.) to provide clear environmental landmarks.
- **Step Labeling:** Steps 1-22 should be labeled using the `step-indicator` style, capitalized and paired with the Primary Teal color.
- **Hierarchy:** Use font weight rather than size to differentiate information within cards. Primary data points should be Semibold (600), while supporting metadata should be Regular (400) in the secondary text color.

## Layout & Spacing

The layout employs a **12-column fluid grid** for desktop, transitioning to a single-column stack for mobile devices. 

- **The Storyboard Rail:** A horizontal or vertical persistent progress rail tracks the 22 steps. Each of the 4 phases is visually grouped using background shading or distinct borders.
- **Content Density:** Use `md` (24px) padding for primary cards. Information-heavy lists should use `sm` (16px) vertical spacing to maintain high visibility.
- **Breakpoints:**
  - Mobile: < 640px (Margins: 16px)
  - Tablet: 640px - 1024px (Margins: 24px)
  - Desktop: > 1024px (Margins: Auto, Max-width: 1280px)

## Elevation & Depth

This design system uses **Ambient Shadows** to define the card-based layout without creating visual clutter.

- **Level 0 (Surface):** The main background (#F9FAFB).
- **Level 1 (Cards):** White background (#FFFFFF) with a very soft, diffused shadow: `0px 1px 3px rgba(0,0,0,0.1), 0px 1px 2px rgba(0,0,0,0.06)`.
- **Level 2 (Hover/Active):** Increased shadow depth to indicate interactivity: `0px 10px 15px -3px rgba(0,0,0,0.1)`.
- **Dividers:** Use 1px borders (#E5E7EB) instead of shadows for internal card sections to maintain a crisp, professional look.

## Shapes

The shape language is **Soft** and precise. 

- **Cards & Inputs:** Use a 4px (0.25rem) corner radius. This maintains a structured, business-professional feel that is more modern than sharp corners but more serious than highly rounded ones.
- **Phase Indicators:** The 4 major phase containers may use slightly larger 8px (0.5rem) radii to distinguish them from individual data cards.
- **Buttons:** Match the card roundedness (4px) for a unified appearance.

## Components

### Buttons
- **Primary:** Background #49C5B6, Text #FFFFFF. Solid fill, no gradient.
- **Secondary:** Background #FFFFFF, Border 1px #49C5B6, Text #49C5B6.
- **Ghost:** Text #015048, no background. Used for secondary navigation actions.

### Step Indicators (The 22-Step Storyboard)
- **Completed:** Circular checkmark in Primary Teal.
- **Current:** Primary Teal border with a pulse effect; bold text.
- **Upcoming:** Light gray border and text.
- **Phase Grouping:** A subtle background tint of Secondary Teal at 5% opacity should wrap steps belonging to the same phase (e.g., Discovery).

### Cards
- Standard containers for lead info, deal value, and sales notes. Every card must have a consistent 24px internal padding.

### Inputs
- **Default State:** 1px gray border (#D1D5DB).
- **Focus State:** 2px Primary Teal border with a soft teal outer glow.
- **Labeling:** Always use top-aligned labels in `label-sm` style.

### Phase Badges
- Small, uppercase badges indicating the current phase (QUALIFICATION, DISCOVERY, etc.) should appear at the top of every view to ensure the user never loses context within the 22-step flow.