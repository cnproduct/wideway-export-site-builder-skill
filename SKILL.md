---
name: B2B Export Site Builder & CMS Master
description: 全生命周期工业出海 B2B 独立站与 Master CMS 管理后台自动化构建技能。支持 20+ 出海落地页极速生成、Shopify 双列商品主控器、50MB 4K/1080P 产品视频展厅、多视角图库、直观可视化在位编辑、AI-Ready 深度 SEO/GEO 矩阵生成与一键 SSH 部署。
---

# 🚀 B2B Export Site Builder & Master CMS Skill

本技能是一套出版级、高度数据驱动的 **B2B 工业出海独立站与 Master CMS 全栈建站引擎**。旨在让外贸制造企业（鞋业、服装、箱包、石材、汽配、电子、五金、医疗耗材等）在数秒内构建拥有全球顶级工业美学、完整制造实力证明、Shopify 级产品编辑中台及 AI 搜索引擎优先索引（GEO/SEO）的官方出海门户。

---

## 🌟 核心特性与架构能力

### 1. 20+ 工业制造出海专属页面（标准覆盖全决策链路）
* **品牌与生产实力**：`index.html`（超级首页/工厂全景/360° VR实景/Archival专区/合作品牌）、`production-capacity.html`（产能线/自动化/月产统计）、`quality-control.html`（32道物理测试/SATRA实验室/零缺陷QC）、`certifications.html`（BSCI/SEDEX/ISO9001/GRS/OEKO-TEX证书验真）、`sustainability.html`（环保再生材料/生物基/屋顶光伏）。
* **定制与研发体系**：`oem-odm.html`（定制开发流程/48-72h极速打样/鞋楦模具研发/小单孵化）、`case-studies.html`（国际商超代工案例/独立品牌孵化）、`heritage-footwear-reproduction.html`（1:1 档案复刻/历史鞋楦逆向工程）、`brand-identity.html`（企业视觉规范与品牌故事）。
* **产品矩阵与详情**：`products.html`（全品类筛选/搜索/类目Tab/多维度排序）、`product-detail.html`（动态 ID/Slug 解析、多角度图库轮播、4K/1080P 视频播放器、规格参数表、离线询盘弹窗）、动态分类聚合页（`*-wholesale.html`, `*-manufacturer.html`）。
* **内容与权威背书**：`news.html` & `news-detail.html`（行业洞察/展会动态/定期发布引擎）、`videos.html`（4K 视频工厂展厅）、`glossary.html`（出海专业术语库）、`whitepapers.html`（行业采购白皮书）、`knowledge-base.html`（采购FAQ/Incoterms/验货标准）、`knowledge-graph.html`（供应链知识图谱）。
* **转化与直通触达**：`contact.html`（多业务员 WhatsApp/邮箱直通分流、Google 地图定位、RFQ 表单）。

### 2. Shopify 风格双列商品主控器 (`admin.html` + `server.py`)
* **全属性精细化管理**：品名、SKU、URL Slug、类目、徽章标签、梯队 MOQ、FOB 价格带、交期。
* **多视角图库与高层级素材库**：支持 1 行 1 个 URL 追加角度，缩略图实时预览；媒体库弹窗采用 `z-index: 20000` 最顶层设计，在商品编辑弹窗上层直接打开选图并自动追加，无需关闭或丢失当前编辑进度。
* **4K/1080P 视频展示展厅**：支持最大 **50MB** 视频上传或外链绑定，前端商品详情页自动切换高保真全屏视频播放器。
* **规格参数矩阵**：面料材质、内里、鞋垫、大底、尺码跨度、可选配色、打样周期、包装方式、权威认证。
* **SEO & GEO 精准投放**：每个 SKU 独立配置 SEO 标题、Meta Description、搜索关键词与目标国家/地区（Target GEO）。

### 3. 可视化在位实时编辑 (Visual In-Place CMS)
* 在管理后台直观定位任意页面的文本段落、标题、Banner 轮播图、图片与视频，直接在线替换并秒级全站发布。

### 4. 2026 AI 搜索引擎与反爬虫矩阵
* **Google Image-Extended `sitemap.xml`**：自动抓取并绑定所有产品高清图。
* **AI-Ready & Anti-Clone `robots.txt`**：规范 Googlebot、Bingbot 爬取，同时阻断无授权恶意抓取。
* **`llms.txt` & `llms-full.txt`**：为 ChatGPT Search、Perplexity、Gemini、Claude 等 AI 搜索代理生成标准的 Markdown 结构化企业事实库。

### 5. 极速一键部署与运维保障 (`deploy_production_sync.py`)
* 自动打包、SSH/SCP 差量传输、解压并更新权限、Nginx 重新加载与 systemd 后台 API 服务无缝重启。

---

## 📂 技能目录与资源结构

```text
b2b-export-site-builder/
├── SKILL.md                          # 本说明文档
├── README.md                         # 项目主页与快速入门
├── scaffold_new_site.py              # 🚀 核心自动化脚手架脚本
├── config.example.json               # 标准通用配置文件
├── config.footwear.json              # 鞋类外贸企业预设
├── config.sportswear.json            # 服装与运动服饰预设
├── config.bags.json                  # 箱包与户外背包预设
├── config.stone.json                 # 石材与建筑材料预设
└── resources/                        # 核心全套模板与编译器
    ├── build_site.py                 # 静态 CMS 编译器
    ├── server.py                     # Python 后台 API 服务
    ├── deploy_production_sync.py     # SSH/Nginx 部署脚本
    ├── admin.html                    # 现代化后台管理控制台
    ├── scratch/
    │   └── build_admin_html.py       # 后台控制台生成器
    ├── css/
    │   └── style.css                 # 工业出海响应式设计系统
    ├── js/
    │   └── main.js                   # 3D 罗盘导航/图库/询盘交互
    ├── data/
    │   ├── site_content.template.json# 结构化企业事实库模板
    │   └── auth.json                 # 后台安全哈希密码
    └── templates/                    # 20+ 标准 HTML 页面模板
        ├── index.html
        ├── products.html
        ├── product-detail.html
        ├── oem-odm.html
        ├── production-capacity.html
        ├── quality-control.html
        ├── certifications.html
        ├── sustainability.html
        ├── case-studies.html
        ├── heritage-footwear-reproduction.html
        ├── brand-identity.html
        ├── news.html
        ├── news-detail.html
        ├── videos.html
        ├── glossary.html
        ├── whitepapers.html
        ├── knowledge-base.html
        ├── knowledge-graph.html
        └── contact.html
```

---

## 🛠️ 快速建站实战指南 (3种创建方式)

### 方式一：使用 JSON 配置文件一键生成（推荐）

1. 复制并编辑配置文件（例如 `my_company.json`）：
```json
{
  "name_en": "Quanzhou Apex Garment Co., Ltd.",
  "name_zh": "泉州巅峰服饰有限公司",
  "brand": "APEX APPAREL",
  "domain": "apexgarment.com",
  "industry": "sportswear",
  "email": "export@apexgarment.com",
  "phone": "+86 185 0595 9266",
  "whatsapp": "+86 185 0595 9266",
  "address": "Shishi Garment Industrial Park, Quanzhou, Fujian, China",
  "port": "Xiamen Port",
  "founding_year": "2010",
  "slogan": "Engineered Performance Teamwear & Seamless Activewear",
  "primary_color": "#0ea5e9",
  "secondary_color": "#6366f1",
  "password": "admin2026"
}
```

2. 执行脚手架命令生成新站点：
```bash
python3 scaffold_new_site.py --config my_company.json --out-dir ../apex-garment-portal
```

---

### 方式二：使用 CLI 命令行参数快速生成

```bash
python3 scaffold_new_site.py \
  --name-en "Tianya Cultural Stone Co., Ltd." \
  --name-zh "天涯石业有限公司" \
  --brand "TIANYA STONE" \
  --domain "tianyalimestone.com" \
  --industry "stone" \
  --email "sales@tianyalimestone.com" \
  --phone "+86 185 0000 0000" \
  --primary-color "#d97706" \
  --out-dir ../tianya-stone-site
```

---

### 方式三：交互式问答模式

直接运行不带参数的脚本，按终端提示输入即可：
```bash
python3 scaffold_new_site.py --interactive
```

---

## 💻 本地预览与管理后台启动

进入生成好的新网站目录：
```bash
cd <out-dir>

# 启动本地服务器（默认 8080 端口）
python3 server.py 8080
```

* **前台网站**：访问 `http://localhost:8080`
* **管理后台**：访问 `http://localhost:8080/admin.html`
* **默认账号密码**：可在 `config.json` 中配置，默认为密码 `admin2026`（登录后可在后台右上角设置修改）。

---

## 🌐 生产环境一键部署

1. 在新站点目录中打开 `deploy_production_sync.py`，配置你的生产服务器信息：
```python
SERVER_IP = "43.130.32.54"
SSH_PORT = 2222
SSH_USER = "ubuntu"
REMOTE_PATH = "/var/www/my-domain.com"
```

2. 运行一键部署脚本：
```bash
python3 deploy_production_sync.py
```
脚本将自动完成打包、上传、解压、权限配置、Nginx 重载以及后台 API 服务重启。

---

## 🔄 内容更新与二次构建

当你在 `data/site_content.json` 中手动添加了新的分类或修改了全局数据后，只需运行：
```bash
python3 build_site.py
```
系统将自动重新生成所有静态页面、更新分类聚合页、并重新编译最新的 `sitemap.xml` 和 `llms.txt`。
