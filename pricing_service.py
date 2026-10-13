"""
Smart Pricing Assistant Service for Kalamkari Artisans
Calculates fair, cost-based selling prices based on raw materials, natural dyes,
artisan labour, packaging, transport, and profit margins.
"""

class PricingService:
    MIN_PROFIT_MARGIN = 0.0
    MAX_PROFIT_MARGIN = 300.0
    DEFAULT_PROFIT_MARGIN = 25.0
    MIN_QUANTITY = 1
    MAX_QUANTITY = 10000

    @classmethod
    def validate_inputs(cls, data):
        """
        Validates raw user inputs. Returns (is_valid, cleaned_data, error_messages).
        """
        errors = []
        cleaned = {}

        # 1. Product Name
        product_name = str(data.get('product_name', '')).strip()
        if not product_name:
            errors.append("Product name is required.")
        elif len(product_name) > 150:
            errors.append("Product name must be under 150 characters.")
        cleaned['product_name'] = product_name or "Handcrafted Kalamkari Item"

        # 2. Numeric Cost Fields (must be non-negative numbers)
        cost_fields = [
            ('material_cost', 'Material cost (fabric, cloth)'),
            ('dye_cost', 'Natural dye & colour cost'),
            ('labour_cost', 'Artisan labour cost'),
            ('packaging_cost', 'Packaging cost'),
            ('transport_cost', 'Transport & other expenses')
        ]

        for field_key, field_label in cost_fields:
            val_raw = data.get(field_key, 0)
            try:
                val = float(val_raw)
                if val < 0:
                    errors.append(f"{field_label} cannot be negative.")
                elif val > 1000000:
                    errors.append(f"{field_label} cannot exceed Rs 10,00,000.")
                cleaned[field_key] = round(val, 2)
            except (ValueError, TypeError):
                errors.append(f"{field_label} must be a valid numeric amount.")
                cleaned[field_key] = 0.0

        # 3. Profit Margin (0% to 300%)
        margin_raw = data.get('profit_margin', cls.DEFAULT_PROFIT_MARGIN)
        try:
            margin = float(margin_raw)
            if margin < cls.MIN_PROFIT_MARGIN:
                errors.append(f"Profit margin cannot be less than {cls.MIN_PROFIT_MARGIN}%.")
            elif margin > cls.MAX_PROFIT_MARGIN:
                errors.append(f"Profit margin cannot exceed {cls.MAX_PROFIT_MARGIN}%.")
            cleaned['profit_margin'] = round(margin, 2)
        except (ValueError, TypeError):
            errors.append(f"Profit margin must be a valid percentage between {cls.MIN_PROFIT_MARGIN}% and {cls.MAX_PROFIT_MARGIN}%.")
            cleaned['profit_margin'] = cls.DEFAULT_PROFIT_MARGIN

        # 4. Quantity (must be positive integer >= 1)
        qty_raw = data.get('quantity', 1)
        try:
            qty = int(qty_raw)
            if qty < cls.MIN_QUANTITY:
                errors.append(f"Quantity must be at least {cls.MIN_QUANTITY}.")
            elif qty > cls.MAX_QUANTITY:
                errors.append(f"Quantity cannot exceed {cls.MAX_QUANTITY}.")
            cleaned['quantity'] = qty
        except (ValueError, TypeError):
            errors.append("Quantity must be a whole positive number.")
            cleaned['quantity'] = 1

        is_valid = len(errors) == 0
        return is_valid, cleaned, errors

    @classmethod
    def calculate_pricing(cls, cleaned_data, custom_price_override=None):
        """
        Executes the verified pricing calculations.
        """
        material = cleaned_data['material_cost']
        dye = cleaned_data['dye_cost']
        labour = cleaned_data['labour_cost']
        packaging = cleaned_data['packaging_cost']
        transport = cleaned_data['transport_cost']
        margin = cleaned_data['profit_margin']
        quantity = cleaned_data['quantity']

        # Total Cost Per Item = Material + Dye + Labour + Packaging + Transport
        cost_per_item = material + dye + labour + packaging + transport

        # Profit Per Item = Total Cost Per Item * (Profit Margin / 100)
        profit_per_item = cost_per_item * (margin / 100.0)

        # Suggested Selling Price Per Item = Total Cost Per Item + Profit Per Item
        suggested_price = cost_per_item + profit_per_item

        # Allow user custom price override if provided and valid
        is_custom_price = False
        effective_price = suggested_price
        if custom_price_override is not None:
            try:
                override_val = float(custom_price_override)
                if override_val >= 0:
                    effective_price = override_val
                    is_custom_price = True
            except (ValueError, TypeError):
                pass

        # Total Suggested Price = Selling Price * Quantity
        total_price = effective_price * quantity
        total_cost = cost_per_item * quantity
        total_profit = (effective_price - cost_per_item) * quantity

        # Cost Breakdown Percentages
        breakdown = {
            'material': {
                'amount': material,
                'pct': round((material / cost_per_item * 100), 1) if cost_per_item > 0 else 0
            },
            'dye': {
                'amount': dye,
                'pct': round((dye / cost_per_item * 100), 1) if cost_per_item > 0 else 0
            },
            'labour': {
                'amount': labour,
                'pct': round((labour / cost_per_item * 100), 1) if cost_per_item > 0 else 0
            },
            'packaging': {
                'amount': packaging,
                'pct': round((packaging / cost_per_item * 100), 1) if cost_per_item > 0 else 0
            },
            'transport': {
                'amount': transport,
                'pct': round((transport / cost_per_item * 100), 1) if cost_per_item > 0 else 0
            }
        }

        # Effective profit percentage if price was overridden
        effective_margin = margin
        if cost_per_item > 0:
            effective_margin = round(((effective_price - cost_per_item) / cost_per_item) * 100.0, 2)

        return {
            'product_name': cleaned_data['product_name'],
            'material_cost': material,
            'dye_cost': dye,
            'labour_cost': labour,
            'packaging_cost': packaging,
            'transport_cost': transport,
            'profit_margin': margin,
            'effective_margin': effective_margin,
            'quantity': quantity,
            'cost_per_item': round(cost_per_item, 2),
            'profit_per_item': round(profit_per_item, 2),
            'suggested_price': round(suggested_price, 2),
            'effective_price': round(effective_price, 2),
            'is_custom_price': is_custom_price,
            'total_cost': round(total_cost, 2),
            'total_profit': round(total_profit, 2),
            'total_price': round(total_price, 2),
            'breakdown': breakdown,
            'disclaimer': 'Cost-based artisan estimate. Market conditions, complexity of freehand kalam work, and GI certification may permit higher valuation.'
        }
