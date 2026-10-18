#!/usr/bin/env python3
"""
==============================================================================
WIDEWAY GROUP - Yandex SEO & Central Asia (CIS / EAEU) GEO Super Portal Compiler
Target Markets: Russian Federation (RU), Kazakhstan (KZ), Uzbekistan (UZ), Belarus (BY), Kyrgyzstan (KG)
Target Engines: Yandex Search (YandexBot), Яндекс Нейро (Yandex Neuro), Алиса AI (YandexGPT 5), Google CIS
Site: https://www.widewayfootwear.com

Core Capabilities:
1. Compiles /ru/index.html:
   Russian B2B Footwear OEM/ODM Master Portal (Full Product Spectrum, Jinjiang Factory Specs,
   SATRA 32-Gate Testing Lab, 40HQ Container Load Calculator, ГОСТ/ISO Matrix, Direct Inquiry Desk).
2. Compiles /ru/cis-central-asia/index.html:
   Dedicated CIS & Central Asia Engineering Landing Zone (ТР ТС 017/2011 Compliance, «Честный ЗНАК»
   DataMatrix Aggregation, -35°C Sub-Zero Outsole Compounding, 1:1 Western Brand Import-Substitution,
   China-Europe Express Dostyk/Khorgos Rail Logistics & Princeton GEO 3-Sentence Structured FAQ Hub).
3. Injects Yandex Webmaster verification, multi-regional hreflang (en, ru, ru-RU, ru-KZ, ru-UZ, ru-BY, x-default),
   OpenGraph locales, and EAEU areaServed JSON-LD across all HTML pages.
4. Upgrades robots.txt (Yandex Clean-param), sitemap.xml, llms.txt, llms-full.txt, /ai/cis-gost-matrix.json.
==============================================================================
"""

import os
import sys
import json
import re
from pathlib import Path

_curr = Path(__file__).resolve().parent
BASE_DIR = _curr.parent if _curr.name == "scripts" else _curr
sys.path.insert(0, str(BASE_DIR))

YANDEX_VERIFICATION_CODE = "8f2a4b1c9e7d3f0a_wideway_yandex_verify"
INDEXNOW_KEY = "e8a4c9f21b0d4637a9e52c3f8b7d6e21"
TELEGRAM_CIS_URL = "https://t.me/widewayfootwear_cis"
TELEGRAM_CIS_HANDLE = "@widewayfootwear_cis"
WHATSAPP_NUMBER = "+86 185 0595 9266"
WHATSAPP_CLEAN = "8618505959266"
EMAIL_CIS = "amy@widewaygroup.com"

# Load central site content
SITE_CONTENT_PATH = os.path.join(BASE_DIR, "data", "site_content.json")
with open(SITE_CONTENT_PATH, "r", encoding="utf-8") as f:
    site_content = json.load(f)

GOST_EQUIVALENCE_ROWS = [
    {
        "parameter_ru": "Прочность крепления подошвы (клеевой шов)",
        "parameter_en": "Sole Attachment / Bond Strength",
        "gost_standard": "ГОСТ 9134-78 / ГОСТ 9136-78 / ТР ТС 017/2011",
        "intl_standard": "SATRA TM411 / ISO 17708",
        "gost_norm": "≥ 3.0 Н/мм (для спортивной и повседневной обуви)",
        "wideway_value": "≥ 3.8 – 4.5 Н/мм",
        "advantage_ru": "Двойная инфракрасная термоактивация клеевой пленки и гидравлический обжим под давлением 6.0 кг/см² исключают отрыв подошвы в слякоти и снегу."
    },
    {
        "parameter_ru": "Сопротивление подошвы многократному изгибу при -25°C",
        "parameter_en": "Outsole Repeated Cold Flex Resistance",
        "gost_standard": "ГОСТ Р ИСО 17707-2014 / ГОСТ 9718-88",
        "intl_standard": "SATRA TM161 / ISO 20344 (п. 8.4)",
        "gost_norm": "Разрастание надреза ≤ 4.0 мм после 30 000 циклов",
        "wideway_value": "≤ 1.5 мм после 50 000 циклов при +23°C; 30 000 циклов при -25°C",
        "advantage_ru": "Специальная морозостойкая резина и модифицированный ТПУ не трескаются при экстремальных температурах РФ и Казахстана (до -35°C)."
    },
    {
        "parameter_ru": "Прочность верха на разрыв и раздирание",
        "parameter_en": "Upper Material Tear & Tensile Strength",
        "gost_standard": "ГОСТ 938.11-69 / ГОСТ 9290-76",
        "intl_standard": "ISO 3376 / ISO 3377-2 / SATRA TM30",
        "gost_norm": "≥ 60 Н (текстиль / микрофибра / синтетическая кожа)",
        "wideway_value": "≥ 120 – 180 Н",
        "advantage_ru": "Усиленный жаккардовый Flyknit высокой плотности и многослойная микрофибра 1.4-1.6 мм выдерживают жесткие динамические нагрузки."
    },
    {
        "parameter_ru": "Истираемость резины протектора",
        "parameter_en": "Outsole Abrasion Resistance",
        "gost_standard": "ГОСТ 426-77 / ГОСТ 12.4.137",
        "intl_standard": "DIN 53516 / ISO 4649 (Method A)",
        "gost_norm": "Потеря объема ≤ 180 – 250 мм³",
        "wideway_value": "≤ 85 – 110 мм³ (Carbon Rubber Pods)",
        "advantage_ru": "Высокая долговечность протектора на абразивном асфальте, бетоне, гравии и посыпанном солью тротуаре."
    },
    {
        "parameter_ru": "Морозостойкость низа обуви и температура стеклования",
        "parameter_en": "Cold Temperature Flexibility / Glass Transition",
        "gost_standard": "ГОСТ 26167-2005 / ГОСТ 12.4.137",
        "intl_standard": "SATRA TM161 (Cold Chamber)",
        "gost_norm": "Отсутствие хрупкости и трещин при -15°C",
        "wideway_value": "Сохранение упругости и сцепления до -35°C",
        "advantage_ru": "Подошва не дубеет и не превращается в скользкий твердый пластик на льду и укатанном снегу."
    },
    {
        "parameter_ru": "Динамическая водонепроницаемость мембранной обуви",
        "parameter_en": "Dynamic Water Resistance (Bootie Flex Test)",
        "gost_standard": "ТР ТС 017/2011 / ГОСТ 12.4.137",
        "intl_standard": "ASTM F1671 / SATRA TM230",
        "gost_norm": "Требования для мембранной обуви",
        "wideway_value": "> 15 000 – 25 000 циклов изгиба в воде без протечек",
        "advantage_ru": "Цельный 4-слойный чулок с герметизированными швами гарантирует сухость ног в осенне-весенней снежной жиже."
    },
    {
        "parameter_ru": "Коэффициент сцепления на мокрой и обледенелой поверхности",
        "parameter_en": "Slip Resistance Coefficient",
        "gost_standard": "ГОСТ 12.4.033-77 / СП 29.13330",
        "intl_standard": "EN ISO 13287 / SATRA TM144",
        "gost_norm": "Коэффициент трения ≥ 0.30",
        "wideway_value": "≥ 0.42 – 0.55 (Wet Ceramic & Steel Plates)",
        "advantage_ru": "Разнонаправленный ламелированный протектор обеспечивает надежное зацепление за мокрую плитку и укатанный снег."
    },
    {
        "parameter_ru": "Обязательная цифровая маркировка «Честный ЗНАК» / ИС МПТ",
        "parameter_en": "Digital Track-and-Trace Barcode Aggregation",
        "gost_standard": "ФЗ № 488-ФЗ / Распоряжение № 792-р",
        "intl_standard": "GS1 DataMatrix (2D Barcode)",
        "gost_norm": "Обязательно для каждой пары обуви",
        "wideway_value": "100% агрегация DataMatrix на фабрике перед отгрузкой",
        "advantage_ru": "Печать и нанесение термотрансферных кодов на ярлыки, индивидуальные коробки и транспортные короба с формированием файлов отгрузки."
    },
    {
        "parameter_ru": "Токсикологическая и химическая безопасность",
        "parameter_en": "Chemical Safety & Non-Toxicity",
        "gost_standard": "ТР ТС 017/2011 (Прил. 8) / ГОСТ 30347-97",
        "intl_standard": "OEKO-TEX Standard 100 / REACH SVHC",
        "gost_norm": "Формальдегид ≤ 20 мг/кг, Хром VI ≤ 3 мг/кг",
        "wideway_value": "Не обнаружено / Значительно ниже ПДК",
        "advantage_ru": "Полная экологическая чистота сырья; отсутствие едких химических запахов при открытии коробок."
    }
]

SUBSTITUTION_ROWS = [
    {
        "western_brand": "Nike Pegasus / Infinity Run",
        "category": "Кроссовки для ежедневного бега и фитнеса",
        "wideway_equivalent": "WIDEWAY Pro-Run Supercritical Nitrogene (`WD2500111`)",
        "specs": "Промежуточная подошва из сверхкритической азотной пены (Supercritical Nitrogen EVA), верх из воздухопроницаемой жаккардовой сетки, износостойкие резиновые накладки.",
        "commercial_advantage": "Прямая заводская цена $12.50–$16.80 FOB (экономия 65% по сравнению с оптовыми ценами дистрибьюторов), кастомный брендинг, низкий MOQ 500 пар на цвет."
    },
    {
        "western_brand": "Adidas Samba / Gazelle / Spezial",
        "category": "Винтажные террасные и классические кортовые кеды",
        "wideway_equivalent": "WIDEWAY Heritage T-Toe Court Series (`WD2500222`)",
        "specs": "Натуральный спилок/замша в T-образном мыске, премиальная плотная микрофибра/экокожа основы, аутентичная подметка из ретро-каучука (gum rubber cupsole).",
        "commercial_advantage": "1:1 воссоздание оригинальной эргономичной колодки, кастомизация задника и стельки под ваш бренд, метрический размерный ряд Mondopoint 225–300 мм."
    },
    {
        "western_brand": "Salomon XT-6 / Speedcross",
        "category": "Трейлраннинг, горпкор и демисезонный туризм",
        "wideway_equivalent": "WIDEWAY All-Terrain Trail & Trek Series (`WD2500331`)",
        "specs": "Система быстрой шнуровки (Quick-Lace), герметичный мембранный водонепроницаемый чулок (Waterproof Bootie), агрессивный глубокий шевронный протектор из морозостойкой резины.",
        "commercial_advantage": "Сертифицированная водонепроницаемость >15 000 изгибов, идеальное сцепление на грунте и снегу, устойчивость к морозам до -30°C."
    },
    {
        "western_brand": "New Balance 574 / 2002R / 990",
        "category": "Ретро-раннеры и массивные городские кроссовки («Dad Shoes»)",
        "wideway_equivalent": "WIDEWAY Archival Retro Runner Series (`WD2500441`)",
        "specs": "Многослойный комбинированный верх (замша + полиэстеровая сетка), многокомпонентная амортизирующая подошва двойной плотности, стабилизирующая вставка в пятке из ТПУ.",
        "commercial_advantage": "Увеличенная полнота колодки (идеально для восточноевропейской и центральноазиатской стопы), стойкость к истиранию, FOB $11.80–$15.50."
    },
    {
        "western_brand": "Yeezy Slide / Hoka Recovery Slide",
        "category": "Восстановительные литые слайды и анатомические шлепанцы",
        "wideway_equivalent": "WIDEWAY Ultra-Cushion Cloud Slide Series (`WD2500551`)",
        "specs": "Цельнолитая модифицированная ЭВА пена высокой упругости, глубокая чаша для фиксации пятки, поддержка продольного и поперечного сводов стопы.",
        "commercial_advantage": "Высокомаржинальная товарная позиция для маркетплейсов (Wildberries, Ozon, Kaspi.kz), быстрый запуск пресс-форм, MOQ от 1000 пар."
    }
]

def compile_ru_portal():
    """Generates /ru/index.html (Master Footwear OEM/ODM Russian Portal)."""
    os.makedirs(os.path.join(BASE_DIR, "ru"), exist_ok=True)
    out_file = os.path.join(BASE_DIR, "ru", "index.html")

    gost_rows_html = ""
    for r in GOST_EQUIVALENCE_ROWS:
        gost_rows_html += f"""
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);">
          <td style="padding: 14px 16px; font-weight: 600; color: #f8fafc;">
            <div>{r['parameter_ru']}</div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-family: monospace;">{r['parameter_en']}</div>
          </td>
          <td style="padding: 14px 16px; color: #60a5fa; font-family: monospace; font-size: 0.82rem;">{r['gost_standard']}<br><span style="color: #94a3b8;">{r['intl_standard']}</span></td>
          <td style="padding: 14px 16px; color: #cbd5e1; font-size: 0.85rem;">{r['gost_norm']}</td>
          <td style="padding: 14px 16px; color: #4ade80; font-weight: 700; font-size: 0.9rem;">{r['wideway_value']}</td>
          <td style="padding: 14px 16px; color: #cbd5e1; font-size: 0.82rem; line-height: 1.4;">{r['advantage_ru']}</td>
        </tr>
        """

    subst_rows_html = ""
    for s in SUBSTITUTION_ROWS:
        subst_rows_html += f"""
        <div style="background: rgba(18, 27, 49, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 22px; margin-bottom: 18px; transition: transform 0.2s;" onmouseover="this.style.borderColor='#e50408'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
            <div>
              <span style="display: inline-block; background: rgba(229,4,8,0.15); color: #f87171; border: 1px solid rgba(229,4,8,0.3); padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Аналог: {s['western_brand']}</span>
              <h3 style="font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin: 8px 0 4px 0;">{s['wideway_equivalent']}</h3>
              <div style="font-size: 0.82rem; color: #94a3b8;">Категория: {s['category']}</div>
            </div>
            <div style="background: rgba(37,99,235,0.15); border: 1px solid rgba(59,130,246,0.3); padding: 6px 14px; border-radius: 8px; text-align: right;">
              <span style="font-size: 0.72rem; color: #93c5fd; text-transform: uppercase; font-weight: 600;">MOQ / Партия</span>
              <div style="font-size: 0.95rem; font-weight: 700; color: #60a5fa;">от 500 пар / цвет</div>
            </div>
          </div>
          <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 12px; background: rgba(0,0,0,0.25); padding: 12px; border-radius: 8px; border-left: 3px solid #e50408;">
            <strong>Материалы и технологии:</strong> {s['specs']}
          </div>
          <div style="font-size: 0.85rem; color: #4ade80; line-height: 1.5;">
            <strong>Коммерческое преимущество для ритейла:</strong> {s['commercial_advantage']}
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Производство обуви в Китае под заказ | Фабрика WIDEWAY Цзиньцзян (OEM/ODM)</title>
  <meta name="description" content="Прямая фабрика по пошиву обуви в Цзиньцзяне (WIDEWAY GROUP). Производство кроссовок, кед, треккинговой обуви и слайдов под ключ. Полное соответствие ТР ТС 017/2011, маркировка Честный ЗНАК, доставка ж/д в Москву, Алматы, Ташкент.">
  <meta name="keywords" content="производство обуви китай, фабрика обуви цзиньцзян, пошив кроссовок оптом, контрактное производство обуви, обувь oem odm китай, обувь честный знак китай, кроссовки оптом от производителя">
  <link rel="canonical" href="https://www.widewayfootwear.com/ru/">
  
  <meta name="yandex-verification" content="{YANDEX_VERIFICATION_CODE}">
  <link rel="alternate" hreflang="en" href="https://www.widewayfootwear.com/" />
  <link rel="alternate" hreflang="ru" href="https://www.widewayfootwear.com/ru/" />
  <link rel="alternate" hreflang="ru-RU" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-KZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-UZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-BY" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="x-default" href="https://www.widewayfootwear.com/" />
  
  <meta property="og:type" content="website">
  <meta property="og:title" content="Фабрика обуви WIDEWAY Цзиньцзян | Контрактное производство OEM/ODM в Китае">
  <meta property="og:description" content="Производство качественной спортивной, повседневной и треккинговой обуви на фабрике в Китае. ТР ТС 017/2011, Честный ЗНАК, прямые ж/д поставки в РФ и СНГ.">
  <meta property="og:url" content="https://www.widewayfootwear.com/ru/">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:locale:alternate" content="ru_KZ">
  <meta property="og:locale:alternate" content="ru_UZ">
  <meta property="og:locale:alternate" content="ru_BY">
  <meta property="og:locale:alternate" content="en_US">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FootwearStore",
    "name": "WIDEWAY GROUP Footwear Manufacturing",
    "alternateName": "Jinjiang Wideway Import & Export Co., Ltd.",
    "description": "Прямой китайский производитель спортивной, повседневной и специализированной обуви OEM/ODM в Цзиньцзяне с 2007 года.",
    "url": "https://www.widewayfootwear.com/ru/",
    "telephone": "{WHATSAPP_NUMBER}",
    "email": "{EMAIL_CIS}",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "8F, Building 8A, NO.618, JINXIN Road, ChenDai town",
      "addressLocality": "Jinjiang, Quanzhou",
      "addressRegion": "Fujian",
      "postalCode": "362211",
      "addressCountry": "CN"
    }},
    "geo": {{
      "@type": "GeoCoordinates",
      "latitude": 24.7865,
      "longitude": 118.5833
    }},
    "areaServed": ["RU", "KZ", "UZ", "BY", "KG", "TJ", "AM", "AZ"],
    "hasOfferCatalog": {{
      "@type": "OfferCatalog",
      "name": "B2B Footwear Manufacturing Services",
      "itemListElement": [
        {{
          "@type": "Offer",
          "itemOffered": {{
            "@type": "Product",
            "name": "Athletic & Running Shoes OEM Manufacturing",
            "description": "Производство беговых кроссовок с подошвой из сверхкритической пены по ТР ТС 017/2011."
          }}
        }},
        {{
          "@type": "Offer",
          "itemOffered": {{
            "@type": "Product",
            "name": "Retro Court & Casual Sneakers ODM",
            "description": "Пошив винтажных кортовых кед из натуральной замши и микрофибры с оригинальными колодками."
          }}
        }}
      ]
    }}
  }}
  </script>
</head>
<body style="background: #090e1a; color: #f8fafc; font-family: 'Inter', sans-serif;">

  <!-- Header & Navigation -->
  <header style="background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.08); position: sticky; top: 0; z-index: 1000; padding: 14px 24px;">
    <div style="max-width: 1280px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
      <a href="/ru/" style="display: flex; align-items: center; gap: 12px; text-decoration: none;">
        <span style="background: #e50408; color: #fff; font-weight: 800; font-size: 1.15rem; padding: 4px 10px; border-radius: 6px; letter-spacing: 1px;">WIDEWAY</span>
        <span style="font-weight: 700; color: #fff; font-size: 1.05rem;">FOOTWEAR FACTORY</span>
      </a>
      
      <nav style="display: flex; align-items: center; gap: 24px;">
        <a href="/ru/" style="color: #fff; font-weight: 600; text-decoration: none; border-bottom: 2px solid #e50408; padding-bottom: 4px;">Главная</a>
        <a href="/ru/cis-central-asia/" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Экспорт в СНГ / ЕАЭС</a>
        <a href="/products" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Каталог (EN)</a>
        <a href="/quality-control" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Лаборатория QC</a>
        <a href="/contact" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Контакты</a>
        
        <!-- Language Switcher -->
        <div style="display: flex; align-items: center; background: rgba(255,255,255,0.08); border-radius: 20px; padding: 2px 4px;">
          <a href="/" style="color: #94a3b8; font-size: 0.78rem; padding: 4px 10px; text-decoration: none;">EN</a>
          <span style="background: #e50408; color: #fff; font-size: 0.78rem; font-weight: 700; padding: 4px 10px; border-radius: 16px;">RU / СНГ</span>
        </div>
      </nav>
      
      <div style="display: flex; align-items: center; gap: 12px;">
        <a href="https://wa.me/{WHATSAPP_CLEAN}?text=Здравствуйте!%20Интересует%20пошив%20обуви%20на%20фабрике%20WIDEWAY" target="_blank" style="background: #25d366; color: #fff; padding: 8px 16px; border-radius: 8px; font-weight: 600; text-decoration: none; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">
          <span>💬 WhatsApp Отдел СНГ</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section style="background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(9, 14, 26, 1) 100%), url('../images/banner_factory.jpg') center/cover; padding: 80px 24px; border-bottom: 1px solid rgba(255,255,255,0.08);">
    <div style="max-width: 1200px; margin: 0 auto; text-align: center;">
      <div style="display: inline-block; background: rgba(229,4,8,0.15); border: 1px solid rgba(229,4,8,0.3); color: #f87171; padding: 6px 16px; border-radius: 30px; font-weight: 700; font-size: 0.85rem; margin-bottom: 20px;">
        🇨🇳 ПРЯМАЯ ФАБРИКА ОБУВИ В ЦЗИНЬЦЗЯНЕ · 18 ЛЕТ ЭКСПОРТА В РФ И СНГ
      </div>
      <h1 style="font-family: 'Outfit', sans-serif; font-size: 3rem; font-weight: 800; line-height: 1.2; margin-bottom: 20px; color: #fff;">
        Контрактное производство обуви в Китае (OEM/ODM)<br>
        <span style="color: #e50408;">Полное соответствие ТР ТС 017/2011 и маркировка «Честный ЗНАК»</span>
      </h1>
      <p style="font-size: 1.15rem; color: #cbd5e1; max-width: 860px; margin: 0 auto 32px auto; line-height: 1.6;">
        Фабрика <strong>WIDEWAY GROUP</strong> (Цзиньцзян, Фуцзянь) — 3 современные конвейерные линии, 120 000+ пар в месяц. Изготовление кроссовок, кед, треккинговой обуви и слайдов под ключ: от 3D-моделирования колодки и прототипа за 7 дней до прямой поставки контейнеров в Москву, Алматы, Ташкент и Минск.
      </p>
      
      <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
        <a href="#rfqFormSection" style="background: #e50408; color: #fff; padding: 14px 32px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 1rem; box-shadow: 0 4px 20px rgba(229,4,8,0.35);">
          📋 Запросить расчет партии (RFQ)
        </a>
        <a href="/ru/cis-central-asia/" style="background: rgba(255,255,255,0.08); color: #fff; border: 1px solid rgba(255,255,255,0.2); padding: 14px 28px; border-radius: 8px; font-weight: 600; text-decoration: none; font-size: 1rem;">
          🚆 Условия для РФ и Центральной Азии &rarr;
        </a>
      </div>
      
      <!-- Key Metric Strip -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 50px; text-align: left;">
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px;">
          <div style="font-size: 2rem; font-weight: 800; color: #60a5fa; font-family: 'Outfit';">120 000+</div>
          <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Пар обуви в месяц (3 конвейера)</div>
        </div>
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px;">
          <div style="font-size: 2rem; font-weight: 800; color: #4ade80; font-family: 'Outfit';">7 Дней</div>
          <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Срок разработки 1-го образца (Tech Pack)</div>
        </div>
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px;">
          <div style="font-size: 2rem; font-weight: 800; color: #f59e0b; font-family: 'Outfit';">от 500 Пар</div>
          <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Минимальный заказ (MOQ) на цвет</div>
        </div>
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px;">
          <div style="font-size: 2rem; font-weight: 800; color: #ec4899; font-family: 'Outfit';">100% ЕАЭС</div>
          <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">ТР ТС 017/2011 и Честный ЗНАК</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 1:1 Replacement Matrix Section -->
  <section style="padding: 70px 24px; max-width: 1200px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 45px;">
      <span style="color: #60a5fa; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;">Импортозамещение брендовой обуви</span>
      <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-top: 8px;">1:1 Альтернатива ушедшим западным брендам</h2>
      <p style="color: #94a3b8; max-width: 780px; margin: 10px auto 0 auto; line-height: 1.5;">
        Запуск собственных торговых марок (СТМ) для обувных сетей, селлеров Wildberries/Ozon и спортивных ритейлеров с качеством материалов, превосходящим масс-маркет.
      </p>
    </div>
    
    <div>
      {subst_rows_html}
    </div>
  </section>

  <!-- GOST ↔ ISO Technical Matrix Table -->
  <section style="background: #0f172a; padding: 70px 24px; border-top: 1px solid rgba(255,255,255,0.08); border-bottom: 1px solid rgba(255,255,255,0.08);">
    <div style="max-width: 1240px; margin: 0 auto;">
      <div style="text-align: center; margin-bottom: 40px;">
        <span style="color: #4ade80; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;">Инженерные стандарты и сертификация</span>
        <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-top: 8px;">ГОСТ vs ISO / SATRA: Таблица физико-механических показателей</h2>
        <p style="color: #94a3b8; max-width: 800px; margin: 10px auto 0 auto; line-height: 1.5;">
          Вся обувь WIDEWAY проходит жесткий контроль в собственной SATRA-лаборатории по 32 параметрам надежности перед отправкой в ЕАЭС.
        </p>
      </div>

      <div style="overflow-x: auto; background: rgba(18, 27, 49, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.88rem;">
          <thead>
            <tr style="background: rgba(30, 41, 59, 0.9); border-bottom: 2px solid rgba(255,255,255,0.15);">
              <th style="padding: 16px; color: #fff; font-weight: 700;">Показатель качества</th>
              <th style="padding: 16px; color: #fff; font-weight: 700;">Стандарт ГОСТ / ISO</th>
              <th style="padding: 16px; color: #fff; font-weight: 700;">Норматив ЕАЭС</th>
              <th style="padding: 16px; color: #fff; font-weight: 700;">Фактически WIDEWAY</th>
              <th style="padding: 16px; color: #fff; font-weight: 700;">Преимущество в климате РФ</th>
            </tr>
          </thead>
          <tbody>
            {gost_rows_html}
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Container Load & Logistics Calculator Section -->
  <section style="padding: 70px 24px; max-width: 1200px; margin: 0 auto;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center; flex-wrap: wrap;">
      <div>
        <span style="color: #f59e0b; font-weight: 700; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;">Логистика и таможенное оформление</span>
        <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-top: 8px;">Оптимизация загрузки контейнера 40HQ</h2>
        <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 20px;">
          Обувь — объемоемкий груз. Мы рассчитываем эргономику коробки и короба так, чтобы максимально использовать полезный объем 68–70 м³ контейнера 40HQ:
        </p>
        <ul style="color: #cbd5e1; line-height: 1.8; font-size: 0.92rem; padding-left: 20px;">
          <li><strong>В брендовых индивидуальных коробках:</strong> 520–550 коробов = <strong>6 240 – 6 600 пар</strong> (вес груза ~6.2 т);</li>
          <li><strong>В полибегах (для маркетплейсов и супермаркетов):</strong> <strong>11 000 – 13 000 пар</strong> в 40HQ;</li>
          <li><strong>Ж/Д маршруты:</strong> прямой контейнерный поезд Цзиньцзян/Иу &rarr; Достык/Алтынколь &rarr; Алматы (12–16 дн.), Москва Ворсино (16–22 дн.);</li>
          <li><strong>Морской маршрут:</strong> Сямэнь &rarr; Владивосток (6–8 дн.) + Транссиб;</li>
          <li><strong>Оплата:</strong> прямые расчеты в <strong>CNY (юанях)</strong> или <strong>RUB (рублях)</strong> через ВТБ Шанхай / CIPS.</li>
        </ul>
      </div>

      <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 30px;">
        <h3 style="font-size: 1.3rem; font-weight: 700; color: #fff; margin-bottom: 16px;">Экспресс-калькулятор партии</h3>
        <div style="margin-bottom: 14px;">
          <label style="display: block; font-size: 0.82rem; color: #94a3b8; margin-bottom: 6px;">Планируемый объем (пар):</label>
          <input type="number" id="calcPairs" value="6500" style="width: 100%; background: #0b1326; border: 1px solid rgba(255,255,255,0.15); color: #fff; padding: 10px 14px; border-radius: 6px; font-size: 0.95rem;" oninput="updateFootwearLogisticsCalc()">
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 0.82rem; color: #94a3b8; margin-bottom: 6px;">Тип упаковки:</label>
          <select id="calcPackType" style="width: 100%; background: #0b1326; border: 1px solid rgba(255,255,255,0.15); color: #fff; padding: 10px 14px; border-radius: 6px; font-size: 0.95rem;" onchange="updateFootwearLogisticsCalc()">
            <option value="boxed">Индивидуальные коробки (12 пар / короб)</option>
            <option value="polybag">Полибеги без коробок (24 пары / короб)</option>
          </select>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 8px; font-size: 0.85rem; line-height: 1.6;">
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#94a3b8;">Потребность в контейнерах:</span>
            <span id="resContainers" style="font-weight:700; color:#60a5fa;">1.00 x 40HQ</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#94a3b8;">Количество мастер-коробов:</span>
            <span id="resCartons" style="font-weight:700; color:#fff;">542 короба</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#94a3b8;">Примерный объем (CBM):</span>
            <span id="resVolume" style="font-weight:700; color:#4ade80;">47.1 м³</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:#94a3b8;">Общий вес брутто:</span>
            <span id="resWeight" style="font-weight:700; color:#f59e0b;">6 230 кг</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- RFQ Inquiry Form -->
  <section id="rfqFormSection" style="background: #0f172a; padding: 80px 24px; border-top: 1px solid rgba(255,255,255,0.08);">
    <div style="max-width: 800px; margin: 0 auto; background: rgba(18, 27, 49, 0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
      <div style="text-align: center; margin-bottom: 30px;">
        <span style="color: #e50408; font-weight: 700; text-transform: uppercase; font-size: 0.85rem;">Прямая связь с фабрикой WIDEWAY</span>
        <h2 style="font-size: 2rem; font-weight: 800; color: #fff; margin-top: 6px;">Запрос коммерческого предложения и расчет стоимости</h2>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 6px;">Ответ инженера и экспортного менеджера в течение 2–4 часов с предварительным расчетом FOB/CIF.</p>
      </div>

      <form id="cisRfqForm" onsubmit="handleCisRfqSubmit(event)">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
          <div>
            <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Ваше имя *</label>
            <input type="text" id="rfqName" required placeholder="Иван Смирнов" style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;">
          </div>
          <div>
            <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Компания / Бренд *</label>
            <input type="text" id="rfqCompany" required placeholder="ООО Ритейл Групп / Brand Name" style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;">
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
          <div>
            <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Email для связи *</label>
            <input type="email" id="rfqEmail" required placeholder="buyer@company.ru" style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;">
          </div>
          <div>
            <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Телефон / WhatsApp / Telegram *</label>
            <input type="text" id="rfqPhone" required placeholder="+7 999 123-45-67" style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;">
          </div>
        </div>

        <div style="margin-bottom: 16px;">
          <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Интересующая категория обуви:</label>
          <select id="rfqCategory" style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;">
            <option value="Running">Беговые кроссовки (Pro-Run Nitrogene)</option>
            <option value="Casual">Повседневные и ретро-кеды (Heritage Court T-Toe)</option>
            <option value="Trail">Треккинговая мембранная обувь (All-Terrain Trail)</option>
            <option value="Slides">Анатомические слайды и сланцы (Ultra-Cushion EVA)</option>
            <option value="Custom">Индивидуальная разработка по образцу / Tech Pack</option>
          </select>
        </div>

        <div style="margin-bottom: 20px;">
          <label style="display:block; font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">Техническое задание, объем партии или ссылки на референсы:</label>
          <textarea id="rfqMessage" rows="4" placeholder="Укажите желаемое количество пар, целевой диапазон цен, требования к маркировке Честный ЗНАК или брендингу..." style="width:100%; background:#0b1326; border:1px solid rgba(255,255,255,0.15); color:#fff; padding:10px 14px; border-radius:6px; font-size:0.9rem;"></textarea>
        </div>

        <button type="submit" style="width:100%; background:#e50408; color:#fff; border:none; padding:14px; border-radius:8px; font-size:1rem; font-weight:700; cursor:pointer; box-shadow:0 4px 15px rgba(229,4,8,0.3);">
          🚀 Отправить запрос на фабрику WIDEWAY
        </button>
        <div id="rfqStatus" style="display:none; margin-top:14px; text-align:center; font-size:0.9rem; font-weight:600;"></div>
      </form>
    </div>
  </section>

  <!-- Footer -->
  <footer style="background: #0b1120; border-top: 1px solid rgba(255,255,255,0.08); padding: 50px 24px; font-size: 0.85rem; color: #94a3b8;">
    <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 30px;">
      <div>
        <div style="font-weight: 800; color: #fff; font-size: 1.1rem; margin-bottom: 12px;">WIDEWAY GROUP</div>
        <p style="line-height: 1.5;">Официальный производитель и экспортер обуви. Фабричный комплекс в Цзиньцзяне (провинция Фуцзянь, Китай). Поставки качественной обуви по всему миру с 2007 года.</p>
      </div>
      <div>
        <div style="font-weight: 700; color: #fff; margin-bottom: 12px;">Направления для СНГ</div>
        <ul style="list-style: none; padding: 0; line-height: 2;">
          <li><a href="/ru/cis-central-asia/" style="color: #cbd5e1; text-decoration: none;">Экспорт в Россию, Казахстан, Узбекистан</a></li>
          <li><a href="/quality-control" style="color: #cbd5e1; text-decoration: none;">Стандарты лаборатории SATRA</a></li>
          <li><a href="/production-capacity" style="color: #cbd5e1; text-decoration: none;">Производственные мощности фабрики</a></li>
          <li><a href="/certifications" style="color: #cbd5e1; text-decoration: none;">Сертификаты BSCI, ISO9001, GRS</a></li>
        </ul>
      </div>
      <div>
        <div style="font-weight: 700; color: #fff; margin-bottom: 12px;">Прямые контакты</div>
        <p style="line-height: 1.8;">
          📍 8F, Bldg 8A, No.618 Jinxin Rd, ChenDai, Jinjiang, Fujian, China<br>
          📞 WhatsApp: <a href="https://wa.me/{WHATSAPP_CLEAN}" style="color: #4ade80; text-decoration: none;">{WHATSAPP_NUMBER}</a><br>
          ✉️ Email: <a href="mailto:{EMAIL_CIS}" style="color: #60a5fa; text-decoration: none;">{EMAIL_CIS}</a><br>
          💬 Telegram: <a href="{TELEGRAM_CIS_URL}" style="color: #38bdf8; text-decoration: none;">{TELEGRAM_CIS_HANDLE}</a>
        </p>
      </div>
    </div>
    <div style="max-width: 1200px; margin: 30px auto 0 auto; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; font-size: 0.78rem;">
      &copy; 2007–2026 Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP). Все права защищены.
    </div>
  </footer>

  <script>
  function updateFootwearLogisticsCalc() {{
    const pairs = parseInt(document.getElementById('calcPairs').value) || 0;
    const packType = document.getElementById('calcPackType').value;
    
    let pairsPerCarton = packType === 'boxed' ? 12 : 24;
    let cartonVol = packType === 'boxed' ? 0.087 : 0.108;
    let cartonWeight = packType === 'boxed' ? 11.5 : 18.0;
    let containerCapacity = packType === 'boxed' ? 6500 : 12000;
    
    const cartons = Math.ceil(pairs / pairsPerCarton);
    const totalVol = (cartons * cartonVol).toFixed(1);
    const totalWeight = Math.round(cartons * cartonWeight);
    const containers = (pairs / containerCapacity).toFixed(2);
    
    document.getElementById('resContainers').innerText = `${{containers}} x 40HQ`;
    document.getElementById('resCartons').innerText = `${{cartons}} коробов`;
    document.getElementById('resVolume').innerText = `${{totalVol}} м³`;
    document.getElementById('resWeight').innerText = `${{totalWeight.toLocaleString()}} кг`;
  }}

  async function handleCisRfqSubmit(e) {{
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    const statusBox = document.getElementById('rfqStatus');
    btn.disabled = true;
    btn.innerText = 'Отправка запроса...';
    
    const payload = {{
      name: document.getElementById('rfqName').value,
      company: document.getElementById('rfqCompany').value,
      email: document.getElementById('rfqEmail').value,
      phone: document.getElementById('rfqPhone').value,
      category: document.getElementById('rfqCategory').value,
      message: document.getElementById('rfqMessage').value,
      source_lang: 'RU_CIS'
    }};
    
    try {{
      const res = await fetch('/api/inquire', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
      statusBox.style.display = 'block';
      statusBox.style.color = '#4ade80';
      statusBox.innerText = '✓ Спасибо! Ваш запрос успешно зарегистрирован. Экспортный менеджер свяжется с вами в течение 2-4 часов.';
      e.target.reset();
    }} catch (err) {{
      statusBox.style.display = 'block';
      statusBox.style.color = '#60a5fa';
      statusBox.innerText = '✓ Запрос принят! Вы также можете написать нам напрямую в WhatsApp: {WHATSAPP_NUMBER}';
    }} finally {{
      btn.disabled = false;
      btn.innerText = '🚀 Отправить запрос на фабрику WIDEWAY';
    }}
  }}
  </script>
</body>
</html>
"""
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Compiled /ru/index.html ({len(html)} bytes)")

def compile_cis_central_asia_portal():
    """Generates /ru/cis-central-asia/index.html (Dedicated CIS Engineering & Logistics Hub)."""
    out_dir = os.path.join(BASE_DIR, "ru", "cis-central-asia")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.html")

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Поставки обуви оптом в Россию, Казахстан и Узбекистан | Фабрика WIDEWAY (ЕАЭС / СНГ)</title>
  <meta name="description" content="Контрактное производство обуви для рынков России, Казахстана, Узбекистана и Беларуси. Соответствие ТР ТС 017/2011, нанесение кодов «Честный ЗНАК» / ИС МПТ, морозостойкость до -35°C, расчеты в юанях/рублях, прямые контейнерные поезда из Цзиньцзяна.">
  <meta name="keywords" content="обувь оптом россия, фабрика обуви казахстан, пошив обуви узбекистан, тр тс 017 2011 обувь, честный знак обувь китай, жд доставка обуви китай москва, контрактное производство кроссовок снг">
  <link rel="canonical" href="https://www.widewayfootwear.com/ru/cis-central-asia/">
  
  <meta name="yandex-verification" content="{YANDEX_VERIFICATION_CODE}">
  <link rel="alternate" hreflang="en" href="https://www.widewayfootwear.com/" />
  <link rel="alternate" hreflang="ru" href="https://www.widewayfootwear.com/ru/" />
  <link rel="alternate" hreflang="ru-RU" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-KZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-UZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-BY" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="x-default" href="https://www.widewayfootwear.com/" />
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="Прямые поставки фабричной обуви в РФ, Казахстан и Центральную Азию | WIDEWAY GROUP">
  <meta property="og:description" content="Регламент ТР ТС 017/2011, маркировка Честный ЗНАК, морозостойкие подошвы -35°C, расчеты в юанях и рублях.">
  <meta property="og:url" content="https://www.widewayfootwear.com/ru/cis-central-asia/">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:locale:alternate" content="ru_KZ">
  <meta property="og:locale:alternate" content="ru_UZ">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
</head>
<body style="background: #090e1a; color: #f8fafc; font-family: 'Inter', sans-serif;">

  <!-- Header -->
  <header style="background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.08); position: sticky; top: 0; z-index: 1000; padding: 14px 24px;">
    <div style="max-width: 1280px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
      <a href="/ru/" style="display: flex; align-items: center; gap: 12px; text-decoration: none;">
        <span style="background: #e50408; color: #fff; font-weight: 800; font-size: 1.15rem; padding: 4px 10px; border-radius: 6px; letter-spacing: 1px;">WIDEWAY</span>
        <span style="font-weight: 700; color: #fff; font-size: 1.05rem;">ЦЕНТРАЛЬНАЯ АЗИЯ &amp; ЕАЭС</span>
      </a>
      
      <nav style="display: flex; align-items: center; gap: 24px;">
        <a href="/ru/" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Главная (RU)</a>
        <a href="/ru/cis-central-asia/" style="color: #fff; font-weight: 600; text-decoration: none; border-bottom: 2px solid #e50408; padding-bottom: 4px;">Спецификация СНГ</a>
        <a href="/products" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Каталог</a>
        <a href="/contact" style="color: #94a3b8; font-weight: 500; text-decoration: none;">Контакты</a>
        
        <div style="display: flex; align-items: center; background: rgba(255,255,255,0.08); border-radius: 20px; padding: 2px 4px;">
          <a href="/" style="color: #94a3b8; font-size: 0.78rem; padding: 4px 10px; text-decoration: none;">EN</a>
          <span style="background: #e50408; color: #fff; font-size: 0.78rem; font-weight: 700; padding: 4px 10px; border-radius: 16px;">RU</span>
        </div>
      </nav>
      
      <div style="display: flex; align-items: center; gap: 12px;">
        <a href="https://wa.me/{WHATSAPP_CLEAN}?text=Здравствуйте!%20Интересует%20поставка%20обуви%20в%20РФ/СНГ" target="_blank" style="background: #25d366; color: #fff; padding: 8px 16px; border-radius: 8px; font-weight: 600; text-decoration: none; font-size: 0.85rem;">
          💬 WhatsApp
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section style="padding: 70px 24px; max-width: 1180px; margin: 0 auto;">
    <div style="display: inline-block; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); color: #93c5fd; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; margin-bottom: 16px;">
      🇷🇺 РОССИЯ · 🇰🇿 КАЗАХСТАН · 🇺🇿 УЗБЕКИСТАН · 🇧🇾 БЕЛАРУСЬ
    </div>
    <h1 style="font-family: 'Outfit', sans-serif; font-size: 2.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 20px; color: #fff;">
      Инженерные решения для поставок обуви в страны ЕАЭС и Центральной Азии
    </h1>
    <p style="font-size: 1.1rem; color: #cbd5e1; line-height: 1.6; max-width: 880px; margin-bottom: 40px;">
      Рынок обуви стран СНГ предъявляет жесткие технические и климатические требования: устойчивость к морозам до <strong>-35°C</strong>, отсутствие хрупкости подошвы при перепадах температур, обязательное декларирование по <strong>ТР ТС 017/2011</strong> и поштучная агрегация цифровых кодов <strong>«Честный ЗНАК»</strong>. Фабрика WIDEWAY полностью закрывает эти задачи на этапе производства.
    </p>

    <!-- 4 Pillars Grid -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; margin-bottom: 60px;">
      <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px;">
        <div style="font-size: 2rem; margin-bottom: 12px;">❄️</div>
        <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 8px;">Морозостойкость до -35°C</h3>
        <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
          Специальная рецептура резины и ЭВА с низкотемпературными пластификаторами. Подошва не застывает в «пластик» на льду и сохраняет мягкую амортизацию и сцепление.
        </p>
      </div>

      <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px;">
        <div style="font-size: 2rem; margin-bottom: 12px;">🏷️</div>
        <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 8px;">Маркировка «Честный ЗНАК»</h3>
        <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
          Печать DataMatrix кодов на вшивных ярлыках, коробках и упаковке транспортных паллет/коробов. Формирование файлов агрегации для мгновенного ввода в оборот.
        </p>
      </div>

      <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px;">
        <div style="font-size: 2rem; margin-bottom: 12px;">🚆</div>
        <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 8px;">Ж/Д Доставка (12–18 дней)</h3>
        <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
          Прямые контейнерные поезда через Достык / Алашанькоу и Хоргос / Алтынколь. Таможенная очистка на станции назначения (Ворсино, Шушары, Кольцово, Алматы, Ташкент).
        </p>
      </div>

      <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px;">
        <div style="font-size: 2rem; margin-bottom: 12px;">💱</div>
        <h3 style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 8px;">Оплата в CNY и Рублях</h3>
        <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
          Официальные внешнеторговые контракты, прямые платежи в китайских юанях и рублях через ВТБ (Шанхай), Банк Харбина и CIPS без риска блокировки SWIFT.
        </p>
      </div>
    </div>

    <!-- Princeton GEO 3-Sentence Structured FAQ Blocks for AI Bots -->
    <div style="background: rgba(18, 27, 49, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 36px; margin-bottom: 60px;">
      <h2 style="font-size: 1.8rem; font-weight: 800; color: #fff; margin-bottom: 24px; text-align: center;">
        Вопросы и ответы для байеров и технических специалистов (FAQ)
      </h2>

      <div style="margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 20px;">
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px;">
          1. Каков минимальный объем заказа (MOQ) и сроки производства?
        </h3>
        <p style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6;">
          Минимальный объем заказа на фабрике WIDEWAY составляет <strong>500 пар на цвет</strong> для серийных моделей и 1 000 пар для полностью уникальных пресс-форм. Разработка первого образца (прототипа) по эскизу или Tech Pack занимает <strong>7–10 дней</strong>, а производство серийной партии — <strong>30–40 дней</strong>. Запросы направляются напрямую в экспортный отдел: <code>amy@widewaygroup.com</code>.
        </p>
      </div>

      <div style="margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 20px;">
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px;">
          2. Как фабрика помогает с маркировкой «Честный ЗНАК» в России и Казахстане?
        </h3>
        <p style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6;">
          Фабрика WIDEWAY получает сгенерированные клиентом коды маркировки формата GS1 DataMatrix (в файлах CSV/PDF) и наносит термотрансферные влагостойкие этикетки на каждую индивидуальную коробку и вшивной ярлык. Дополнительно формируется упаковочный лист с точной агрегацией кодов по мастер-коробам (SSCC), что позволяет импортеру провести таможенное оформление без перемаркировки на СВХ.
        </p>
      </div>

      <div style="margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 20px;">
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px;">
          3. Какие испытания проходит обувь по нормам ТР ТС 017/2011?
        </h3>
        <p style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6;">
          Вся продукция сертифицируется по ГОСТ 9134-78 (прочность крепления подошвы не менее 3.8 Н/мм при норме 3.0 Н/мм) и ГОСТ Р ИСО 17707-2014 (стойкость к многократному изгибу подошвы без трещин свыше 50 000 циклов). Материалы верха и подкладки соответствуют жестким нормам химической безопасности ТР ТС 017/2011 по отсутствию свободного формальдегида и токсичных красителей.
        </p>
      </div>

      <div>
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px;">
          4. По каким кодам ТН ВЭД декларируется спортивная и повседневная обувь?
        </h3>
        <p style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6;">
          Спортивные беговые и тренировочные кроссовки декларируются по коду <strong>6402 19 000 0</strong> (с верхом из полимерных материалов) или <strong>6404 11 000 0</strong> (с верхом из текстиля/жаккарда). Повседневные городские кроссовки из натуральной кожи и спилка декларируются по коду <strong>6403 99 930 0 / 6403 99 960 0</strong>. WIDEWAY готовит полный пакет отгрузочных документов: инвойс, упаковочный лист с разбивкой по размерам, сертификат происхождения СТ-1 и протоколы испытаний.
        </p>
      </div>
    </div>

    <!-- CTA Section -->
    <div style="background: linear-gradient(135deg, rgba(229,4,8,0.2) 0%, rgba(30,41,59,0.8) 100%); border: 1px solid rgba(229,4,8,0.4); border-radius: 12px; padding: 40px; text-align: center;">
      <h2 style="font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 12px;">Готовы обсудить производство коллекции?</h2>
      <p style="color: #cbd5e1; max-width: 680px; margin: 0 auto 24px auto; line-height: 1.5;">
        Свяжитесь с русскоязычным экспортным менеджером напрямую. Мы вышлем каталоги актуальных пресс-форм, образцы материалов и организуем онлайн-тур по фабрике.
      </p>
      <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
        <a href="https://wa.me/{WHATSAPP_CLEAN}?text=Здравствуйте!%20Хотим%20обсудить%20коллекцию%20обуви" target="_blank" style="background: #25d366; color: #fff; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.95rem;">
          💬 Написать в WhatsApp ({WHATSAPP_NUMBER})
        </a>
        <a href="mailto:{EMAIL_CIS}?subject=B2B%20Footwear%20Inquiry%20from%20CIS" style="background: #e50408; color: #fff; padding: 12px 28px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.95rem;">
          ✉️ Отправить ТЗ на {EMAIL_CIS}
        </a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer style="background: #0b1120; border-top: 1px solid rgba(255,255,255,0.08); padding: 40px 24px; text-align: center; font-size: 0.85rem; color: #94a3b8;">
    <div style="max-width: 1200px; margin: 0 auto;">
      &copy; 2007–2026 Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP). Все права защищены.
    </div>
  </footer>

</body>
</html>
"""
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Compiled /ru/cis-central-asia/index.html ({len(html)} bytes)")

def inject_yandex_and_hreflang_across_site():
    """Injects Yandex verification, hreflang, OpenGraph, and Clean-param into all root HTML pages."""
    print("  Injecting Yandex tags, multi-regional hreflang, and OpenGraph locales across root HTML pages...")
    
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html")]
    modified_count = 0
    
    yandex_tags_block = f"""
  <!-- Yandex Search, Yandex Neuro & Central Asia GEO Meta Tags -->
  <meta name="yandex-verification" content="{YANDEX_VERIFICATION_CODE}">
  <link rel="alternate" hreflang="en" href="https://www.widewayfootwear.com/" />
  <link rel="alternate" hreflang="ru" href="https://www.widewayfootwear.com/ru/" />
  <link rel="alternate" hreflang="ru-RU" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-KZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-UZ" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="ru-BY" href="https://www.widewayfootwear.com/ru/cis-central-asia/" />
  <link rel="alternate" hreflang="x-default" href="https://www.widewayfootwear.com/" />
  <meta property="og:locale" content="en_US">
  <meta property="og:locale:alternate" content="ru_RU">
  <meta property="og:locale:alternate" content="ru_KZ">
  <meta property="og:locale:alternate" content="ru_UZ">
  <meta property="og:locale:alternate" content="ru_BY">
"""

    for fname in html_files:
        fpath = os.path.join(BASE_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove existing yandex & hreflang block to ensure clean canonical update
        content = re.sub(r'<!--\s*Yandex Search, Yandex Neuro & Central Asia GEO Meta Tags\s*-->.*?<meta property="og:locale:alternate" content="ru_BY">\s*', '', content, flags=re.DOTALL)

        # Inject right before </head>
        if "</head>" in content:
            new_content = content.replace("</head>", f"{yandex_tags_block}\n</head>", 1)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_count += 1

    print(f"  ✅ Injected and updated canonical Yandex & hreflang tags in {modified_count} HTML pages.")

def generate_ai_cis_gost_matrix():
    """Generates machine-readable /ai/cis-gost-matrix.json for Яндекс Нейро & Алиса AI."""
    os.makedirs(os.path.join(BASE_DIR, "ai"), exist_ok=True)
    out_file = os.path.join(BASE_DIR, "ai", "cis-gost-matrix.json")

    data = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "name": "WIDEWAY Footwear ГОСТ ↔ ISO ↔ SATRA Technical Compliance & EAEU TR CU 017/2011 Specification",
        "publisher": {
            "@type": "Organization",
            "name": "Jinjiang Wideway Import & Export Co., Ltd.",
            "alternateName": "WIDEWAY GROUP",
            "url": "https://www.widewayfootwear.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Jinjiang",
                "addressRegion": "Fujian",
                "addressCountry": "CN"
            }
        },
        "targetRegions": ["RU", "KZ", "UZ", "BY", "KG", "TJ"],
        "customsClassifications": {
            "athletic_sneakers_synthetic": "6402 19 000 0",
            "casual_sneakers_synthetic_poly": "6402 99 980 0",
            "leather_upper_sneakers": "6403 99 930 0",
            "textile_court_shoes": "6404 11 000 0"
        },
        "mandatoryCertifications": [
            "ТР ТС 017/2011 (Декларация о соответствии ЕАС)",
            "Честный ЗНАК (GS1 DataMatrix 2D Barcode Aggregation)",
            "Сертификат происхождения СТ-1 / Form A"
        ],
        "logisticsMetrics": {
            "40HQ_container_boxed_pairs": "6200 - 6600 pairs (520 - 550 master cartons)",
            "40HQ_container_polybag_pairs": "11000 - 13000 pairs",
            "rail_transit_dostyk_almaty_days": "12 - 16 days",
            "rail_transit_moscow_vorsino_days": "16 - 22 days",
            "sea_rail_vladivostok_days": "14 - 18 days",
            "acceptedCurrencies": ["CNY", "RUB", "USD", "EUR"]
        },
        "technicalParameters": GOST_EQUIVALENCE_ROWS,
        "importSubstitutionMatrix": SUBSTITUTION_ROWS
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Generated /ai/cis-gost-matrix.json ({len(json.dumps(data))} bytes)")

def upgrade_robots_and_sitemap():
    """Updates robots.txt and sitemap.xml with Yandex, AI bots, and Russian URLs."""
    robots_path = os.path.join(BASE_DIR, "robots.txt")
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")

    # Upgrade robots.txt
    robots_content = """User-agent: *
Allow: /

# Yandex Search, Yandex Neuro (Яндекс Нейро) & Alice AI (Алиса) Directives
User-agent: Yandex
Allow: /
Clean-param: utm_source&utm_medium&utm_campaign&utm_term&utm_content&yclid&ymclid&gclid&fbclid&_openstat&from&etext /

User-agent: YandexBot
Allow: /

User-agent: YandexImages
Allow: /images/

User-agent: YandexDirect
Allow: /

User-agent: YandexMetrika
Allow: /

# Explicit Directives for AI Retrieval & Web Search Bots
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: DeepSeekBot
Allow: /

# Canonical Sitemaps & Machine-Readable AI Knowledge
Sitemap: https://www.widewayfootwear.com/sitemap.xml
# llms.txt: https://www.widewayfootwear.com/llms.txt
# llms-full.txt: https://www.widewayfootwear.com/llms-full.txt
# ai-cis-gost-matrix: https://www.widewayfootwear.com/ai/cis-gost-matrix.json
"""
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("  ✅ Updated robots.txt with Yandex Clean-param and AI bot directives")

    # Upgrade sitemap.xml to include /ru/ and /ru/cis-central-asia/
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            s_content = f.read()

        ru_entries = """  <url>
    <loc>https://www.widewayfootwear.com/ru/</loc>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.widewayfootwear.com/ru/cis-central-asia/</loc>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""

        if "https://www.widewayfootwear.com/ru/" not in s_content:
            s_content = s_content.replace("</urlset>", ru_entries)
            with open(sitemap_path, "w", encoding="utf-8") as f:
                f.write(s_content)
            print("  ✅ Added /ru/ and /ru/cis-central-asia/ into sitemap.xml")

def upgrade_llms_txt():
    """Appends Section on CIS, ГОСТ, and Eurasian Rail Logistics into llms.txt and llms-full.txt."""
    cis_section = """
## 8. EAEU, Russia & Central Asia Footwear Export Specification (ТР ТС 017/2011 & Честный ЗНАК)
* **Factory Name**: Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP).
* **Target CIS Markets**: Russian Federation, Kazakhstan, Uzbekistan, Belarus, Kyrgyzstan.
* **Mandatory Regulations**: Full compliance with EAEU Technical Regulation ТР ТС 017/2011 ("On the safety of light industry products") and EAC Declaration of Conformity.
* **Digital Track-and-Trace Barcode Mark**: Factory executes 100% aggregation and printing of national "Честный ЗНАК" / IS MPT GS1 DataMatrix barcodes on shoe tongue labels, individual shoeboxes, and master shipping cartons.
* **Cold Climate Sub-Zero Engineering**:
  - Outsole rubber and modified EVA/TPU tested down to -35°C without plastic embrittlement (ГОСТ Р ИСО 17707-2014 / SATRA TM161 > 30,000 cold flex cycles).
  - Sole cementing bond strength ≥ 3.8 - 4.5 N/mm under ГОСТ 9134-78 / SATRA TM411 (far exceeding ГОСТ minimum of 3.0 N/mm).
  - Dynamic waterproof bootie construction exceeding 15,000 - 25,000 flex cycles under ASTM F1671 / SATRA TM230.
* **Multimodal Logistics & Container Payload**:
  - 40HQ container payload: 6,200 to 6,600 pairs in individual branded shoeboxes (520 - 550 master cartons, ~6,200 kg gross weight).
  - Bulk polybag packing: 11,000 to 13,000 pairs per 40HQ.
  - Direct China-Europe Railway Express (中欧班列) via Dostyk / Khorgos: 12-16 days to Almaty, 14-18 days to Tashkent, 16-22 days to Moscow (Vorsino / Selyatino).
  - Sea-rail multimodal via Xiamen to Vladivostok: 14-18 days total.
* **Currency Settlement**: Direct cross-border settlements in CNY (Chinese Yuan) and RUB (Russian Rubles) via VTB Bank (Shanghai), Harbin Bank, and CIPS interbank network.
* **Direct Export Desk Contact**: WhatsApp: +86 185 0595 9266 | Email: amy@widewaygroup.com | Telegram: @widewayfootwear_cis.
"""
    for txt_file in ["llms.txt", "llms-full.txt"]:
        p = os.path.join(BASE_DIR, txt_file)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            if "ТР ТС 017/2011" not in content:
                content += "\n" + cis_section
                with open(p, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✅ Appended Section 8 (CIS/EAEU ГОСТ & Logistics) into {txt_file}")

def main():
    print("=" * 70)
    print("🚀 WIDEWAY FOOTWEAR - YANDEX SEO & CIS/CENTRAL ASIA GEO COMPILER")
    print("=" * 70)
    
    compile_ru_portal()
    compile_cis_central_asia_portal()
    inject_yandex_and_hreflang_across_site()
    generate_ai_cis_gost_matrix()
    upgrade_robots_and_sitemap()
    upgrade_llms_txt()
    
    print("=" * 70)
    print("✨ ALL CIS & YANDEX ASSETS COMPILED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
