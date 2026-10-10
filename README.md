# 🌐 WIDEWAY Export Site Builder & Master CMS Engine (2026 Edition)

> **Enterprise-Grade B2B Standalone Export Website & Master CMS Automation Framework**  
> Transform any manufacturing enterprise into a high-converting, AI-indexed B2B export powerhouse with 20+ responsive pages, Shopify-style product master catalog, 50MB 4K video showcase, visual in-place editing, and 1-click deployment.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AI-Ready](https://img.shields.io/badge/AI--Ready-LLMS.txt%20%7C%20GEO%20Schema-success.svg)](https://llmstxt.org/)
[![Deploy: SSH / Nginx](https://img.shields.io/badge/Deploy-SSH%20%7C%20Nginx%20%7C%20Systemd-orange.svg)]()

---

## ⚡ 1-Minute Quickstart

### Step 1: Clone the Repository
```bash
git clone https://github.com/cnproduct/wideway-export-site-builder-skill.git
cd wideway-export-site-builder-skill
```

### Step 2: Generate a Brand New Website
Choose any preset or provide your own JSON configuration:

```bash
# Option A: Using Footwear Preset
python3 scaffold_new_site.py --config config.footwear.json --out-dir ../my-footwear-site

# Option B: Using Sportswear Preset
python3 scaffold_new_site.py --config config.sportswear.json --out-dir ../my-sportswear-site

# Option C: Using Bags & Luggage Preset
python3 scaffold_new_site.py --config config.bags.json --out-dir ../my-bags-site

# Option D: Using Stone & Building Materials Preset
python3 scaffold_new_site.py --config config.stone.json --out-dir ../my-stone-site

# Option E: Interactive Mode
python3 scaffold_new_site.py --interactive
```

### Step 3: Run Locally & Manage Content
```bash
cd ../my-footwear-site
python3 server.py 8080
```
- 🖥️ **Front-End Website**: Open `http://localhost:8080`
- ⚙️ **Master Admin Console**: Open `http://localhost:8080/admin.html` (Password: `admin2026`)

---

## 💎 Core Architecture & Capabilities

```
+---------------------------------------------------------------------------------+
|                       B2B EXPORT STANDALONE SITE MATRIX                         |
+---------------------------------------------------------------------------------+
|  [Manufacturing & Capacity]  |  [Product Catalog & Hubs]  |   [OEM/ODM R&D Lab]   |
|  * Factory Capacity 120k/mo  |  * Shopify Master Editor   |   * 48h Prototyping   |
|  * 32-Gate Physical QC Lab   |  * 50MB 4K Video Showcase  |   * Tech Pack Re-eng  |
|  * BSCI / SEDEX / ISO Audits |  * Multi-Angle Gallery     |   * Low MOQ Incubator |
|  * GRS Eco Sustainability    |  * Category Dynamic Spec   |   * Private Label Hub |
+---------------------------------------------------------------------------------+
|                    MASTER ADMINISTRATIVE CONSOLE (admin.html)                   |
|  * Visual In-Place CMS (Edit any text, heading, banner, image, video in real-time) |
|  * Media Vault & In-Place Replacements (z-index: 20000 top-layer modal overlay)  |
|  * Leads CRM & Inquiries Relay (FormSubmit.co + Zoho/Corporate SMTP dispatch)   |
|  * 1-Click SSH / SCP Packaging & Remote Production Synchronization Daemon       |
+---------------------------------------------------------------------------------+
|                    2026 AI-READY SEO & GEO CITATION ENGINE                      |
|  * Google Image-Extended sitemap.xml  * Anti-Cloning robots.txt                 |
|  * Standardized llms.txt & llms-full.txt for ChatGPT, Perplexity, Claude, Gemini|
+---------------------------------------------------------------------------------+
```

---

## 📋 Comprehensive 20+ Page Suite

| Category | Pages & URLs | Key Features & Value Proposition |
| :--- | :--- | :--- |
| **Factory Strength** | `index.html`<br>`production-capacity.html`<br>`quality-control.html`<br>`certifications.html`<br>`sustainability.html` | Ultra-high resolution plant tour, automated lasting lines, SATRA 32-gate testing, audit badges, GRS recycled materials |
| **R&D & Customization** | `oem-odm.html`<br>`case-studies.html`<br>`heritage-footwear-reproduction.html`<br>`brand-identity.html` | Custom development flowchart, 1:1 archival reproduction, master shoe lasts, pattern grading, brand visual system |
| **Product Showcase** | `products.html`<br>`product-detail.html`<br>`*-wholesale.html`<br>`*-manufacturer.html` | Dual-view product catalog, dynamic SKU URL routing, 4K/1080P video player, multi-angle thumbnails, spec tables |
| **Content & Authority** | `news.html`<br>`news-detail.html`<br>`videos.html`<br>`glossary.html`<br>`whitepapers.html` | Industry trend articles, 4K video clips, technical vocabulary SEO booster, downloadable B2B sourcing whitepapers |
| **Conversion & Contact**| `contact.html`<br>`knowledge-base.html`<br>`knowledge-graph.html` | Multi-sales rep WhatsApp direct routing, RFQ quotation modal, interactive Incoterms & FAQ knowledge base |

---

## 🛠️ Configuration Guide (`config.json`)

You can customize all aspects of your new enterprise portal in a single JSON file:

```json
{
  "name_en": "Apex Footwear Manufacturing Co., Ltd.",
  "name_zh": "巅峰鞋业制造有限公司",
  "brand": "APEX FOOTWEAR",
  "domain": "apexfootwear.com",
  "industry": "footwear",
  "email": "sales@apexfootwear.com",
  "phone": "+86 185 0595 9266",
  "whatsapp": "+86 185 0595 9266",
  "address": "8F, Apex Industrial Center, Jinjiang, Quanzhou, Fujian, China",
  "port": "Xiamen Port / Quanzhou Port",
  "founding_year": "2008",
  "slogan": "Precision Footwear Engineering & Global OEM/ODM Partner",
  "primary_color": "#e50408",
  "secondary_color": "#007aff",
  "password": "admin2026",
  "geo_region": "CN-FJ",
  "geo_placename": "Jinjiang, Quanzhou, Fujian, China",
  "geo_position": "24.7865;118.5833"
}
```

---

## 🚀 Production Deployment (`deploy_production_sync.py`)

1. Open `deploy_production_sync.py` and set your server details:
```python
SERVER_IP = "your-server-ip"
SSH_PORT = 2222
SSH_USER = "ubuntu"
REMOTE_PATH = "/var/www/your-domain.com"
```

2. Execute deployment:
```bash
python3 deploy_production_sync.py
```

The script automatically:
1. Compiles and verifies all web assets.
2. Creates an optimized gzip tarball.
3. Uploads via SSH/SCP to the production server.
4. Extracts and configures Nginx permissions (`www-data:www-data`).
5. Reloads Nginx and restarts the background Python API systemd service.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
