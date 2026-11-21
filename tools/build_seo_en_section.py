import json, html
import sys
OUT=sys.argv[1] if len(sys.argv)>1 else 'en_content.liquid'
faq=[
("How often is NŪR Protocol used, and does NŪR Skincoach set the frequency?",
 "NŪR Protocol does not ship with a single factory setting. The frequency of use, the wavelength combination and the products to pair are defined in NŪR Skincoach, which builds a weekly protocol from the assessment (an optional selfie and a short questionnaire) and updates it as the skin changes. Sessions follow the plan shown in the app; frequency is not increased independently."),
("Can NŪR Protocol be used with a retinoid (retinol, tretinoin, adapalene)?",
 "Retinoids such as retinol, tretinoin and adapalene can leave the skin more reactive, so this FAQ does not set the combination. Any retinoid in use is declared during the NŪR Skincoach assessment so the protocol accounts for it, and the sequence is confirmed with the prescribing dermatologist before the first session. Use is interrupted if irritation appears."),
("Is NŪR Protocol safe around the eyes?",
 "The LEDs are never looked at directly, and sessions run with the eyes closed, as the user manual describes. Two silicone eye protectors are included in the box and are put in place before the mask is switched on. Any ocular pathology, recent eye surgery or eye sensitivity requires an ophthalmologist's advice before use; the device does not treat eye conditions."),
("Can NŪR Protocol be used during pregnancy or breastfeeding?",
 "This FAQ does not issue a medical opinion on LED use during pregnancy or breastfeeding, and no session frequency is recommended here for those periods. NŪR Skincoach can prepare the routine, but use of the device is validated beforehand with a dermatologist, an obstetrician or the physician following the pregnancy, and that instruction prevails over the app's protocol."),
("What is the minimum age for NŪR Protocol?",
 "NŪR Protocol is an adult skincare device, intended for users aged 18 and over. Below that age, a session must be validated with a dermatologist or a paediatrician before use, and the protocol is not applied without that advice."),
("What does the NŪR Skincoach diagnosis change in practice?",
 "The analysis (an optional selfie and a short questionnaire) maps fine lines, texture, redness and acne, then converts them into a weekly protocol: which of the seven wavelengths to combine, in which order, how often to use it and which products to pair. NŪR Skincoach records a first assessment as a baseline, so progress is compared with the skin's starting point, not a generic reference."),
]
ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
faq_html='\n'.join(f'    <div class="nur-seo__faq-item">\n      <h3>{html.escape(q,quote=False)}</h3>\n      <p>{html.escape(a,quote=False)}</p>\n    </div>' for q,a in faq)
waves=[("Red — 633 nm","The deepest of the seven. Used for firmness and collagen support."),
("Blue — 440–450 nm","Used on visible pores, in the clarity step."),
("Yellow — 590 nm","Used for radiance, uneven tone and sun spots."),
("Green — 540–550 nm","Used on the appearance of dark spots."),
("Cyan — 490 nm","Used on skin that reacts easily."),
("White — 440–630 nm","A broad band, used for renewal."),
("Magenta — red + blue","Clarity and firmness in one session.")]
waves_html='\n'.join(f'      <div class="nur-seo__wave">\n        <h3>{t}</h3>\n        <p>{d}</p>\n      </div>' for t,d in waves)

def esc(x): return html.escape(x,quote=False)
swatch={'Red':'background:#E0313B;box-shadow:0 0 18px rgba(224,49,59,.45)','Blue':'background:#3D6BFF;box-shadow:0 0 18px rgba(61,107,255,.45)','Yellow':'background:#F4C542;box-shadow:0 0 18px rgba(244,197,66,.55)','Green':'background:#34B36B;box-shadow:0 0 18px rgba(52,179,107,.45)','Cyan':'background:#2EC4D6;box-shadow:0 0 18px rgba(46,196,214,.5)','White':'background:#FFFFFF;border:1px solid #DDD6C6;box-shadow:0 0 18px rgba(200,169,110,.35)','Magenta':'background:linear-gradient(135deg,#E0313B,#3D6BFF);box-shadow:0 0 18px rgba(160,60,200,.45)'}
waves_html='\n'.join('      <div class="nur-seo__wave">\n        <span class="nur-seo__dot" style="%s" aria-hidden="true"></span>\n        <div>\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>\n      </div>' % (swatch[t.split(' ')[0]], t, d) for t,d in waves)
faq_html='\n'.join('    <details class="nur-seo__faq-item">\n      <summary><h3>%s</h3><span class="nur-seo__plus" aria-hidden="true"></span></summary>\n      <p>%s</p>\n    </details>' % (esc(q),esc(a)) for q,a in faq)
steps=[("Cleanse and dry","Skin is clean and dry, without the products the protocol excludes."),
("Eye protectors","The two silicone eye protectors, included in the box, are positioned before the device is switched on."),
("Fit","Face mask and neck panel, held by the two adjustable straps, in the same session."),
("Settings","The combination and order of the week, read in the app and applied on the controller."),
("Duration","About 10 minutes; intensity and light combination follow the week's protocol in NŪR Skincoach."),
("After","The skin is left to the products named in the protocol.")]
steps_html='\n'.join('      <li class="nur-seo__step"><span class="nur-seo__num">%02d</span><h3>%s</h3><p>%s</p></li>' % (i+1,t,d) for i,(t,d) in enumerate(steps))
specs=[("Treatment areas","Full face mask, plus a neck and décolleté panel."),
("Wavelengths","633 nm, 440–450 nm, 590 nm, 540–550 nm, 490 nm, 440–630 nm, and red + blue combined."),
("Irradiance","30 mW/cm²."),
("NŪR Skincoach","Access with the digital Gold Card (QR code); an access card is in the box."),
("In the box","Face mask, neck panel, controller, 2 adjustable straps, 2 silicone eye protectors, USB-C cable, user manual, NŪR Skincoach access card."),
("Warranty","2 years."),
("Price","{{ nur_price | money_without_trailing_zeros }}{% if nur_klarna %}, or 3 × {{ nur_third | money_without_trailing_zeros }} with Klarna{% endif %}.")]
specs_html='\n'.join('      <div class="nur-seo__spec"><dt>%s</dt><dd>%s</dd></div>' % s for s in specs)
liq = """{%- liquid
  assign nur_fr = false
  if request.locale.iso_code == 'fr'
    assign nur_fr = true
  endif
  assign nur_product = closest.product | default: product
  assign nur_price = nur_product.selected_or_first_available_variant.price
  assign nur_third = nur_price | divided_by: 3
  assign nur_klarna = false
  if cart.currency.iso_code == 'EUR'
    assign nur_klarna = true
  endif
-%}
{%- comment -%}
  English-only SEO content for the product page (UAE landing page), from the
  SEO consultant's brief of 2026-11-21. The French page keeps its own content.
  Generated by scratchpad seo/build.py: the FAQPage JSON-LD and the visible
  FAQ come from the same strings, so they match character for character.
  FAQ answers sit in <details>: still in the DOM, so readable by Google.
{%- endcomment -%}
{%- unless nur_fr -%}
<style>
  .nur-seo { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1A1A1A; max-width: 1040px; margin: 0 auto; padding: 64px 0 24px; }
  .nur-seo section { padding: 48px 0; border-top: 1px solid #ECEAE5; }
  .nur-seo section:first-child { border-top: 0; padding-top: 0; }
  .nur-seo h2 { font-size: 28px; font-weight: 500; line-height: 1.25; letter-spacing: -0.3px; margin: 0 0 14px; color: #1A1A1A; }
  .nur-seo h3 { font-size: 15px; font-weight: 700; line-height: 1.4; margin: 0 0 6px; color: #1A1A1A; }
  .nur-seo p, .nur-seo dd { font-size: 15px; line-height: 1.7; color: #4A4A4A; }
  .nur-seo p { margin: 0 0 12px; }
  .nur-seo a { color: #1A1A1A; text-decoration: underline; text-underline-offset: 3px; }
  .nur-seo__eyebrow { display: block; font-size: 11px; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; color: #C8A96E; margin-bottom: 12px; }
  .nur-seo__lead { max-width: 720px; }
  .nur-seo__head { text-align: center; max-width: 720px; margin: 0 auto 32px; }
  .nur-seo__note { font-size: 13px !important; color: #8A8A8A !important; text-align: center; margin-top: 22px !important; }
  /* Skincoach: three cards */
  .nur-seo__cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }
  .nur-seo__card { background: #FAFAF8; padding: 26px 24px; }
  .nur-seo__card p { font-size: 14px; margin: 0; }
  .nur-seo__num { display: block; font-size: 13px; font-weight: 600; letter-spacing: 1px; color: #C8A96E; margin-bottom: 10px; }
  /* Wavelengths: colour swatches */
  .nur-seo__waves { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 30px 24px; }
  .nur-seo__wave { display: flex; gap: 14px; align-items: flex-start; }
  .nur-seo__dot { flex: 0 0 34px; width: 34px; height: 34px; border-radius: 50%; margin-top: 2px; }
  .nur-seo__wave h3 { font-size: 14px; }
  .nur-seo__wave p { font-size: 13.5px; line-height: 1.6; margin: 0; }
  /* Session: numbered steps */
  .nur-seo__steps { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px 32px; }
  .nur-seo__step { border-top: 1px solid #C8A96E; padding-top: 14px; }
  .nur-seo__step p { font-size: 14px; margin: 0; }
  /* Specs table */
  .nur-seo__specs { margin: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 40px; }
  .nur-seo__spec { display: grid; grid-template-columns: 140px 1fr; gap: 16px; padding: 14px 0; border-bottom: 1px solid #ECEAE5; }
  .nur-seo__spec dt { font-size: 13px; font-weight: 700; color: #1A1A1A; }
  .nur-seo__spec dd { margin: 0; font-size: 14px; line-height: 1.6; }
  /* Two cards: testers + delivery */
  .nur-seo__duo { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; border-top: 1px solid #ECEAE5; padding: 48px 0; }
  .nur-seo__duo > div { background: #FAFAF8; padding: 30px 28px; }
  .nur-seo__duo h2 { font-size: 22px; }
  .nur-seo__duo p { font-size: 14px; }
  .nur-seo__stars { color: #C8A96E; letter-spacing: 2px; font-size: 16px; margin-bottom: 10px; display: block; }
  /* Reserve band */
  .nur-seo__reserve { text-align: center; background: #1A1A1A; padding: 44px 24px !important; border-top: 0 !important; }
  .nur-seo__reserve h2 { color: #FFFFFF; }
  .nur-seo__reserve p { color: #CFCAC0; max-width: 640px; margin: 0 auto 20px; }
  .nur-seo__cta { display: inline-block; padding: 16px 34px; background: #C8A96E; color: #1A1A1A !important; border: 0; font-family: inherit; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; text-decoration: none !important; cursor: pointer; }
  .nur-seo__cta:hover { background: #D6BC88; }
  /* FAQ accordion */
  .nur-seo__faq { max-width: 820px; margin: 0 auto; }
  .nur-seo__faq-item { border-bottom: 1px solid #ECEAE5; }
  .nur-seo__faq-item summary { list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; cursor: pointer; }
  .nur-seo__faq-item summary::-webkit-details-marker { display: none; }
  .nur-seo__faq-item summary h3 { margin: 0; font-size: 15px; }
  .nur-seo__plus { position: relative; flex: 0 0 14px; width: 14px; height: 14px; }
  .nur-seo__plus::before, .nur-seo__plus::after { content: ''; position: absolute; background: #1A1A1A; left: 0; top: 6px; width: 14px; height: 1.5px; transition: transform .25s ease; }
  .nur-seo__plus::after { transform: rotate(90deg); }
  .nur-seo__faq-item[open] .nur-seo__plus::after { transform: rotate(0deg); }
  .nur-seo__faq-item p { margin: 0 0 22px; font-size: 14.5px; }
  @media (max-width: 989px) {
    .nur-seo__waves { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .nur-seo__specs { grid-template-columns: 1fr; }
  }
  @media (max-width: 749px) {
    .nur-seo { padding: 40px 0 16px; }
    .nur-seo section, .nur-seo__duo { padding: 36px 0; }
    .nur-seo h2 { font-size: 22px; }
    .nur-seo__cards, .nur-seo__steps, .nur-seo__duo { grid-template-columns: 1fr; }
    .nur-seo__waves { grid-template-columns: 1fr; gap: 20px; }
    .nur-seo__spec { grid-template-columns: 110px 1fr; }
    .nur-seo__head { text-align: left; }
  }
</style>

<div class="nur-seo">
  <section>
    <div class="nur-seo__head">
      <span class="nur-seo__eyebrow">NŪR Protocol</span>
      <h2>Why a fixed programme is a guess</h2>
      <p>An LED mask ships with a set of programmes. The user picks one and repeats it, week after week. Texture, breakouts, redness and fine lines rarely call for the same wavelength in the same order. NŪR Protocol moves that decision into the app: NŪR Skincoach reads a selfie and a short questionnaire, then sets the weekly protocol. The set covers face and neck.</p>
    </div>
  </section>

  <section>
    <div class="nur-seo__head">
      <h2>NŪR Skincoach: the diagnosis and the weekly protocol</h2>
      <p>The diagnosis changes the use of the device: a selfie and a few questions in the app return a protocol, not a score.</p>
    </div>
    <div class="nur-seo__cards">
      <div class="nur-seo__card">
        <span class="nur-seo__num">01</span>
        <h3>The selfie assessment</h3>
        <p>The app maps fine lines, texture, redness and acne from one photograph, and records it as a baseline. The selfie is optional: the assessment can also run on the questionnaire alone. Products in use, treatments in progress and retinoids are declared in the same step.</p>
      </div>
      <div class="nur-seo__card">
        <span class="nur-seo__num">02</span>
        <h3>What the weekly protocol changes</h3>
        <p>Each week the app returns a plan: wavelengths, order, frequency, and the products to pair. The plan is read before the session and followed as written; frequency is not raised on a separate decision. Progress is read against the user's own baseline.</p>
      </div>
      <div class="nur-seo__card">
        <span class="nur-seo__num">03</span>
        <h3>Personalised protocol versus factory setting</h3>
        <p>LED masks are usually compared on wavelength, LED count, session length and price. On most of them, the programme is chosen by the user and stays fixed. NŪR Protocol adds a step: the combination is set from the assessment and updated every week.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="nur-seo__head">
      <h2>What each of the seven wavelengths does</h2>
      <p>Seven settings at 30 mW/cm², each selected for one concern.</p>
    </div>
    <div class="nur-seo__waves">
""" + waves_html + """
    </div>
    <p class="nur-seo__note">NŪR Protocol is a cosmetic device. No medical claim is made.</p>
  </section>

  <section>
    <div class="nur-seo__head">
      <h2>How a session runs</h2>
    </div>
    <ol class="nur-seo__steps">
""" + steps_html + """
    </ol>
  </section>

  <section id="nur-specs">
    <div class="nur-seo__head">
      <h2>Technical specifications</h2>
    </div>
    <dl class="nur-seo__specs">
""" + specs_html + """
    </dl>
  </section>

  <div class="nur-seo__duo">
    <div>
      <span class="nur-seo__stars" aria-hidden="true">★★★★★</span>
      <h2>Tester results: 4.6/5</h2>
      <p>Twelve testers rated NŪR Protocol 4.6/5. Their unedited reviews are on the <a href="/pages/reviews">NŪR Protocol tester reviews page</a>.</p>
      <p>The product gallery above shows before and after photos from real testers: eye area and fine lines, pigmentation, tone and texture. Same light, same angle, written consent, no retouching beyond exposure correction. They document individual results, not a guarantee.</p>
    </div>
    <div>
      <span class="nur-seo__eyebrow">Delivery &amp; support</span>
      <h2>Delivery and support in the United Arab Emirates</h2>
      <p>NŪR Protocol ships worldwide. For the United Arab Emirates, delivery takes up to 2 weeks and shipping is free; the total is confirmed at checkout. Every order ships with tracking.</p>
      <p>Orders, protocols and returns go through the <a href="/pages/contact">NŪR Protocol contact page</a>, with individual replies. Returns are accepted within 14 days of delivery, as set out in the <a href="/policies/refund-policy">refund policy</a>. Warranty: 2 years.</p>
    </div>
  </div>

  <section id="nur-faq-usage" aria-labelledby="nur-faq-usage-title">
    <div class="nur-seo__head">
      <h2 id="nur-faq-usage-title">Using NŪR Protocol: sessions, skin treatments and safety</h2>
    </div>
    <div class="nur-seo__faq">
""" + faq_html + """
    </div>
  </section>

  <section class="nur-seo__reserve">
    <h2>Reserve NŪR Protocol</h2>
    <p>{{ nur_price | money_without_trailing_zeros }}{% if nur_klarna %}, or 3 × {{ nur_third | money_without_trailing_zeros }} with Klarna at checkout{% endif %}. The set holds the face mask, the neck panel, the controller, the eye protectors and NŪR Skincoach.</p>
    <button type="button" class="nur-seo__cta" onclick="var b=document.querySelector('.buy-buttons-block')||document.querySelector('product-form-component');if(b){b.scrollIntoView({behavior:'smooth',block:'center'});}">Reserve NŪR Protocol</button>
  </section>
</div>

<script type="application/ld+json">
""" + json.dumps(ld, ensure_ascii=False, indent=2) + """
</script>
{%- endunless -%}
"""

open(OUT,'w').write(liq)
# verify visible == ld strings (html escape of apostrophe? quote=False keeps ' as is)
for q,a in faq:
    assert html.escape(a,quote=False)==a, a
    assert html.escape(q,quote=False)==q, q
print('ok', len(liq))
