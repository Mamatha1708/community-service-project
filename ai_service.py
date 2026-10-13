import os
import random
import requests
from config import Config

class AIService:
    """
    AI Assistant for Kalamkari Artisans and Customers.
    Supports Google Gemini Live API when GEMINI_API_KEY is configured in .env,
    and provides a rich, intelligent offline demo fallback when no API key is present.
    """

    MOTIF_MEANINGS = {
        'Tree of Life': {
            'symbolism': 'Universal harmony, connection between earthly roots, heavenly branches, and continuous regeneration of life.',
            'cultural_roots': 'Ancient Indus & Deccan spiritual iconography representing abundance and interconnected nature.',
            'dyes': 'Fermented iron rust (Kasinam) for the detailed trunk and Madder root for foliage highlights.',
            'recommended_room': 'Living room focal wall, study meditation space, or dining hall.'
        },
        'Peacock & Swan': {
            'symbolism': 'Divine grace, beauty, prosperity, and sacred vehicle (Vahana) of Goddess Saraswati.',
            'cultural_roots': 'Temple ceilings and courtly textiles of the Vijayanagara empire.',
            'dyes': 'Indigo extract, pomegranate rind yellow, and alum mordants.',
            'recommended_room': 'Master bedroom, puja room entrance, or festive wardrobe.'
        },
        'Mythological & Epics': {
            'symbolism': 'Narrative episodes from the Ramayana, Mahabharata, and Puranic folklore invoking protection and wisdom.',
            'cultural_roots': 'Srikalahasti temple scroll traditions drawn by traditional kalam pens dipped in milk-treated cloth.',
            'dyes': 'Traditional mineral iron black outlines with natural madder and myrobalan backgrounds.',
            'recommended_room': 'Gallery walls, corporate cultural lounges, and heritage home corridors.'
        },
        'Floral & Paisley': {
            'symbolism': 'Feminine fertility, blossoming springtime, and eternal life (Mankolam / ambi motif).',
            'cultural_roots': 'Machilipatnam coastal trade motifs blending Persian floral delicacy with Andhra block printing.',
            'dyes': 'Natural indigo vat dyeing, kasim black, and boiled chayroot red.',
            'recommended_room': 'Contemporary bedrooms, everyday luxury apparel, and dining table runners.'
        },
        'Lotus & Elephants': {
            'symbolism': 'Purity rising above water, royal strength, wisdom, and auspicious fortune (Gaja Lakshmi motifs).',
            'cultural_roots': 'Dravidian temple architecture and ritual textile canopies.',
            'dyes': 'Alum-mordanted madder red, myrobalan tannin yellow, and tamarind seed paste resist.',
            'recommended_room': 'Entry foyer, meditation nook, or ceremonial gift.'
        }
    }

    STYLE_STORIES = {
        'Srikalahasti Pen Kalamkari': {
            'cluster': 'Srikalahasti, Tirupati District, Andhra Pradesh',
            'gi_status': 'Geographical Indication (GI) Registered Craft',
            'technique': 'Completely freehand hand-drawn with bamboo pens (toda kalam) dipped in kasinam (fermented iron slag and jaggery) on buffalo-milk treated cotton.',
            'water_source': 'Washed in the flowing holy waters of River Swarnamukhi which balances natural mineral mordants.'
        },
        'Machilipatnam Block Kalamkari': {
            'cluster': 'Pedana & Machilipatnam, Krishna District, Andhra Pradesh',
            'gi_status': 'Geographical Indication (GI) Registered Craft',
            'technique': 'Intricate relief hand-carved teakwood blocks pressed sequentially with natural vegetable pastes, followed by indigo vat immersion.',
            'water_source': 'Processed in the mineral-rich waters of the Krishna river delta ensuring brilliant color fastness.'
        },
        'Karuppur Kalamkari': {
            'cluster': 'Tanjavur Delta Heritage',
            'gi_status': 'Heritage Court Textile',
            'technique': 'Combines metallic zari brocade with kalam-applied natural dye outlines and wax resists.',
            'water_source': 'Kaveri river washings yielding deep royal tones.'
        }
    }

    @classmethod
    def is_api_configured(cls):
        return bool(Config.GEMINI_API_KEY and len(Config.GEMINI_API_KEY.strip()) > 10)

    @classmethod
    def generate_product_story(cls, title, style, category, motif, dyes="", custom_notes=""):
        """Generate high-converting artisan storytelling & product description."""
        prompt = (
            f"You are a master Kalamkari art historian and ethical handloom curator. "
            f"Write an authentic, evocative product description for this handcrafted piece:\n"
            f"- Product Title: {title}\n"
            f"- Kalamkari Style: {style}\n"
            f"- Craft Category: {category}\n"
            f"- Central Motif: {motif}\n"
            f"- Natural Dyes: {dyes or 'Traditional vegetable & mineral dyes'}\n"
            f"- Artisan Notes: {custom_notes or 'Handmade with 17-step traditional artisan process'}\n"
            f"Include the cultural symbolism, artisan process, styling tips, and natural dye care guide."
        )

        if cls.is_api_configured():
            api_result = cls._call_gemini_api(prompt)
            if api_result:
                return {
                    'mode': 'live_api',
                    'engine': 'Google Gemini Live AI',
                    'text': api_result
                }

        # Offline Intelligent Fallback
        motif_info = cls.MOTIF_MEANINGS.get(motif, cls.MOTIF_MEANINGS['Tree of Life'])
        style_info = cls.STYLE_STORIES.get(style, cls.STYLE_STORIES['Srikalahasti Pen Kalamkari'])
        dyes_str = dyes if dyes else "Myrobalan (Karakkaya), Natural Indigo, Madder root, and Fermented Iron Jaggery"

        fallback_text = (
            f"### 🌿 Heritage Craft Narrative: {title}\n\n"
            f"Immerse your space in the living history of India with this breathtaking **{title}**, hand-crafted by master artisans in **{style_info['cluster']}**. "
            f"Rooted in the prestigious tradition of **{style}** ({style_info['gi_status']}), every stroke and contour represents days of dedicated handwork.\n\n"
            f"#### ✨ Cultural Motif & Symbolism: *{motif}*\n"
            f"The central focus of this creation celebrates the **{motif}**. In Indian philosophical aesthetics, this motif signifies {motif_info['symbolism']} "
            f"Historically celebrated across {motif_info['cultural_roots']}, this piece brings an aura of timeless dignity and peaceful grounding into any modern home.\n\n"
            f"#### 🎨 Authentic 17-Step Natural Dye Alchemy\n"
            f"True to century-old Kalamkari ethics, no synthetic toxic chemicals touch this fabric. The artisan begins by scouring unbleached organic cotton in buffalo milk and myrobalan nut astringent to prevent dye bleeding. "
            f"The palette features **{dyes_str}**. {style_info['technique']} Finally, the textile undergoes curative washing in {style_info['water_source']}, setting colors that grow richer with age.\n\n"
            f"#### 🏛️ Styling & Occasion Guide\n"
            f"- **Best Suited For:** {motif_info['recommended_room']}, festive heirlooms, and conscientious gift collections.\n"
            f"- **Artisan Signature:** Handcrafted irregularities and subtle brush marks are authentic hallmarks of genuine human craft, ensuring no two pieces are ever identical.\n"
            f"- **Care Instructions:** Gentle dry clean or cold water dip with eco-friendly soap nut (Reetha). Dry in shaded breeze away from harsh direct midday sunlight."
        )

        return {
            'mode': 'demo_fallback',
            'engine': 'Kalamkari Mitra Intelligent Craft Engine (Demo Mode)',
            'text': fallback_text
        }

    @classmethod
    def generate_marketing_captions(cls, title, style, category, price, discount_note=""):
        """Generate high-engagement social media posts with hashtags and hooks."""
        prompt = (
            f"Generate 3 vibrant social media marketing captions (Instagram, Facebook, and WhatsApp Business) "
            f"for a Kalamkari artisan selling:\n"
            f"Title: {title}\n"
            f"Style: {style}\n"
            f"Category: {category}\n"
            f"Price: Rs. {price}\n"
            f"Notes: {discount_note}\n"
            f"Include cultural hashtags, engaging storytelling hooks, and direct artisan support CTAs."
        )

        if cls.is_api_configured():
            api_result = cls._call_gemini_api(prompt)
            if api_result:
                return {
                    'mode': 'live_api',
                    'engine': 'Google Gemini Live AI',
                    'text': api_result
                }

        # Offline Intelligent Fallback
        fallback_text = (
            f"### 📱 Social Media Ready Campaign Pack\n\n"
            f"#### 📸 Option 1: Story-Driven Instagram Post\n"
            f"**Headline:** Wear 3,000 Years of Living Heritage ✨\n\n"
            f"Every single curve on our new **{title}** is drawn with a handmade bamboo pen and bathed in organic vegetable dyes. "
            f"When you choose authentic **{style}**, you aren't just buying a craft — you are keeping an entire artisan village in Andhra Pradesh thriving without middlemen. 🌿\n\n"
            f"🏷️ **Fair Price:** ₹{price} (Direct to Artisan)\n"
            f"📦 **Shipping:** Free eco-friendly packaging across India!\n"
            f"🔗 *Tap the link in bio to support our artisan community through Kalamkari Connect!*\n\n"
            f"#KalamkariConnect #AuthenticKalamkari #Srikalahasti #HandmadeInIndia #VocalForLocal #SlowFashion #EcoFriendlyDyes #IndianHandlooms #DirectArtisanSupport\n\n"
            f"---\n\n"
            f"#### 💬 Option 2: WhatsApp Community / Direct Broadcast\n"
            f"Namaste art lovers! 🙏\n"
            f"New handloom arrival direct from our artisan cluster:\n"
            f"🌿 **Product:** {title}\n"
            f"🎨 **Style:** {style} ({category})\n"
            f"🌱 **Dyes:** 100% Plant & Mineral Dyes (Milk & Myrobalan treated)\n"
            f"💰 **Artisan Fair Wage Price:** ₹{price}\n\n"
            f"Each piece takes over 14 days of dedicated handcrafting. Limited single stock piece available on our college Community Service Project portal: Kalamkari Connect.\n"
            f"Reply *ORDER* or visit our marketplace to reserve yours now! ✨\n\n"
            f"---\n\n"
            f"#### 🌐 Option 3: Facebook / Heritage Collector Group\n"
            f"**Why authentic Kalamkari is becoming one of the most cherished collectibles worldwide:**\n"
            f"Unlike screen prints and digital imitations flooding commercial markets, this **{title}** is prepared using authentic mordant-dye chemistry passed down through four generations. "
            f"Every purchase on Kalamkari Connect channels 100% of fair compensation directly to the craftsperson's family. Support ethical art today. 🕊️"
        )

        return {
            'mode': 'demo_fallback',
            'engine': 'Kalamkari Mitra Intelligent Craft Engine (Demo Mode)',
            'text': fallback_text
        }

    @classmethod
    def recommend_for_buyer(cls, preference_query, available_products=[]):
        """Recommend matching Kalamkari craft items based on buyer's room, occasion, or style."""
        prompt = (
            f"A customer is asking for Kalamkari craft advice: '{preference_query}'. "
            f"Provide insightful recommendations explaining which Kalamkari style (Pen vs Block), "
            f"motif (Tree of Life, Peacock, Lotus, Epics), and color palette best suits their requirement, "
            f"and explain why handloom natural dyes make it special."
        )

        if cls.is_api_configured():
            api_result = cls._call_gemini_api(prompt)
            if api_result:
                return {
                    'mode': 'live_api',
                    'engine': 'Google Gemini Live AI',
                    'text': api_result,
                    'matched_products': []
                }

        # Offline Intelligent Fallback based on keyword matching
        query_lower = preference_query.lower()
        
        # Determine theme
        if any(w in query_lower for w in ['living', 'wall', 'decor', 'room', 'home', 'hanging', 'interior', 'painting']):
            recommended_style = "Srikalahasti Pen Kalamkari"
            recommended_motif = "Tree of Life"
            ideal_category = "Wall Hangings & Scrolls"
            advice = (
                "For wall decor and living spaces, the **Tree of Life** in **Srikalahasti Pen Kalamkari** is the world's most acclaimed motif. "
                "The expansive branches fill empty vertical wall spaces with warmth, while natural kasinam (fermented iron black) and earthy madder red create an organic focal point that harmonizes beautifully with wooden furniture and warm lighting."
            )
        elif any(w in query_lower for w in ['wedding', 'saree', 'bridal', 'silk', 'reception', 'festival', 'temple', 'puja']):
            recommended_style = "Srikalahasti Pen Kalamkari"
            recommended_motif = "Peacock & Swan"
            ideal_category = "Sarees"
            advice = (
                "For weddings, festive gatherings, and sacred occasions, a hand-drawn **Peacock & Swan motif** on pure Tussar or Mangalagiri cotton-silk is supreme. "
                "The peacock symbolizes prosperity, romantic grace, and spiritual elevation, making it the most celebrated motif in South Indian celebration wear."
            )
        elif any(w in query_lower for w in ['office', 'daily', 'casual', 'gift', 'dupatta', 'kurti', 'dress', 'summer']):
            recommended_style = "Machilipatnam Block Kalamkari"
            recommended_motif = "Floral & Paisley"
            ideal_category = "Dupattas & Shawls"
            advice = (
                "For daily elegance, modern workwear, or thoughtful gifting, **Machilipatnam Block Printed Dupattas & Stoles** are lightweight, breathable, and versatile. "
                "The rhythmic block impressions dyed in natural Indigo and madder red pair effortlessly with plain cotton kurtas or linen shirts."
            )
        else:
            recommended_style = "Srikalahasti Pen Kalamkari"
            recommended_motif = "Lotus & Elephants"
            ideal_category = "Home Decor & Furnishing"
            advice = (
                "Based on your query, we recommend a timeless **Lotus & Elephant craft piece**. "
                "Elephants represent auspicious fortitude and strength, while the pristine lotus represents clarity and renewal. It is revered in Vastu and traditional Indian architecture."
            )

        # Filter catalog products if provided
        matched = []
        for p in available_products:
            if p.motif_type == recommended_motif or p.kalamkari_style == recommended_style or p.category == ideal_category:
                matched.append(p)

        fallback_text = (
            f"### 🧭 Kalamkari Heritage Recommendation\n\n"
            f"**Your Query:** \"{preference_query}\"\n\n"
            f"#### 💡 Craft Expert Analysis:\n"
            f"{advice}\n\n"
            f"#### 🎯 Recommended Specifications:\n"
            f"- **Best Technique:** {recommended_style}\n"
            f"- **Recommended Central Motif:** {recommended_motif}\n"
            f"- **Ideal Category:** {ideal_category}\n"
            f"- **Color Palette:** Warm Indigo celestial blues, turmeric/myrobalan yellows, and earthy madder brick red.\n"
            f"- **Artisan Advantage:** Purchasing through Kalamkari Connect guarantees direct fair compensation to rural Andhra craft clusters."
        )

        return {
            'mode': 'demo_fallback',
            'engine': 'Kalamkari Mitra Intelligent Craft Engine (Demo Mode)',
            'text': fallback_text,
            'matched_products': matched[:4]
        }

    @classmethod
    def _call_gemini_api(cls, prompt_text):
        """Helper to invoke Google Gemini REST API safely."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt_text}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text
        except Exception as e:
            # Silently fallback to offline mode if network issue or key error
            return None
        return None
