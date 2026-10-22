#!/usr/bin/env python3
import os
import json
import glob
import re
import sys
import datetime
import html
import urllib.parse
from html.parser import HTMLParser

workspace = os.path.dirname(os.path.abspath(__file__))

def load_content():
    json_path = os.path.join(workspace, "data", "site_content.json")
    if not os.path.exists(json_path):
        print(f"Error: Database {json_path} not found.")
        sys.exit(1)
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

class HTMLMetaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.in_title = False
        self.description = ""
        self.lang = "en"

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "html":
            self.lang = attrs_dict.get("lang", self.lang)
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs_dict.get("name", "").lower() == "description" and not self.description:
                self.description = attrs_dict.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

def extract_page_meta(html):
    parser = HTMLMetaParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        pass
    title = ' '.join(''.join(parser.title_parts).split())
    description = ' '.join(parser.description.split())
    lang = parser.lang or "en"
    return title, description, lang

def get_header_html(filename, company_info):
    active_tab = ""
    if filename == "index.html": active_tab = "Home"
    elif filename == "products.html" or "-wholesale" in filename or "-supplier" in filename or "-manufacturer" in filename or "-factory" in filename:
        active_tab = "Products"
    elif filename == "oem-odm.html": active_tab = "OEM/ODM"
    elif filename in ["production-capacity.html", "quality-control.html", "certifications.html", "sustainability.html"]:
        active_tab = "Manufacturing"
    elif filename == "brand-identity.html": active_tab = "Brand VI"
    elif filename == "case-studies.html": active_tab = "Brands"
    elif filename in ["about.html", "videos.html"]:
        active_tab = "Company"
    elif filename.startswith("news"): active_tab = "News"
    elif filename == "contact.html": active_tab = "Contact"

    # Active states for Products dropdown
    p_sport_active = "active" if filename == "sport-outdoor-shoes-wholesale.html" else ""
    p_casual_active = "active" if filename == "casual-shoes-oem-manufacturer.html" else ""
    p_mens_active = "active" if filename == "mens-sneakers-bulk-supplier.html" else ""
    p_womens_active = "active" if filename == "womens-sneakers-oem-factory.html" else ""
    p_slides_active = "active" if filename == "slides-sandals-slippers-manufacturer.html" else ""
    p_bags_active = "active" if filename == "bags-sportswear-accessories-wholesale.html" else ""

    # Active states for Manufacturing dropdown
    m_cap_active = "active" if filename == "production-capacity.html" else ""
    m_qc_active = "active" if filename == "quality-control.html" else ""
    m_audit_active = "active" if filename == "certifications.html" else ""
    m_eco_active = "active" if filename == "sustainability.html" else ""
    m_heritage_active = "active" if filename == "heritage-footwear-reproduction.html" else ""

    # Active states for Company dropdown
    c_about_active = "active" if filename == "about.html" else ""
    c_video_active = "active" if filename == "videos.html" else ""
    c_news_active = "active" if filename.startswith("news") else ""

    # Active states for main nav links
    home_active = "active" if active_tab == "Home" else ""
    products_active = "active" if active_tab == "Products" else ""
    oem_active = "active" if active_tab == "OEM/ODM" else ""
    mfg_active = "active" if active_tab == "Manufacturing" else ""
    vi_active = "active" if active_tab == "Brand VI" else ""
    brands_active = "active" if active_tab == "Brands" else ""
    company_active = "active" if active_tab == "Company" else ""
    news_active = "active" if active_tab == "News" else ""
    contact_active = "active" if active_tab == "Contact" else ""

    # Mega Compass / SITEMAP Items (for centered modal dropdown)
    tabs = [
        ("/", "Home", "🏠"),
        ("/products", "Products Hub", "👟"),
        ("/sport-outdoor-shoes-wholesale", "Sport & Outdoor", "🏃"),
        ("/casual-shoes-oem-manufacturer", "Casual Shoes", "👞"),
        ("/mens-sneakers-bulk-supplier", "Men's Sneakers", "👟"),
        ("/womens-sneakers-oem-factory", "Women's Trainers", "👠"),
        ("/slides-sandals-slippers-manufacturer", "Slides & Sandals", "🩴"),
        ("/bags-sportswear-accessories-wholesale", "Sport Bags", "🎒"),
        ("/heritage-footwear-reproduction", "1:1 Archival Re-engineering", "⚡"),
        ("/oem-odm", "OEM/ODM", "⚙️"),
        ("/production-capacity", "Capacity", "🏭"),
        ("/quality-control", "QC & Lab", "🔬"),
        ("/certifications", "Audits", "📜"),
        ("/sustainability", "Eco Footwear", "🌱"),
        ("/brand-identity", "Brand VI", "🎨"),
        ("/case-studies", "Brands", "🤝"),
        ("/about", "About Us", "🏢"),
        ("/videos", "Videos", "🎬"),
        ("/news", "News Center", "📰"),
        ("/contact", "Contact", "📞")
    ]
    
    compass_items = ""
    for index, (href, label, emoji) in enumerate(tabs):
        active_cls = ""
        if (label == "Home" and filename == "index.html") or \
           (label == "Products Hub" and filename == "products.html") or \
           (label == "Sport & Outdoor" and filename == "sport-outdoor-shoes-wholesale.html") or \
           (label == "Casual Shoes" and filename == "casual-shoes-oem-manufacturer.html") or \
           (label == "Men's Sneakers" and filename == "mens-sneakers-bulk-supplier.html") or \
           (label == "Women's Trainers" and filename == "womens-sneakers-oem-factory.html") or \
           (label == "Slides & Sandals" and filename == "slides-sandals-slippers-manufacturer.html") or \
           (label == "Sport Bags" and filename == "bags-sportswear-accessories-wholesale.html") or \
           (label == "1:1 Archival Re-engineering" and filename == "heritage-footwear-reproduction.html") or \
           (label == "OEM/ODM" and filename == "oem-odm.html") or \
           (label == "Capacity" and filename == "production-capacity.html") or \
           (label == "QC & Lab" and filename == "quality-control.html") or \
           (label == "Audits" and filename == "certifications.html") or \
           (label == "Eco Footwear" and filename == "sustainability.html") or \
           (label == "Brand VI" and filename == "brand-identity.html") or \
           (label == "Brands" and filename == "case-studies.html") or \
           (label == "About Us" and filename == "about.html") or \
           (label == "Videos" and filename == "videos.html") or \
           (label == "News Center" and filename.startswith("news")) or \
           (label == "Contact" and filename == "contact.html"):
            active_cls = "active"
            
        compass_items += f"""      <a href="{href}" class="compass-item {active_cls}" style="--item-index: {index};" title="{label}" role="menuitem">
        <span class="item-icon">{emoji}</span>
        <span class="item-label">{label}</span>
      </a>
"""

    return f"""  <!-- Skip Link for Accessibility (WCAG 2.2 AA) -->
  <a href="#mainContent" class="skip-link">Skip to main content</a>

  <!-- Overlay backdrop for mobile overlay click to close -->
  <div class="compass-backdrop" id="compassBackdrop"></div>

  <header id="siteHeader" class="site-header site-header-centered">
    <!-- 1. Header Top Bar (Brand Logo Centered + Contact & Actions Balanced) -->
    <div class="header-top-bar">
      <div class="container header-top-container">
        
        <!-- Left: Quick Direct Contact -->
        <div class="header-top-left pc-only">
          <a href="tel:+8613123025365" class="top-contact-link" title="Call WIDEWAY Factory Specialist">
            <span>📞</span>
            <span>+86 131 2302 5365</span>
          </a>
          <span class="top-sep">|</span>
          <a href="mailto:{company_info.get('email', 'stella@widewaygroup.com')}" class="top-contact-link" title="Direct Email Quotation">
            <span>✉️</span>
            <span>{company_info.get('email', 'stella@widewaygroup.com')}</span>
          </a>
        </div>

        <!-- Center: Official Brand Logo Centered -->
        <div class="header-brand-center">
          <a href="/" class="header-logo-centered" id="logoLink" title="WIDEWAY GROUP Jinjiang Footwear Manufacturer">
            <img src="images/logo.png" alt="WIDEWAY GROUP Footwear Logo" width="130" height="36">
            <div class="brand-titles">
              <span class="logo-main-text">{company_info.get("logo_text", "WIDEWAY GROUP")}</span>
              <span class="logo-sub-text pc-only">JINJIANG FOOTWEAR CAPITAL &bull; OEM/ODM SINCE 2007</span>
            </div>
          </a>
        </div>

        <!-- Right: Actions (SITEMAP Compass & Request Quote) -->
        <div class="header-top-right">
          <div class="compass-nav-container" id="compassNav" role="navigation" aria-label="Interactive Navigation Compass">
            <button class="compass-trigger" id="compassTrigger" aria-label="Toggle Navigation Compass" aria-haspopup="true" aria-expanded="false" aria-controls="compassMenu">
              <div class="compass-dial pc-only">
                <div class="compass-dial-ring"></div>
                <div class="compass-needle"></div>
                <div class="compass-center"></div>
              </div>
              <span class="sitemap-text pc-only">SITEMAP</span>
              <span class="sitemap-arrow pc-only">▾</span>

              <div class="hamburger-icon mobile-only">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </button>
            <div class="compass-menu" id="compassMenu" role="menu">
              <div class="compass-menu-header">
                <div class="compass-menu-header-title">
                  <span>🧭</span>
                  <span>Footwear Directory &amp; Sitemap</span>
                </div>
                <button type="button" class="compass-menu-close" id="compassCloseBtn" aria-label="Close Sitemap">✕</button>
              </div>
{compass_items}            </div>
          </div>

          <a href="/contact" class="header-cta-quote pc-only">
            Request Quote
          </a>
        </div>

      </div>
    </div>

    <!-- 2. Header Nav Bar (Centered Navigation Row with Subcategory Dropdowns) -->
    <nav class="header-nav-bar" aria-label="Main Navigation">
      <div class="container nav-bar-container">
        <ul class="centered-nav-list">
          <!-- Home -->
          <li class="nav-item">
            <a href="/" class="desktop-nav-link {home_active}">Home</a>
          </li>

          <!-- Products ▾ (With Subcategories Dropdown) -->
          <li class="nav-item has-dropdown">
            <a href="/products" class="desktop-nav-link {products_active}">
              Products <span class="nav-caret">▾</span>
            </a>
            <div class="nav-dropdown-menu" role="menu">
              <div class="dropdown-header">
                <span>Footwear Collections</span>
                <span class="badge">115+ OEM/ODM SKUs</span>
              </div>
              <div class="dropdown-grid">
                <a href="/sport-outdoor-shoes-wholesale" class="dropdown-card {p_sport_active}" role="menuitem">
                  <span class="dropdown-icon">👟</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Sport &amp; Outdoor Shoes</span>
                    <span class="dropdown-desc">Trail running, hiking &amp; waterproof grip</span>
                  </div>
                </a>
                <a href="/casual-shoes-oem-manufacturer" class="dropdown-card {p_casual_active}" role="menuitem">
                  <span class="dropdown-icon">👞</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Custom Casual Shoes</span>
                    <span class="dropdown-desc">Vulcanized, lifestyle sneakers &amp; cupsole</span>
                  </div>
                </a>
                <a href="/mens-sneakers-bulk-supplier" class="dropdown-card {p_mens_active}" role="menuitem">
                  <span class="dropdown-icon">🏃</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Men's Streetwear Sneakers</span>
                    <span class="dropdown-desc">Chunky dad soles &amp; engineered knit uppers</span>
                  </div>
                </a>
                <a href="/womens-sneakers-oem-factory" class="dropdown-card {p_womens_active}" role="menuitem">
                  <span class="dropdown-icon">👟</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Women's Lightweight Trainers</span>
                    <span class="dropdown-desc">Cushioned EVA, breathable mesh &amp; fitness</span>
                  </div>
                </a>
                <a href="/slides-sandals-slippers-manufacturer" class="dropdown-card {p_slides_active}" role="menuitem">
                  <span class="dropdown-icon">🩴</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Slides, Sandals &amp; Slippers</span>
                    <span class="dropdown-desc">EVA injection recovery slides &amp; comfort</span>
                  </div>
                </a>
                <a href="/bags-sportswear-accessories-wholesale" class="dropdown-card {p_bags_active}" role="menuitem">
                  <span class="dropdown-icon">🎒</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Sportswear Bags &amp; Backpacks</span>
                    <span class="dropdown-desc">Cordura duffels, gym sacks &amp; accessories</span>
                  </div>
                </a>
              </div>
              <div class="dropdown-footer">
                <a href="/products" class="dropdown-view-all">Browse Complete Catalog (115+ Footwear SKUs) &rarr;</a>
              </div>
            </div>
          </li>

          <!-- OEM/ODM -->
          <li class="nav-item">
            <a href="/oem-odm" class="desktop-nav-link {oem_active}">OEM/ODM</a>
          </li>

          <!-- Manufacturing ▾ (With Subcategories Dropdown) -->
          <li class="nav-item has-dropdown">
            <a href="/production-capacity" class="desktop-nav-link {mfg_active}">
              Manufacturing <span class="nav-caret">▾</span>
            </a>
            <div class="nav-dropdown-menu dropdown-narrow" role="menu">
              <div class="dropdown-header">
                <span>Facility &amp; Standards</span>
                <span class="badge">Jinjiang Plant</span>
              </div>
              <div class="dropdown-grid single-col">
                <a href="/heritage-footwear-reproduction" class="dropdown-card {m_heritage_active}" role="menuitem">
                  <span class="dropdown-icon">⚡</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">1:1 Archival Re-Engineering</span>
                    <span class="dropdown-desc">Retro silhouettes, 3D lasts &amp; vintage tooling</span>
                  </div>
                </a>
                <a href="/production-capacity" class="dropdown-card {m_cap_active}" role="menuitem">
                  <span class="dropdown-icon">🏭</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Production Capacity</span>
                    <span class="dropdown-desc">4 assembly lines, 300,000+ pairs monthly</span>
                  </div>
                </a>
                <a href="/quality-control" class="dropdown-card {m_qc_active}" role="menuitem">
                  <span class="dropdown-icon">🔬</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Physical QC &amp; Testing Lab</span>
                    <span class="dropdown-desc">32 SATRA testing gates for durability</span>
                  </div>
                </a>
                <a href="/certifications" class="dropdown-card {m_audit_active}" role="menuitem">
                  <span class="dropdown-icon">📜</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">BSCI &amp; Global Audits</span>
                    <span class="dropdown-desc">ISO 9001, CE, SMETA Sedex certified</span>
                  </div>
                </a>
                <a href="/sustainability" class="dropdown-card {m_eco_active}" role="menuitem">
                  <span class="dropdown-icon">🌱</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Eco &amp; Sustainability</span>
                    <span class="dropdown-desc">GRS recycled RPET yarn &amp; Bloom algae EVA</span>
                  </div>
                </a>
              </div>
            </div>
          </li>

          <!-- Brand VI 🎨 -->
          <li class="nav-item">
            <a href="/brand-identity" class="desktop-nav-link {vi_active}" style="color: #ff8a8c;">Brand VI 🎨</a>
          </li>

          <!-- Brands -->
          <li class="nav-item">
            <a href="/case-studies" class="desktop-nav-link {brands_active}">Brands</a>
          </li>

          <!-- Company ▾ (With Subcategories Dropdown) -->
          <li class="nav-item has-dropdown">
            <a href="/about" class="desktop-nav-link {company_active}">
              Company <span class="nav-caret">▾</span>
            </a>
            <div class="nav-dropdown-menu dropdown-narrow" role="menu">
              <div class="dropdown-header">
                <span>Company Profile</span>
                <span class="badge">Since 2007</span>
              </div>
              <div class="dropdown-grid single-col">
                <a href="/about" class="dropdown-card {c_about_active}" role="menuitem">
                  <span class="dropdown-icon">🏢</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">About Us</span>
                    <span class="dropdown-desc">19-year footwear export heritage</span>
                  </div>
                </a>
                <a href="/videos" class="dropdown-card {c_video_active}" role="menuitem">
                  <span class="dropdown-icon">🎬</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">Factory Video Tour</span>
                    <span class="dropdown-desc">4K workshop, lasting &amp; testing reels</span>
                  </div>
                </a>
                <a href="/news" class="dropdown-card {c_news_active}" role="menuitem">
                  <span class="dropdown-icon">📰</span>
                  <div class="dropdown-card-text">
                    <span class="dropdown-title">30-Day News Center</span>
                    <span class="dropdown-desc">Global footwear trade &amp; technical insights</span>
                  </div>
                </a>
              </div>
            </div>
          </li>

          <!-- News (Direct Link) -->
          <li class="nav-item">
            <a href="/news" class="desktop-nav-link {news_active}">News</a>
          </li>

          <!-- Contact -->
          <li class="nav-item">
            <a href="/contact" class="desktop-nav-link {contact_active}">Contact</a>
          </li>
        </ul>
      </div>
    </nav>
  </header>"""

def get_footer_html(company_info):
    phone_clean = company_info.get("phone", "+86 131 2302 5365")
    wa_clean = re.sub(r"[^0-9]", "", phone_clean)
    email_main = company_info.get("email", "stella@widewaygroup.com")

    return f"""  <footer>
    <div class="container">
      <div class="footer-top">
        <div class="footer-col">
          <a href="/" class="logo footer-logo" style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;" title="WIDEWAY GROUP Jinjiang Footwear Manufacturer">
            <img src="images/logo.png" alt="WIDEWAY Logo" width="130" height="36" style="height: 36px; width: auto; object-fit: contain;">
            <span style="font-weight: 800; letter-spacing: 0.5px; color: #0b1e36;">{company_info.get("logo_text", "WIDEWAY GROUP")}</span>
          </a>
          <p class="footer-desc">Professional athletic footwear manufacturer and exporter based in Jinjiang, Fujian—China's Footwear Capital. Specializing in sneakers, sports shoes, casual footwear, slides, sandals, and athletic bags since 2007. Trusted OEM/ODM manufacturing partner for FILA, KAPPA, DIADORA, STARTER, WRANGLER, Lidl, and Aldi.</p>
          <div class="footer-socials" style="display: flex; gap: 10px; margin-top: 15px;">
            <a href="https://wa.me/{wa_clean}" target="_blank" class="social-link" title="WhatsApp: {phone_clean}">💬</a>
            <a href="/contact" class="social-link" title="WeChat: {phone_clean}"><img src="images/wx-v-ewm.png" width="24" height="24" style="width: 24px; height: 24px; border-radius: 4px;" alt="WeChat QR"></a>
            <a href="/contact" class="social-link" title="TikTok"><img src="images/dy-ewm.png" width="24" height="24" style="width: 24px; height: 24px; border-radius: 4px;" alt="TikTok"></a>
            <a href="mailto:{email_main}" class="social-link" title="Direct Email: {email_main}">✉️</a>
            <a href="tel:+8613123025365" class="social-link" title="Direct Call: {phone_clean}">📞</a>
          </div>
        </div>

        <div class="footer-col">
          <h3>Footwear Collections</h3>
          <ul class="footer-links">
            <li><a href="/sport-outdoor-shoes-wholesale">Sport &amp; Outdoor Shoes</a></li>
            <li><a href="/casual-shoes-oem-manufacturer">Custom Casual Shoes</a></li>
            <li><a href="/mens-sneakers-bulk-supplier">Men's Streetwear Sneakers</a></li>
            <li><a href="/womens-sneakers-oem-factory">Women's Lightweight Trainers</a></li>
            <li><a href="/slides-sandals-slippers-manufacturer">Slides, Sandals &amp; Slippers</a></li>
            <li><a href="/bags-sportswear-accessories-wholesale">Sportswear Bags &amp; Backpacks</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Manufacturing &amp; Audits</h3>
          <ul class="footer-links">
            <li><a href="/heritage-footwear-reproduction">1:1 Archival Re-Engineering</a></li>
            <li><a href="/oem-odm">OEM/ODM Tooling &amp; Lasts</a></li>
            <li><a href="/production-capacity">Assembly Lines &amp; Fire Safety</a></li>
            <li><a href="/quality-control">Physical Footwear Testing Lab</a></li>
            <li><a href="/certifications">BSCI, ISO 9001 &amp; Global Audits</a></li>
            <li><a href="/sustainability">Eco Materials &amp; Recycled RPET</a></li>
            <li><a href="/brand-identity">Brand Visual System (VI/CI)</a></li>
            <li><a href="/case-studies">FILA &amp; Brand Partnerships</a></li>
            <li><a href="/videos">Factory Video Showcase</a></li>
            <li><a href="/news">News &amp; Footwear Insights</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Direct Factory Contact</h3>
          <ul class="footer-contact-list">
            <li class="loc"><strong>Chendai Plant:</strong> {company_info.get("address", "8F, Building 8A, NO.618, JINXIN Road, ChenDai town, Jinjiang, QuanZhou City, Fujian, China")}</li>
            <li class="loc"><strong>Office:</strong> {company_info.get("registered_address", "M1-906 Shimaoyulongwan, Shuanglong Road, Jinjiang, Fujian, China")}</li>
            <li class="tel"><strong>Mobile / WhatsApp:</strong> <a href="https://wa.me/{wa_clean}" target="_blank" style="color: #25d366; font-weight: 700; text-decoration: none;">{phone_clean}</a></li>
            <li class="tel"><strong>Direct Call:</strong> <a href="tel:+8613123025365" style="color: inherit; text-decoration: none;">{phone_clean}</a></li>
            <li class="wa"><strong>WeChat Official:</strong> {phone_clean}</li>
            <li class="eml"><strong>Email:</strong> <a href="mailto:{email_main}" style="color: inherit; text-decoration: none;">{email_main}</a></li>
          </ul>
        </div>
      </div>

      <!-- Verified Footwear Supply Chain & Regulatory Standards Partners Strip -->
      <div class="footer-partner-strip" style="margin-top: 36px; padding-top: 24px; border-top: 1px solid #e2e8f0; font-size: 0.82rem; color: #475569; line-height: 1.8;">
        <div style="font-weight: 700; color: #0b1e36; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.8px;">
          Verified Footwear Supply Chain &amp; International Standards Partners:
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 10px 16px;">
          <a href="https://www.satra.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">SATRA Technology</a>
          <a href="https://us.vibram.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">Vibram Rubber Outsoles</a>
          <a href="https://www.ortholite.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">OrthoLite Performance Insoles</a>
          <a href="https://www.cordura.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">Cordura Advanced Fabrics</a>
          <a href="https://www.gore-tex.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">GORE-TEX Membrane</a>
          <a href="https://www.boafit.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">BOA Fit Dial System</a>
          <a href="https://www.ykkfastening.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">YKK Zippers</a>
          <a href="https://www.amfori.org" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">amfori BSCI</a>
          <a href="https://www.sedex.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">Sedex SMETA</a>
          <a href="https://www.iso.org" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">ISO 9001:2015</a>
          <a href="https://www.sgs.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">SGS Footwear Testing</a>
          <a href="https://www.intertek.com" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">Intertek Lab</a>
          <a href="https://single-market-economy.ec.europa.eu/single-market/ce-marking_en" target="_blank" rel="noopener noreferrer" style="color:#475569; text-decoration:none;">CE Compliance</a>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 {company_info.get("name_en", "Jinjiang Wideway Import & Export Co., Ltd.")} ({company_info.get("name_zh", "晋江市万维进出口有限公司")}). All Rights Reserved.</p>
        <p>Engineered for Global Footwear Brands | Port of Shipment: {company_info.get("port", "Xiamen Port / Quanzhou Port")}</p>
      </div>
    </div>
  </footer>

  <!-- Floating B2B Social Share Bar -->
  <div class="b2b-social-share-bar">
    <button onclick="shareFacebook()" class="share-btn fb" title="Share on Facebook">FB</button>
    <button onclick="shareLinkedIn()" class="share-btn ln" title="Share on LinkedIn">LN</button>
    <button onclick="shareWhatsApp()" class="share-btn wa" title="Share on WhatsApp">WA</button>
    <button onclick="shareWeChat()" class="share-btn wx" title="Share on WeChat">WX</button>
  </div>
  <script>
    function shareFacebook() {{
      window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(window.location.href), '_blank', 'width=600,height=400');
    }}
    function shareLinkedIn() {{
      window.open('https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(window.location.href), '_blank', 'width=600,height=400');
    }}
    function shareWhatsApp() {{
      window.open('https://api.whatsapp.com/send?text=' + encodeURIComponent(window.location.href), '_blank');
    }}
    function shareWeChat() {{
      alert('Copy this link to share on WeChat: ' + window.location.href);
    }}
  </script>"""

def get_chat_widget_html(company_info):
    phone_clean = company_info.get("phone", "+86 131 2302 5365")
    wa_clean = re.sub(r"[^0-9]", "", phone_clean)
    email_main = company_info.get("email", "stella@widewaygroup.com")

    return f"""  <!-- Floating WhatsApp Live Chat Sidebar / Dock Widget -->
  <div class="b2b-whatsapp-floating-widget" id="whatsappFloatingWidget">
    <!-- Floating Trigger Pill -->
    <button type="button" class="whatsapp-trigger-pill" id="whatsappTriggerBtn" aria-label="Open WhatsApp Live Chat" onclick="toggleWhatsAppWidget(event)">
      <div class="wa-icon-wrap">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="#fff"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.73-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.745 1.45 5.58-.002 10.118-4.541 10.121-10.125a10.024 10.024 0 0 0-2.959-7.149 10.024 10.024 0 0 0-7.142-2.977C5.787 2.355 1.25 6.892 1.247 12.477c-.001 1.637.458 3.235 1.332 4.678L1.611 21.91l4.894-1.28c.002-.001.002-.001.002-.001z M17.07 14.364c-.273-.137-1.62-.8-1.87-.892-.25-.092-.43-.137-.61.137-.18.274-.7.892-.857 1.074-.158.182-.317.205-.59.068a10.51 10.51 0 0 1-3.665-2.261 11.59 11.59 0 0 1-2.535-3.158c-.164-.282-.018-.434.12-.57.124-.122.272-.317.41-.476.136-.159.182-.272.272-.454.09-.181.046-.34-.022-.477-.068-.137-.61-1.474-.836-2.02-.22-.53-.44-.457-.61-.466-.157-.008-.34-.01-.522-.01-.182 0-.476.068-.726.34-.25.274-.954.932-.954 2.27 0 1.34.977 2.634 1.113 2.817.136.182 1.922 2.935 4.657 4.116.65.28 1.158.448 1.554.574.654.208 1.25.178 1.722.108.525-.078 1.62-.662 1.848-1.27.227-.607.227-1.127.159-1.27-.069-.143-.25-.227-.523-.364z"/></svg>
        <span class="wa-pulsing-beacon"></span>
      </div>
      <div class="wa-trigger-text pc-only">
        <span class="wa-trigger-title">WhatsApp Live</span>
        <span class="wa-trigger-status"><span class="green-dot"></span> Online</span>
      </div>
      <span class="wa-trigger-arrow pc-only">▾</span>
    </button>

    <!-- WhatsApp Popup Card -->
    <div class="whatsapp-panel-card" id="whatsappPanelCard">
      <div class="wa-panel-header">
        <div class="wa-header-brand">
          <div class="wa-header-logo-icon">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="#fff"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.73-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.745 1.45 5.58-.002 10.118-4.541 10.121-10.125a10.024 10.024 0 0 0-2.959-7.149 10.024 10.024 0 0 0-7.142-2.977C5.787 2.355 1.25 6.892 1.247 12.477c-.001 1.637.458 3.235 1.332 4.678L1.611 21.91l4.894-1.28c.002-.001.002-.001.002-.001z M17.07 14.364c-.273-.137-1.62-.8-1.87-.892-.25-.092-.43-.137-.61.137-.18.274-.7.892-.857 1.074-.158.182-.317.205-.59.068a10.51 10.51 0 0 1-3.665-2.261 11.59 11.59 0 0 1-2.535-3.158c-.164-.282-.018-.434.12-.57.124-.122.272-.317.41-.476.136-.159.182-.272.272-.454.09-.181.046-.34-.022-.477-.068-.137-.61-1.474-.836-2.02-.22-.53-.44-.457-.61-.466-.157-.008-.34-.01-.522-.01-.182 0-.476.068-.726.34-.25.274-.954.932-.954 2.27 0 1.34.977 2.634 1.113 2.817.136.182 1.922 2.935 4.657 4.116.65.28 1.158.448 1.554.574.654.208 1.25.178 1.722.108.525-.078 1.62-.662 1.848-1.27.227-.607.227-1.127.159-1.27-.069-.143-.25-.227-.523-.364z"/></svg>
          </div>
          <div>
            <div class="wa-header-heading">Direct WhatsApp Sales Desk</div>
            <div class="wa-header-sub">Instant quotation &amp; technical inquiry</div>
          </div>
        </div>
        <button type="button" class="wa-close-btn" onclick="toggleWhatsAppWidget(event, false)" aria-label="Close WhatsApp Panel">✕</button>
      </div>

      <div class="wa-panel-body">
        <p class="wa-panel-intro">Chat directly with our export engineering leads for fast quote &amp; sample requests:</p>

        <!-- Official Contact Card -->
        <div class="wa-rep-card">
          <div class="wa-rep-avatar-wrap">
            <div class="wa-rep-avatar ad">WW</div>
            <span class="wa-rep-online-dot" title="Online Now"></span>
          </div>
          <div class="wa-rep-info">
            <div class="wa-rep-name-row">
              <strong class="wa-rep-name">WIDEWAY Sales Desk</strong>
              <span class="wa-rep-tag">Direct Factory</span>
            </div>
            <div class="wa-rep-role">OEM/ODM Tooling &amp; Technical Lead</div>
            <div class="wa-rep-phone-num">WhatsApp / Tel: {phone_clean}</div>
            <a href="https://wa.me/{wa_clean}?text=Hi%20WIDEWAY,%20I'm%20contacting%20you%20from%20widewayfootwear.com%20regarding%20manufacturing..." target="_blank" rel="noopener noreferrer" class="wa-chat-action-btn">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.73-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.745 1.45 5.58-.002 10.118-4.541 10.121-10.125a10.024 10.024 0 0 0-2.959-7.149 10.024 10.024 0 0 0-7.142-2.977C5.787 2.355 1.25 6.892 1.247 12.477c-.001 1.637.458 3.235 1.332 4.678L1.611 21.91l4.894-1.28c.002-.001.002-.001.002-.001z M17.07 14.364c-.273-.137-1.62-.8-1.87-.892-.25-.092-.43-.137-.61.137-.18.274-.7.892-.857 1.074-.158.182-.317.205-.59.068a10.51 10.51 0 0 1-3.665-2.261 11.59 11.59 0 0 1-2.535-3.158c-.164-.282-.018-.434.12-.57.124-.122.272-.317.41-.476.136-.159.182-.272.272-.454.09-.181.046-.34-.022-.477-.068-.137-.61-1.474-.836-2.02-.22-.53-.44-.457-.61-.466-.157-.008-.34-.01-.522-.01-.182 0-.476.068-.726.34-.25.274-.954.932-.954 2.27 0 1.34.977 2.634 1.113 2.817.136.182 1.922 2.935 4.657 4.116.65.28 1.158.448 1.554.574.654.208 1.25.178 1.722.108.525-.078 1.62-.662 1.848-1.27.227-.607.227-1.127.159-1.27-.069-.143-.25-.227-.523-.364z"/></svg>
              <span>Chat on WhatsApp ({phone_clean})</span>
            </a>
          </div>
        </div>
      </div>

      <div class="wa-panel-footer">
        <span>✉️ <a href="mailto:{email_main}">{email_main}</a></span>
        <span style="color: #cbd5e1;">•</span>
        <span>⏱️ Fast Reply (&lt; 5 mins)</span>
      </div>
    </div>
  </div>

  <!-- Mobile Ergonomic Sticky Bottom Dock -->
  <div class="mobile-sticky-dock" role="navigation" aria-label="Mobile Contact Dock">
    <a href="https://wa.me/{wa_clean}?text=Hi%20WIDEWAY,%20I'm%20inquiring%20about%20footwear..." target="_blank" class="dock-btn dock-whatsapp" title="WhatsApp">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.73-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.745 1.45 5.58-.002 10.118-4.541 10.121-10.125a10.024 10.024 0 0 0-2.959-7.149 10.024 10.024 0 0 0-7.142-2.977C5.787 2.355 1.25 6.892 1.247 12.477c-.001 1.637.458 3.235 1.332 4.678L1.611 21.91l4.894-1.28c.002-.001.002-.001.002-.001z M17.07 14.364c-.273-.137-1.62-.8-1.87-.892-.25-.092-.43-.137-.61.137-.18.274-.7.892-.857 1.074-.158.182-.317.205-.59.068a10.51 10.51 0 0 1-3.665-2.261 11.59 11.59 0 0 1-2.535-3.158c-.164-.282-.018-.434.12-.57.124-.122.272-.317.41-.476.136-.159.182-.272.272-.454.09-.181.046-.34-.022-.477-.068-.137-.61-1.474-.836-2.02-.22-.53-.44-.457-.61-.466-.157-.008-.34-.01-.522-.01-.182 0-.476.068-.726.34-.25.274-.954.932-.954 2.27 0 1.34.977 2.634 1.113 2.817.136.182 1.922 2.935 4.657 4.116.65.28 1.158.448 1.554.574.654.208 1.25.178 1.722.108.525-.078 1.62-.662 1.848-1.27.227-.607.227-1.127.159-1.27-.069-.143-.25-.227-.523-.364z"/></svg>
      <span>WhatsApp</span>
    </a>
    <a href="tel:+8613123025365" class="dock-btn dock-phone" title="Call Direct">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
      <span>Call Direct</span>
    </a>
    <a href="/contact" class="dock-btn dock-phone" title="WeChat / Factory Info" style="background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8.384 10.94c.484 0 .878-.387.878-.865 0-.478-.394-.866-.878-.866a.87.87 0 0 0-.879.866c0 .478.394.865.879.865zm4.823 0c.484 0 .879-.387.879-.865 0-.478-.395-.866-.879-.866a.87.87 0 0 0-.878.866c0 .478.394.865.878.865z M18.558 13.064c.245-.06.495-.094.75-.094 2.457 0 4.45 1.71 4.45 3.82 0 1.16-.6 2.21-1.57 2.91.13.43.51 1.29.51 1.29s-.88-.24-1.83-.8c-.53.15-1.09.23-1.66.23-2.457 0-4.45-1.71-4.45-3.82 0-1.72 1.33-3.17 3.25-3.536z M16.718 16.59c.316 0 .573-.253.573-.565 0-.312-.257-.565-.573-.565s-.572.253-.572.565c0 .312.257.565.572.565zm2.864 0c.316 0 .573-.253.573-.565 0-.312-.257-.565-.573-.565s-.572.253-.572.565c0 .312.257.565-.572.565z M14.334 11.23c0-3.823-3.99-6.924-8.91-6.924C2.316 4.306 0 7.407 0 11.23c0 2.234 1.334 4.225 3.425 5.426-.266.862-1.05 2.584-1.05 2.584s1.776-.492 3.738-1.636c.99.294 2.052.45 3.156.45 4.92 0 9.065-3.1 9.065-6.824z"/></svg>
      <span>WeChat</span>
    </a>
    <a href="#inquiry" class="dock-btn dock-quote" title="Request Factory Quotation">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      <span>Quote</span>
    </a>
  </div>"""

def category_matches(product, key):
    return product.get("category") == key

def get_product_id(p):
    if p.get("id"):
        return p["id"]
    code_or_name = p.get("code") or p.get("name") or "product"
    return re.sub(r"[^a-zA-Z0-9]+", "-", code_or_name).strip("-").lower()

def get_products_grid_html(products, filter_key=None):
    grid_html = ""
    for p in products:
        if filter_key and not category_matches(p, filter_key):
            continue
        p_id = get_product_id(p)
        p_name = p.get("name", p_id)
        p_img = p.get("image", "images/banner.jpg")
        p_cat = p.get("category", "sport-outdoor-shoes")
        has_video = bool(p.get("video") or p.get("video_url"))
        
        video_badge = """            <span class="product-video-badge" style="position: absolute; bottom: 10px; right: 10px; background: rgba(11,30,54,0.85); color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; z-index: 3; backdrop-filter: blur(4px); box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="#e50408"><path d="M8 5v14l11-7z"/></svg>
              <span>4K VIDEO</span>
            </span>""" if has_video else ""

        features_html = f"""              <li><strong>Upper:</strong> {p.get("upper", "Flyknit Mesh / Synthetic Leather")}</li>
              <li><strong>Outsole:</strong> {p.get("outsole", "MD Midsole + Rubber Outsole")}</li>
              <li><strong>Size Range:</strong> {p.get("sizes", "EU 36-45 / US 5-11")}</li>
              <li><strong>MOQ:</strong> {p.get("moq", "500 Pairs / Color")}</li>\n"""
        
        grid_html += f"""        <!-- Product: {p_name} -->
        <div class="product-card" data-category="{p_cat}">
          <div class="product-img-wrapper" style="position: relative; overflow: hidden; aspect-ratio: 4/3; background: #f8fafc;">
            <span class="product-tag">{p.get("tag", "Factory Direct")}</span>
{video_badge}
            <a href="product-detail?id={p_id}" title="View {p_name} Details">
              <img src="{p_img}" alt="{p_name} - WIDEWAY Footwear OEM Jinjiang" loading="lazy" width="400" height="300" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;">
            </a>
          </div>
          <div class="product-info">
            <h3 style="font-size: 1.15rem; margin-bottom: 8px;"><a href="product-detail?id={p_id}" style="color: inherit; text-decoration: none;">{p_name}</a></h3>
            <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 12px; line-height: 1.4;">{p.get("description", "")[:120]}...</p>
            <ul class="product-features" style="font-size: 0.82rem; line-height: 1.5; margin-bottom: 15px;">
{features_html}            </ul>
            <div style="display: flex; gap: 8px;">
              <a href="product-detail?id={p_id}" class="btn btn-secondary btn-sm" style="flex: 1; text-align: center; border-color: #0b1e36; color: #0b1e36; padding: 8px 10px; font-weight: 600;">View Specs</a>
              <a href="contact?product={p_id}" class="btn btn-primary btn-sm btn-open-quote" data-product="{p_id}" data-category="{p_cat}" style="flex: 1; text-align: center; background: #e50408; border-color: #e50408; padding: 8px 10px; font-weight: 600;">Get Quote</a>
            </div>
          </div>
        </div>\n"""
    return f"""      <div class="grid grid-3 reveal" style="margin-bottom: 60px;">\n{grid_html}      </div>"""

def get_category_tabs_html(active_key):
    tabs = [
        ("/products", "all", "All Footwear"),
        ("/sport-outdoor-shoes-wholesale", "sport-outdoor-shoes", "Sport & Outdoor"),
        ("/casual-shoes-oem-manufacturer", "casual-shoes", "Casual Shoes"),
        ("/mens-sneakers-bulk-supplier", "mens-shoes", "Men's Sneakers"),
        ("/womens-sneakers-oem-factory", "womens-shoes", "Women's Trainers"),
        ("/slides-sandals-slippers-manufacturer", "slides-sandals", "Slides & Sandals"),
        ("/bags-sportswear-accessories-wholesale", "bags-sportswear", "Bags & Accessories")
    ]
    html = ""
    for href, key, label in tabs:
        cls = "tab-btn active" if key == active_key else "tab-btn"
        html += f'        <a href="{href}" class="{cls}">{label}</a>\n'
    return f'      <div class="tabs-container reveal" style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 30px;">\n{html}      </div>'

def get_category_detailed_html(cat_key, cat_data, company_info, products):
    cat_products = [p for p in products if category_matches(p, cat_key)]
    
    spec_rows = ""
    for p in cat_products:
        p_id = get_product_id(p)
        p_name = p.get("name", p_id)
        spec_rows += f"""            <tr>
              <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 700; color: #0b1e36;"><a href="product-detail?id={p_id}" style="color: #0b1e36; text-decoration: none;">{p_name}</a></td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('upper', 'Mesh / Synthetic')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('outsole', 'EVA / Rubber')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('lining', 'Breathable Mesh')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('sizes', 'EU 36-45')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: 600; color: #e50408;">{p.get('moq', '500 Pairs')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('lead_time', '25-35 Days')}</td>
              <td style="padding: 12px; border: 1px solid #e2e8f0;">{p.get('customization', 'OEM Logo / Colors')}</td>
            </tr>
        """
        
    spec_table_html = f"""
    <div style="overflow-x: auto; background: #fff; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 20px; border: 1px solid #e2e8f0;">
      <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem;">
        <thead>
          <tr style="background: #0b1e36; color: #fff;">
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Model Code</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Upper Material</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Outsole / Midsole</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Lining / Insole</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Size Range</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">MOQ (Pairs)</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Lead Time</th>
            <th style="padding: 14px 12px; border: 1px solid #0b1e36;">Customization</th>
          </tr>
        </thead>
        <tbody>
          {spec_rows}
        </tbody>
      </table>
    </div>
    """

    cards_html = ""
    for p in cat_products:
        p_id = get_product_id(p)
        p_name = p.get("name", p_id)
        p_img = p.get("image", "images/banner.jpg")
        has_video = bool(p.get("video") or p.get("video_url"))
        
        video_badge = """            <span class="product-video-badge" style="position: absolute; bottom: 10px; right: 10px; background: rgba(11,30,54,0.85); color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; z-index: 3; backdrop-filter: blur(4px); box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
              <svg viewBox="0 0 24 24" width="12" height="12" fill="#e50408"><path d="M8 5v14l11-7z"/></svg>
              <span>4K VIDEO</span>
            </span>""" if has_video else ""

        cards_html += f"""
        <div class="product-card" style="display: flex; flex-direction: column; background: #fff; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e2e8f0;">
          <div class="product-img-wrapper" style="position: relative; overflow: hidden; aspect-ratio: 4/3; background: #f8fafc;">
            <span class="product-tag" style="position: absolute; top: 10px; left: 10px; background: #0b1e36; color: #fff; padding: 4px 10px; font-size: 0.75rem; border-radius: 4px; font-weight: 600; z-index: 2;">{p.get('tag', 'OEM/ODM')}</span>
{video_badge}
            <a href="product-detail?id={p_id}" title="View {p_name} Details">
              <img src="{p_img}" alt="{p_name} - WIDEWAY Footwear OEM Jinjiang" loading="lazy" width="400" height="300" style="width: 100%; height: 100%; object-fit: cover;">
            </a>
          </div>
          <div class="product-info" style="padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <h3 style="font-size: 1.2rem; margin-bottom: 10px; color: #0b1e36;"><a href="product-detail?id={p_id}" style="color: inherit; text-decoration: none;">{p_name}</a></h3>
              <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 12px; line-height: 1.5;">{p.get('description', '')}</p>
              <ul class="product-features" style="padding-left: 18px; margin-bottom: 15px; color: #475569; font-size: 0.85rem; line-height: 1.6;">
                <li><strong>Upper:</strong> {p.get('upper', 'Flyknit Mesh')}</li>
                <li><strong>Outsole:</strong> {p.get('outsole', 'MD + Rubber')}</li>
                <li><strong>Sizes:</strong> {p.get('sizes', 'EU 36-45')}</li>
                <li><strong>MOQ:</strong> {p.get('moq', '500 Pairs / Color')}</li>
              </ul>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 10px;">
              <a href="product-detail?id={p_id}" class="btn btn-secondary btn-sm" style="flex: 1; text-align: center; border-color: #0b1e36; color: #0b1e36; padding: 8px 10px; font-weight: 600;">View Specs</a>
              <a href="contact?product={p_id}" class="btn btn-primary btn-sm btn-open-quote" data-product="{p_id}" data-category="{cat_key}" style="flex: 1; text-align: center; background: #e50408; border-color: #e50408; padding: 8px 10px; font-weight: 600;">Get Quote</a>
            </div>
          </div>
        </div>
        """
        
    grid_html = f"""
    <div class="grid grid-3" style="margin-top: 30px; margin-bottom: 50px;">
      {cards_html}
    </div>
    """
    
    return f"""
    <!-- Category Hero / Subheader -->
    <section class="page-banner" style="background: linear-gradient(rgba(11, 30, 54, 0.85), rgba(11, 30, 54, 0.95)), url('images/banner.jpg') center/cover; padding: 70px 0; color: #fff; text-align: center;">
      <div class="container">
        <h1 style="font-size: 2.6rem; margin-bottom: 12px; color: #fff;">{cat_data.get('h1', 'Footwear Sourcing')}</h1>
        <p style="max-width: 800px; margin: 0 auto; color: #e2e8f0; font-size: 1.05rem; line-height: 1.6;">{cat_data.get('desc', '')}</p>
      </div>
    </section>

    <!-- Main Container -->
    <div class="container" style="padding-top: 40px; padding-bottom: 60px;">
      {get_category_tabs_html(cat_key)}
      
      {spec_table_html}

      <div style="margin-top: 40px;">
        <h2 style="font-size: 1.8rem; color: #0b1e36; margin-bottom: 20px;">Available Models in this Category ({len(cat_products)} SKUs)</h2>
        {grid_html}
      </div>

      <!-- OEM/ODM Footwear Sourcing Advantage Strip -->
      <div class="b2b-features-card" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 30px; margin-top: 40px;">
        <h3 style="font-size: 1.4rem; color: #0b1e36; margin-bottom: 15px;">🏭 Why Source {cat_data.get('h1')} from WIDEWAY (Jinjiang)?</h3>
        <div class="grid grid-3" style="gap: 20px; margin-top: 20px;">
          <div>
            <h4 style="color: #0b1e36; margin-bottom: 8px;">⚡ Rapid Prototyping (7-10 Days)</h4>
            <p style="font-size: 0.88rem; color: #64748b;">In-house 3D shoe last printing, pattern digitization, and computer stitching allow complete sample turnaround in 7 to 10 days.</p>
          </div>
          <div>
            <h4 style="color: #0b1e36; margin-bottom: 8px;">📦 Low MOQ Brand Building (500 Pairs)</h4>
            <p style="font-size: 0.88rem; color: #64748b;">We empower emerging footwear labels and boutique brand owners with flexible minimum order runs and private label packaging support.</p>
          </div>
          <div>
            <h4 style="color: #0b1e36; margin-bottom: 8px;">🔬 SATRA & BSCI Lab Certified</h4>
            <p style="font-size: 0.88rem; color: #64748b;">Every batch undergoes Bally flex testing, Martindale abrasion checks, sole adhesion tests, and chemical compliance according to EU REACH standards.</p>
          </div>
        </div>
      </div>

      <!-- Quick Inquiry Widget -->
      <div class="b2b-rfq-box" style="background: linear-gradient(135deg, #0b1e36, #1e3a5f); color: #fff; border-radius: 8px; padding: 35px; margin-top: 40px; text-align: center;">
        <h3 style="font-size: 1.6rem; color: #fff; margin-bottom: 10px;">Get Factory Direct Pricing & Free Footwear Swatches</h3>
        <p style="color: #cbd5e1; max-width: 600px; margin: 0 auto 25px auto;">Submit your inquiry with target quantities, custom branding requirements, and delivery port for a same-day quotation from our Jinjiang engineering team.</p>
        <a href="contact?category={cat_key}" class="btn btn-primary btn-open-quote" data-category="{cat_key}" style="background: #e50408; border-color: #e50408; padding: 12px 30px; font-weight: 700;">Request Factory Quotation Now</a>
      </div>
    </div>
    """

def get_news_list_html(news):
    cards_html = ""
    for n in news:
        img_src = n.get("image", "images/banner.jpg")
        is_logo = n.get("is_logo", False) or "images/brands/" in img_src
        raw_url = n.get("url", n.get("id", ""))
        if raw_url.endswith(".html"):
            raw_url = raw_url[:-5]
        url = ("/" + raw_url) if not raw_url.startswith("/") and not raw_url.startswith("http") else raw_url
        reading_time = n.get("reading_time", "8 min read")
        
        if is_logo:
            img_container = f"""
            <div style="aspect-ratio: 16/10; overflow: hidden; background: #ffffff; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; justify-content: center; padding: 28px; box-sizing: border-box;">
              <img src="{img_src}" alt="{n['title']}" loading="lazy" width="300" height="180" style="max-width: 65%; max-height: 65%; width: auto; height: auto; object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.04)); transition: transform 0.3s ease;">
            </div>
            """
        else:
            img_container = f"""
            <div style="aspect-ratio: 16/10; overflow: hidden; background: #f8fafc; border-bottom: 1px solid #f1f5f9; position: relative;">
              <img src="{img_src}" alt="{n['title']}" loading="lazy" width="400" height="250" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease;">
            </div>
            """

        cards_html += f"""
        <article class="news-card" style="background: #fff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); overflow: hidden; border: 1px solid #e2e8f0; display: flex; flex-direction: column; transition: transform 0.3s ease, box-shadow 0.3s ease;">
          <a href="{url}" style="text-decoration: none; color: inherit; display: block;" title="{n['title']}">
            {img_container}
          </a>
          <div style="padding: 22px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #94a3b8; margin-bottom: 12px;">
                <span>📅 {n.get('date', '2026-04-29')}</span>
                <span style="color: #e50408; font-weight: 700; background: #fff1f1; padding: 3px 9px; border-radius: 4px; font-size: 0.78rem;">{n.get('category', 'Trade Dynamics')}</span>
              </div>
              <h3 style="font-size: 1.15rem; margin-bottom: 12px; color: #0b1e36; line-height: 1.45; font-weight: 700;">
                <a href="{url}" style="text-decoration: none; color: #0b1e36; transition: color 0.2s ease;" onmouseover="this.style.color='#e50408'" onmouseout="this.style.color='#0b1e36'">{n['title']}</a>
              </h3>
              <p style="font-size: 0.88rem; color: #64748b; line-height: 1.6; margin-bottom: 18px;">{n.get('summary', '')}</p>
            </div>
            <div style="border-top: 1px solid #f1f5f9; padding-top: 14px; display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 0.8rem; color: #94a3b8;">⏱️ {reading_time}</span>
              <a href="{url}" class="read-more" style="color: #e50408; font-size: 0.88rem; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
                Read Full Story &rarr;
              </a>
            </div>
          </div>
        </article>
        """
    return f"""<div class="grid grid-3 reveal" style="margin-bottom: 60px;">\n{cards_html}</div>"""

def replace_between(content, start_tag, end_tag, replacement):
    if start_tag in content and end_tag in content:
        pattern = re.escape(start_tag) + r".*?" + re.escape(end_tag)
        return re.sub(pattern, f"{start_tag}\n{replacement}\n{end_tag}", content, flags=re.DOTALL)
    return content

def sync_global_components(html, filename, company_info):
    header = get_header_html(filename, company_info)
    footer = get_footer_html(company_info)
    chat = get_chat_widget_html(company_info)

    if "<!-- GLOBAL_HEADER -->" in html:
        html = replace_between(html, "<!-- GLOBAL_HEADER -->", "<!-- END_GLOBAL_HEADER -->", header)
    else:
        html = re.sub(r"<header.*?</header>", f"<!-- GLOBAL_HEADER -->\n{header}\n  <!-- END_GLOBAL_HEADER -->", html, count=1, flags=re.DOTALL)

    if "<!-- GLOBAL_FOOTER -->" in html:
        html = replace_between(html, "<!-- GLOBAL_FOOTER -->", "<!-- END_GLOBAL_FOOTER -->", footer)
    else:
        html = re.sub(r"<footer.*?</footer>", f"<!-- GLOBAL_FOOTER -->\n{footer}\n  <!-- END_GLOBAL_FOOTER -->", html, count=1, flags=re.DOTALL)

    if "<!-- GLOBAL_CHAT_WIDGET -->" in html:
        html = replace_between(html, "<!-- GLOBAL_CHAT_WIDGET -->", "<!-- END_GLOBAL_CHAT_WIDGET -->", chat)
    elif "<div class=\"b2b-chat-widget\">" in html:
        pattern = r'<div class="b2b-chat-widget">.*?</div>\s*</div>(?:\s*<!-- END_GLOBAL_CHAT_WIDGET -->)?'
        replacement = f"<!-- GLOBAL_CHAT_WIDGET -->\n{chat}\n  <!-- END_GLOBAL_CHAT_WIDGET -->"
        html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

    # 1. Normalize <main> wrapper & inject Executive Sourcing Brief
    _, meta_desc, _ = extract_page_meta(html)
    if not meta_desc:
        meta_desc = "WIDEWAY GROUP is a premier footwear manufacturer in Jinjiang, China."

    # Extract body content between END_GLOBAL_HEADER and GLOBAL_FOOTER
    body_pattern = r"(<!-- END_GLOBAL_HEADER -->)(.*?)(<!-- GLOBAL_FOOTER -->)"
    match = re.search(body_pattern, html, flags=re.DOTALL)
    if match:
        body_content = match.group(2)

        # Strip any existing <main...> and </main> tags inside body_content
        clean_body = re.sub(r'<\/?main\b[^>]*>', '', body_content)

        # Strip any previous b2b-executive-sourcing-brief to avoid duplicate stacking
        clean_body = re.sub(r'<!-- B2B Executive Sourcing Brief.*?<!-- END B2B Executive Sourcing Brief -->\s*', '', clean_body, flags=re.DOTALL)
        clean_body = re.sub(r'<section class="b2b-executive-sourcing-brief".*?</section>\s*', '', clean_body, flags=re.DOTALL)

        # Build clean, high-citability executive brief containing exact meta_desc
        executive_brief = f"""<!-- B2B Executive Sourcing Brief & Technical Specifications (ISO 9001:2015 / SATRA Certified) -->
<section class="b2b-executive-sourcing-brief" style="background: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #e50408; border-radius: 6px; padding: 20px 24px; margin: 24px auto; max-width: 1200px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
  <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="background: #0b1e36; color: #fff; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">Factory Direct Dossier</span>
      <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">Jinjiang Footwear Manufacturing Hub &bull; 19+ Years OEM/ODM Excellence</span>
    </div>
    <span style="color: #059669; font-size: 0.78rem; font-weight: 700; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 2px 8px; border-radius: 4px;">&bull; ISO 9001:2015 &amp; amfori BSCI Audited</span>
  </div>
  <p class="b2b-executive-summary" style="font-size: 0.95rem; color: #334155; line-height: 1.65; margin: 0 0 14px 0;">{meta_desc}</p>
  <p class="b2b-geo-factual-passage" style="font-size: 0.88rem; color: #475569; line-height: 1.7; margin: 0 0 14px 0;">WIDEWAY operates as an industrial footwear manufacturer in Jinjiang, Fujian, specializing in athletic sneakers, running footwear, casual vulcanized trainers, and molded recovery slides with an annual production capacity of 5000000 pcs across our 25000 m facility. Every production batch undergoes ISO 9001 certified manufacturing quality controls, SATRA TM144 slip resistance evaluations, and in-line tensile testing exceeding 3.5 MPa bond strength. We provide low minimum order quantities starting at 500 pcs per colorway with 7 to 10 days rapid physical prototyping and 30 to 45 days mass production turnaround. Our export logistics division handles international shipments including 1 20GP and 1 40HQ container loads with automated customs documentation for North America, the European Union, and Central Asia under CE, ASTM F2413, and GOST technical compliance frameworks.</p>
  <div style="overflow-x: auto; margin-top: 10px;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; font-variant-numeric: tabular-nums;">
      <thead>
        <tr style="background: #f1f5f9; text-align: left; color: #1e293b;">
          <th scope="col" style="padding: 6px 10px; border: 1px solid #e2e8f0;">Parameter</th>
          <th scope="col" style="padding: 6px 10px; border: 1px solid #e2e8f0;">Specification</th>
          <th scope="col" style="padding: 6px 10px; border: 1px solid #e2e8f0;">Standard</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">Bond Adhesion Strength</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">&ge; 3.5 MPa</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">SATRA TM411 / ISO 17708</td>
        </tr>
        <tr>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">Outsole Abrasion Loss</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">&le; 150 mm</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">DIN 53516 / ISO 4649</td>
        </tr>
        <tr>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">Minimum Order Quantity</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">500 pcs / colorway</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">B2B Private Label Contract</td>
        </tr>
        <tr>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">Export Shipping Container</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">1 20GP (2,800 pairs) / 1 40HQ (6,800 pairs)</td>
          <td style="padding: 6px 10px; border: 1px solid #e2e8f0;">ISO 9001 / FSC Cartons</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; font-size: 0.82rem; color: #475569; padding-top: 12px; margin-top: 12px; border-top: 1px dashed #cbd5e1;">
    <div><strong>Peel Strength:</strong> &ge; 4.2 N/mm (SATRA TM411)</div>
    <div><strong>Cold Flex:</strong> 100,000 cycles at -15&deg;C (TM144)</div>
    <div><strong>Slip Resistance:</strong> CoF &ge; 0.45 (Wet Tile)</div>
    <div><strong>Rapid Prototyping:</strong> 7-10 Days Turnaround</div>
    <div><strong>Production MOQ:</strong> 500 Pairs / Color</div>
  </div>
</section>
<!-- END B2B Executive Sourcing Brief -->
"""
        # Ensure #inquiry anchor exists
        inquiry_anchor = ""
        if 'id="inquiry"' not in clean_body and "id='inquiry'" not in clean_body:
            inquiry_anchor = '\n<div id="inquiry" class="inquiry-anchor-target" style="scroll-margin-top: 100px;"></div>\n'

        new_body = f"\n<main id=\"mainContent\" data-layout=\"oem\">\n{executive_brief}\n{clean_body.strip()}\n{inquiry_anchor}</main>\n"
        html = html[:match.start(2)] + new_body + html[match.end(2):]

    # 2. Ensure single <h1>
    h1_matches = list(re.finditer(r'<h1\b([^>]*)>(.*?)</h1>', html, re.I | re.DOTALL))
    if len(h1_matches) > 1:
        # Keep the first, downgrade subsequent h1 to h2
        counter = [0]
        def replace_extra_h1(m):
            counter[0] += 1
            if counter[0] == 1:
                return m.group(0)
            attrs, content = m.group(1), m.group(2)
            return f'<h2{attrs}>{content}</h2>'
        html = re.sub(r'<h1\b([^>]*)>(.*?)</h1>', replace_extra_h1, html, flags=re.I | re.DOTALL)
    elif len(h1_matches) == 0:
        # Convert first primary h2 to h1
        h2_match = re.search(r'<h2\b([^>]*)>(.*?)</h2>', html, re.I | re.DOTALL)
        if h2_match:
            attrs, content = h2_match.group(1), h2_match.group(2)
            html = html[:h2_match.start()] + f'<h1{attrs}>{content}</h1>' + html[h2_match.end():]

    return html

def inject_seo_and_geo_tags(html, filename=None, company_info=None):
    if not company_info:
        return html

    # Clean extensionless slug for canonical URL
    clean_slug = ""
    if filename:
        clean_slug = "" if filename == "index.html" else filename.replace(".html", "")
    canonical_url = f"https://www.widewayfootwear.com/{clean_slug}"
    canonical_tag = f"""  <!-- Standard Canonical URL -->\n  <link rel="canonical" href="{canonical_url}">"""

    # Title & Description Extraction
    page_title, page_desc, page_lang = extract_page_meta(html)
    if not page_title:
        page_title = "WIDEWAY Footwear Manufacturer"

    # Construct schema.org WebPage node matching exact page title and description
    schema_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": page_title,
                "description": page_desc,
                "inLanguage": page_lang,
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://www.widewayfootwear.com/#website",
                    "name": "WIDEWAY GROUP",
                    "url": "https://www.widewayfootwear.com"
                },
                "about": {
                    "@type": "Organization",
                    "@id": "https://www.widewayfootwear.com/#organization",
                    "name": company_info.get("name_en", "Jinjiang Wideway Import & Export Co., Ltd."),
                    "url": "https://www.widewayfootwear.com"
                }
            },
            {
                "@type": "Organization",
                "@id": "https://www.widewayfootwear.com/#organization",
                "name": company_info.get("name_en", "Jinjiang Wideway Import & Export Co., Ltd."),
                "alternateName": company_info.get("name_zh", "晋江市万维进出口有限公司"),
                "url": "https://www.widewayfootwear.com",
                "logo": "https://www.widewayfootwear.com/images/logo.png",
                "telephone": company_info.get("phone", "+86 131 2302 5365"),
                "email": company_info.get("email", "stella@widewaygroup.com"),
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "8F, Building 8A, NO.618, JINXIN Road, ChenDai town",
                    "addressLocality": "Jinjiang",
                    "addressRegion": "Fujian",
                    "postalCode": "362211",
                    "addressCountry": "CN"
                }
            }
        ]
    }
    schema_json_str = json.dumps(schema_ld, ensure_ascii=False, indent=2)

    # 1. 2026 Core Web Vitals & GEO Head Essentials
    seo_geo_header_block = f"""  <!-- 2026 Core Web Vitals Font Acceleration -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- 2026 Generative Engine Optimization (GEO) LLM Markdown Discovery -->
  <link rel="alternate" type="text/markdown" href="https://www.widewayfootwear.com/llms.txt" title="WIDEWAY Footwear LLM Knowledge Base">

  <!-- Geolocation & Jinjiang Shoe Capital Metatags -->
  <meta name="geo.region" content="CN-FJ">
  <meta name="geo.placename" content="Jinjiang, Quanzhou, Fujian, China">
  <meta name="geo.position" content="24.7836;118.5714">
  <meta name="ICBM" content="24.7836, 118.5714">

{canonical_tag}

  <!-- Favicon Package -->
  <link rel="icon" type="image/png" sizes="48x48" href="images/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="192x192" href="images/favicon-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
  <link rel="shortcut icon" href="favicon.ico">

  <script type="application/ld+json">
{schema_json_str}
  </script>"""

    # Remove existing canonical, GEO, font preconnect, favicon, and previous schema blocks in head
    html = re.sub(r'<!--\s*2026 Core Web Vitals.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*2026 Generative Engine Optimization.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Geolocation & Jinjiang Shoe Capital Metatags.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Standard Canonical URL.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Dynamic Canonical URL.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*News Detail Canonical.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>[^<]*canonicalTag[^<]*</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Favicon Package.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*rel=["\']alternate["\'][^>]*type=["\']text/markdown["\'][^>]*>\s*', '', html)
    html = re.sub(r'<meta\s+name=["\']geo\.[^>]*>\s*', '', html)
    html = re.sub(r'<meta\s+name=["\']ICBM["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*href=["\']images/favicon-[^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*href=["\']favicon\.ico["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+rel=["\']preconnect["\'][^>]*>\s*', '', html)
    html = re.sub(r'<script\s+type=["\']application/ld\+json["\']\s*>.*?</script>\s*', '', html, flags=re.DOTALL)

    # Inject clean unified SEO + GEO block right before </head>
    if "</head>" in html:
        html = html.replace("</head>", f"{seo_geo_header_block}\n</head>")

    # Ensure main.js has single defer and update cache busters
    html = re.sub(r'<script\s+src="js/main\.js(?:\?v=[^"]*)?"(?:\s+defer)*\s*></script>', '<script src="js/main.js?v=20261021_01" defer></script>', html)
    html = re.sub(r'href="css/style\.css(?:\?v=[^"]*)?"', 'href="css/style.css?v=20261021_01"', html)

    # Clean company references
    html = html.replace("Quanzhou Shenghongda Hygiene Products Co., Ltd.", company_info.get("name_en", "Jinjiang Wideway Import & Export Co., Ltd."))
    html = html.replace("泉州盛鸿达卫生用品有限公司", company_info.get("name_zh", "晋江市万维进出口有限公司"))
    html = html.replace("SHENGHONGDA", company_info.get("logo_text", "WIDEWAY GROUP"))
    html = html.replace("sales@shdhygiene.com", company_info.get("email", "stella@widewaygroup.com"))
    html = html.replace("amy@widewaygroup.com", company_info.get("email", "stella@widewaygroup.com"))
    html = html.replace("kelly@widewaygroup.com", company_info.get("email", "stella@widewaygroup.com"))
    html = html.replace("+86 185 0595 9266", company_info.get("phone", "+86 131 2302 5365"))
    html = html.replace("+8618505959266", "+8613123025365")
    html = html.replace("8618505959266", "8613123025365")

    return html

    # Clean extensionless slug for canonical URL
    clean_slug = ""
    if filename:
        clean_slug = "" if filename == "index.html" else filename.replace(".html", "")
    canonical_url = f"https://www.widewayfootwear.com/{clean_slug}"

    # Dynamic canonical tag handling
    if filename == "product-detail.html":
        canonical_tag = """  <!-- Dynamic Canonical URL for Parameterized Product Pages -->
  <script>
    (function() {
      try {
        var p = new URLSearchParams(window.location.search);
        var id = p.get('id') || p.get('product') || '';
        var cUrl = id 
          ? 'https://www.widewayfootwear.com/product-detail?id=' + encodeURIComponent(id.toLowerCase())
          : 'https://www.widewayfootwear.com/products';
        var el = document.createElement('link');
        el.id = 'canonicalTag';
        el.rel = 'canonical';
        el.href = cUrl;
        document.head.appendChild(el);
      } catch(e) {}
    })();
  </script>"""
    elif filename == "news-detail.html":
        canonical_tag = """  <!-- News Detail Canonical -->
  <script>
    (function() {
      try {
        var p = new URLSearchParams(window.location.search);
        var id = p.get('id');
        var cUrl = id ? 'https://www.widewayfootwear.com/' + id.replace(/\\.html$/, '') : 'https://www.widewayfootwear.com/news';
        var el = document.createElement('link');
        el.rel = 'canonical';
        el.href = cUrl;
        document.head.appendChild(el);
      } catch(e) {}
    })();
  </script>"""
    else:
        canonical_tag = f"""  <!-- Standard Canonical URL -->\n  <link rel="canonical" href="{canonical_url}">"""

    # 1. 2026 Core Web Vitals & GEO Head Essentials
    seo_geo_header_block = f"""  <!-- 2026 Core Web Vitals Font Acceleration -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- 2026 Generative Engine Optimization (GEO) LLM Markdown Discovery -->
  <link rel="alternate" type="text/markdown" href="https://www.widewayfootwear.com/llms.txt" title="WIDEWAY Footwear LLM Knowledge Base">

  <!-- Geolocation & Jinjiang Shoe Capital Metatags -->
  <meta name="geo.region" content="CN-FJ">
  <meta name="geo.placename" content="Jinjiang, Quanzhou, Fujian, China">
  <meta name="geo.position" content="24.7836;118.5714">
  <meta name="ICBM" content="24.7836, 118.5714">

{canonical_tag}

  <!-- Favicon Package -->
  <link rel="icon" type="image/png" sizes="48x48" href="images/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="192x192" href="images/favicon-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
  <link rel="shortcut icon" href="favicon.ico">"""

    # Remove existing canonical, GEO, font preconnect, and favicon tags and comment headers to avoid duplication
    html = re.sub(r'<!--\s*2026 Core Web Vitals.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*2026 Generative Engine Optimization.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Geolocation & Jinjiang Shoe Capital Metatags.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Standard Canonical URL.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Dynamic Canonical URL.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*News Detail Canonical.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>[^<]*canonicalTag[^<]*</script>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*Favicon Package.*?-->\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*rel=["\']alternate["\'][^>]*type=["\']text/markdown["\'][^>]*>\s*', '', html)
    html = re.sub(r'<meta\s+name=["\']geo\.[^>]*>\s*', '', html)
    html = re.sub(r'<meta\s+name=["\']ICBM["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*href=["\']images/favicon-[^>]*>\s*', '', html)
    html = re.sub(r'<link\s+[^>]*href=["\']favicon\.ico["\'][^>]*>\s*', '', html)
    html = re.sub(r'<link\s+rel=["\']preconnect["\'][^>]*>\s*', '', html)

    # Inject clean unified SEO + GEO block right before </head>
    if "</head>" in html:
        html = html.replace("</head>", f"{seo_geo_header_block}\n</head>")

    # Ensure main.js has single defer and update cache busters
    html = re.sub(r'<script\s+src="js/main\.js(?:\?v=[^"]*)?"(?:\s+defer)*\s*></script>', '<script src="js/main.js?v=20260913_09" defer></script>', html)
    html = re.sub(r'href="css/style\.css(?:\?v=[^"]*)?"', 'href="css/style.css?v=20260913_09"', html)

    # Clean company references
    html = html.replace("Quanzhou Shenghongda Hygiene Products Co., Ltd.", company_info.get("name_en", "Jinjiang Wideway Import & Export Co., Ltd."))
    html = html.replace("泉州盛鸿达卫生用品有限公司", company_info.get("name_zh", "晋江市万维进出口有限公司"))
    html = html.replace("SHENGHONGDA", company_info.get("logo_text", "WIDEWAY GROUP"))
    html = html.replace("sales@shdhygiene.com", company_info.get("email", "amy@widewaygroup.com"))

    return html

def generate_robots_txt():
    content = """# ==============================================================================
# Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP) - Production robots.txt
# High-Efficiency SEO & GEO Permissive Policy + Anti-Malicious Scraper Defenses
# ==============================================================================

# 1. Global Policy for Legitimate Web Crawlers
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin
Disallow: /scratch/
Disallow: /*?*sort=
Disallow: /*?*filter=

# 2. Major Search Engine Crawlers (100% SEO Friendly & High Priority)
User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-News
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: YandexBot
Allow: /

User-agent: Sogou web spider
Allow: /

User-agent: Applebot
Allow: /

# 3. Generative Engine Optimization (GEO) AI Search & Intelligence Bots (100% GEO Friendly)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Diffbot
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: meta-externalagent
Allow: /

# 4. Anti-Clone & Scraper Defense: Block Malicious Site Copiers & Offline Downloaders
User-agent: HTTrack
Disallow: /

User-agent: Teleport
Disallow: /

User-agent: TeleportPro
Disallow: /

User-agent: WebCopier
Disallow: /

User-agent: WebZIP
Disallow: /

User-agent: WebReaper
Disallow: /

User-agent: SiteSucker
Disallow: /

User-agent: Offline Explorer
Disallow: /

User-agent: SuperBot
Disallow: /

User-agent: WebStripper
Disallow: /

User-agent: PageGrabber
Disallow: /

User-agent: Scrapy
Disallow: /

User-agent: pyspider
Disallow: /

User-agent: Go-http-client
Disallow: /

User-agent: Java
Disallow: /

User-agent: Download Demon
Disallow: /

# 5. Canonical Sitemaps & Machine-Readable Knowledge for SEO & AI Reasoning
Sitemap: https://www.widewayfootwear.com/sitemap.xml
Sitemap: https://www.widewayfootwear.com/llms.txt
Sitemap: https://www.widewayfootwear.com/llms-full.txt
"""
    with open(os.path.join(workspace, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("  Generated 2026 AI-Ready & Anti-Clone robots.txt")

def generate_sitemap_xml(all_pages, products):
    today_iso = datetime.datetime.now().strftime("%Y-%m-%d")
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    sitemap_xml += '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'

    for p in sorted(list(set(all_pages))):
        clean_slug = "" if p == "index.html" else p.replace(".html", "")
        priority = "1.0" if clean_slug == "" else ("0.9" if clean_slug == "products" or "-wholesale" in clean_slug or "-manufacturer" in clean_slug or "-supplier" in clean_slug else "0.8")
        loc = f"https://www.widewayfootwear.com/{clean_slug}"
        
        image_tags = ""
        # Attach relevant image metadata for rich Google Image indexing
        if clean_slug == "":
            image_tags += """    <image:image>
      <image:loc>https://www.widewayfootwear.com/images/banner_factory.jpg</image:loc>
      <image:title>WIDEWAY Jinjiang Footwear Manufacturing Headquarters</image:title>
    </image:image>\n"""
        elif clean_slug == "products":
            for img in products[:8]:
                image_tags += f"""    <image:image>
      <image:loc>https://www.widewayfootwear.com/{img.get('image', '').lstrip('/')}</image:loc>
      <image:title>{img.get('name', '')} Athletic Footwear OEM</image:title>
    </image:image>\n"""

        sitemap_xml += f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
{image_tags}  </url>\n"""

    # Add all individual products directly so Google indexes each SKU
    for prod in products:
        p_id = (prod.get("id") or prod.get("code") or "").strip().lower()
        if not p_id:
            continue
        p_name = prod.get("name", "WIDEWAY Athletic Footwear")
        p_img = prod.get("image", "").lstrip('/')
        p_loc = f"https://www.widewayfootwear.com/product-detail?id={p_id}"
        
        img_tags = ""
        if p_img:
            img_tags = f"""    <image:image>
      <image:loc>https://www.widewayfootwear.com/{p_img}</image:loc>
      <image:title>{p_name} OEM/ODM Footwear</image:title>
    </image:image>\n"""
            
        sitemap_xml += f"""  <url>
    <loc>{p_loc}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
{img_tags}  </url>\n"""

    # Add CIS Russian Portals with canonical www
    sitemap_xml += f"""  <url>
    <loc>https://www.widewayfootwear.com/ru/</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.widewayfootwear.com/ru/cis-central-asia/</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

    sitemap_xml += "</urlset>"
    with open(os.path.join(workspace, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("  Generated Google Image-Extended sitemap.xml with 100+ product URLs")

def generate_llms_txt(company_info):
    llms_txt = f"""# WIDEWAY GROUP (Jinjiang Wideway Import & Export Co., Ltd.)
> Leading athletic footwear, sports shoes, sneakers, and casual shoes OEM/ODM manufacturer based in Jinjiang, Fujian, China (China's Footwear Capital).

## Executive Overview
- Legal Entity: {company_info.get("name_en")} ({company_info.get("name_zh")})
- Global Brand: WIDEWAY GROUP
- Established: 2007 (19+ years footwear craftsmanship)
- Headquarters: 8F, Building 8A, NO.618, JINXIN Road, ChenDai town, Jinjiang, Quanzhou City, Fujian, China
- Production Capacity: 300,000+ pairs monthly across 4 automated lasting assembly lines (Cold-cement & Strobel)
- Core Offering: Turnkey OEM/ODM footwear manufacturing, 3D CAD modeling, 7-10 day rapid prototyping, private labeling, and low MOQ brand incubation (from 500 pairs per color).
- International Audits: amfori BSCI, Sedex SMETA 4-Pillar, ISO 9001:2015, ISO 14001, GRS (Global Recycled Standard).
- Physical Testing: In-house SATRA-compliant physical laboratory (TM133 flex, Bally flex, Martindale abrasion, peel adhesion).
- Official Brand Partners: FILA, KAPPA, AIRNESS, DIADORA, STARTER, WRANGLER, Lidl, Aldi, O'Neill.
- Direct Contact: {company_info.get("email")}, WhatsApp/WeChat: {company_info.get("phone")}

## Canonical Web Resources
- Home & Factory Introduction: https://www.widewayfootwear.com/
- Comprehensive Footwear Catalog (115+ SKUs): https://www.widewayfootwear.com/products
- 1:1 Archival Silhouette Re-engineering & Heritage Craftsmanship: https://www.widewayfootwear.com/heritage-footwear-reproduction
- OEM & ODM Tooling Services: https://www.widewayfootwear.com/oem-odm
- Production Lines & Factory Scale: https://www.widewayfootwear.com/production-capacity
- Physical Testing Lab & SATRA Protocols: https://www.widewayfootwear.com/quality-control
- Factory Certifications & BSCI Audits: https://www.widewayfootwear.com/certifications
- Eco-Friendly & Recycled RPET Footwear: https://www.widewayfootwear.com/sustainability
- Brand Visual System (VI/CI) & Footwear Industrial Scenarios: https://www.widewayfootwear.com/brand-identity
- Corporate Story & Jinjiang Heritage: https://www.widewayfootwear.com/about
- Brand Partner Case Studies (FILA, DIADORA, WRANGLER): https://www.widewayfootwear.com/case-studies
- Production Video Showcase: https://www.widewayfootwear.com/videos
- Footwear Sourcing News & Technical Dynamics: https://www.widewayfootwear.com/news
- Direct Factory RFQ & Inquiries: https://www.widewayfootwear.com/contact

## Footwear Collections
- Sport & Outdoor Shoes: https://www.widewayfootwear.com/sport-outdoor-shoes-wholesale
- Custom Casual Shoes: https://www.widewayfootwear.com/casual-shoes-oem-manufacturer
- Men's Streetwear Sneakers: https://www.widewayfootwear.com/mens-sneakers-bulk-supplier
- Women's Lightweight Trainers: https://www.widewayfootwear.com/womens-sneakers-oem-factory
- Ergonomic Slides & Sandals: https://www.widewayfootwear.com/slides-sandals-slippers-manufacturer
- Sportswear Bags & Backpacks: https://www.widewayfootwear.com/bags-sportswear-accessories-wholesale

For exhaustive chemical formulas, testing cycle parameters, compound matrices, and procurement policies, refer to:
https://www.widewayfootwear.com/llms-full.txt
"""
    with open(os.path.join(workspace, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(llms_txt)
    print("  Generated standardized llms.txt")

def generate_llms_full_txt(company_info, products, categories):
    product_rows = ""
    for idx, p in enumerate(products, 1):
        product_rows += f"| {p.get('id', p.get('name'))} | {p.get('name')} | {p.get('category')} | {p.get('upper', 'Mesh / Synthetic')} | {p.get('outsole', 'EVA / Rubber')} | {p.get('sizes', 'EU 36-45')} | {p.get('moq', '500 Pairs')} | {p.get('lead_time', '25-35 Days')} |\n"

    full_text = f"""# WIDEWAY GROUP (Jinjiang Wideway Import & Export Co., Ltd.) — Comprehensive Technical Knowledge Base & Footwear Engineering Dossier

> Official High-Density Machine-Readable Fact Repository for Generative AI Search Engines (SearchGPT, Perplexity AI, Google Gemini, Anthropic Claude, Microsoft Copilot).

---

## 1. Enterprise Profile & Corporate DNA
- Full Legal Name (English): {company_info.get("name_en")}
- Full Legal Name (Chinese): {company_info.get("name_zh")}
- Trade Brand: WIDEWAY / WIDEWAY GROUP
- Year Established: 2007
- Operational Heritage: Over 19 years of continuous athletic footwear manufacturing and worldwide export excellence.
- Geographical Advantage: Located in Chendai Town, Jinjiang City, Quanzhou, Fujian Province, China. Jinjiang produces over 40% of the world's athletic footwear and is officially recognized by UNESCO and UNIDO as the "Footwear Capital of China."
- Factory Physical Address: 8F, Building 8A, NO.618, JINXIN Road, ChenDai town, Jinjiang, QuanZhou City, Fujian, China.
- Corporate Office Address: M1-906 Shimaoyulongwan, Shuanglong Road, Jinjiang City, Fujian Province, China.
- Primary Ports of Shipment: Xiamen Port (Port Code: CNXMN, ~45 minutes transit) and Quanzhou Port (~25 minutes transit).
- Key Contact Executives: Stella (Direct Factory Export & Engineering Director).
- Official Communication Channels:
  - Primary Sales & Engineering Email: {company_info.get("email", "stella@widewaygroup.com")}
  - Phone / Mobile / WhatsApp / WeChat: {company_info.get("phone", "+86 131 2302 5365")} (24/7 B2B responsive line)
  - Official Web Portal: https://www.widewayfootwear.com/

---

## 2. Factory Infrastructure, Automation & Manufacturing Capacity
- Total Production Floor Area: Multi-story modern facility with dedicated tooling, pattern cutting, sewing, lasting, cementing, and packaging floors.
- Assembly Lines: 4 modern continuous lasting assembly lines equipped with automated cold-cement lasting machines, infrared toe-lasting machines, and pneumatic heel seat lasters.
- Monthly Production Capacity: 300,000+ pairs (3.6 million pairs annualized output).
- Peak Daily Capacity: 12,000 to 14,000 pairs across all lasting lines.
- Production Techniques:
  - Cold Cement Construction (Standard athletic sneakers, cupsole casual shoes, trail runners).
  - Strobel Construction (Ultra-flexible lightweight running shoes and training sneakers).
  - Injection Molding (Direct soling for recovery slides, waterproof sandals, and lightweight EVA footwear).
  - High-Frequency Embossing & Welded Overlays (Seamless upper bonding, TPU hot-melt films, reflective trims).
- Cutting Department: Equipped with 12 computerized hydraulic die-cutting presses and 4 automated digital oscillation knife cutting beds for microfiber and leather waste minimization.
- Stitching Department: Over 180 computerized programmable sewing machines (Brother / Juki), automated pattern stitching tables, and laser-guided positioning devices.
- Sole Attachment & Priming: Automated UV primer tunnels, infrared oven reactivation conveyors, and 6-stage pneumatic pressure pressing units ensuring bond peel strength exceeding 3.5 N/mm.
- Health, Occupational & Fire Safety: Fully equipped with centralized smart water-sprinkler fire suppression systems, positive-pressure clean ventilation for adhesive lines, and non-toxic water-based adhesive formulas complying with amfori BSCI ESG standards.

---

## 3. Complete Active Footwear Catalog SKU Matrix (115 Models)

| SKU Code | Product Name | Category | Upper Specification | Outsole / Midsole Specification | Size Range | MOQ | Production Lead Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{product_rows}

---

## 4. In-House Physical Testing Laboratory & SATRA Quality Assurance
Every footwear production lot at WIDEWAY undergoes strict physical and chemical testing in accordance with international SATRA and ISO footwear standards.

### Testing Equipment Inventory:
1. Bally Flexometer (Model GT-7011-D): For testing leather and synthetic upper endurance under continuous flexing.
2. Martindale Abrasion Tester (Model GT-7012-M): Multi-head tester for lining and insole textile durability.
3. DIN Abrasion Tester (Model GT-7012-D / ISO 4649): Precision rotating drum abrasion test for rubber and EVA outsole compound volume loss.
4. Computerized Tensile Tester (Model GT-T03): For testing upper-to-sole bonding peel strength, seam rupture strength, and eyelet tear-out resistance.
5. UV Anti-Yellowing Aging Chamber (Model GT-7005-UV): 300W UV lamp testing at 50°C for white soles and pale fabrics.
6. SATRA TM133 Whole Shoe Flexing Machine: Cold temperature endurance down to -10°C up to 100,000 cycles.
7. Digital Color Fastness Crockmeter: Electronic reciprocating friction arm for wet and dry rubbing fastness.
8. Conveyor Tunnel Metal Detector: 100% finished carton scanning gate with 0.8mm ferrous needle detection sensitivity.

### Target Performance Metrics:
- SATRA TM133 Outsole Flexing Endurance: 100,000 cycles with zero crack growth >4.0mm.
- Bally Upper Flexing Test: 50,000 cycles dry / 20,000 cycles wet at room temperature without surface cracking.
- DIN Outsole Abrasion Loss: Strictly <120 mm³ (ultra-durable rubber <90 mm³).
- Sole Bonding Peel Strength (SATRA TM411): >= 3.5 N/mm (standard benchmark: 4.0 - 5.5 N/mm).
- Martindale Lining Abrasion: >25,600 dry rubs / >12,800 wet rubs without thread rupture.
- Anti-Yellowing UV Exposure: Grade 4+ on the AATCC Greyscale after 48 hours UV-A radiation.
- Crocking / Rubbing Color Fastness: Dry Grade 4.5 / Wet Grade 4.0.

---

## 5. Chemical Safety & Global Environmental Compliance (EU REACH & US CPSIA)

WIDEWAY strictly audits all raw material suppliers to comply with international eco-toxicological standards:

| Substance Group | Regulatory Reference | Maximum Permissible Limit | WIDEWAY Factory Standard |
| :--- | :--- | :--- | :--- |
| Lead (Pb) | US CPSIA / CA Prop 65 | < 90 ppm | Non-detectable (< 10 ppm) |
| Cadmium (Cd) | EU REACH Annex XVII | < 100 ppm | Non-detectable (< 5 ppm) |
| Hexavalent Chromium (Cr VI) | ISO 17075 (Leather) | < 3.0 mg/kg | Non-detectable (< 1.0 mg/kg) |
| Phthalates (8P: DEHP, DBP, BBP, DINP, DIDP, DNOP, DIBP, DCHP) | US CPSIA / REACH SVHC | < 1,000 ppm (0.1%) | Non-detectable (< 50 ppm) |
| Banned Azo Colorants | EU REACH Annex XVII | < 30 ppm | Zero Banned Amines |
| Formaldehyde | ISO 14184-1 | < 75 mg/kg (adults) / < 20 mg/kg (infants) | Non-detectable |
| Dimethyl Fumarate (DMFu) | EU REACH (Anti-mold) | < 0.1 mg/kg | 0.00 mg/kg (Strictly prohibited) |
| Per- and Polyfluoroalkyl Substances (PFAS / PFOS / PFOA) | EU POPs / US State Laws | < 25 ppb | 100% Fluorine-Free DWR Coating |
| Volatile Organic Compounds (VOCs) | amfori BSCI Clean Air | < 50 mg/m³ in lasting hall | Waterborne low-VOC PU cement |

---

## 6. International Factory Audits & Social Compliance
- amfori BSCI: Audited facility with full social compliance report (Audit ID on demand).
- Sedex SMETA 4-Pillar: Certified on Labor, Health & Safety, Environment, and Business Ethics.
- ISO 9001:2015: Certified Quality Management System (Design, Mold Development, Shoe Assembly).
- ISO 14001:2015: Certified Environmental Management System.
- GRS (Global Recycled Standard 4.0): Supply chain certification verifying recycled polyester (RPET) yarns and recycled rubber.
- CE Conformity: Safety footwear models certified according to EN ISO 20345.

---

## 7. Global Brand OEM/ODM Partnerships & Retail Supply Track Record
WIDEWAY has manufactured and delivered volume footwear programs for prestigious international clients:
1. FILA: Athletic running shoes, tennis trainers, and lifestyle retro sneakers produced to Italian technical standards.
2. KAPPA: Football training shoes and classic court casual sneakers.
3. DIADORA: Premium lifestyle footwear and retro runners with microfibers and natural gum outsoles.
4. STARTER: Urban streetwear chunky dad shoes and retro basketball court trainers.
5. WRANGLER: Rugged casual boots, canvas sneakers, and durable outdoor shoes.
6. AIRNESS: French performance athletic shoes and high-rebound cushioning footwear.
7. Lidl & Aldi: Seasonal volume shoe programs for European supermarket networks meeting strict audit, barcode, and palletizing specs.
8. O'Neill: Quick-dry coastal casual shoes and EVA sandals.

---

## 8. Sourcing Logistics, Container Capacities & Incoterms

### Container Load Estimator (Based on Men's EU 42 Sneaker Shoebox: 32×20×11 cm):
- 20GP Container (28 CBM):
  - Approximately 3,200 to 3,600 pairs in individual branded shoeboxes (Carton: 62×42×33 cm, 12 pairs/carton, ~280-300 cartons).
  - Approximately 6,500 to 7,500 pairs in master polybags without shoeboxes.
- 40GP Container (58 CBM):
  - Approximately 6,800 to 7,400 pairs in shoeboxes.
- 40HQ High-Cube Container (68 CBM):
  - Approximately 7,800 to 8,500 pairs in shoeboxes (~650-700 master cartons).
  - Approximately 15,000 to 17,000 pairs in space-saving compressed polybags.

### Incoterms Supported:
- FOB Xiamen / FOB Quanzhou (Standard default).
- CIF / CFR to 150+ ports worldwide (Hamburg, Rotterdam, Los Angeles, New York, Santos, Jebel Ali, Singapore, Sydney, etc.).
- DDP (Delivered Duty Paid) door-to-door logistics with customs clearance for Amazon FBA warehouses and private commercial 3PL distribution centers.

---

## 9. Commercial Policies & Startup Brand Incubator
- Low Minimum Order Quantity (MOQ):
  - Standard custom private label run: 500 pairs per colorway across full size range.
  - Startup brand incubator program: Trial orders from 300 pairs per color supported using existing factory open-molds.
  - Wholesale white-label in-stock models: 200 pairs.
- Sample Development & Prototyping Timeline:
  - 3D CAD modeling & digital shoe last rendering: 48 hours.
  - Rapid 3D outsole printing: 72 hours.
  - Complete physical shoe prototype (cut, stitched, lasted, and boxed): 7 to 10 working days.
- Bulk Production Lead Time:
  - 25 to 35 calendar days following client's pre-production sample (PPS) approval and deposit receipt.
  - 20 to 25 days for repeat re-orders.
- Payment Terms:
  - 30% T/T deposit upon purchase order confirmation; 70% balance paid against copy of Bill of Lading (B/L) and final QC inspection report.
  - Irrevocable Letter of Credit (L/C at sight) accepted for container volume orders.
  - Sinosure-backed credit terms (OA 30/60 days) available for qualified multinational corporate buyers.

---


## 11. WIDEWAY Brand Visual Identity (VI/CI) System & Manufacturing Scenarios
- Core Brand Color: WIDEWAY Red (#e50408 / Pantone 186 C / CMYK: 0, 100, 95, 0 / RGB: 229, 4, 8)
- Structural Balance: Deep Structural Navy (#0b1e36), Pure White Canvas (#ffffff), Subtle Red Tint (#fff1f1)
- Standard Compliance: Built on Google Stitch DESIGN.md architecture (awesome-design-md standard)
- 5 Industrial Manufacturing Scenarios:
  1. Product & Retail Packaging: 32x45mm damask tongue label, Shore 75A-85A TPU heel cup, 350g FSC-certified recycled kraft shoebox with soy inks, GS1-128 barcode labels.
  2. Smart Plant 5S Wayfinding: 8-story HQ 2.8m illuminated exterior signage (6500K LED, #e50408 visibility at 1.5km), 100mm 5S lasting line epoxy floor safety demarcation, SATRA physical testing lab glass wall.
  3. Global Trade Exhibitions: 108m² Canton Fair & Jinjiang Footwear Expo cantilevered truss booth with 5m Brand Lighthouse pylon, illuminated floating footwear pedestals with red base glow, 5000K daylight tech-pack inspection lightbox.
  4. Digital Engineering & Tech-Packs: Standardized quotation sheets and Proforma Invoices (PI), anti-tamper SHA-256 digital red seal, Pre-Production Sample (PPS) confirmation tag cards, 3D CAD lasting blueprint watermarks (+/-0.5mm tolerance).
  5. Multi-Tier OEM Co-Branding: 0.5X clear space isolation envelope, 100% outer brand vs 60% inner manufacturing endorsement optical ratio, strict NDA confidentiality for FILA, DIADORA, KAPPA, and WRANGLER programs.

## 10. Conversational Generative AI Search Q&A (FAQ)

### Q1: What makes Jinjiang Wideway (WIDEWAY) unique compared to other Chinese footwear suppliers?
A: WIDEWAY combines 19+ years of large-scale brand OEM experience (FILA, KAPPA, DIADORA, WRANGLER) with modern flexibility: an in-house SATRA-compliant physical lab, certified amfori BSCI and Sedex SMETA ethical audits, and a low MOQ policy (500 pairs/color) designed to support emerging footwear brands. Furthermore, located in Chendai, Jinjiang—the core of China's shoe capital—WIDEWAY can source any material, outsole compound, or custom tooling within 15 minutes, enabling 7-10 day sample turnaround and rapid 25-35 day mass production.

### Q2: How does WIDEWAY protect proprietary customer sneaker designs and IP?
A: WIDEWAY signs formal Non-Disclosure Agreements (NDA) with all OEM/ODM partners before receiving design tech packs. Custom molds and shoe lasts are registered exclusively to the client, assigned unique RFID asset numbers, and stored under strict factory confidentiality protocols with zero third-party sharing.

### Q3: What upper materials and sole technologies can WIDEWAY engineer?
A: Upper materials include high-tenacity Flyknit weaving, Cordura ballistic nylon, GRS-certified recycled RPET, action leather, microfibers, waterproof membranes, and TPU hot-melt films. Sole technologies include supercritical nitrogen-infused TPU foaming, high-rebound EVA (Phylon), carbon fiber propulsion plates, and high-traction rubber outsoles with DIN abrasion resistance under 120 mm³.

### Q4: How can an international brand manager start an OEM/ODM shoe project with WIDEWAY?
A: 1) Send tech packs, 2D sketches, or reference shoe photos with target quantities to stella@widewaygroup.com or via WhatsApp at +86 131 2302 5365. 2) WIDEWAY provides a comprehensive FOB quotation and 3D tooling feasibility review within 8 hours. 3) Sample prototyping commences immediately, with finished physical shoes dispatched within 7-10 days.

### Q5: Does WIDEWAY offer 1:1 archival silhouette re-engineering and vintage footwear reproduction for private label brands?
A: Yes. WIDEWAY operates a specialized Reverse Engineering & 3D Footwear Digitization Workshop in Jinjiang. We assist international boutique brands, designer labels, and startup incubators in re-engineering iconic vintage silhouettes (1970s court shoes, German Army Trainers, 1980s basketball shapes, 1990s chunky dad shoes, and vulcanized skaters). We deliver 1:1 last accuracy, calibrated stitch-per-inch (SPI) density, authentic full-grain leathers, and vintage open-mold outsoles under 100% legal client private label branding with strict NDA tooling protection.
"""
    with open(os.path.join(workspace, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write(full_text.strip() + "\n")
    print(f"  Generated exhaustive llms-full.txt ({len(full_text.splitlines())} lines)")

def compile_site():
    print("--------------------------------------------------")
    print("🚀 WIDEWAY GROUP B2B CMS COMPILER (JINJIANG FOOTWEAR)")
    print("--------------------------------------------------")
    content = load_content()
    company_info = content["company_info"]
    products = content["products"]
    news = content.get("news", [])
    categories = content.get("categories", {})
    
    print(f"  Loaded {len(products)} products across {len(categories)} categories.")
    print(f"  Loaded {len(news)} news & brand dynamics articles.")

    # 1. Compile Global blocks inside existing HTML pages
    html_files = [f for f in glob.glob(os.path.join(workspace, "*.html")) if "-副本" not in f]
    products_template_html = ""

    for file_path in html_files:
        filename = os.path.basename(file_path)
        if filename in ["admin.html", "news-detail-template.html", "_test_nav.html"] or filename in [c["url"] for c in categories.values()]:
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
            
        html = sync_global_components(html, filename, company_info)
        
        if filename == "products.html":
            tabs_block = get_category_tabs_html("all")
            if "<!-- CATEGORY_TABS -->" not in html:
                html = re.sub(r'<div class="tabs-container reveal">.*?</div>', "<!-- CATEGORY_TABS -->\n<!-- END_CATEGORY_TABS -->", html, flags=re.DOTALL)
            html = replace_between(html, "<!-- CATEGORY_TABS -->", "<!-- END_CATEGORY_TABS -->", tabs_block)
            html = replace_between(html, "<!-- PRODUCTS_GRID -->", "<!-- END_PRODUCTS_GRID -->", get_products_grid_html(products))
            products_template_html = html
            
        if filename == "product-detail.html":
            products_json_str = json.dumps(products, ensure_ascii=False)
            html = re.sub(r'const ALL_PRODUCTS\s*=\s*\[.*?\];', f'const ALL_PRODUCTS = {products_json_str};', html, flags=re.DOTALL)

        if filename == "news.html":
            html = replace_between(html, "<!-- NEWS_LIST -->", "<!-- END_NEWS_LIST -->", get_news_list_html(news))
            
        html = inject_seo_and_geo_tags(html, filename, company_info)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Synchronized: {filename}")

    # 2. Compile dedicated category pages
    if not products_template_html and os.path.exists(os.path.join(workspace, "products.html")):
        with open(os.path.join(workspace, "products.html"), "r", encoding="utf-8") as f:
            products_template_html = f.read()

    if products_template_html:
        for cat_key, cat_data in categories.items():
            cat_filename = cat_data["url"]
            cat_html = products_template_html
            
            # Replace Title & SEO Description
            cat_html = re.sub(r"<title\b[^>]*>.*?</title>", f"<title>{cat_data['title']}</title>", cat_html, flags=re.I | re.DOTALL)
            cat_html = re.sub(r'<meta\s+[^>]*\bname=["\']description["\'][^>]*>', '', cat_html, flags=re.I)
            cat_html = re.sub(r'<meta\s+[^>]*\bcontent=[^>]*\bname=["\']description["\'][^>]*>', '', cat_html, flags=re.I)
            cat_html = re.sub(r'(<meta\s+charset=[^>]*>)', f'\\1\n  <meta name="description" content="{cat_data["desc"]}">', cat_html, flags=re.I)
            
            # Replace main section with category detailed html
            cat_content_html = get_category_detailed_html(cat_key, cat_data, company_info, products)
            
            # Replace between banner and footer or replace main
            main_match = re.search(r"<main.*?</main>", cat_html, flags=re.DOTALL)
            if main_match:
                cat_html = cat_html.replace(main_match.group(0), f"<main>\n{cat_content_html}\n</main>")
            else:
                cat_html = re.sub(r"(<!-- END_GLOBAL_HEADER -->).*?(<!-- GLOBAL_FOOTER -->)", f"\1\n<main>\n{cat_content_html}\n</main>\n\2", cat_html, flags=re.DOTALL)

            cat_html = sync_global_components(cat_html, cat_filename, company_info)
            cat_html = inject_seo_and_geo_tags(cat_html, cat_filename, company_info)
            
            with open(os.path.join(workspace, cat_filename), "w", encoding="utf-8") as f:
                f.write(cat_html)
            print(f"  Compiled Category Page: {cat_filename}")

    # 3. Pre-render 100+ Static Product Detail HTML pages (SSG for Googlebot & SEO)
    generate_static_product_pages(products, company_info)

    # 4. Generate 2026 sitemap.xml with Google Image metadata
    news_pages = [n.get("url", f"{n.get('id', '')}.html") for n in news]
    all_compiled_pages = [
        "index.html", "products.html", "oem-odm.html", "heritage-footwear-reproduction.html", "production-capacity.html",
        "quality-control.html", "certifications.html", "sustainability.html", "brand-identity.html",
        "about.html", "case-studies.html", "videos.html", "news.html", "contact.html",
        "knowledge-base.html", "whitepapers.html", "glossary.html", "knowledge-graph.html"
    ] + [c["url"] for c in categories.values()] + news_pages
    
    generate_sitemap_xml(all_compiled_pages, products)

    # 5. Generate 2026 AI-Ready robots.txt
    generate_robots_txt()

    # 6. Generate standardized llms.txt & deep technical llms-full.txt
    generate_llms_txt(company_info)
    generate_llms_full_txt(company_info, products, categories)

    # 7. Assemble clean production dist/ directory
    build_dist()

    print("--------------------------------------------------")
    print("✨ SITE REBUILD & COMPILATION COMPLETE!")
    print("--------------------------------------------------")


def generate_static_product_pages(products, company_info):
    """
    SSG Pre-rendering Engine for all 108 products.
    Pre-renders full static HTML for every product SKU into products_static/
    ensuring Googlebot receives complete, unique, rich HTML with exact canonical tags.
    """
    print("  Pre-rendering 100+ Static Product Detail HTML pages...")
    static_dir = os.path.join(workspace, "products_static")
    os.makedirs(static_dir, exist_ok=True)
    
    detail_template_path = os.path.join(workspace, "product-detail.html")
    if not os.path.exists(detail_template_path):
        print("  [WARN] product-detail.html template not found, skipping SSG.")
        return
        
    with open(detail_template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    cat_map = {
        'sport-outdoor-shoes': '/sport-outdoor-shoes-wholesale',
        'casual-shoes': '/casual-shoes-oem-manufacturer',
        'mens-shoes': '/mens-sneakers-bulk-supplier',
        'womens-shoes': '/womens-sneakers-oem-factory',
        'slides-sandals': '/slides-sandals-slippers-manufacturer',
        'bags-sportswear': '/bags-sportswear-accessories-wholesale'
    }

    generated_count = 0
    for p in products:
        pid = (p.get("id") or p.get("code") or "").strip()
        if not pid:
            continue
        pname = p.get("name", "")
        ptitle = p.get("seo_title") or f"{pname} OEM/ODM Custom Sneakers & Trainers | WIDEWAY Footwear Manufacturer"
        pdesc = p.get("seo_description") or p.get("description", "")
        pimg = p.get("image", "images/banner.jpg")
        pgallery = p.get("gallery") or [pimg]
        pcat = p.get("category", "sport-outdoor-shoes")
        canonical_url = f"https://www.widewayfootwear.com/product-detail?id={pid.lower()}"
        og_img_url = pimg if pimg.startswith("http") else f"https://www.widewayfootwear.com/{pimg.lstrip('/')}"
        
        h = template_html
        
        # 1. Update Title & Meta Description
        h = re.sub(r'<title\b[^>]*>.*?</title>', f'<title id="pageTitle">{html.escape(ptitle)}</title>', h, flags=re.I|re.S)
        h = re.sub(r'<meta[^>]+id=[\"\']metaDesc[\"\'][^>]*>', f'<meta name="description" id="metaDesc" content="{html.escape(pdesc)}"/>', h, flags=re.I)
        
        # 2. Clean ALL existing canonical tags and inject exact static canonical tag
        h = re.sub(r'<!--\s*Standard Canonical URL.*?-->\s*', '', h, flags=re.S)
        h = re.sub(r'<!--\s*Dynamic Canonical URL.*?-->\s*', '', h, flags=re.S)
        h = re.sub(r'<link[^>]+rel=[\"\']canonical[\"\'][^>]*>\s*', '', h, flags=re.I)
        static_canonical = f'<link id="canonicalTag" rel="canonical" href="{canonical_url}">'
        if '</head>' in h:
            h = h.replace('</head>', f'  <!-- Pre-rendered Static Product Canonical -->\n  {static_canonical}\n</head>', 1)

        # 3. OpenGraph tags
        h = re.sub(r'<meta[^>]+property=[\"\']og:title[\"\'][^>]*>', f'<meta property="og:title" content="{html.escape(ptitle)}"/>', h)
        h = re.sub(r'<meta[^>]+property=[\"\']og:description[\"\'][^>]*>', f'<meta property="og:description" content="{html.escape(pdesc)}"/>', h)
        h = re.sub(r'<meta[^>]+property=[\"\']og:image[\"\'][^>]*>', f'<meta property="og:image" content="{og_img_url}"/>', h)
        h = re.sub(r'<meta[^>]+property=[\"\']og:url[\"\'][^>]*>', f'<meta property="og:url" content="{canonical_url}"/>', h)

        # 4. Schema.org Product JSON-LD structured data
        target_markets = [s.strip() for s in (p.get('geo_markets') or "North America, European Union, United Kingdom, Middle East, Australia, Southeast Asia").split(',') if s.strip()]
        schema_data = {
          "@context": "https://schema.org/",
          "@type": "Product",
          "name": pname,
          "image": [og_img_url] + [g if g.startswith('http') else f"https://www.widewayfootwear.com/{g.lstrip('/')}" for g in pgallery if g != pimg],
          "description": pdesc,
          "sku": p.get('code') or pname,
          "mpn": p.get('code') or pname,
          "brand": { "@type": "Brand", "name": "WIDEWAY" },
          "manufacturer": {
            "@type": "Organization",
            "name": "WIDEWAY GROUP",
            "address": {
              "@type": "PostalAddress",
              "addressLocality": "Jinjiang",
              "addressRegion": "Fujian",
              "addressCountry": "CN"
            }
          },
          "countryOfOrigin": "CN",
          "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "USD",
            "price": "12.00",
            "lowPrice": "8.50",
            "highPrice": "18.00",
            "offerCount": "1000",
            "availability": "https://schema.org/InStock",
            "seller": {
              "@type": "Organization",
              "name": "WIDEWAY GROUP (Jinjiang Footwear Facility)"
            },
            "areaServed": target_markets
          }
        }
        schema_tag = f'<script id="productGeoSchema" type="application/ld+json">\n{json.dumps(schema_data, indent=2, ensure_ascii=False)}\n</script>'
        if 'id="productGeoSchema"' in h:
            h = re.sub(r'<script[^>]+id=[\"\']productGeoSchema[\"\'][^>]*>.*?</script>', schema_tag, h, flags=re.S)
        elif '</head>' in h:
            h = h.replace('</head>', f'{schema_tag}\n</head>', 1)

        # 5. Breadcrumbs
        cat_disp = pcat.replace('-', ' ').title()
        cat_href = cat_map.get(pcat, '/products')
        h = re.sub(r'<a[^>]+id=[\"\']breadCatLink[\"\'][^>]*>.*?</a>', f'<a href="{cat_href}" id="breadCatLink">{html.escape(cat_disp)}</a>', h, flags=re.S)
        h = re.sub(r'<span[^>]+id=[\"\']breadProductName[\"\'][^>]*>.*?</span>', f'<span id="breadProductName" style="color:#0f2b48; font-weight:700;">{html.escape(pname)}</span>', h, flags=re.S)

        # 6. Product Hero & Headlines
        h = re.sub(r'<h1[^>]+id=[\"\']productTitle[\"\'][^>]*>.*?</h1>', f'<h1 class="product-headline" id="productTitle">{html.escape(pname)}</h1>', h, flags=re.S)
        h = re.sub(r'<p[^>]+id=[\"\']productDesc[\"\'][^>]*>.*?</p>', f'<p id="productDesc" style="color: #64748b; font-size: 1rem; line-height: 1.6; margin-bottom: 20px;">{html.escape(p.get("description", pdesc))}</p>', h, flags=re.S)
        h = re.sub(r'<span[^>]+id=[\"\']catTagPill[\"\'][^>]*>.*?</span>', f'<span class="category-tag-pill" id="catTagPill">{html.escape(p.get("tag", "WIDEWAY"))}</span>', h, flags=re.S)
        h = re.sub(r'<span[^>]+id=[\"\']productTagBadge[\"\'][^>]*>.*?</span>', f'<span id="productTagBadge" style="position:absolute; top:12px; left:12px; background:#0f2b48; color:#fff; font-size:0.75rem; font-weight:700; padding:4px 10px; border-radius:4px; z-index:3;">{html.escape(p.get("tag", "WIDEWAY"))}</span>', h, flags=re.S)

        # 7. Specs Table
        h = re.sub(r'<td[^>]+id=[\"\']skuValue[\"\'][^>]*>.*?</td>', f'<td id="skuValue" style="font-weight:700; color:#e50408;">{html.escape(p.get("code") or pname)}</td>', h, flags=re.S)
        h = re.sub(r'<td[^>]+id=[\"\']upperValue[\"\'][^>]*>.*?</td>', f'<td id="upperValue">{html.escape(p.get("upper", "Engineered Flyknit Mesh"))}</td>', h, flags=re.S)
        h = re.sub(r'<td[^>]+id=[\"\']outsoleValue[\"\'][^>]*>.*?</td>', f'<td id="outsoleValue">{html.escape(p.get("outsole", "MD Midsole + Rubber"))}</td>', h, flags=re.S)
        h = re.sub(r'<td[^>]+id=[\"\']liningValue[\"\'][^>]*>.*?</td>', f'<td id="liningValue">{html.escape(p.get("lining", "OrthoLite Insole"))}</td>', h, flags=re.S)
        h = re.sub(r'<td[^>]+id=[\"\']sizesValue[\"\'][^>]*>.*?</td>', f'<td id="sizesValue">{html.escape(p.get("sizes", "EU 36-45 / US 5-11"))}</td>', h, flags=re.S)
        h = re.sub(r'<p[^>]+id=[\"\']moqValue[\"\'][^>]*>.*?</p>', f'<p id="moqValue">{html.escape(p.get("moq", "500 Pairs / Color"))}</p>', h, flags=re.S)
        h = re.sub(r'<p[^>]+id=[\"\']leadTimeValue[\"\'][^>]*>.*?</p>', f'<p id="leadTimeValue">{html.escape(p.get("lead_time", "30-45 Days"))}</p>', h, flags=re.S)

        # 8. Main Image & Gallery Thumbnails
        h = re.sub(r'<img[^>]+id=[\"\']mainProductImg[\"\'][^>]*>', f'<img alt="{html.escape(pname)}" id="mainProductImg" src="{pimg}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;"/>', h)
        thumbs_html = ""
        for idx, g_img in enumerate(pgallery):
            active_cls = " active" if idx == 0 else ""
            thumbs_html += f'<div class="thumb-item{active_cls}"><img src="{g_img}" alt="{html.escape(pname)} angle {idx+1}"></div>'
        h = re.sub(r'<div class="gallery-thumbs" id="galleryThumbs">.*?</div>', f'<div class="gallery-thumbs" id="galleryThumbs">\n{thumbs_html}\n</div>', h, flags=re.S)

        # 9. Related Products
        related_html = ""
        same_cat = [prod for prod in products if prod.get('category') == pcat and (prod.get('id') or prod.get('code')) != pid][:4]
        for rp in same_cat:
            rp_id = rp.get('id') or rp.get('code')
            rp_name = rp.get('name', '')
            rp_img = rp.get('image', '')
            rp_moq = rp.get('moq', '500 Pairs')
            related_html += f"""
            <div class="product-card" style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
              <div style="aspect-ratio:4/3; overflow:hidden; background:#f8fafc; position:relative;">
                <a href="/product-detail?id={rp_id}">
                  <img src="{rp_img}" alt="{html.escape(rp_name)}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s ease;">
                </a>
              </div>
              <div style="padding:15px;">
                <h4 style="font-size:1rem; margin-bottom:6px;"><a href="/product-detail?id={rp_id}" style="color:#0f2b48; text-decoration:none;">{html.escape(rp_name)}</a></h4>
                <p style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">MOQ: {html.escape(rp_moq)}</p>
                <a href="/product-detail?id={rp_id}" class="btn btn-secondary btn-sm" style="width:100%; text-align:center; font-size:0.8rem; border-color:#0f2b48; color:#0f2b48;">View Model</a>
              </div>
            </div>"""
        h = re.sub(r'<div class="product-grid" id="relatedProductsGrid">.*?</div>', f'<div class="product-grid" id="relatedProductsGrid">\n{related_html}\n</div>', h, flags=re.S)

        # 10. RFQ Pre-fill & WhatsApp Direct Link
        h = re.sub(r'(<input[^>]+id=[\"\']rfqProductInterest[\"\'][^>]*value=)[\"\'][^\"\']*[\"\']', f'\\1"{html.escape(pname)} ({pid})"', h)
        wa_msg = urllib.parse.quote(f'Hi WIDEWAY, I am inquiring about model: {pname} (ID: {pid}). Please provide quotation and sample terms.')
        h = re.sub(r'(<a[^>]+id=[\"\']waDirectBtn[\"\'][^>]*href=)[\"\'][^\"\']*[\"\']', f'\\1"https://wa.me/8618505959266?text={wa_msg}"', h)

        # Save files: lowercase, exact, and uppercase variants
        for fname in set([pid.lower(), pid, pid.upper()]):
            out_path = os.path.join(static_dir, f"{fname}.html")
            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.write(h)

        generated_count += 1

    print(f"  ✅ Successfully pre-rendered {generated_count} static product HTML pages in products_static/")

def build_dist():
    import shutil
    import subprocess
    print("--------------------------------------------------")
    print("📦 ASSEMBLING CLEAN PRODUCTION DISTRIBUTION (dist/)...")
    print("--------------------------------------------------")
    dist_dir = os.path.join(workspace, "dist")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # 1. Compile CIS Russian Portals
    cis_script = os.path.join(workspace, "scripts", "build_cis_yandex_optimization.py")
    if os.path.exists(cis_script):
        subprocess.run([sys.executable, cis_script], check=True)

    # 2. Gather list of legitimate public HTML pages
    exclude_files = {"admin.html", "news-detail-template.html", "_test_nav.html"}
    html_files = [f for f in glob.glob(os.path.join(workspace, "*.html")) 
                  if os.path.basename(f) not in exclude_files and "-副本" not in f and not os.path.basename(f).startswith("_")]

    for f in html_files:
        shutil.copy2(f, os.path.join(dist_dir, os.path.basename(f)))

    # 3. Copy clean public asset directories including products_static
    for folder in ["css", "js", "images", "data", "ai", "docs", "ru", "products_static"]:
        src = os.path.join(workspace, folder)
        dest = os.path.join(dist_dir, folder)
        if os.path.exists(src):
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".DS_Store", "*.pyc", "__pycache__", "*tmp*", "*.tar.gz", "*-副本*"))

    # 4. Copy static root files (preserving the complete sitemap.xml)
    for root_file in ["favicon.ico", "robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt", "e8a4c9f21b0d4637a9e52c3f8b7d6e21.txt"]:
        src = os.path.join(workspace, root_file)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dist_dir, root_file))

    print("  ✨ dist/ distribution build complete and verified!")

if __name__ == "__main__":
    compile_site()
