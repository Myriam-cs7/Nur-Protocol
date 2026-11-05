# Nur Protocol — Shopify theme

AI LED face + neck mask, $549 bundle, differentiated by **Nur Skincoach** (an AI skin diagnostic widget). Store: `678kkd-ng.myshopify.com` (domain nurprotocol.com). Theme: Horizon, Online Store 2.0.

## Deploying changes

There are exactly **TWO** custom themes, and they swap roles every time one gets published:

```
199272530304   "Nur Protocol - Sync GitHub"
201019752832   "Nur Protocol - Staging (founder photo update)"
```

Whichever one is **MAIN** (published) is what customers see. **The Shopify MCP tools refuse to write files to whichever theme has role MAIN** — you can only push to the other one (role UNPUBLISHED).

**Before every push**, check which is which:
```graphql
query { themes(first: 10) { nodes { id name role } } }
```
Push your file changes (via `themeFilesUpsert` with `body: {type: URL, value: "<raw GitHub URL>"}` — never inline large files, see "Pushing large files" below) to whichever theme is **UNPUBLISHED**. Then the user previews it and manually publishes it from Shopify Admin (Online Store > Themes > "..." > Publish) once she approves — this swaps the roles, and the theme you just pushed to becomes MAIN.

**Do not hardcode "always push to ID X"** — that assumption caused a real incident (2026-11-05) where code pushes kept landing on the no-longer-live theme for an extended period while a separate, unrelated theme was actually live, silently diverging for hours before being caught. Always re-check roles with the query above immediately before pushing, every single time.

**Never create a new theme** (`--unpublished --theme="<new name>"`, or any flow that creates a theme instead of using one of the two IDs above) — that's how we previously ended up with 5+ stray draft themes cluttering Shopify Admin. Only ever use the two fixed IDs above.

Always share the preview URL in the response after pushing, don't just say "done." Never publish automatically — the user always does that herself after approving.

If either theme ID is ever lost/deleted, list existing themes first (`themes(first: 10){nodes{id name role}}` via GraphQL) before creating a new one, and update this file with the new fixed ID immediately.

### Pushing large files safely

Never retype/inline large theme files by hand in a `themeFilesUpsert` mutation — this has caused silent content corruption twice (dropped repeated HTML blocks from LLM repetition-collapse). Always push via `body: {type: URL, value: "<raw.githubusercontent.com URL>"}` on the already-committed-and-pushed GitHub file, and verify the URL returns 200 via `curl` before calling the mutation. After pushing, always re-fetch the file from the theme and diff it against the local source before considering the push done.

### Settings only editable live (app embeds, some block settings)

Some things — app embed toggles (Theme Editor → App embeds), and some live-only settings — are **per-theme** and do **not** carry over automatically when you push code to the other theme or when a publish swap happens. After any publish, diff `config/settings_data.json`'s `current.blocks` between the two themes if an app integration seems to have silently stopped working; this is what happened with the Depo deposit app embed on 2026-11-05.

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
3. ~~Store is on Shopify's "Pause and Build" plan~~ — upgraded to **Basic** plan (confirmed via `shop.plan.publicDisplayName` on 2026-11-04). Checkout and real payments should now work; re-verify Shopify Payments / installment provider (Klarna, Shop Pay Installments) status before assuming it's still blocked.
4. SEO, GA4/Meta pixel, remove storefront password before public launch
5. Real before/after photos from early testers (the current section is an honest "coming soon" placeholder, never fill it with stock/fake images)
