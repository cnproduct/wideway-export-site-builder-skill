#!/usr/bin/env python3
"""
================================================================================
🚀 B2B EXPORT STANDALONE SITE & MASTER CMS SCAFFOLDER (2026 EDITION)
================================================================================
Empowers rapid generation of enterprise-grade B2B export portals with:
  * Full 20+ responsive pages (Home, Products, Detail, OEM/ODM, QC, Audits, etc.)
  * Shopify-style master product catalog editor & visual in-place CMS
  * 4K/1080p video showcase (<=50MB) + multi-angle gallery with z-index 20000 vault
  * AI-Ready SEO/GEO matrix (Sitemap with image-extension, robots.txt, llms.txt)
  * Dynamic category compilation & specification comparison tables
  * Inquiries CRM + FormSubmit & SMTP notification relay
  * Production deployment sync daemon (SSH/Nginx/systemd)

Usage:
  python3 scaffold_new_site.py --config config.example.json --out-dir ../my-new-b2b-site
  python3 scaffold_new_site.py --name-en "Tianya Stone Co., Ltd." --brand "TIANYA STONE" --domain "tianyastone.com" --out-dir ./tianya_site
  python3 scaffold_new_site.py --interactive
================================================================================
"""

import os
import sys
import json
import re
import datetime
import shutil
import argparse
import hashlib
import uuid
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")

# Industry category presets
INDUSTRY_PRESETS = {
    "footwear": {
        "primary_keyword": "Footwear Manufacturer China",
        "secondary_keywords": [
            "China sports shoes factory",
            "OEM sneaker manufacturer",
            "casual shoes wholesale supplier",
            "running shoes OEM ODM",
            "private label footwear factory",
            "low MOQ custom sneakers",
            "slides and sandals manufacturer"
        ],
        "categories": {
            "sport-outdoor-shoes": {
                "title": "Sport & Outdoor Shoes Wholesale Manufacturer",
                "desc": "Source professional athletic footwear, trail running shoes, and outdoor sneakers directly from verified factory. High-elastic cushioning, breathable mesh, and low MOQ OEM/ODM.",
                "h1": "Sport & Outdoor Shoes Manufacturing",
                "url": "sport-outdoor-shoes-wholesale.html",
                "spec_headers": ["Model Code", "Upper Material", "Outsole / Midsole", "Lining / Insole", "Size Range", "MOQ (Pairs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            },
            "casual-shoes": {
                "title": "OEM Casual Shoes Factory & Sourcing",
                "desc": "Custom private label casual shoes and lifestyle sneakers crafted with premium microfibers, lightweight EVA outsoles, and ergonomic fits for international fashion brands.",
                "h1": "Custom OEM Casual Shoes Wholesale",
                "url": "casual-shoes-oem-manufacturer.html",
                "spec_headers": ["Model Code", "Upper Material", "Outsole / Midsole", "Lining / Insole", "Size Range", "MOQ (Pairs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            },
            "mens-sneakers": {
                "title": "Men's Sneakers Bulk Supplier & Custom Factory",
                "desc": "High-volume OEM manufacturing for men's athletic trainers, chunky dad shoes, and street sneakers with custom branding, colorways, and SATRA physical testing.",
                "h1": "Men's Sneakers Wholesale & Custom Production",
                "url": "mens-sneakers-bulk-supplier.html",
                "spec_headers": ["Model Code", "Upper Material", "Outsole / Midsole", "Lining / Insole", "Size Range", "MOQ (Pairs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            },
            "womens-sneakers": {
                "title": "Women's Sneakers OEM Factory & Direct Supplier",
                "desc": "Specialized women's athletic shoes, fashion platform sneakers, and walking shoes featuring lightweight EVA midsoles and ergonomic arch support.",
                "h1": "Women's Sneakers Manufacturing & Bulk Supply",
                "url": "womens-sneakers-oem-factory.html",
                "spec_headers": ["Model Code", "Upper Material", "Outsole / Midsole", "Lining / Insole", "Size Range", "MOQ (Pairs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            }
        }
    },
    "sportswear": {
        "primary_keyword": "Custom Sportswear Manufacturer China",
        "secondary_keywords": [
            "OEM athletic apparel factory",
            "gym clothing wholesale supplier",
            "dry fit t-shirts manufacturer",
            "running jackets OEM ODM",
            "yoga leggings bulk supplier",
            "sublimation teamwear factory"
        ],
        "categories": {
            "activewear-tops": {
                "title": "Custom Athletic Tops & Performance T-Shirts Wholesale",
                "desc": "OEM manufacturing of breathable quick-dry shirts, compression tops, and athletic hoodies for global fitness brands.",
                "h1": "Athletic Tops & T-Shirts Manufacturing",
                "url": "athletic-tops-tshirts-wholesale.html",
                "spec_headers": ["Style Code", "Fabric Composition", "Weight (GSM)", "Features", "Size Run", "MOQ (Pcs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            },
            "leggings-shorts": {
                "title": "Seamless Yoga Leggings & Athletic Shorts OEM Factory",
                "desc": "High-stretch squat-proof leggings, running shorts, and compression bottoms with 4-needle 6-thread seamless stitching.",
                "h1": "Yoga Leggings & Athletic Shorts Production",
                "url": "yoga-leggings-athletic-shorts-oem.html",
                "spec_headers": ["Style Code", "Fabric Composition", "Weight (GSM)", "Features", "Size Run", "MOQ (Pcs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            },
            "outerwear-jackets": {
                "title": "Waterproof Windbreaker & Running Jackets Supplier",
                "desc": "Custom lightweight windbreakers, softshell jackets, and waterproof sports outerwear with seam-taped technology.",
                "h1": "Sports Jackets & Windbreakers Wholesale",
                "url": "sports-jackets-windbreakers-wholesale.html",
                "spec_headers": ["Style Code", "Fabric Composition", "Weight (GSM)", "Features", "Size Run", "MOQ (Pcs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            }
        }
    },
    "bags": {
        "primary_keyword": "Custom Bags & Backpacks Manufacturer",
        "secondary_keywords": [
            "OEM backpack factory China",
            "duffel bags wholesale supplier",
            "custom sports gym bags",
            "waterproof outdoor backpacks",
            "laptop bags bulk manufacturer",
            "promotional tote bags OEM"
        ],
        "categories": {
            "sports-backpacks": {
                "title": "Custom Sports & Outdoor Backpacks Wholesale",
                "desc": "Durable water-resistant backpacks, tactical bags, and school bags manufactured with reinforced bartack stitching and YKK zippers.",
                "h1": "Sports Backpacks Manufacturing",
                "url": "sports-backpacks-wholesale.html",
                "spec_headers": ["Model Code", "Main Material", "Lining", "Capacity (L)", "Dimensions", "MOQ (Pcs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "lining", "outsole", "sizes", "moq", "lead_time", "customization"]
            },
            "gym-duffel-bags": {
                "title": "OEM Travel & Gym Duffel Bags Manufacturer",
                "desc": "Custom gym duffels, shoe-compartment sports bags, and weekend travel bags with heavy-duty ripstop nylon and custom embroidery.",
                "h1": "Gym & Travel Duffel Bags Production",
                "url": "gym-duffel-bags-manufacturer.html",
                "spec_headers": ["Model Code", "Main Material", "Lining", "Capacity (L)", "Dimensions", "MOQ (Pcs)", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "lining", "outsole", "sizes", "moq", "lead_time", "customization"]
            }
        }
    },
    "stone": {
        "primary_keyword": "Natural Limestone & Cultural Stone Manufacturer",
        "secondary_keywords": [
            "architectural limestone supplier",
            "custom stone cladding factory",
            "exterior wall tiles wholesale",
            "honed limestone pavers",
            "stone veneer bulk supplier"
        ],
        "categories": {
            "limestone-cladding": {
                "title": "Natural Limestone Wall Cladding & Panels Wholesale",
                "desc": "Precision-cut natural limestone panels for luxury facades, exterior cladding, and interior architectural features.",
                "h1": "Architectural Limestone Cladding Production",
                "url": "limestone-wall-cladding-wholesale.html",
                "spec_headers": ["Product Code", "Stone Origin", "Surface Finish", "Dimensions (mm)", "Thickness (mm)", "MOQ (sqm)", "Lead Time", "ASTM/CE"],
                "spec_keys": ["name", "upper", "lining", "sizes", "outsole", "moq", "lead_time", "customization"]
            },
            "cultural-stone": {
                "title": "Handcrafted Cultural Stone & Veneer Factory",
                "desc": "Rustic ledge stone, stacked stone veneer, and castle rock panels for residential and commercial masonry projects.",
                "h1": "Cultural Stone & Veneer Manufacturing",
                "url": "cultural-stone-veneer-manufacturer.html",
                "spec_headers": ["Product Code", "Stone Type", "Colorway", "Dimensions (mm)", "Coverage / Box", "MOQ (sqm)", "Lead Time", "ASTM/CE"],
                "spec_keys": ["name", "upper", "lining", "sizes", "outsole", "moq", "lead_time", "customization"]
            }
        }
    },
    "general": {
        "primary_keyword": "B2B OEM ODM Manufacturer China",
        "secondary_keywords": [
            "custom product manufacturing",
            "direct factory supplier",
            "low MOQ private label",
            "wholesale export supplier"
        ],
        "categories": {
            "series-a": {
                "title": "Custom Series A Products Wholesale",
                "desc": "Premium OEM/ODM manufacturing series featuring top-grade materials, custom branding, and rigorous quality inspection.",
                "h1": "Series A Custom Manufacturing",
                "url": "series-a-wholesale-manufacturer.html",
                "spec_headers": ["Model Code", "Material", "Specifications", "Dimensions", "Packaging", "MOQ", "Lead Time", "Customization"],
                "spec_keys": ["name", "upper", "outsole", "lining", "sizes", "moq", "lead_time", "customization"]
            }
        }
    }
}

def hash_password(password, salt=None):
    if not salt:
        salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def scaffold_site(config, out_dir):
    print(f"\n========================================================")
    print(f"🏗️  SCAFFOLDING B2B EXPORT PORTAL: {config.get('name_en')}")
    print(f"📂 Target Directory: {out_dir}")
    print(f"========================================================\n")

    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Create subdirectories
    subdirs = ["css", "js", "data", "images", "images/products", "images/factory", "images/certifications", "images/news", "scratch"]
    for sd in subdirs:
        os.makedirs(os.path.join(out_dir, sd), exist_ok=True)

    # 2. Copy static base resources
    res_css = os.path.join(RESOURCES_DIR, "css", "style.css")
    res_js = os.path.join(RESOURCES_DIR, "js", "main.js")
    
    if os.path.exists(res_css):
        shutil.copy2(res_css, os.path.join(out_dir, "css", "style.css"))
    if os.path.exists(res_js):
        shutil.copy2(res_js, os.path.join(out_dir, "js", "main.js"))

    # 3. Copy base template HTML pages
    templates_dir = os.path.join(RESOURCES_DIR, "templates")
    if os.path.exists(templates_dir):
        for f in os.listdir(templates_dir):
            if f.endswith(".html"):
                shutil.copy2(os.path.join(templates_dir, f), os.path.join(out_dir, f))

    # 4. Copy build scripts & server
    for script_name in ["build_site.py", "server.py", "deploy_production_sync.py", "admin.html"]:
        src_path = os.path.join(RESOURCES_DIR, script_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(out_dir, script_name))

    scratch_src = os.path.join(RESOURCES_DIR, "scratch", "build_admin_html.py")
    if os.path.exists(scratch_src):
        shutil.copy2(scratch_src, os.path.join(out_dir, "scratch", "build_admin_html.py"))

    # 5. Build customized data/site_content.json
    industry = config.get("industry", "footwear").lower()
    preset = INDUSTRY_PRESETS.get(industry, INDUSTRY_PRESETS["general"])

    # Load template data if available
    template_data_path = os.path.join(RESOURCES_DIR, "data", "site_content.template.json")
    if os.path.exists(template_data_path):
        with open(template_data_path, "r", encoding="utf-8") as f:
            site_data = json.load(f)
    else:
        site_data = {"company_info": {}, "categories": {}, "products": [], "articles": [], "certifications": []}

    # Populate company_info
    c_info = site_data.get("company_info", {})
    c_info["name_en"] = config.get("name_en", "Apex B2B Manufacturing Co., Ltd.")
    c_info["name_zh"] = config.get("name_zh", "")
    c_info["logo_text"] = config.get("brand", "APEX GROUP")
    c_info["brand_name"] = config.get("brand", "APEX")
    c_info["domain"] = config.get("domain", "apexb2b.com")
    c_info["phone"] = config.get("phone", "+86 185 0000 0000")
    c_info["mobile"] = config.get("phone", "+86 185 0000 0000")
    c_info["whatsapp"] = config.get("whatsapp", "+86 185 0000 0000")
    c_info["wechat"] = config.get("wechat", config.get("phone", "+86 185 0000 0000"))
    c_info["email"] = config.get("email", "sales@apexb2b.com")
    c_info["email_secondary"] = config.get("email_secondary", f"info@{config.get('domain', 'apexb2b.com')}")
    c_info["address"] = config.get("address", "Industrial Zone, Fujian Province, China")
    c_info["port"] = config.get("port", "Xiamen Port / Shenzhen Port")
    c_info["founding_year"] = str(config.get("founding_year", "2008"))
    c_info["slogan"] = config.get("slogan", "Precision Engineering & Global Export Excellence")
    c_info["slogan_sub"] = config.get("slogan_sub", "A Masterpiece of Craftsmanship, Presenting Superior Quality")
    c_info["primary_keyword"] = config.get("primary_keyword", preset["primary_keyword"])
    c_info["secondary_keywords"] = config.get("secondary_keywords", preset["secondary_keywords"])
    c_info["meta_description"] = f"{c_info['name_en']} ({c_info['brand_name']}) is a leading {industry} manufacturer in China since {c_info['founding_year']}. Specializing in high-volume OEM/ODM production and global private label supply."
    c_info["geo_region"] = config.get("geo_region", "CN-FJ")
    c_info["geo_placename"] = config.get("geo_placename", "Quanzhou, Fujian, China")
    c_info["geo_position"] = config.get("geo_position", "24.8741;118.6757")
    c_info["icbm"] = config.get("icbm", "24.8741, 118.6757")

    # Sales team direct routing
    c_info["sales_team"] = [
        {
            "name": f"{c_info['brand_name']} Export Lead",
            "role": "Direct Factory Sales & Engineering Lead",
            "phone": c_info["phone"],
            "whatsapp": c_info["whatsapp"],
            "whatsapp_raw": c_info["whatsapp"].replace(" ", "").replace("-", ""),
            "whatsapp_clean": c_info["whatsapp"].replace("+", "").replace(" ", "").replace("-", ""),
            "status": "Online (Avg reply < 5m)",
            "avatar_initials": c_info['brand_name'][:2].upper(),
            "specialty": "OEM/ODM Tooling, Low MOQ, Tech Packs & Rapid Quotations"
        }
    ]

    site_data["company_info"] = c_info

    # Populate categories if custom or from preset
    if config.get("categories"):
        site_data["categories"] = config["categories"]
    else:
        site_data["categories"] = preset["categories"]

    # Write data/site_content.json
    with open(os.path.join(out_dir, "data", "site_content.json"), "w", encoding="utf-8") as f:
        json.dump(site_data, f, indent=2, ensure_ascii=False)
    print("  ✅ Configured data/site_content.json")

    # 6. Setup Admin Auth in data/auth.json
    admin_password = config.get("password", "admin2026")
    hashed, salt = hash_password(admin_password)
    with open(os.path.join(out_dir, "data", "auth.json"), "w", encoding="utf-8") as f:
        json.dump({"hashed_password": hashed, "salt": salt}, f, indent=2)
    print(f"  ✅ Initialized admin credentials (Password: {admin_password})")

    # Empty inquiries list
    with open(os.path.join(out_dir, "data", "inquiries.json"), "w", encoding="utf-8") as f:
        json.dump([], f)

    # 7. Customize Brand Colors in css/style.css
    primary_color = config.get("primary_color", "#e50408")
    secondary_color = config.get("secondary_color", "#007aff")
    accent_color = config.get("accent_color", primary_color)
    
    css_path = os.path.join(out_dir, "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_text = f.read()
        
        # Replace root color tokens
        css_text = re.sub(r'--brand-red:\s*#[0-9a-fA-F]+;', f'--brand-red: {primary_color};', css_text)
        css_text = re.sub(r'--primary-color:\s*#[0-9a-fA-F]+;', f'--primary-color: {primary_color};', css_text)
        css_text = re.sub(r'--secondary-color:\s*#[0-9a-fA-F]+;', f'--secondary-color: {secondary_color};', css_text)
        css_text = re.sub(r'--accent-color:\s*#[0-9a-fA-F]+;', f'--accent-color: {accent_color};', css_text)
        
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_text)
        print(f"  ✅ Applied Brand Colors: Primary={primary_color}, Secondary={secondary_color}")

    # 8. Customize server.py default email and domain
    server_path = os.path.join(out_dir, "server.py")
    if os.path.exists(server_path):
        with open(server_path, "r", encoding="utf-8") as f:
            srv_code = f.read()
        srv_code = re.sub(r'DEFAULT_TARGET_EMAIL\s*=\s*"[^"]*"', f'DEFAULT_TARGET_EMAIL = "{c_info["email"]}"', srv_code)
        srv_code = re.sub(r'target_email\s*=\s*"[^"]*"', f'target_email = "{c_info["email"]}"', srv_code)
        srv_code = re.sub(r'https://www\.widewayfootwear\.com', f'https://www.{c_info["domain"]}', srv_code)
        srv_code = re.sub(r'WIDEWAY-Footwear-Portal/2026', f'{c_info["brand_name"]}-B2B-Portal/2026', srv_code)
        with open(server_path, "w", encoding="utf-8") as f:
            f.write(srv_code)
        print("  ✅ Configured server.py email and domain bindings")

    # 9. Rebuild Admin HTML with new Brand Name
    admin_build_script = os.path.join(out_dir, "scratch", "build_admin_html.py")
    if os.path.exists(admin_build_script):
        with open(admin_build_script, "r", encoding="utf-8") as f:
            adm_code = f.read()
        adm_code = adm_code.replace("WIDEWAY MASTER B2B CMS", f"{c_info['brand_name']} MASTER B2B CMS")
        adm_code = adm_code.replace("WIDEWAY GROUP", c_info['logo_text'])
        with open(admin_build_script, "w", encoding="utf-8") as f:
            f.write(adm_code)
        # Execute generator
        try:
            subprocess.run([sys.executable, admin_build_script], cwd=out_dir, check=True, capture_output=True)
            print("  ✅ Compiled master admin.html dashboard")
        except Exception as err:
            print(f"  ⚠️ Warning: Admin compilation: {err}")

    # 10. Run build_site.py to compile all HTML files, sitemaps, robots.txt, and llms.txt
    build_script = os.path.join(out_dir, "build_site.py")
    if os.path.exists(build_script):
        try:
            res = subprocess.run([sys.executable, build_script], cwd=out_dir, check=True, capture_output=True, text=True)
            print("  ✅ Compiled all static pages, category hubs, sitemap.xml, robots.txt, and llms.txt")
        except Exception as err:
            print(f"  ⚠️ Warning: build_site.py execution: {err}")

    print(f"\n========================================================")
    print(f"🎉 B2B EXPORT SITE GENERATION COMPLETE!")
    print(f"========================================================")
    print(f"Company: {c_info['name_en']} ({c_info['brand_name']})")
    print(f"Domain:  https://{c_info['domain']}")
    print(f"Admin:   Password '{admin_password}' (Change in admin.html Settings)")
    print(f"--------------------------------------------------------")
    print(f"👉 Local Preview:")
    print(f"   cd {out_dir}")
    print(f"   python3 server.py 8080")
    print(f"   Open: http://localhost:8080 (Website)")
    print(f"   Open: http://localhost:8080/admin.html (Admin Console)")
    print(f"--------------------------------------------------------")
    print(f"👉 Production Deployment:")
    print(f"   Edit server host & SSH settings in deploy_production_sync.py")
    print(f"   python3 deploy_production_sync.py")
    print(f"========================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a brand-new B2B export website and CMS backend.")
    parser.add_argument("--config", help="Path to JSON configuration file.")
    parser.add_argument("--out-dir", default="./new_b2b_site", help="Output directory path.")
    parser.add_argument("--name-en", help="English company name.")
    parser.add_argument("--name-zh", help="Chinese company name.")
    parser.add_argument("--brand", help="Brand name or acronym (e.g. WIDEWAY, APEX).")
    parser.add_argument("--domain", help="Target domain (e.g. apexb2b.com).")
    parser.add_argument("--industry", default="footwear", choices=["footwear", "sportswear", "bags", "stone", "general"], help="Industry preset.")
    parser.add_argument("--email", help="Sales inquiry email.")
    parser.add_argument("--phone", help="Contact / WhatsApp number.")
    parser.add_argument("--whatsapp", help="WhatsApp number.")
    parser.add_argument("--address", help="Factory address.")
    parser.add_argument("--primary-color", default="#e50408", help="Brand primary color (Hex).")
    parser.add_argument("--secondary-color", default="#007aff", help="Brand secondary color (Hex).")
    parser.add_argument("--password", default="admin2026", help="Default admin console password.")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive prompt.")

    args = parser.parse_args()

    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)

    if args.interactive or (len(sys.argv) == 1 and not args.config):
        print("\n🚀 --- B2B STANDALONE SITE INTERACTIVE BUILDER --- 🚀\n")
        config["name_en"] = input("1. English Company Name [e.g. Jinjiang Apex Footwear Co., Ltd.]: ").strip() or "Apex Footwear Co., Ltd."
        config["name_zh"] = input("2. Chinese Company Name [Optional]: ").strip()
        config["brand"] = input("3. Brand / Logo Text [e.g. APEX]: ").strip() or "APEX"
        config["domain"] = input("4. Domain Name [e.g. apexfootwear.com]: ").strip() or "apexfootwear.com"
        config["industry"] = input("5. Industry Vertical (footwear/sportswear/bags/stone/general) [footwear]: ").strip() or "footwear"
        config["email"] = input("6. Sales Inquiry Email [e.g. sales@apexfootwear.com]: ").strip() or f"sales@{config['domain']}"
        config["phone"] = input("7. Phone & WhatsApp Number [e.g. +86 185 0000 0000]: ").strip() or "+86 185 0000 0000"
        config["whatsapp"] = config["phone"]
        config["address"] = input("8. Factory Address: ").strip() or "Industrial Zone, Fujian, China"
        config["primary_color"] = input("9. Primary Brand Color Hex [#e50408]: ").strip() or "#e50408"
        config["secondary_color"] = input("10. Secondary Color Hex [#007aff]: ").strip() or "#007aff"
        config["password"] = input("11. Admin Password [admin2026]: ").strip() or "admin2026"
        out_dir = input(f"12. Output Directory [{args.out_dir}]: ").strip() or args.out_dir
    else:
        # Override config with CLI flags if provided
        if args.name_en: config["name_en"] = args.name_en
        if args.name_zh: config["name_zh"] = args.name_zh
        if args.brand: config["brand"] = args.brand
        if args.domain: config["domain"] = args.domain
        if args.industry: config["industry"] = args.industry
        if args.email: config["email"] = args.email
        if args.phone: config["phone"] = args.phone
        if args.whatsapp: config["whatsapp"] = args.whatsapp
        elif args.phone and "whatsapp" not in config: config["whatsapp"] = args.phone
        if args.address: config["address"] = args.address
        if args.primary_color: config["primary_color"] = args.primary_color
        if args.secondary_color: config["secondary_color"] = args.secondary_color
        if args.password: config["password"] = args.password
        out_dir = args.out_dir

    scaffold_site(config, out_dir)

if __name__ == "__main__":
    main()
