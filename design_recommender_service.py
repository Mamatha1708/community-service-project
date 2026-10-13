"""
Trending Kalamkari Design Recommender Service
Lightweight rule-based recommendation engine for authentic Srikalahasti
and Machilipatnam Kalamkari design inspirations with filter-ranked matching.
"""

# Curated Authentic Kalamkari Design Inspiration Dataset
DESIGN_DATASET = [
    {
        'id': 'des-01',
        'title': 'Celestial Mayura (Peacock) Border Handloom',
        'product_type': 'saree',
        'motif': 'peacock',
        'color': 'indigo_blue',
        'color_palette': 'Indigo Blue, Madder Red & Warm Ochre',
        'style': 'traditional',
        'kalamkari_school': 'Srikalahasti Pen Kalamkari',
        'description': 'Hand-drawn royal peacock motifs dancing along the saree pallu with intricate plumage detailed using fine bamboo pens and natural indigo dye.',
        'difficulty': 'Master Craft (14 days)',
        'dyes_used': 'Indigofera tinctoria, Alum, Madder root',
        'image': '/static/images/samples/peacock_saree.svg'
    },
    {
        'id': 'des-02',
        'title': 'Vriksha: Sacred Tree of Life Wall Tapestry',
        'product_type': 'home_decor',
        'motif': 'nature',
        'color': 'earthy_black',
        'color_palette': 'Fermented Iron Black (Kasinam), Terracotta & Mustard',
        'style': 'traditional',
        'kalamkari_school': 'Srikalahasti Pen Kalamkari',
        'description': 'Ancient cosmic Tree of Life motif showing deep roots and blossoming branches harboring deer, peacocks, and singing koels, drawn with charcoal outlines and vegetable dyes.',
        'difficulty': 'Heritage Epic (21 days)',
        'dyes_used': 'Fermented jaggery iron rust, Myrobalan fruit wash',
        'image': '/static/images/samples/tree_of_life.svg'
    },
    {
        'id': 'des-03',
        'title': 'Nandi Floral Vine Chanderi Dupatta',
        'product_type': 'dupatta',
        'motif': 'floral',
        'color': 'terracotta_red',
        'color_palette': 'Terracotta Red, Pale Cream & Pomegranate Yellow',
        'style': 'traditional',
        'kalamkari_school': 'Machilipatnam Block Kalamkari',
        'description': 'Hand-carved teakwood blocks stamping interlocking lotus blooms and meandering jasmine vines across a feather-light natural tussar silk dupatta.',
        'difficulty': 'Moderate (5 days)',
        'dyes_used': 'Madder bark, Alum mordant, Pomegranate rind',
        'image': '/static/images/samples/paisley_dupatta.svg'
    },
    {
        'id': 'des-04',
        'title': 'Contemporary Minimalist Geometrics Runner',
        'product_type': 'home_decor',
        'motif': 'geometric',
        'color': 'sage_green',
        'color_palette': 'Earthy Sage Green, Indigo & Warm Ivory',
        'style': 'contemporary',
        'kalamkari_school': 'Machilipatnam Block Kalamkari',
        'description': 'Modernized step-and-diamond block patterns combining centuries-old vegetable dye formulas with sleek, Scandinavian-friendly minimalist dining and living aesthetics.',
        'difficulty': 'Accessible (4 days)',
        'dyes_used': 'Copper sulphate natural fixative, Indigo + Pomegranate rind yellow for green',
        'image': '/static/images/samples/elephant_runner.svg'
    },
    {
        'id': 'des-05',
        'title': 'Hamsa (Swan) & Lotus Kurti Dress Material',
        'product_type': 'dress_material',
        'motif': 'birds',
        'color': 'mustard_yellow',
        'color_palette': 'Haldi Mustard Yellow, Madder Red & Charcoal',
        'style': 'traditional',
        'kalamkari_school': 'Pedana Hand Block',
        'description': 'Pairs of sacred Hamsa swans gliding amid sacred blue lotuses, perfect for festive unstitched kurtis and Anarkali suits with breathable pure mangalagiri cotton.',
        'difficulty': 'Moderate (6 days)',
        'dyes_used': 'Turmeric, Harda (Myrobalan), Alum',
        'image': '/static/images/samples/indigo_fabric.svg'
    },
    {
        'id': 'des-06',
        'title': 'Ramayana Epic Narrative Temple Hanging',
        'product_type': 'home_decor',
        'motif': 'mythology',
        'color': 'terracotta_red',
        'color_palette': 'Terracotta Red, Kasinam Black & Cream',
        'style': 'traditional',
        'kalamkari_school': 'Srikalahasti Temple Scroll',
        'description': 'Narrative panels depicting mythological scenes from the Sundara Kanda, with traditional Telugu script captions explaining the holy episodes.',
        'difficulty': 'Master Craft (30 days)',
        'dyes_used': 'Buffalo milk wash, Myrobalan, Madder, Iron acetate',
        'image': '/static/images/samples/ramayana_scroll.svg'
    },
    {
        'id': 'des-07',
        'title': 'Urban Fusion Botanical Cape & Stole',
        'product_type': 'other',
        'motif': 'floral',
        'color': 'cream',
        'color_palette': 'Cream, Soft Muted Indigo & Earthy Tan',
        'style': 'contemporary',
        'kalamkari_school': 'Contemporary Kalamkari Studio',
        'description': 'Contemporary asymmetrical placement prints featuring oversized hibiscus and wild forest foliage designed for modern fusion wear, scarves, and trench accents.',
        'difficulty': 'Innovative (7 days)',
        'dyes_used': 'Natural tannin extracts, Indigo reduction vat',
        'image': '/static/images/samples/paisley_dupatta.svg'
    },
    {
        'id': 'des-08',
        'title': 'Vibrant Peacock & Paisley Festive Saree',
        'product_type': 'saree',
        'motif': 'peacock',
        'color': 'terracotta_red',
        'color_palette': 'Madder Terracotta, Indigo Blue & Antique Gold',
        'style': 'traditional',
        'kalamkari_school': 'Srikalahasti Pen Kalamkari',
        'description': 'Intricately drawn double-headed peacock buttas with sweeping paisley swirls along the borders, washed in the currents of the sacred Swarnamukhi river.',
        'difficulty': 'Master Craft (18 days)',
        'dyes_used': 'Indigo, Madder, Alum, Fermented iron',
        'image': '/static/images/samples/peacock_saree.svg'
    },
    {
        'id': 'des-09',
        'title': 'Contemporary Forest Fauna Linen Yardage',
        'product_type': 'dress_material',
        'motif': 'nature',
        'color': 'sage_green',
        'color_palette': 'Forest Sage Green, Natural Ecru & Bark Brown',
        'style': 'contemporary',
        'kalamkari_school': 'Contemporary Eco-Print',
        'description': 'Subtle dancing deer and tree bough block prints tailored for tailored jackets, men’s kurtas, and contemporary resort-wear garments.',
        'difficulty': 'Moderate (5 days)',
        'dyes_used': 'Babul bark, Pomegranate, Indigo',
        'image': '/static/images/samples/elephant_runner.svg'
    },
    {
        'id': 'des-10',
        'title': 'Gajraj Royal Elephant Table Runner & Cushions',
        'product_type': 'home_decor',
        'motif': 'nature',
        'color': 'mustard_yellow',
        'color_palette': 'Mustard Yellow, Terracotta & Ink Black',
        'style': 'traditional',
        'kalamkari_school': 'Machilipatnam Block Kalamkari',
        'description': 'Procession of caparisoned temple elephants bearing lotus blossoms, framed by traditional temple gopuram borders.',
        'difficulty': 'Moderate (5 days)',
        'dyes_used': 'Harda, Alum, Madder, Iron jaggery',
        'image': '/static/images/samples/elephant_runner.svg'
    },
    {
        'id': 'des-11',
        'title': 'Contemporary Geometric Mandala Silk Scarf',
        'product_type': 'dupatta',
        'motif': 'geometric',
        'color': 'indigo_blue',
        'color_palette': 'Deep Indigo Blue & Natural Raw Silk Ivory',
        'style': 'contemporary',
        'kalamkari_school': 'Contemporary Kalamkari Studio',
        'description': 'Concentric diamond mandalas rendered with modern negative space layouts, creating a versatile accessory for formal Western and ethnic styling.',
        'difficulty': 'Moderate (6 days)',
        'dyes_used': 'Pure indigo dye vats with tamarind seed paste resist',
        'image': '/static/images/samples/indigo_fabric.svg'
    },
    {
        'id': 'des-12',
        'title': 'Kamalam (Lotus) Garden Daily Wear Saree',
        'product_type': 'saree',
        'motif': 'floral',
        'color': 'cream',
        'color_palette': 'Cream, Soft Coral Pink & Sage Green',
        'style': 'contemporary',
        'kalamkari_school': 'Pedana Block Handloom',
        'description': 'Lightweight daily wear cotton saree sprinkled with delicate hand-blocked blooming lotus buds and subtle wave borders.',
        'difficulty': 'Accessible (5 days)',
        'dyes_used': 'Madder extract, Turmeric, Alum',
        'image': '/static/images/samples/paisley_dupatta.svg'
    }
]


class DesignRecommenderService:
    @classmethod
    def get_all_designs(cls):
        return DESIGN_DATASET

    @classmethod
    def recommend_designs(cls, product_type=None, motif=None, preferred_color=None, style=None):
        """
        Ranks design ideas based on exact and partial matches with user criteria.
        Returns a list of designs with computed match scores and match reasons.
        """
        results = []

        # Normalize filter inputs
        product_type = (product_type or '').strip().lower()
        motif = (motif or '').strip().lower()
        preferred_color = (preferred_color or '').strip().lower()
        style = (style or '').strip().lower()

        for item in DESIGN_DATASET:
            score = 0
            match_reasons = []

            # 1. Product Type Match (Weight: 35 points)
            if product_type and product_type != 'all':
                if item['product_type'] == product_type:
                    score += 35
                    match_reasons.append(f"Crafted specifically for {item['product_type'].replace('_', ' ').title()}")
                elif product_type in ['saree', 'dupatta'] and item['product_type'] in ['saree', 'dupatta']:
                    score += 15
                    match_reasons.append(f"Adaptable handloom drape format")

            # 2. Motif Match (Weight: 30 points)
            if motif and motif != 'all':
                if item['motif'] == motif:
                    score += 30
                    match_reasons.append(f"Features signature {item['motif'].title()} iconography")
                elif motif in ['peacock', 'birds'] and item['motif'] in ['peacock', 'birds']:
                    score += 20
                    match_reasons.append("Avian heritage motif harmony")
                elif motif in ['floral', 'nature'] and item['motif'] in ['floral', 'nature']:
                    score += 18
                    match_reasons.append("Botanical organic motif harmony")

            # 3. Preferred Color Match (Weight: 20 points)
            if preferred_color and preferred_color != 'all':
                if item['color'] == preferred_color:
                    score += 20
                    match_reasons.append(f"Rooted in authentic {preferred_color.replace('_', ' ').title()} natural dye palette")
                elif preferred_color in item['color_palette'].lower():
                    score += 12
                    match_reasons.append("Palette includes chosen shade")

            # 4. Style Match (Weight: 15 points)
            if style and style != 'all':
                if item['style'] == style:
                    score += 15
                    match_reasons.append(f"True to {item['style'].title()} Kalamkari aesthetics")

            # Baseline score so every design has context even when no filters are set
            if not any([product_type, motif, preferred_color, style]) or all([
                x in ['', 'all'] for x in [product_type, motif, preferred_color, style]
            ]):
                match_reasons.append("Curated traditional craft suggestion based on seasonal artisan demand")
                score = 50

            # If some filters were selected but no specific match reason was found
            if not match_reasons:
                match_reasons.append("Heritage handloom inspiration sharing complementary vegetable dye techniques")

            design_copy = dict(item)
            design_copy['match_score'] = min(score, 100)
            design_copy['match_reason'] = " • ".join(match_reasons)
            results.append(design_copy)

        # Sort descending by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results

    @classmethod
    def get_design_by_id(cls, design_id):
        for item in DESIGN_DATASET:
            if item['id'] == design_id:
                return dict(item)
        return None
