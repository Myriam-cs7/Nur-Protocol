# Nur Protocol — Shopify theme

AI LED face + neck mask, $549 bundle, differentiated by **Nur Skincoach** (an AI skin diagnostic widget). Store: `678kkd-ng.myshopify.com` (domain nurprotocol.com). Theme: Horizon, Online Store 2.0.

## Deploying changes

There is exactly **ONE** canonical draft/preview theme. Its Shopify theme ID is:

```
199272530304   (name in Shopify Admin: "Nur Protocol - Sync GitHub")
```

After editing files in this repo:

```
git add -A && git commit -m "..." && git push
shopify theme push --store=678kkd-ng.myshopify.com --theme=199272530304
```

**Never use `--unpublished --theme="<new name>"` again** — that flag combination always creates a brand-new theme, which is how we ended up with 5+ stray draft themes ("v2", "v3", "v4", "Live", "Updated copy of Horizon") cluttering Shopify Admin, none of them being the one actually iterated on. Always push to the fixed ID above so every change lands on the same preview theme.

This prints a preview URL — share that URL directly in the response, don't just say "done." The user then manually publishes it from Shopify Admin (Online Store > Themes) once she approves the preview. Never publish automatically.

If this theme ID is ever lost/deleted, list existing themes first (`shopify theme list --store=678kkd-ng.myshopify.com`) before creating a new one, and update this file with the new fixed ID immediately.

## Compliance rules — do not violate these

The original copy-pasted theme code contained fabricated/unsubstantiated claims (FDA-Cleared, Dermatologist Approved, Clinical-Grade, specific % results, a fake testimonial). These have been removed. Rules going forward:

- **No FDA claims anywhere.** The only certificates on file are RoHS (materials) and a partial CE (EMC directive only, no LVD) for model M19. No FDA clearance exists.
- **No specific clinical percentages or "clinically proven" claims** (e.g. "36% wrinkle reduction") unless the user provides real study data.
- **The Institut Ambre Oriental partnership and testimonial are real and confirmed by the user** — safe to keep, but keep the visual treatment consistent with the rest of the page (centered testimonial, not a full-bleed photo split).
- When in doubt about a claim, ask the user before adding it back.

## Design system

Visual language established across all custom sections (in `templates/index.json`, `snippets/nur-skincoach-chat.liquid`): gold accent `#C8A96E`, near-black `#1A1A1A`, cream background `#FAFAF8`, white `#FFFFFF`, font stack `'Helvetica Neue', Helvetica, Arial, sans-serif`, generous whitespace, thin gold dividers, eyebrow labels in uppercase letter-spaced text. Match this for any new section rather than introducing a new style.

## Architecture notes

- Homepage content lives in `templates/index.json` as a series of `custom-liquid` sections (hero, shop-by-concern, social proof, differentiators, wavelengths, before/after, guarantees+CTA, testimonial). Do not add marketing content to `sections/header-group.json` — that renders on every page site-wide (this was the original bug, already fixed).
- The Nur Skincoach chat widget lives in `snippets/nur-skincoach-chat.liquid`, rendered site-wide via `layout/theme.liquid`, with a floating "Ask Nur Skincoach" launcher button. `nurOpenChat(concernKey)` accepts an optional pre-selected concern (`wrinkles`, `pigmentation`, `acne`, `dullness`, `sensitivity`) to skip straight to step 2.
- The Skincoach quiz is currently a scripted demo (hardcoded questions/results), not a real AI backend. Task #5/#6 in the roadmap: build a real backend (e.g. Cloudflare Worker) calling the Claude API, so the diagnostic becomes a genuine conversational agent.
- Hero image is the shop file `NURP.Cover.png` (uploaded via Shopify Admin > Content > Files), referenced with `{{ 'NURP.Cover.png' | file_url }}` — shown uncropped, no text overlaid on it (the image already carries its own logo/copy).
- Product: single bundle "Nur Protocol — AI LED Face & Neck Mask", handle `nur-protocol`, $549, status ACTIVE.

## Remaining roadmap

1. Real Nur Skincoach AI backend (Claude API via a serverless function, product recommendations)
2. Legal pages (mentions légales, CGV, politique de confidentialité) — business is France-based (Aix-en-Provence), selling in USD to a US-first market
3. Store is on Shopify's "Pause and Build" plan — must upgrade before checkout can work
4. SEO, GA4/Meta pixel, remove storefront password before public launch
5. Real before/after photos from early testers (the current section is an honest "coming soon" placeholder, never fill it with stock/fake images)
