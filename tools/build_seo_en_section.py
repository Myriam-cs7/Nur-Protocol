"""Builds the product-page content section `custom_liquid_seo_en` (English + French).

Usage: python3 tools/build_seo_en_section.py <en.liquid> <fr.liquid>
then paste each output into templates/product.json →
sections.custom_liquid_seo_en / custom_liquid_seo_fr .settings.custom_liquid.
Two sections, not one, to stay well under the size limit of a liquid setting.

Each language has its own copy (French written for France, not a word-for-word
translation) and its own FAQPage JSON-LD, generated from the same strings as the
visible FAQ so they match character for character. Shared CSS lives in
tools/seo_section.css.liquid.
"""
import json, html, os, sys

OUT_EN, OUT_FR = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'seo_section.css.liquid')).read()
NB = ' '  # French non-breaking space before ; : ? !


def esc(x):
    return html.escape(x, quote=False)


SWATCH = {
    'red': 'background:#E0313B;box-shadow:0 0 18px rgba(224,49,59,.45)',
    'blue': 'background:#3D6BFF;box-shadow:0 0 18px rgba(61,107,255,.45)',
    'yellow': 'background:#F4C542;box-shadow:0 0 18px rgba(244,197,66,.55)',
    'green': 'background:#34B36B;box-shadow:0 0 18px rgba(52,179,107,.45)',
    'cyan': 'background:#2EC4D6;box-shadow:0 0 18px rgba(46,196,214,.5)',
    'white': 'background:#FFFFFF;border:1px solid #DDD6C6;box-shadow:0 0 18px rgba(200,169,110,.35)',
    'magenta': 'background:linear-gradient(135deg,#E0313B,#3D6BFF);box-shadow:0 0 18px rgba(160,60,200,.45)',
}

EN = {
    'lang': 'en',
    'faq': [
        ("How often is NŪR Protocol used, and does NŪR Skincoach set the frequency?",
         "NŪR Protocol does not follow one standard routine for everyone. The frequency, the wavelength combination and the skincare products to pair are set in NŪR Skincoach, which builds your personalised routine from your skin assessment (a short questionnaire, plus a selfie if you choose) and adapts it as your skin changes. The user manual recommends 3 to 5 sessions a week, in 4-week cycles; sessions follow the routine shown in the app, and frequency is never increased on your own initiative."),
        ("Can NŪR Protocol be used with a retinoid (retinol, tretinoin, adapalene)?",
         "Retinoids such as retinol, tretinoin and adapalene can leave the skin more reactive, so this FAQ does not set the combination. Any retinoid in use is declared during the NŪR Skincoach assessment so that your routine accounts for it, and the sequence is confirmed with the prescribing dermatologist before the first session. The session stops if irritation appears."),
        ("What precautions apply to the eyes?",
         "The LEDs are never looked at directly. Two silicone eye protectors are included and, as the user manual describes, are put in place before the mask is switched on. The user manual advises against the device for people with a hereditary eye condition; for any other eye condition, recent eye surgery or particular sensitivity, ask an ophthalmologist before use. The device does not treat eye conditions."),
        ("Can NŪR Protocol be used during pregnancy or breastfeeding?",
         "No. The user manual rules out pregnancy and breastfeeding, and NŪR Skincoach does not offer a routine during these periods."),
        ("From what age can NŪR Protocol be used?",
         "NŪR Protocol is a skincare device for adults, intended for people aged 18 and over."),
        ("Is the neck panel used at the same time as the mask?",
         "Yes. The face mask and the neck panel both plug into the same controller, with the Y adapter cable included, and run during the same session."),
        ("What does the NŪR Skincoach assessment change in practice?",
         "The assessment (a short questionnaire, plus a selfie if you choose) maps fine lines, texture, redness and blemishes, then turns them into a personalised routine: which of the seven wavelengths to combine, in which order, how often and with which skincare products. NŪR Skincoach records this first assessment as your starting point, so your progress is measured against your own skin, not an average."),
    ],
    'waves': [
        ('red', "Red — 633 nm", "The deepest of the seven. Used for firmness and collagen support."),
        ('blue', "Blue — 440–450 nm", "Used on visible pores, in the clarity step."),
        ('yellow', "Yellow — 550–630 nm", "Used for radiance, uneven tone and sun spots."),
        ('green', "Green — 540–550 nm", "Used on the appearance of dark spots."),
        ('cyan', "Cyan — 440–550 nm", "Used on skin that reacts easily."),
        ('white', "White — 440–630 nm", "A broad band, used for renewal."),
        ('magenta', "Magenta — red + blue", "Clarity and firmness in one session."),
    ],
    'steps': [
        ("Cleanse and dry", "Clean, dry skin, without make-up or the products your routine excludes."),
        ("Eye protectors", "The two silicone protectors, included, go in place before the device is switched on."),
        ("Fit", "The face mask and the neck panel, held by the two adjustable straps, in the same session."),
        ("Settings", "The lights and their order, read in your routine for the week and applied on the controller."),
        ("Duration", "About 10 minutes; intensity and light combination follow your routine for the week in NŪR Skincoach."),
        ("After", "Time for the skincare products named in your routine."),
    ],
    'specs': [
        ("Treatment areas", "Full face mask, plus a neck and décolleté panel."),
        ("Wavelengths", "633 nm, 440–450 nm, 550–630 nm, 540–550 nm, 440–550 nm, 440–630 nm, and red + blue combined."),
        ("Irradiance", "30 mW/cm²."),
        ("LEDs", "104: 60 on the face mask, 44 on the neck panel."),
        ("NŪR Skincoach", "Access with the digital Gold Card (QR code); an access card is in the box."),
        ("In the box", "Face mask, neck panel, controller, Y adapter cable, 2 adjustable straps, 2 silicone eye protectors, USB-C cable, user manual, NŪR Skincoach access card."),
        ("Warranty", "2 years."),
        ("Price", "{{ nur_price | money_without_trailing_zeros }}{% if nur_klarna %}, or 3 × {{ nur_third | money_without_trailing_zeros }} with Klarna{% endif %}."),
    ],
    'idea_idx': "The idea", 'idea_h2': "Why a fixed programme is a guess",
    'idea_lead': "An LED mask ships with a set of programmes. The user picks one and repeats it, week after week. Texture, breakouts, redness and fine lines rarely call for the same wavelength in the same order.",
    'idea_p': "NŪR Protocol moves that choice into the app: NŪR Skincoach assesses your skin, and that assessment gives your personalised LED routine, week after week. The LED mask treats the face and the neck.",
    'coach_idx': "NŪR Skincoach", 'coach_h2': "NŪR Skincoach: from your skin assessment to your personalised routine",
    'coach_p': "The assessment changes how you use the mask: a few questions in the app, plus a selfie if you choose, return a personalised skincare routine, not just a score.",
    'card1_alt': "Nur Skincoach app: selfie skin analysis of texture, fine lines, redness and acne, with a baseline created",
    'card1_h3': "Your skin assessment",
    'card1_p': "The app maps fine lines, texture, redness and acne from your answers to the questionnaire and, if you choose, a selfie. That assessment becomes your baseline. Skincare products in use, treatments in progress and retinoids are declared in the same step.",
    'card2_alt': "Nur Skincoach app on a phone: the weekly routine with LED sessions, focus, skincare pairing and progress against the baseline",
    'card2_h3': "Your personalised routine, week by week",
    'card2_p': "Each week the app returns your routine: wavelengths, order, frequency, and the skincare products to pair. The routine is read before the session and followed as written; frequency is not raised on a separate decision. Progress is read against the user's own baseline.",
    'card3_alt': "Nur Protocol face mask, neck panel and controller with the seven LED wavelengths",
    'card3_h3': "Personalised routine versus standard routine",
    'card3_p': "LED masks are usually compared on wavelength, LED count, session length and price. On most of them, the programme is chosen by the user and stays fixed. NŪR Protocol adds a step: your routine is set from your assessment and adapted every week.",
    'light_idx': "The light", 'light_h2': "What each of the seven wavelengths does",
    'light_p': "Seven settings at 30 mW/cm², each selected for one concern.",
    'light_note': "NŪR Protocol is a cosmetic device. No medical claim is made.",
    'ritual_idx': "The ritual", 'ritual_h2': "How a session runs",
    'specs_idx': "Details", 'specs_h2': "Technical specifications",
    'test_idx': "Testers", 'test_h2': "Tester results: 4.6/5",
    'test_p1': 'Twelve testers rated NŪR Protocol 4.6/5. Their unedited reviews are on the <a href="/pages/reviews">NŪR Protocol tester reviews page</a>.',
    'test_p2': "The product gallery above shows before and after photos from real testers: eye area and fine lines, pigmentation, tone and texture. Same light, same angle, written consent, no retouching beyond exposure correction. They document individual results, not a guarantee. More photos, and how they were taken, in our <a href=\"/blogs/news/led-face-mask-before-and-after\">before and after article</a>.",
    'deliv_idx': "Delivery", 'deliv_h2': "Delivery and support in the United Arab Emirates",
    'deliv_p1': "NŪR Protocol ships worldwide. For the United Arab Emirates, delivery takes up to 2 weeks and shipping is free; the total is confirmed at checkout. Every order ships with tracking.",
    'deliv_p2': 'Orders, questions about your routine and returns go through the <a href="/pages/contact">NŪR Protocol contact page</a>, with individual replies. Returns are accepted within 14 days of delivery, as set out in the <a href="/policies/refund-policy">refund policy</a>. Warranty: 2 years.',
    'faq_idx': "Questions",
    'res_alt': "Woman holding a Nur Protocol LED face mask glowing red",
    'res_idx': "Reserve", 'res_h2': "Reserve NŪR Protocol",
    'res_p': "The set holds the face mask, the neck panel, the controller, the eye protectors and NŪR Skincoach.",
    'res_cta': "Reserve NŪR Protocol",
    'res_klarna': "or 3 × {{ nur_third | money_without_trailing_zeros }} with Klarna at checkout",
    'as1': ("Warranty", "2 years"), 'as2': ("Delivery", "Up to 2 weeks, tracked"), 'as3': ("Included", "NŪR Skincoach"),
}

FR = {
    'lang': 'fr',
    'faq': [
        (f"À quelle fréquence utiliser NŪR Protocol, et est-ce NŪR Skincoach qui la fixe{NB}?",
         f"NŪR Protocol ne suit pas une routine standardisée, la même pour tout le monde. La fréquence, la combinaison de longueurs d’onde et les produits à associer sont définis dans NŪR Skincoach, qui compose votre routine personnalisée à partir du bilan de votre peau (un court questionnaire, et un selfie si vous le souhaitez) et la fait évoluer avec votre peau. La notice recommande 3 à 5 séances par semaine, par cycles de 4 semaines{NB}; les séances suivent la routine affichée dans l’application, et la fréquence ne s’augmente jamais de sa propre initiative."),
        (f"Peut-on utiliser NŪR Protocol avec un rétinoïde (rétinol, trétinoïne, adapalène){NB}?",
         f"Les rétinoïdes comme le rétinol, la trétinoïne ou l’adapalène peuvent rendre la peau plus réactive{NB}: cette FAQ ne fixe donc pas l’association. Tout rétinoïde en cours se déclare lors du bilan NŪR Skincoach, pour que votre routine en tienne compte, et l’enchaînement se valide avec le dermatologue prescripteur avant la première séance. La séance s’interrompt en cas d’irritation."),
        (f"Quelles précautions pour les yeux{NB}?",
         f"On ne regarde jamais les LED directement. Deux protections oculaires en silicone sont fournies et, comme l’indique la notice, se mettent en place avant d’allumer le masque. La notice déconseille l’appareil aux personnes atteintes d’une maladie héréditaire des yeux{NB}; pour toute autre affection oculaire, une chirurgie récente des yeux ou une sensibilité particulière, demandez l’avis d’un ophtalmologiste avant usage. L’appareil ne traite aucune affection des yeux."),
        (f"Peut-on utiliser NŪR Protocol pendant la grossesse ou l’allaitement{NB}?",
         "Non. La notice d’utilisation exclut la grossesse et l’allaitement, et NŪR Skincoach ne propose pas de routine pendant ces périodes."),
        (f"À partir de quel âge peut-on utiliser NŪR Protocol{NB}?",
         "NŪR Protocol est un appareil de soin pour adultes, destiné aux personnes de 18 ans et plus."),
        (f"Le panneau cou s’utilise-t-il en même temps que le masque{NB}?",
         "Oui. Le masque visage et le panneau cou se branchent tous les deux sur la même télécommande, grâce au câble adaptateur en Y fourni, et fonctionnent pendant la même séance."),
        (f"Qu’est-ce que le bilan NŪR Skincoach change concrètement{NB}?",
         f"Le bilan (un court questionnaire, et un selfie si vous le souhaitez) repère ridules, texture, rougeurs et imperfections, puis les traduit en routine personnalisée{NB}: quelles longueurs d’onde associer parmi les sept, dans quel ordre, à quelle fréquence et avec quels produits skincare. NŪR Skincoach enregistre ce premier bilan comme point de départ{NB}: vos progrès se mesurent par rapport à votre peau, pas à une moyenne."),
    ],
    'waves': [
        ('red', "Rouge — 633 nm", "La plus profonde des sept. Utilisée pour la fermeté et le soutien du collagène."),
        ('blue', "Bleu — 440–450 nm", "Utilisée sur les pores visibles, dans l’étape clarté."),
        ('yellow', "Jaune — 550–630 nm", "Utilisée pour l’éclat, le teint irrégulier et les taches de soleil."),
        ('green', "Vert — 540–550 nm", "Utilisée sur l’apparence des taches."),
        ('cyan', "Cyan — 440–550 nm", "Utilisée sur les peaux qui réagissent facilement."),
        ('white', "Blanc — 440–630 nm", "Une large bande, utilisée pour le renouvellement."),
        ('magenta', "Magenta — rouge + bleu", "Clarté et fermeté en une seule séance."),
    ],
    'steps': [
        ("Nettoyer et sécher", "Une peau propre et sèche, sans maquillage ni les produits que votre routine exclut."),
        ("Protections oculaires", "Les deux protections en silicone, fournies, se placent avant d’allumer l’appareil."),
        ("Mise en place", "Le masque visage et le panneau cou, tenus par les deux sangles réglables, pendant la même séance."),
        ("Réglages", "Les lumières et leur ordre, lus dans votre routine de la semaine et appliqués sur la télécommande."),
        ("Durée", f"Environ 10 minutes{NB}; l’intensité et la combinaison de lumières suivent votre routine de la semaine dans NŪR Skincoach."),
        ("Après", "Place aux soins skincare indiqués dans votre routine."),
    ],
    'specs': [
        ("Zones traitées", "Masque visage complet, plus un panneau cou et décolleté."),
        ("Longueurs d’onde", "633 nm, 440–450 nm, 550–630 nm, 540–550 nm, 440–550 nm, 440–630 nm, et rouge + bleu combinés."),
        ("Irradiance", "30 mW/cm²."),
        ("LED", f"104{NB}: 60 sur le masque visage, 44 sur le panneau cou."),
        ("NŪR Skincoach", f"Accès avec la carte Gold digitale (QR code){NB}; une carte d’accès est dans la boîte."),
        ("Contenu de la boîte", "Masque visage, panneau cou, télécommande, câble adaptateur en Y, 2 sangles réglables, 2 protections oculaires en silicone, câble USB-C, notice d’utilisation, carte d’accès NŪR Skincoach."),
        ("Garantie", "2 ans."),
        ("Prix", "{{ nur_price | money_without_trailing_zeros }}{% if nur_klarna %}, ou 3 × {{ nur_third | money_without_trailing_zeros }} avec Klarna{% endif %}."),
    ],
    'idea_idx': "L’idée", 'idea_h2': "Pourquoi un programme fixe reste une approximation",
    'idea_lead': "Un masque LED est livré avec quelques programmes. On en choisit un et on le répète, semaine après semaine. Or texture, imperfections, rougeurs et ridules appellent rarement la même longueur d’onde, dans le même ordre.",
    'idea_p': f"NŪR Protocol confie ce choix à l’application{NB}: NŪR Skincoach fait le bilan de votre peau, et ce bilan donne votre routine LED personnalisée, semaine après semaine. Le masque LED traite le visage et le cou.",
    'coach_idx': "NŪR Skincoach", 'coach_h2': f"NŪR Skincoach{NB}: du bilan de votre peau à votre routine personnalisée",
    'coach_p': f"Le bilan change la façon d’utiliser votre masque{NB}: quelques questions dans l’application, et un selfie si vous le souhaitez, donnent une routine skincare personnalisée, pas une simple note.",
    'card1_alt': "Application Nur Skincoach : analyse de la peau par selfie (texture, ridules, rougeurs, imperfections) et création d’un point de départ",
    'card1_h3': "Le bilan de votre peau",
    'card1_p': "L’application repère ridules, texture, rougeurs et imperfections, à partir de vos réponses au questionnaire et, si vous le souhaitez, d’un selfie. Ce bilan devient votre point de départ. Vos produits skincare, vos traitements en cours et vos rétinoïdes se déclarent à la même étape.",
    'card2_alt': "Application Nur Skincoach sur téléphone : la routine de la semaine avec les séances LED, l’objectif, les produits associés et les progrès",
    'card2_h3': "Votre routine personnalisée, semaine après semaine",
    'card2_p': f"Chaque semaine, l’application vous propose votre routine{NB}: longueurs d’onde, ordre, fréquence et produits skincare à associer. Vous la consultez avant la séance et la suivez telle quelle{NB}; la fréquence ne s’augmente pas à part. Vos progrès se lisent par rapport à votre propre point de départ.",
    'card3_alt': "Masque visage, panneau cou et télécommande Nur Protocol avec les sept longueurs d’onde LED",
    'card3_h3': "Routine personnalisée ou routine standardisée",
    'card3_p': f"On compare souvent les masques LED sur les longueurs d’onde, le nombre de LED, la durée de séance et le prix. Sur la plupart, le programme se choisit à la main et reste figé. NŪR Protocol ajoute une étape{NB}: votre routine découle de votre bilan et s’adapte chaque semaine.",
    'light_idx': "La lumière", 'light_h2': "Ce que fait chacune des sept longueurs d’onde",
    'light_p': "Sept réglages à 30 mW/cm², chacun choisi pour une préoccupation.",
    'light_note': "NŪR Protocol est un appareil cosmétique. Aucune allégation médicale n’est faite.",
    'ritual_idx': "Le rituel", 'ritual_h2': "Le déroulé d’une séance",
    'specs_idx': "Détails", 'specs_h2': "Caractéristiques techniques",
    'test_idx': "Avis", 'test_h2': f"Avis des testeurs{NB}: 4,6/5",
    'test_p1': 'Douze personnes ont testé NŪR Protocol et lui ont donné 4,6/5. Leurs avis, non retouchés, sont sur la <a href="{{ nur_root }}/pages/reviews">page des avis des testeurs NŪR Protocol</a>.',
    'test_p2': f"La galerie produit, plus haut, montre des photos avant/après de vrais testeurs{NB}: contour des yeux et ridules, pigmentation, teint et texture. Même lumière, même angle, consentement écrit, aucune retouche au-delà de la correction d’exposition. Elles montrent des résultats individuels, pas une garantie. Toutes les photos, et la façon dont elles ont été prises, sont dans notre <a href=\"{{{{ nur_root }}}}/blogs/news/masque-led-visage-avant-apres\">article avant/après</a>.",
    'deliv_idx': "Livraison", 'deliv_h2': "Livraison en France et en Europe",
    'deliv_p1': f"NŪR Protocol est livré en France, dans toute l’Union européenne, en Suisse, au Royaume-Uni et en Norvège, en 2 semaines maximum, avec suivi. La livraison est offerte en France, en Suisse, au Royaume-Uni et en Norvège{NB}; elle coûte 22 € vers les autres pays de l’Union européenne. Le total est confirmé au moment du paiement.",
    'deliv_p2': f'Commandes, questions sur votre routine et retours passent par la <a href="{{{{ nur_root }}}}/pages/contact">page contact NŪR Protocol</a>, avec une réponse personnelle. Les retours sont acceptés sous 14 jours après la livraison, comme le prévoit la <a href="{{{{ nur_root }}}}/policies/refund-policy">politique de remboursement</a>. Garantie{NB}: 2 ans.',
    'faq_idx': "Questions",
    'res_alt': "Femme tenant un masque LED Nur Protocol allumé en rouge",
    'res_idx': "Réserver", 'res_h2': "Réserver NŪR Protocol",
    'res_p': "Le coffret réunit le masque visage, le panneau cou, la télécommande, les protections oculaires et NŪR Skincoach.",
    'res_cta': "Réserver NŪR Protocol",
    'res_klarna': "ou 3 × {{ nur_third | money_without_trailing_zeros }} avec Klarna au paiement",
    'as1': ("Garantie", "2 ans"), 'as2': ("Livraison", "2 semaines max., avec suivi"), 'as3': ("Inclus", "NŪR Skincoach"),
}


def body(L):
    for q, a in L['faq']:
        assert esc(q) == q and esc(a) == a, (q, a)  # visible text == JSON-LD text
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": L['lang'],
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in L['faq']]}
    if L['lang'] == 'en':
        del ld['inLanguage']  # keep the English JSON-LD exactly as published
    waves = '\n'.join('      <div class="nur-seo__wave">\n        <span class="nur-seo__dot" style="%s" aria-hidden="true"></span>\n        <div>\n          <h3>%s</h3>\n          <p>%s</p>\n        </div>\n      </div>' % (SWATCH[k], t, d) for k, t, d in L['waves'])
    steps = '\n'.join('      <li class="nur-seo__step"><span class="nur-seo__num">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, d) for i, (t, d) in enumerate(L['steps']))
    specs = '\n'.join('      <div class="nur-seo__spec"><dt>%s</dt><dd>%s</dd></div>' % s for s in L['specs'])
    faq = '\n'.join('    <details class="nur-seo__faq-item">\n      <summary><h3>%s</h3><span class="nur-seo__plus" aria-hidden="true"></span></summary>\n      <p>%s</p>\n    </details>' % (esc(q), esc(a)) for q, a in L['faq'])
    g = L.get
    return f"""<div class="nur-seo" lang="{g('lang')}">
  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('idea_idx')}</span><h2>{g('idea_h2')}</h2></div>
    <div>
      <p class="nur-seo__lead">{g('idea_lead')}</p>
      <p>{g('idea_p')}</p>
    </div>
  </section>

  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('coach_idx')}</span><h2>{g('coach_h2')}</h2></div>
    <div>
      <p>{g('coach_p')}</p>
      <div class="nur-seo__cards">
        <div class="nur-seo__card">
          <img class="nur-seo__card-img" src="{{{{ 'nur-skincoach-step-1-selfie.webp' | asset_url }}}}" width="700" height="700" loading="lazy" alt="{g('card1_alt')}">
          <span class="nur-seo__num">01</span>
          <h3>{g('card1_h3')}</h3>
          <p>{g('card1_p')}</p>
        </div>
        <div class="nur-seo__card">
          <img class="nur-seo__card-img" src="{{{{ 'nur-skincoach-step-2-weekly.webp' | asset_url }}}}" width="700" height="700" loading="lazy" alt="{g('card2_alt')}">
          <span class="nur-seo__num">02</span>
          <h3>{g('card2_h3')}</h3>
          <p>{g('card2_p')}</p>
        </div>
        <div class="nur-seo__card">
          <img class="nur-seo__card-img" src="{{{{ 'nur-skincoach-step-3-wavelengths.webp' | asset_url }}}}" width="700" height="700" loading="lazy" alt="{g('card3_alt')}">
          <span class="nur-seo__num">03</span>
          <h3>{g('card3_h3')}</h3>
          <p>{g('card3_p')}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('light_idx')}</span><h2>{g('light_h2')}</h2></div>
    <div>
      <p>{g('light_p')}</p>
      <div class="nur-seo__waves">
{waves}
      </div>
      <p class="nur-seo__note">{g('light_note')}</p>
    </div>
  </section>

  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('ritual_idx')}</span><h2>{g('ritual_h2')}</h2></div>
    <ol class="nur-seo__steps">
{steps}
    </ol>
  </section>

  <section class="nur-seo__row" id="nur-specs">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('specs_idx')}</span><h2>{g('specs_h2')}</h2></div>
    <dl class="nur-seo__specs">
{specs}
    </dl>
  </section>

  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('test_idx')}</span><h2>{g('test_h2')}</h2></div>
    <div>
      <span class="nur-seo__stars" aria-hidden="true">★★★★★</span>
      <p>{g('test_p1')}</p>
      <p>{g('test_p2')}</p>
    </div>
  </section>

  <section class="nur-seo__row">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('deliv_idx')}</span><h2>{g('deliv_h2')}</h2></div>
    <div>
      <p>{g('deliv_p1')}</p>
      <p>{g('deliv_p2')}</p>
    </div>
  </section>

  <section class="nur-seo__row" id="nur-faq-usage" aria-labelledby="nur-faq-usage-title">
    <div class="nur-seo__label"><span class="nur-seo__idx">{g('faq_idx')}</span><h2 id="nur-faq-usage-title">FAQ</h2></div>
    <div class="nur-seo__faq">
{faq}
    </div>
  </section>

  <section class="nur-seo__reserve">
    <img class="nur-seo__reserve-img" src="{{{{ 'nur-reserve-red-light.webp' | asset_url }}}}" width="800" height="833" loading="lazy" alt="{g('res_alt')}">
    <div class="nur-seo__reserve-body">
      <span class="nur-seo__idx">{g('res_idx')}</span>
      <h2>{g('res_h2')}</h2>
      <span class="nur-seo__price">{{{{ nur_price | money_without_trailing_zeros }}}}</span>
      <p>{g('res_p')}</p>
      <button type="button" class="nur-seo__cta" onclick="var b=document.querySelector('.buy-buttons-block')||document.querySelector('product-form-component');if(b){{b.scrollIntoView({{behavior:'smooth',block:'center'}});}}">{g('res_cta')}</button>
      {{%- if nur_klarna -%}}<span class="nur-seo__klarna">{g('res_klarna')}</span>{{%- endif -%}}
      <ul class="nur-seo__assure">
        <li><strong>{g('as1')[0]}</strong>{g('as1')[1]}</li>
        <li><strong>{g('as2')[0]}</strong>{g('as2')[1]}</li>
        <li><strong>{g('as3')[0]}</strong>{g('as3')[1]}</li>
      </ul>
    </div>
  </section>
</div>

<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
"""


HEAD = """{%- liquid
  assign nur_fr = false
  if request.locale.iso_code == 'fr'
    assign nur_fr = true
  endif
  assign nur_root = ''
  if nur_fr
    assign nur_root = '/fr'
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
  Product-page content section, English and French, each with its own copy and
  its own FAQPage JSON-LD. English: the SEO consultant's brief of 2026-11-21 (UAE
  landing page). French: written for France, same structure, delivery adapted.
  Generated by tools/build_seo_en_section.py: the FAQPage JSON-LD and the visible
  FAQ come from the same strings, so they match character for character.
  FAQ answers sit in <details>: still in the DOM, so readable by Google.
{%- endcomment -%}
"""

en = HEAD + "{%- unless nur_fr -%}\n" + CSS + "\n" + body(EN) + "{%- endunless -%}\n"
fr = HEAD + "{%- if nur_fr -%}\n" + CSS + "\n" + body(FR) + "{%- endif -%}\n"
for path, liq in ((OUT_EN, en), (OUT_FR, fr)):
    open(path, 'w').write(liq)
    assert len(liq.encode()) < 40000, (path, len(liq.encode()))
    print('ok', path, len(liq.encode()), 'bytes')
