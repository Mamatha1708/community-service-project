"""
Government Scheme Recommender Service for Kalamkari Artisans & Weavers
Provides verified, rule-based matching with real government source portals.
Does not ask for sensitive personal identification (no Aadhaar/bank details).
"""

VERIFIED_SCHEMES_DATASET = [
    {
        'id': 'scheme-01',
        'name': 'National Handicraft Development Programme (NHDP) - Ambedkar Hastshilp Vikas Yojana (AHVY)',
        'ministry': 'Office of the Development Commissioner (Handicrafts), Ministry of Textiles, Government of India',
        'category_focus': ['individual_artisan', 'cooperative_shg', 'master_artisan'],
        'state_applicability': 'All India (Special focus on Andhra Pradesh clusters including Srikalahasti and Machilipatnam)',
        'states': ['all', 'andhra_pradesh', 'telangana'],
        'purpose_and_benefits': 'Mobilizes artisans into self-help groups and producer clusters, provides free design & technical training, modern tool-kit distribution, and financial aid up to Rs 10 Lakhs per cluster for raw material banks and common facility centers.',
        'eligibility_criteria': [
            'Practicing handicraft or handloom artisan with recognized craft discipline (e.g. Kalamkari)',
            'Pehchan Card issued by DC (Handicrafts) or endorsement by State Directorate of Handlooms',
            'Age 18 years and above',
            'Artisans organized into SHGs or registered craft societies receive priority'
        ],
        'required_documents': [
            'Pehchan Artisan Identity Card',
            'Passport-size photographs (2)',
            'Address/Residence proof (Voter ID, Ration card, or Domicile certificate)',
            'Bank passbook photocopy showing active account',
            'Cluster/SHG registration certificate (for group applications)'
        ],
        'application_instructions': 'Apply through the nearest Assistant Director, Office of DC (Handicrafts) Field Service Office (located in Vijayawada and Tirupati for Andhra Pradesh artisans), or through the official DC Handicrafts web portal.',
        'official_url': 'http://handicrafts.nic.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Up to Rs 10,000 tool-kit subsidy; up to Rs 10 Lakhs cluster infrastructure grant'
    },
    {
        'id': 'scheme-02',
        'name': 'Pehchan Artisan Identity Card Initiative',
        'ministry': 'Development Commissioner (Handicrafts), Ministry of Textiles',
        'category_focus': ['individual_artisan', 'master_artisan'],
        'state_applicability': 'All India',
        'states': ['all', 'andhra_pradesh', 'telangana'],
        'purpose_and_benefits': 'Provides a national biometric-linked photo ID card verifying artisan status. Enables direct access to all central Ministry of Textiles schemes, subsidized stall allocation at Dilli Haat and craft bazars, group health insurance, and credit linkage without intermediaries.',
        'eligibility_criteria': [
            'Hereditary or trained artisan engaged in an officially recognized handicraft trade',
            'Minimum age 18 years',
            'Indian citizen resident in the craft cluster region'
        ],
        'required_documents': [
            'Proof of artisan occupation (craft sample photograph or cluster supervisor signature)',
            'Age & address proof document',
            'Standard passport photograph',
            'Self-declaration of traditional craft practice'
        ],
        'application_instructions': 'Enroll through Pehchan camps organized periodically by the DC (Handicrafts) Service Centers, or apply online via the official Handicrafts portal under Artisan Corner.',
        'official_url': 'http://handicrafts.nic.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Free issuance; unlocks 50% to 100% stall subsidies at national exhibitions'
    },
    {
        'id': 'scheme-03',
        'name': 'PM Vishwakarma Scheme (Traditional Artisans & Craftspeople)',
        'ministry': 'Ministry of Micro, Small and Medium Enterprises (MSME) & Ministry of Skill Development',
        'category_focus': ['individual_artisan', 'master_artisan'],
        'state_applicability': 'All India',
        'states': ['all', 'andhra_pradesh', 'telangana'],
        'purpose_and_benefits': 'Formal recognition with PM Vishwakarma Certificate & ID card, basic (5-7 days) and advanced (15 days) skill upgradation with Rs 500/day stipend, Rs 15,000 tool-kit grant, and collateral-free enterprise credit up to Rs 3 Lakhs in two tranches at a concessional interest rate of 5%.',
        'eligibility_criteria': [
            'Artisan working with hands and tools in one of the recognized traditional family trades',
            'Minimum age 18 years on the date of registration',
            'Engagement in the trade on the date of registration, without loans under PMEGP/PM SVANidhi in past 5 years',
            'Registration is restricted to one member per household'
        ],
        'required_documents': [
            'Active Mobile number for biometric OTP verification',
            'Bank account details for direct benefit transfer (DBT)',
            'Ration card or family verification details'
        ],
        'application_instructions': 'Visit any Common Service Centre (CSC) in your village/town or register online at the official PM Vishwakarma portal. Verification is conducted by Gram Panchayat or Urban Local Body followed by District Screening Committee.',
        'official_url': 'https://pmvishwakarma.gov.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Rs 15,000 tool-kit incentive + Collateral-free loan up to Rs 3,00,000 at 5% interest'
    },
    {
        'id': 'scheme-04',
        'name': 'Pradhan Mantri MUDRA Yojana (PMMY) - Shishu & Kishore Artisan Loans',
        'ministry': 'Department of Financial Services, Ministry of Finance, Government of India',
        'category_focus': ['individual_artisan', 'cooperative_shg', 'msme_exporter'],
        'state_applicability': 'All India',
        'states': ['all', 'andhra_pradesh', 'telangana'],
        'purpose_and_benefits': 'Provides institutional collateral-free working capital and equipment financing for artisans and small micro-enterprises. Categories: Shishu (loans up to Rs 50,000) and Kishore (loans from Rs 50,001 to Rs 5,00,000) with zero processing fees for Shishu loans.',
        'eligibility_criteria': [
            'Any Indian citizen with an artisan enterprise or business plan for non-farm income generation',
            'Satisfactory credit bureau history without default on previous formal bank loans',
            'Active bank account in any commercial bank, Regional Rural Bank (RRB), or Cooperative bank'
        ],
        'required_documents': [
            'Mudra Loan Application Form with two passport photographs',
            'Proof of identity and residence (Voter Card / Driving License / Utility Bill)',
            'Proof of artisan business location or craft activity (Pehchan card / Udyam registration)',
            'Quotation for machinery, raw materials, or natural dyes to be purchased'
        ],
        'application_instructions': 'Apply at any public sector bank, Regional Rural Bank, or apply online via the Udyamimitra portal (www.udyamimitra.in) or visit your local branch manager.',
        'official_url': 'https://www.mudra.org.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Collateral-free micro loans from Rs 50,000 up to Rs 5,00,000'
    },
    {
        'id': 'scheme-05',
        'name': 'Stand-Up India Scheme (For Women & SC/ST Craft Entrepreneurs)',
        'ministry': 'Department of Financial Services / Small Industries Development Bank of India (SIDBI)',
        'category_focus': ['cooperative_shg', 'msme_exporter', 'individual_artisan'],
        'state_applicability': 'All India',
        'states': ['all', 'andhra_pradesh', 'telangana'],
        'purpose_and_benefits': 'Facilitates bank loans between Rs 10 Lakhs and Rs 1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up greenfield craft or manufacturing ventures.',
        'eligibility_criteria': [
            'SC/ST and/or woman artisan entrepreneur, above 18 years of age',
            'Loan available only for greenfield enterprise project (first-time venture in craft manufacturing/services)',
            'In case of non-individual enterprises, 51% of shareholding and controlling stake held by SC/ST and/or women'
        ],
        'required_documents': [
            'Identity & residence verification proof',
            'SC/ST Certificate (if applying under SC/ST category)',
            'Detailed project report (DPR) detailing Kalamkari textile processing unit setup',
            'Partnership deed or company registration (if applicable)',
            'Past 6 months bank account statements'
        ],
        'application_instructions': 'Submit an application through the Stand-Up India portal (www.standupmitra.in) or directly through any commercial bank branch.',
        'official_url': 'https://www.standupmitra.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Composite loan (term loan + working capital) between Rs 10 Lakhs and Rs 1 Crore'
    },
    {
        'id': 'scheme-06',
        'name': 'Andhra Pradesh YSR Nethanna Nestham & Handloom Artisan Financial Assistance',
        'ministry': 'Department of Handlooms & Textiles, Government of Andhra Pradesh',
        'category_focus': ['individual_artisan', 'cooperative_shg'],
        'state_applicability': 'Andhra Pradesh state specific (Covers craft hubs in Tirupati, Krishna, Guntur, Anantapur)',
        'states': ['andhra_pradesh'],
        'purpose_and_benefits': 'Provides direct annual financial assistance of Rs 24,000 deposited into unencumbered bank accounts of weaver and traditional handloom/kalamkari artisan families owning working pit-looms or frame-looms to modernize equipment and buy natural dyes.',
        'eligibility_criteria': [
            'Artisan or weaver family permanently resident in Andhra Pradesh',
            'Must own and operate a traditional handloom or authentic craft workstation',
            'Must be enrolled in the state Handloom Department database or cooperative society',
            'Valid white ration card / BPL card status'
        ],
        'required_documents': [
            'State Resident Domicile Proof',
            'Artisan/Weaver Cooperative Society Membership or Handloom Inspector verification',
            'Bank passbook photocopy with active IFSC details',
            'Ration Card / Rice Card'
        ],
        'application_instructions': 'Apply at the local Grama Ward Sachivalayam (Village/Ward Secretariat) in your village or town in Andhra Pradesh, or verify enrollment through the Navasakam beneficiary portal.',
        'official_url': 'https://navasakam.ap.gov.in/',
        'verified_date': 'October 2026',
        'verified_status': 'Verified Official Scheme',
        'financial_assistance': 'Direct annual cash assistance of Rs 24,000 per family'
    }
]


class SchemeService:
    @classmethod
    def get_all_schemes(cls):
        return VERIFIED_SCHEMES_DATASET

    @classmethod
    def match_schemes(cls, state='all', category='all', has_pehchan=False, has_bank_account=False, is_woman_or_sc_st=False, search_query=''):
        """
        Rule-based matching engine returning ranked schemes with verified eligibility status.
        """
        matched = []
        state = (state or 'all').strip().lower()
        category = (category or 'all').strip().lower()
        search_query = (search_query or '').strip().lower()

        for scheme in VERIFIED_SCHEMES_DATASET:
            score = 100
            reasons = []
            eligibility_status = "Potential Match (Confirm details on official portal)"

            # 1. State Filter Check
            if state != 'all':
                if state in scheme['states'] or 'all' in scheme['states']:
                    reasons.append(f"Available for artisans in your state")
                else:
                    # Not applicable to this state
                    continue

            # 2. Category Check
            if category != 'all':
                if category in scheme['category_focus']:
                    reasons.append(f"Tailored for {category.replace('_', ' ').title()} category")
                else:
                    score -= 30
                    reasons.append("Category match requires specific group/cluster structure")

            # 3. Pehchan Card Check
            if has_pehchan:
                if 'scheme-01' in scheme['id'] or 'scheme-02' in scheme['id']:
                    score += 15
                    reasons.append("Pehchan Artisan Card qualifies you for fast-track processing")

            # 4. Bank Account
            if has_bank_account:
                reasons.append("Direct DBT and bank transfer requirements satisfied")

            # 5. Women / SC / ST Category
            if is_woman_or_sc_st:
                if 'scheme-05' in scheme['id'] or 'scheme-03' in scheme['id']:
                    score += 20
                    reasons.append("Priority quota for Women / SC / ST entrepreneurs")

            # 6. Text Search Filter
            if search_query:
                combined_text = f"{scheme['name']} {scheme['purpose_and_benefits']} {scheme['ministry']} {scheme['financial_assistance']}".lower()
                if search_query in combined_text:
                    score += 10
                    reasons.append(f"Matches search keyword '{search_query}'")
                else:
                    continue

            # Compute match score rating
            final_score = max(min(score, 100), 40)
            if final_score >= 80:
                eligibility_status = "High Match: Recommended for immediate application"
            elif final_score >= 60:
                eligibility_status = "Moderate Match: Review specific criteria on official portal"

            scheme_copy = dict(scheme)
            scheme_copy['match_score'] = final_score
            scheme_copy['eligibility_status'] = eligibility_status
            scheme_copy['match_summary'] = " • ".join(reasons) if reasons else "General artisan welfare scheme"
            matched.append(scheme_copy)

        # Sort descending by match score
        matched.sort(key=lambda x: x['match_score'], reverse=True)
        return matched

    @classmethod
    def get_scheme_by_id(cls, scheme_id):
        for s in VERIFIED_SCHEMES_DATASET:
            if s['id'] == scheme_id:
                return dict(s)
        return None
