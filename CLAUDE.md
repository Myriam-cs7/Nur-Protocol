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

Never retype/inline large theme files by hand in a `themeFilesUpsert` mutation — this has caused silent content corruption twice (dropped repeated HTML blocks from LLM repetition-collapse). Always push via `body: {type: URL, value: "<raw.githubusercontent.com URL>"}` on the already-committed-and-pushed GitHub file, and verify the URL returns 200 via `curl` before calling the mutation. **Use the commit-SHA raw URL (`raw.githubusercontent.com/Myriam-cs7/Nur-Protocol/<git rev-parse HEAD>/<path>`), not the branch-name URL** — the branch URL is CDN-cached for several minutes, so a push made right after `git push` can silently re-upload the previous version (no error, file's `updatedAt` doesn't change). After pushing, always re-fetch the file from the theme and diff it against the local source before considering the push done.

**`body: {type: URL}` fails silently on content validation errors.** Confirmed 2026-11-05: a `text`-block `settings.text` value is HTML-sanitized server-side and rejected if invalid — only `<p>`, `<ul>`, `<ol>`, `<h1>`–`<h6>` are allowed as **top-level** tags (no `<style>`, no `<div>`), and inline `style="..."` attributes on nested tags are **also** heavily restricted (confirmed: `display`, `padding`, `border`, `letter-spacing`, `text-transform`, `flex-wrap`, `gap`, `margin` on `<span>`/`<p>` are all rejected — don't assume any CSS property works without testing). When a `text`-block push with invalid markup is sent via `type: URL`, the mutation returns `job: {done: true}` with **no error anywhere** and the file is silently left unchanged — it looks identical to a successful push, and this can waste a lot of time re-pushing/re-verifying without understanding why nothing changes. **For any `text` block content, don't try to style it with inline HTML/CSS at all** — use the block's own native settings instead (`color`, `case` [e.g. `"upper"`], `font_size`, `background`, `background_color`, `corner_radius`, padding fields), which aren't sanitized the same way. If you do need custom markup in a text field, push it via `type: TEXT` with the content passed as a GraphQL variable (safe — no manual retyping risk, since the exact bytes already exist as a variable value, not hand-copied) instead of `type: URL`, specifically because `type: TEXT` surfaces real validation errors in `userErrors` while `type: URL` swallows them. A real successful push via either type returns a non-empty `upsertedThemeFiles` array — if it comes back empty, treat the push as unconfirmed and verify by re-fetching before trusting it, regardless of `job.done`.

### Settings only editable live (app embeds, some block settings)

Some things — app embed toggles (Theme Editor → App embeds), and some live-only settings — are **per-theme** and do **not** carry over automatically when you push code to the other theme or when a publish swap happens. After any publish, diff `config/settings_data.json`'s `current.blocks` between the two themes if an app integration seems to have silently stopped working; this is what happened with the Depo deposit app embed on 2026-11-05.

**French translations of theme text are per-theme too.** French was added 2026-11-05 (Translate & Adapt auto-translate, run on theme 201019752832). Product/page/policy translations are shop-level and survive a publish swap, but translations of theme text (template block settings, e.g. the product page "EARLY ACCESS" line) are stored on one theme only. After a publish swap, re-run Translate & Adapt → French on the newly live theme, then re-apply manual fixes: "EARLY ACCESS" must stay in English on the French site (French line: `<p><strong>EARLY ACCESS</strong> — Réservez dès maintenant votre masque intelligent.</p>`), and the brand stays "Nūr Protocol" (auto-translate turns it into "Protocole Nūr"). Hand-coded `custom-liquid` text isn't translatable there, so it carries its own French: the Klarna and rating lines on the product page, every homepage section, `page.about.json`, `page.reviews.json` and `snippets/nur-skincoach-chat.liquid` start with a `{%- liquid -%}` header that sets `nur_fr` (true when `request.locale.iso_code == 'fr'`) and `nur_root` (`''` in English, `/fr` in French), and each string is written `{% if nur_fr %}FR{% else %}EN{% endif %}`. **Any new or edited copy in those files needs both languages**, and internal links must be `href="{{ nur_root }}/pages/..."` — a bare `/pages/...` link drops the visitor back onto the English site. Text baked into images (hero cover `nur-protocol-hero-cover-v3.webp`, `nur-skincoach-app-guide-v4.webp`, the wavelength video) is English only. The French site lives at `nurprotocol.com/fr/` (French published 2026-11-05; Arabic is added but unpublished).

**Google Search Console** is verified (2026-11-05, URL-prefix property `https://nurprotocol.com`) by the `google-site-verification` meta tag in `layout/theme.liquid`. Both themes carry it; never remove it, or the property loses verification. Homepage SEO title/description live in Online Store → Preferences (shop translatable resource keys `meta_title`/`meta_description`, French registered via `translationsRegister`), not in shop metafields.

**Markets / pricing (2026-11-05):** shop currency is USD ($549). The market formerly called "France" (handle `fr`, id 109267812736) was renamed **"Europe"** and now holds FR + the other 26 EU countries + CH, GB, NO, with a fixed EUR price list of **€549** and local currencies off (everyone there pays in EUR). Before this, those countries weren't in any market, and Google picked up a converted €501.94. Shipping: France has its own zone, the rest of the EU is €22 "Standard International", and CH/GB/NO are in the free-express "International" zone.

**Depo deposit plan (2026-11-05):** Selling plan `gid://shopify/SellingPlan/739236544896`, group `126467637632`. It's a **20% deposit** (PERCENTAGE), calculated on the full price; a discount code comes off the balance. The balance is charged on a **fixed date**: `EXACT_TIME` 2026-12-03T23:00Z = **4 Dec** 00:00 Paris, set 2026-11-07 to match the product page copy. If the agent hasn't confirmed shipment by Nov 29, move it before Dec 4 (Depo date and product-page text together). Until 2026-11-07 it was "21 days after checkout", which charged customers before shipping. It's not known yet whether changing the date in Depo moves orders already placed. Check it on the first real order; if not, shift each order's due date with `paymentTermsUpdate`. Don't use a fixed amount: a fixed deposit is in shop currency (USD), so EUR customers were charged €91.43 instead of €100. When Depo saves, it writes the name of whichever language was saved last into the Shopify plan name, so always save **English last** ("20% Deposit"). Then re-register the French name "Acompte de 20%" with `translationsRegister` (new digest), because the checkout uses Shopify's translation. The widget labels ("Paiement intégral", the remaining-balance text) live in Depo's own widget translations.

**Delivery promise (set 2026-11-07):** the product description (EN + FR translation) and the homepage guarantees strip say **"Delivery planned before Christmas for reservations made by November 25"** (FR: « Livraison prévue avant Noël pour toute réservation jusqu’au 25 novembre »). It replaced "Ships starting November 26" and "Delivered in 15 days". The logistics behind it: the order goes to the agent on Nov 26, the agent ships within 72h to the Dubai printer by air, printing takes 2 days, then express to customers, so delivery is around Dec 9-11. The plan is to offer the deposit only until Nov 25 and switch to full payment only from Nov 26. **After Christmas, revert these texts.**

**Private Early Access block (2026-11-07):** a `custom_liquid_early_access` block in `templates/product.json`, placed after the payment logos and before the description. It covers the three Gold Card privileges (first assessment, preparation protocol, priority Christmas delivery; the user dropped a fourth, lifetime AI updates), both payment options, the promo-code maths, the Nov 25 23:59 Paris deadline and the Dec 1 public opening, in EN and FR. Amounts are computed from the variant price, so they show in the visitor's currency. The text says the balance is charged **December 4**, so the Depo plan date must match. The block hides itself after epoch 1795647540 (25 Nov 22:59 UTC). The user confirmed the real NŪR Skincoach app exists and that customers get it via a digital Gold Card with a QR code.

**Shopify Forms popup (2026-11-14):** form "Private Early Access" (id 1254260): floating popup, bottom left, email only, shown after 30s or on exit intent, on all pages, tag `shopify-forms-1254260`. French is entered in the form's own Languages section ("Private Early Access" stays in English; brand is "NŪR Skincoach"). It needs the **Forms app embed** (`shopify://apps/forms/blocks/forms/...`, block `13768625480086291342` in `config/settings_data.json`), which is per-theme: it was enabled on 201019752832 in the theme editor, then copied to 199272530304 the same day (both themes' `settings_data.json` match, Shopify checksum a9f6d959). The popup has an image (woman holding the app) set inside Forms. No pixel (Meta/Google/TikTok) is hand-coded in the theme, so the Facebook & Instagram app can be installed without duplication.

**Meta + checkout settings (2026-11-14):** the official **Facebook & Instagram** app is installed (business portfolio "Wellness Marketing Digital", which owns the NŪR Protocol page and Instagram; a new Meta pixel and catalog were created; the product is published to that channel). The cookie banner is Shopify's automated one, already shown in the EU (29 regions). Checkout: contact method is **Email only**, first and last name required, shipping phone optional, and the email marketing checkbox is shown unchecked ("Checkout and sign-in"). Before this the checkbox was hidden, so nobody could opt in and the built-in "Recover abandoned checkout" automation (marketing subscribers only) never sent anything. First real abandoned checkout: 11 Nov, €494.10 with GAELLE10, stopped before the shipping address.

## Compliance rules — do not violate these

The original copy-pasted theme code contained fabricated/unsubstantiated claims (FDA-Cleared, Dermatologist Approved, Clinical-Grade, specific % results, a fake testimonial). These have been removed. Rules going forward:

- **No FDA claims anywhere.** The only certificates on file are RoHS (materials) and a partial CE (EMC directive only, no LVD) for model M19. No FDA clearance exists.
- **No specific clinical percentages or "clinically proven" claims** (e.g. "36% wrinkle reduction") unless the user provides real study data.
- **The Institut Ambre Oriental partnership and testimonial are real and confirmed by the user** — safe to keep, but keep the visual treatment consistent with the rest of the page (centered testimonial, not a full-bleed photo split).
- When in doubt about a claim, ask the user before adding it back.

## Brand spelling

Write the brand **NŪR Protocol** and **NŪR Skincoach** (capital NŪR with the macron, matching the logo) in all customer-facing copy, in every language. Never translate the brand ("Protocole NŪR" is wrong). As of 2026-11-05 the product page, homepage, About, Reviews and the Skincoach chat all use it. Exceptions on purpose: image alt texts keep "Nur", and tester quotes keep whatever spelling the tester used ("Nur AI", "Nur Skin Coach AI").

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
