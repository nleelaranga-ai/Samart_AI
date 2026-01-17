import json
import os

# --- MASTER DATABASE (ALL SCHEMES) ---
master_schemes = [
    # --- 1. GENERAL EDUCATION (SC/ST/BC/Kapu/Minority) ---
    {
        "id": 1,
        "name": "Jagananna Vidya Deevena (RTF)",
        "state": "Andhra Pradesh",
        "category": "All (SC/ST/BC/Kapu)",
        "keywords": ["fee", "reimbursement", "btech", "degree", "sc", "st", "bc"],
        "income_limit": 250000,
        "description": "Full fee reimbursement for ITI, Polytechnic, Degree, B.Tech, MBA, MCA.",
        "link": "https://jnanabhumi.ap.gov.in/"
    },
    {
        "id": 2,
        "name": "Jagananna Vasathi Deevena",
        "state": "Andhra Pradesh",
        "category": "All (SC/ST/BC/Kapu)",
        "keywords": ["hostel", "food", "mess", "boarding"],
        "income_limit": 250000,
        "description": "Financial aid for food & hostel expenses (Rs 10K-20K per year).",
        "link": "https://jnanabhumi.ap.gov.in/"
    },
    {
        "id": 3,
        "name": "Ambedkar Overseas Vidya Nidhi",
        "state": "Andhra Pradesh",
        "category": "SC/ST",
        "keywords": ["abroad", "foreign", "masters", "phd", "sc", "st"],
        "income_limit": 600000,
        "description": "Financial assistance up to Rs 15 Lakhs for SC/ST students studying abroad.",
        "link": "https://jnanabhumi.ap.gov.in/"
    },

    # --- 2. BRAHMIN WELFARE (Bharati) ---
    {
        "id": 101,
        "name": "Bharati Scheme for Education",
        "state": "Andhra Pradesh",
        "category": "Brahmin",
        "keywords": ["degree", "pg", "professional", "brahmin"],
        "income_limit": 300000, 
        "description": "Financial assistance for Brahmin students in Graduation, PG, and Professional courses.",
        "link": "https://apadapter.ap.gov.in/"
    },
    {
        "id": 106,
        "name": "Veda Vyasa Scheme",
        "state": "Andhra Pradesh",
        "category": "Brahmin",
        "keywords": ["veda", "vedic", "archaka"],
        "income_limit": 300000,
        "description": "Financial assistance for Vedic Education students.",
        "link": "https://apadapter.ap.gov.in/"
    },

    # --- 3. WORKERS & DISABLED ---
    {
        "id": 201,
        "name": "Scholarships for Children of BOC Workers",
        "state": "Andhra Pradesh",
        "category": "Construction Workers",
        "keywords": ["labour", "worker", "construction", "mason"],
        "income_limit": 300000,
        "description": "Scholarships for children of registered construction workers.",
        "link": "https://labour.ap.gov.in/"
    },
    {
        "id": 301,
        "name": "Sanction of Laptops",
        "state": "Andhra Pradesh",
        "category": "Differently Abled",
        "keywords": ["laptop", "visually challenged", "disabled"],
        "income_limit": 300000,
        "description": "Free laptops for visually/hearing impaired professional students.",
        "link": "https://apte.ap.gov.in/"
    }
]

# --- SAVE TO FILE ---
file_path = os.path.join(os.getcwd(), 'scholarships.json')
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(master_schemes, f, indent=4)
print(f"✅ MASTER DATABASE CREATED: {len(master_schemes)} Schemes Saved.")
