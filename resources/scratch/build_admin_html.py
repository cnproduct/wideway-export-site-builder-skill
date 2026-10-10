#!/usr/bin/env python3
import os

admin_html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WIDEWAY MASTER B2B CMS | Enterprise Footwear Management Console</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #090e1a;
      --bg-sidebar: #0f172a;
      --bg-card: rgba(18, 27, 49, 0.75);
      --bg-card-hover: rgba(26, 39, 70, 0.85);
      --bg-input: #0b1326;
      --primary: #007aff;
      --primary-hover: #005ecb;
      --primary-glow: rgba(0, 122, 255, 0.25);
      --brand-red: #e50408;
      --brand-red-glow: rgba(229, 4, 8, 0.25);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(0, 122, 255, 0.5);
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --purple: #8b5cf6;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Outfit', sans-serif;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      overflow: hidden;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }

    /* Login Screen */
    #loginScreen {
      position: fixed;
      inset: 0;
      background: radial-gradient(circle at 50% 30%, #172554 0%, #090e1a 70%);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .login-box {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 40px;
      width: 440px;
      max-width: 90%;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(20px);
      text-align: center;
    }

    .login-box .logo-lockup {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      margin-bottom: 28px;
    }

    .login-box .logo-lockup img {
      height: 48px;
      width: auto;
    }

    .login-box h2 {
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: -0.5px;
    }

    .login-box p {
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 4px;
    }

    .input-group {
      margin-bottom: 20px;
      text-align: left;
    }

    .input-group label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .input-field {
      width: 100%;
      padding: 12px 14px;
      background: var(--bg-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      color: var(--text);
      font-size: 0.95rem;
      transition: all 0.2s;
    }

    .input-field:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    textarea.input-field {
      min-height: 90px;
      resize: vertical;
    }

    /* Buttons */
    .btn {
      padding: 10px 18px;
      border-radius: var(--radius-md);
      border: none;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 0.9rem;
      user-select: none;
    }

    .btn-primary {
      background: linear-gradient(135deg, #007aff 0%, #0056b3 100%);
      color: white;
      box-shadow: 0 4px 12px var(--primary-glow);
    }
    .btn-primary:hover { background: #0056b3; transform: translateY(-1px); }

    .btn-brand-red {
      background: linear-gradient(135deg, #e50408 0%, #b00306 100%);
      color: white;
      box-shadow: 0 4px 12px var(--brand-red-glow);
    }
    .btn-brand-red:hover { background: #b00306; transform: translateY(-1px); }

    .btn-success {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: white;
    }
    .btn-success:hover { background: #059669; }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text);
      border: 1px solid var(--border);
    }
    .btn-secondary:hover { background: rgba(255, 255, 255, 0.12); }

    .btn-danger {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .btn-danger:hover { background: #ef4444; color: white; }

    .btn-sm { padding: 6px 12px; font-size: 0.82rem; }
    .btn-block { width: 100%; }

    /* App Shell */
    #adminApp {
      display: flex;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
    }

    /* Sidebar */
    .sidebar {
      width: 280px;
      min-width: 280px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      height: 100vh;
    }

    .sidebar-header {
      padding: 24px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sidebar-header img {
      height: 32px;
      width: auto;
    }

    .sidebar-header .title-badge {
      display: flex;
      flex-direction: column;
    }

    .sidebar-header .title-badge span:first-child {
      font-weight: 800;
      font-size: 1.05rem;
      letter-spacing: 0.5px;
      color: #fff;
    }

    .sidebar-header .title-badge span:last-child {
      font-size: 0.72rem;
      color: var(--primary);
      font-weight: 700;
      letter-spacing: 1px;
    }

    .sidebar-nav {
      flex: 1;
      overflow-y: auto;
      padding: 16px 12px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .nav-group-title {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 0 12px;
      margin-bottom: 6px;
    }

    .nav-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: var(--radius-md);
      color: var(--text-muted);
      font-size: 0.9rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }

    .nav-item:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.05);
    }

    .nav-item.active {
      color: #fff;
      background: var(--primary);
      box-shadow: 0 4px 12px var(--primary-glow);
      font-weight: 600;
    }

    .nav-item .nav-icon {
      font-size: 1.1rem;
      width: 20px;
      text-align: center;
    }

    .nav-item .badge-count {
      margin-left: auto;
      background: rgba(255, 255, 255, 0.15);
      padding: 2px 7px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .sidebar-footer {
      padding: 16px 20px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
      color: var(--text-dim);
    }

    /* Main Container */
    .main-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
      background: var(--bg-dark);
    }

    /* Top Navigation Bar */
    .top-bar {
      height: 70px;
      border-bottom: 1px solid var(--border);
      padding: 0 30px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(10px);
    }

    .top-bar-left {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .page-heading {
      font-size: 1.35rem;
      font-weight: 700;
      letter-spacing: -0.3px;
    }

    .quick-search-box {
      position: relative;
      width: 320px;
    }

    .quick-search-box input {
      width: 100%;
      padding: 8px 14px 8px 36px;
      background: var(--bg-input);
      border: 1px solid var(--border);
      border-radius: 20px;
      color: var(--text);
      font-size: 0.85rem;
    }

    .quick-search-box input:focus {
      outline: none;
      border-color: var(--primary);
    }

    .quick-search-box .search-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.85rem;
      color: var(--text-dim);
    }

    .top-bar-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .server-status-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
    }

    .server-status-pill .status-dot {
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.8); }
    }

    /* Main Scroll Area */
    .content-area {
      flex: 1;
      overflow-y: auto;
      padding: 30px;
    }

    /* Tab Panels */
    .tab-panel {
      display: none;
      animation: fadeIn 0.25s ease-out;
    }

    .tab-panel.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Card Panels */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 26px;
      margin-bottom: 24px;
      backdrop-filter: blur(10px);
    }

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }

    .card-header h2 {
      font-size: 1.15rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .card-header .header-desc {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Grid Layouts */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }

    /* Metric Cards */
    .stat-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .stat-card .stat-val {
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -1px;
    }

    .stat-card .stat-label {
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Tables */
    .table-container {
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }

    table.data-table th {
      background: rgba(15, 23, 42, 0.8);
      padding: 12px 16px;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--border);
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.5px;
    }

    table.data-table td {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      color: var(--text);
      vertical-align: middle;
    }

    table.data-table tr:last-child td {
      border-bottom: none;
    }

    table.data-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    /* Status Badges */
    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 9px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .badge-status.new { background: rgba(0, 122, 255, 0.15); color: #60a5fa; border: 1px solid rgba(0, 122, 255, 0.3); }
    .badge-status.contacted { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-status.sample { background: rgba(139, 92, 246, 0.15); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.3); }
    .badge-status.won { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-status.published { background: rgba(16, 185, 129, 0.15); color: #34d399; }
    .badge-status.scheduled { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }

    /* Media Vault Grid */
    .media-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }

    .media-card {
      background: var(--bg-input);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.2s;
      position: relative;
    }

    .media-card:hover {
      border-color: var(--primary);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }

    .media-thumb-container {
      width: 100%;
      height: 130px;
      background: rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }

    .media-thumb-container img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .media-thumb-container video {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .video-play-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(0,0,0,0.7);
      color: white;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 700;
    }

    .media-meta {
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .media-name {
      font-size: 0.8rem;
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: var(--text);
    }

    .media-size {
      font-size: 0.72rem;
      color: var(--text-dim);
    }

    .media-actions {
      display: flex;
      gap: 6px;
      padding: 8px 12px;
      border-top: 1px solid var(--border);
      background: rgba(0, 0, 0, 0.1);
    }

    /* Drag & Drop Upload Zone */
    .drop-zone {
      border: 2px dashed var(--border);
      border-radius: var(--radius-lg);
      padding: 36px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: rgba(15, 23, 42, 0.3);
    }

    .drop-zone:hover, .drop-zone.drag-over {
      border-color: var(--primary);
      background: rgba(0, 122, 255, 0.05);
    }

    /* Visual Editor Preview */
    .visual-viewport-container {
      background: #000;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: calc(100vh - 230px);
    }

    .viewport-toolbar {
      background: #111a2e;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
    }

    .device-switcher {
      display: flex;
      background: rgba(0,0,0,0.3);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 2px;
      gap: 4px;
    }

    .device-btn {
      padding: 4px 10px;
      border-radius: 4px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.8rem;
      font-weight: 600;
    }

    .device-btn.active {
      background: var(--primary);
      color: white;
    }

    .iframe-wrapper {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #0b0f19;
      overflow: hidden;
    }

    .preview-iframe {
      width: 100%;
      height: 100%;
      border: none;
      background: white;
      transition: width 0.3s;
    }

    /* Accordion & Block Cards */
    .block-accordion {
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      margin-bottom: 12px;
      overflow: hidden;
      background: var(--bg-card);
    }

    .accordion-header {
      padding: 16px 20px;
      background: rgba(15, 23, 42, 0.4);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      font-weight: 600;
      font-size: 0.95rem;
    }

    .accordion-header:hover {
      background: rgba(255, 255, 255, 0.03);
    }

    .accordion-content {
      padding: 20px;
      border-top: 1px solid var(--border);
      display: none;
    }

    .accordion-content.open {
      display: block;
    }

    /* Modals */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(6px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 10000;
    }

    .modal-overlay.active {
      display: flex;
    }

    /* Top-layer Sub-Modals (Media Picker, Replace Asset Modals) */
    .modal-overlay-picker,
    #mediaPickerModal,
    #replaceMediaModal {
      z-index: 20000 !important;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
    }

    .modal-dialog {
      background: #111a2e;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      width: 700px;
      max-width: 92%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 30px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    .modal-dialog.modal-lg {
      width: 900px;
    }

    .modal-dialog.modal-xl {
      width: 1200px;
      max-width: 96%;
    }

    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }

    .modal-header h3 {
      font-size: 1.25rem;
      font-weight: 700;
    }

    .modal-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.4rem;
      cursor: pointer;
    }
    .modal-close-btn:hover { color: white; }

    /* Toast Notification */
    #toastContainer {
      position: fixed;
      bottom: 30px;
      right: 30px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 99999;
    }

    .toast-item {
      padding: 14px 20px;
      border-radius: var(--radius-md);
      color: white;
      font-size: 0.9rem;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 280px;
      animation: slideIn 0.3s ease-out;
    }

    .toast-item.success { background: #10b981; }
    .toast-item.error { background: #ef4444; }
    .toast-item.info { background: #007aff; }

    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* Terminal Console */
    .terminal-console {
      background: #060911;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: var(--radius-md);
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #38bdf8;
      height: 280px;
      overflow-y: auto;
      white-space: pre-wrap;
      line-height: 1.6;
    }
  </style>
</head>
<body>

  <!-- 1. Master Login Overlay -->
  <div id="loginScreen">
    <div class="login-box">
      <div class="logo-lockup">
        <img src="images/logo.png" alt="WIDEWAY Logo" onerror="this.src='https://via.placeholder.com/140x40?text=WIDEWAY'">
        <h2>WIDEWAY CMS MASTER</h2>
        <p>Enterprise Footwear Independent Site Console</p>
      </div>
      <form id="loginForm" onsubmit="handleLoginSubmit(event)">
        <div class="input-group">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <label style="margin: 0;">Master Authorization Key</label>
            <button type="button" onclick="toggleLoginPasswordVisibility()" style="background: none; border: none; color: #94a3b8; font-size: 0.78rem; cursor: pointer; padding: 0;">👁️ Show/Hide</button>
          </div>
          <div style="position: relative;">
            <input type="password" id="loginPasswordInput" class="input-field" placeholder="Enter administrative password..." required autofocus style="font-family: var(--font-sans);">
          </div>
          <div style="margin-top: 8px; font-size: 0.75rem; color: #94a3b8; display: flex; justify-content: space-between; align-items: center; background: rgba(30,41,59,0.5); padding: 6px 10px; border-radius: 4px; border: 1px solid #334155;">
            <span>Default: <code style="color: #60a5fa; font-weight: 700; font-size: 0.82rem;">WHJCwhjc2026</code></span>
            <span style="color: #cbd5e1;">(大写WHJC + 小写whjc + 2026)</span>
          </div>
        </div>
        <button type="submit" class="btn btn-primary btn-block" style="padding: 13px; font-size: 0.95rem; font-weight: 700; margin-top: 14px;">
          <span>🔒 Authenticate &amp; Access Admin Desk</span>
        </button>
      </form>
    </div>
  </div>

  <!-- 2. Main Admin App Shell -->
  <div id="adminApp" style="display: none;">

    <!-- Left Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="images/logo.png" alt="WIDEWAY" onerror="this.src='https://via.placeholder.com/120x36?text=WIDEWAY'">
        <div class="title-badge">
          <span>WIDEWAY</span>
          <span>MASTER CMS v3.0</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <!-- Overview Group -->
        <div>
          <div class="nav-group-title">WORKSPACE</div>
          <ul class="nav-list">
            <li class="nav-item active" onclick="switchTab('dashboard')">
              <span class="nav-icon">📊</span>
              <span>Dashboard Overview</span>
            </li>
            <li class="nav-item" onclick="switchTab('global_search')">
              <span class="nav-icon">🔍</span>
              <span>Search &amp; Batch Replace</span>
            </li>
          </ul>
        </div>

        <!-- Content Studio Group -->
        <div>
          <div class="nav-group-title">CONTENT STUDIO</div>
          <ul class="nav-list">
            <li class="nav-item" onclick="switchTab('page_blocks')">
              <span class="nav-icon">📄</span>
              <span>Pages &amp; Block Master</span>
            </li>
            <li class="nav-item" onclick="switchTab('visual_studio')">
              <span class="nav-icon">👁️</span>
              <span>Visual Live Studio</span>
            </li>
            <li class="nav-item" onclick="switchTab('products_matrix')">
              <span class="nav-icon">👟</span>
              <span>Products Matrix</span>
              <span class="badge-count" id="badgeProductCount">115</span>
            </li>
            <li class="nav-item" onclick="switchTab('newsroom')">
              <span class="nav-icon">📰</span>
              <span>News &amp; AI Scheduler</span>
              <span class="badge-count" id="badgeNewsCount">42</span>
            </li>
          </ul>
        </div>

        <!-- Assets & Media Vault -->
        <div>
          <div class="nav-group-title">ASSET VAULT</div>
          <ul class="nav-list">
            <li class="nav-item" onclick="switchTab('media_vault')">
              <span class="nav-icon">🖼️</span>
              <span>Media &amp; Video Vault</span>
            </li>
          </ul>
        </div>

        <!-- CRM & Channels -->
        <div>
          <div class="nav-group-title">LEADS &amp; CHANNELS</div>
          <ul class="nav-list">
            <li class="nav-item" onclick="switchTab('inquiries_crm')">
              <span class="nav-icon">📥</span>
              <span>Inquiries &amp; RFQs</span>
              <span class="badge-count" id="badgeInquiryCount" style="background: var(--primary);">0</span>
            </li>
            <li class="nav-item" onclick="switchTab('contact_channels')">
              <span class="nav-icon">📞</span>
              <span>Global Contact Desk</span>
            </li>
          </ul>
        </div>

        <!-- Growth & AI Suite -->
        <div>
          <div class="nav-group-title">GROWTH &amp; AI</div>
          <ul class="nav-list">
            <li class="nav-item" onclick="switchTab('seo_geo_command')">
              <span class="nav-icon">🌐</span>
              <span>SEO &amp; GEO Command</span>
            </li>
            <li class="nav-item" onclick="switchTab('ai_copywriting')">
              <span class="nav-icon">🤖</span>
              <span>AI Multi-Lang Studio</span>
            </li>
          </ul>
        </div>

        <!-- System & DevOps -->
        <div>
          <div class="nav-group-title">SYSTEM &amp; DEVOPS</div>
          <ul class="nav-list">
            <li class="nav-item" onclick="switchTab('system_devops')">
              <span class="nav-icon">☁️</span>
              <span>Production Deployment</span>
            </li>
          </ul>
        </div>
      </nav>

      <div class="sidebar-footer">
        <span>Server: 43.130.32.54</span>
        <button class="btn btn-danger btn-sm" onclick="handleLogout()" style="padding: 4px 8px;">Logout</button>
      </div>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="main-wrapper">

      <!-- Top Header Bar -->
      <header class="top-bar">
        <div class="top-bar-left">
          <h1 class="page-heading" id="topPageTitle">Dashboard Overview</h1>
          <div class="quick-search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="quickSearchInput" placeholder="Quick Search anything (Ctrl+K)..." onkeyup="handleQuickSearch(event)">
          </div>
        </div>

        <div class="top-bar-actions">
          <div class="server-status-pill">
            <span class="status-dot"></span>
            <span>Production Engine Active</span>
          </div>

          <button class="btn btn-secondary btn-sm" onclick="downloadContentBackup()" title="Download full site JSON backup">
            <span>💾 Backup JSON</span>
          </button>

          <button class="btn btn-primary btn-sm" onclick="triggerRebuildSite()" title="Compile static pages locally">
            <span>🚀 Compile Site</span>
          </button>

          <button class="btn btn-brand-red btn-sm" onclick="triggerProductionDeployModal()" title="Deploy to live production server">
            <span>☁️ Deploy Live</span>
          </button>
        </div>
      </header>

      <!-- Scrollable Tab Content Container -->
      <main class="content-area">

        <!-- =================================================================== -->
        <!-- TAB 1: DASHBOARD OVERVIEW -->
        <!-- =================================================================== -->
        <div id="tab_dashboard" class="tab-panel active">
          <div class="grid-4" style="margin-bottom: 24px;">
            <div class="stat-card">
              <div class="stat-val" style="color: var(--primary);" id="statTotalProducts">115</div>
              <div class="stat-label">Footwear SKUs Registered</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" style="color: var(--success);" id="statTotalNews">42</div>
              <div class="stat-label">Published &amp; Scheduled Articles</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" style="color: var(--warning);" id="statTotalInquiries">0</div>
              <div class="stat-label">Total Inquiries Received</div>
            </div>
            <div class="stat-card">
              <div class="stat-val" style="color: var(--purple);" id="statTotalMedia">0</div>
              <div class="stat-label">Images &amp; Video Assets</div>
            </div>
          </div>

          <div class="grid-2">
            <!-- Quick Actions Panel -->
            <div class="card">
              <div class="card-header">
                <div>
                  <h2>⚡ Quick Action Center</h2>
                  <div class="header-desc">Instant site-wide shortcuts &amp; content generators</div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 12px;">
                <button class="btn btn-secondary" onclick="switchTab('page_blocks')" style="justify-content: flex-start; padding: 14px;">
                  <span style="font-size: 1.2rem;">✏️</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 700;">Edit Every Text, Image &amp; Video</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">Granular block-by-block content editor for all 15+ site pages</div>
                  </div>
                </button>
                <button class="btn btn-secondary" onclick="switchTab('global_search')" style="justify-content: flex-start; padding: 14px;">
                  <span style="font-size: 1.2rem;">🔎</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 700;">Global Search &amp; 1-Click Replace</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">Find any text, phone, email, or image across the entire site</div>
                  </div>
                </button>
                <button class="btn btn-secondary" onclick="switchTab('media_vault')" style="justify-content: flex-start; padding: 14px;">
                  <span style="font-size: 1.2rem;">🖼️</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 700;">Upload Images &amp; 4K Videos</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">Drag-and-drop media vault with instant 1-click replacement</div>
                  </div>
                </button>
                <button class="btn btn-secondary" onclick="switchTab('inquiries_crm')" style="justify-content: flex-start; padding: 14px;">
                  <span style="font-size: 1.2rem;">📥</span>
                  <div style="text-align: left;">
                    <div style="font-weight: 700;">Manage RFQ Leads &amp; Export CSV</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">All inquiries delivered to amy@widewaygroup.com</div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Recent Inquiries Feed -->
            <div class="card">
              <div class="card-header">
                <div>
                  <h2>📥 Recent Inquiries Feed</h2>
                  <div class="header-desc">Live buyer submissions routed to amy@widewaygroup.com</div>
                </div>
                <button class="btn btn-secondary btn-sm" onclick="switchTab('inquiries_crm')">View All</button>
              </div>
              <div id="dashInquiriesList" style="display: flex; flex-direction: column; gap: 10px; max-height: 280px; overflow-y: auto;">
                <div style="color: var(--text-muted); text-align: center; padding: 30px;">Loading inquiries...</div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 2: GLOBAL SEARCH & BATCH REPLACE -->
        <!-- =================================================================== -->
        <div id="tab_global_search" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>🔎 Full-Site Search &amp; Universal Batch Replace</h2>
                <div class="header-desc">Search every single word, phone, email, image path, and video URL across all database entries and replace in 1 click.</div>
              </div>
            </div>

            <div class="grid-2" style="margin-bottom: 20px;">
              <div class="input-group">
                <label>1. Search String (Exact Text / URL / Phone / Image)</label>
                <input type="text" id="globalSearchInput" class="input-field" placeholder="e.g. +86 185 0595 9266 or amy@widewaygroup.com or shoes" onkeyup="executeGlobalSearch()">
              </div>
              <div class="input-group">
                <label>2. Replacement String (Optional for Batch Replace)</label>
                <input type="text" id="globalReplaceInput" class="input-field" placeholder="Enter new string to replace with...">
              </div>
            </div>

            <div style="display: flex; gap: 12px; margin-bottom: 24px;">
              <button class="btn btn-primary" onclick="executeGlobalSearch()">
                <span>🔍 Search Entire Website</span>
              </button>
              <button class="btn btn-brand-red" onclick="executeBatchReplace()">
                <span>⚡ Batch Replace All Occurrences &amp; Recompile</span>
              </button>
            </div>

            <div id="globalSearchResultsContainer">
              <div style="padding: 40px; text-align: center; color: var(--text-muted); border: 1px dashed var(--border); border-radius: var(--radius-md);">
                Type any text or keyword above to see all matching pages, products, news articles, and blocks in real time.
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 3: PAGES & BLOCK MASTER (EVERY TEXT, IMAGE, VIDEO EDITABLE) -->
        <!-- =================================================================== -->
        <!-- =================================================================== -->
        <!-- TAB 3: PAGES & BLOCK MASTER (EVERY TEXT, IMAGE, VIDEO EDITABLE) -->
        <!-- =================================================================== -->
        <div id="tab_page_blocks" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>📄 Visual Page &amp; Section Block Master</h2>
                <div class="header-desc">Edit every title, paragraph, button, metric, image, and video across all core &amp; category pages.</div>
              </div>
              <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                <select id="pageSelectDropdown" class="input-field" style="width: 290px;" onchange="loadSelectedPageBlocks()">
                  <optgroup label="🏠 Core Pages">
                    <option value="home">🏠 Homepage (index.html)</option>
                    <option value="about">🏢 About Us (about.html)</option>
                    <option value="oem_odm">⚙️ OEM/ODM Customization (oem-odm.html)</option>
                    <option value="contact">📞 Contact Us (contact.html)</option>
                  </optgroup>
                  <optgroup label="👟 Footwear Categories">
                    <option value="sport_outdoor_shoes">🏃 Sport &amp; Outdoor Shoes</option>
                    <option value="casual_shoes">👞 Custom Casual Shoes</option>
                    <option value="mens_sneakers">👟 Men's Sneakers</option>
                    <option value="womens_sneakers">👠 Women's Trainers</option>
                    <option value="slides_sandals">🩴 Slides &amp; Sandals</option>
                    <option value="bags_sportswear">🎒 Sport Bags &amp; Accessories</option>
                  </optgroup>
                  <optgroup label="🏭 Manufacturing &amp; Quality">
                    <option value="production_capacity">🏭 Production Capacity (production-capacity.html)</option>
                    <option value="quality_control">🔬 Quality Control Lab (quality-control.html)</option>
                    <option value="certifications">📜 Certifications &amp; Audits (certifications.html)</option>
                    <option value="sustainability">🌱 Sustainability &amp; Eco (sustainability.html)</option>
                    <option value="heritage_footwear">⚡ 1:1 Archival Re-engineering (heritage-footwear-reproduction.html)</option>
                  </optgroup>
                  <optgroup label="📚 Resources &amp; Brand VI">
                    <option value="brand_identity">🎨 Brand Identity Guidelines (brand-identity.html)</option>
                    <option value="case_studies">🤝 Brand Partnerships &amp; Cases (case-studies.html)</option>
                    <option value="videos">🎬 Factory Video Showcase (videos.html)</option>
                    <option value="knowledge_base">📖 Knowledge Base (knowledge-base.html)</option>
                    <option value="whitepapers">📄 Technical Whitepapers (whitepapers.html)</option>
                    <option value="glossary">📚 Footwear Glossary (glossary.html)</option>
                  </optgroup>
                </select>
                <button type="button" class="btn btn-secondary" onclick="openRawHtmlForCurrentPageBlock()" title="Open direct code editor for this page">
                  <span>📝 Raw Code Editor</span>
                </button>
                <button type="button" class="btn btn-primary" onclick="savePageBlocks()">
                  <span>💾 Save &amp; Recompile Site</span>
                </button>
              </div>
            </div>

            <!-- Dynamic Block Editor Container -->
            <div id="pageBlockEditorContainer">
              <!-- Rendered dynamically by JS -->
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 4: VISUAL LIVE STUDIO (CLICK-TO-EDIT & LIVE PAGE MASTER) -->
        <!-- =================================================================== -->
        <div id="tab_visual_studio" class="tab-panel">
          <div class="card" style="padding: 16px; margin-bottom: 0;">
            <div class="visual-viewport-container">
              <div class="viewport-toolbar">
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                  <span style="font-weight: 700; font-size: 0.85rem; color: #cbd5e1;">Preview Page:</span>
                  <select id="visualPagePicker" class="input-field" style="padding: 6px 10px; width: 230px; font-size: 0.85rem;" onchange="updateVisualIframeSrc()">
                    <optgroup label="🏠 Core Pages">
                      <option value="/">Home (index.html)</option>
                      <option value="/about">About Us (about.html)</option>
                      <option value="/products">Products Hub (products.html)</option>
                      <option value="/oem-odm">OEM / ODM Customization (oem-odm.html)</option>
                      <option value="/contact">Contact Us (contact.html)</option>
                    </optgroup>
                    <optgroup label="👟 Footwear Categories">
                      <option value="/sport-outdoor-shoes-wholesale">Sport &amp; Outdoor Shoes</option>
                      <option value="/casual-shoes-oem-manufacturer">Custom Casual Shoes</option>
                      <option value="/mens-sneakers-bulk-supplier">Men's Sneakers</option>
                      <option value="/womens-sneakers-oem-factory">Women's Trainers</option>
                      <option value="/slides-sandals-slippers-manufacturer">Slides &amp; Sandals</option>
                      <option value="/bags-sportswear-accessories-wholesale">Sport Bags &amp; Accessories</option>
                    </optgroup>
                    <optgroup label="🏭 Manufacturing &amp; Quality">
                      <option value="/production-capacity">Production Capacity (production-capacity.html)</option>
                      <option value="/quality-control">Quality Control Lab (quality-control.html)</option>
                      <option value="/certifications">Certifications &amp; Audits (certifications.html)</option>
                      <option value="/sustainability">Sustainability &amp; Eco (sustainability.html)</option>
                      <option value="/heritage-footwear-reproduction">1:1 Archival Re-engineering</option>
                    </optgroup>
                    <optgroup label="📚 Resources &amp; Brand VI">
                      <option value="/brand-identity">Brand Identity Guidelines (brand-identity.html)</option>
                      <option value="/case-studies">Brand Partnerships &amp; Cases (case-studies.html)</option>
                      <option value="/videos">Factory Video Showcase (videos.html)</option>
                      <option value="/news">News Center (news.html)</option>
                      <option value="/knowledge-base">Knowledge Base (knowledge-base.html)</option>
                      <option value="/whitepapers">Technical Whitepapers (whitepapers.html)</option>
                      <option value="/glossary">Footwear Glossary (glossary.html)</option>
                      <option value="/knowledge-graph">Knowledge Graph (knowledge-graph.html)</option>
                    </optgroup>
                  </select>

                  <div style="display: flex; gap: 4px; background: rgba(15, 23, 42, 0.6); padding: 3px; border-radius: 6px; border: 1px solid var(--border);">
                    <button id="btnVisualEditMode" type="button" class="btn btn-primary btn-sm" onclick="setVisualEditMode(true)" style="padding: 4px 10px; font-size: 0.78rem;">
                      <span>🖱️ Click-to-Edit: ON</span>
                    </button>
                    <button id="btnVisualBrowseMode" type="button" class="btn btn-secondary btn-sm" onclick="setVisualEditMode(false)" style="padding: 4px 10px; font-size: 0.78rem;">
                      <span>🌐 Browse Mode</span>
                    </button>
                  </div>
                </div>

                <div class="device-switcher">
                  <button class="device-btn active" onclick="setVisualDevice('100%', this)">🖥️ Desktop</button>
                  <button class="device-btn" onclick="setVisualDevice('1024px', this)">💻 Laptop</button>
                  <button class="device-btn" onclick="setVisualDevice('768px', this)">📱 Tablet</button>
                  <button class="device-btn" onclick="setVisualDevice('375px', this)">📱 Mobile</button>
                </div>

                <div style="display: flex; gap: 8px;">
                  <button class="btn btn-secondary btn-sm" onclick="reloadVisualIframe()" title="Reload preview">🔄 Refresh</button>
                  <button class="btn btn-secondary btn-sm" onclick="openLiveVisualPage()" title="Open live URL in new tab">🌐 Live View ↗</button>
                  <button class="btn btn-primary btn-sm" onclick="openRawHtmlEditorModal()" title="Edit raw HTML code for this page">📝 Edit Raw HTML</button>
                </div>
              </div>

              <!-- Visual Hint Notification Banner -->
              <div id="visualModeBanner" style="background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 6px; padding: 6px 12px; margin-bottom: 10px; font-size: 0.78rem; color: #93c5fd; display: flex; justify-content: space-between; align-items: center;">
                <div>
                  💡 <strong>Click-to-Edit Mode Active:</strong> Move your mouse over any text, heading, image, video, or button on the page below and click directly to edit, replace, or polish!
                </div>
                <div style="font-size: 0.75rem; color: #60a5fa;">
                  Live DOM &amp; File Sync
                </div>
              </div>

              <div class="iframe-wrapper">
                <iframe id="visualPreviewIframe" class="preview-iframe" src="/" onload="attachVisualInspector(this)"></iframe>
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 5: PRODUCTS MATRIX (115+ SKUs) -->
        <!-- =================================================================== -->
        <div id="tab_products_matrix" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>👟 Footwear Products Matrix (115+ SKUs)</h2>
                <div class="header-desc">Manage model codes, upper materials, outsoles, MOQs, and image galleries.</div>
              </div>
              <div style="display: flex; gap: 10px;">
                <input type="text" id="productSearchInput" class="input-field" style="width: 220px;" placeholder="Search by model or name..." onkeyup="filterProductsTable()">
                <select id="productCategoryFilter" class="input-field" style="width: 180px;" onchange="filterProductsTable()">
                  <option value="all">All Categories</option>
                  <option value="sport-outdoor-shoes">Sport &amp; Outdoor</option>
                  <option value="casual-shoes">Casual Shoes</option>
                  <option value="mens-sneakers">Men's Sneakers</option>
                  <option value="womens-sneakers">Women's Trainers</option>
                  <option value="slides-sandals">Slides &amp; Sandals</option>
                  <option value="bags-sportswear">Sport Bags</option>
                </select>
                <button class="btn btn-primary btn-sm" onclick="openAddProductModal()">
                  <span>➕ Add Product SKU</span>
                </button>
              </div>
            </div>

            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th style="width: 70px;">Image</th>
                    <th>Model Code</th>
                    <th>Name &amp; Category</th>
                    <th>Upper Material</th>
                    <th>Outsole</th>
                    <th>MOQ</th>
                    <th>Lead Time</th>
                    <th style="width: 130px; text-align: right;">Actions</th>
                  </tr>
                </thead>
                <tbody id="productsTableBody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 6: NEWSROOM & AI SCHEDULER -->
        <!-- =================================================================== -->
        <div id="tab_newsroom" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>📰 Newsroom &amp; 30-Day Auto-Scheduler</h2>
                <div class="header-desc">Publish industry updates, technical whitepapers, and automated scheduled articles.</div>
              </div>
              <div style="display: flex; gap: 10px;">
                <button class="btn btn-secondary btn-sm" onclick="openBatchScheduleModal()">
                  <span>⚡ 30-Day Batch Scheduler</span>
                </button>
                <button class="btn btn-primary btn-sm" onclick="openAddNewsModal()">
                  <span>➕ Write Article</span>
                </button>
              </div>
            </div>

            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th style="width: 60px;">Image</th>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Publish Date</th>
                    <th>Status</th>
                    <th style="width: 150px; text-align: right;">Actions</th>
                  </tr>
                </thead>
                <tbody id="newsTableBody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 7: MEDIA & VIDEO VAULT -->
        <!-- =================================================================== -->
        <div id="tab_media_vault" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>🖼️ Media &amp; 4K Video Asset Vault</h2>
                <div class="header-desc">Upload, preview, copy URLs, and directly replace images &amp; videos across the entire website in 1 click.</div>
              </div>
              <div style="display: flex; gap: 10px;">
                <input type="text" id="mediaSearchInput" class="input-field" style="width: 200px;" placeholder="Search media by name..." onkeyup="filterMediaGrid()">
                <select id="mediaTypeFilter" class="input-field" style="width: 140px;" onchange="filterMediaGrid()">
                  <option value="all">All Media</option>
                  <option value="images">Images Only</option>
                  <option value="videos">Videos Only</option>
                </select>
                <button class="btn btn-primary btn-sm" onclick="triggerFileInputClick()">
                  <span>📤 Upload File</span>
                </button>
                <input type="file" id="mediaVaultFileInput" style="display: none;" accept="image/*,video/*" multiple onchange="handleMediaVaultUpload(this)">
              </div>
            </div>

            <!-- Helpful Tip Banner -->
            <div style="background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.25); border-radius: var(--radius-md); padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
              <div style="font-size: 0.88rem; color: #93c5fd; line-height: 1.5;">
                <span style="font-size: 1.1rem; vertical-align: middle;">⚡️</span> <strong>就地直接更换图片功能：</strong> 点击任意图片下方的 <code>[ 🔄 更换图片 ]</code> 按钮，选择新图片即可原地覆盖原文件，全站所有页面立即自动更新，无需逐页修改代码！
              </div>
              <button class="btn btn-primary btn-sm" style="white-space: nowrap; font-size: 0.78rem;" onclick="triggerFileInputClick()">
                <span>＋ 上传新图片</span>
              </button>
            </div>

            <!-- Drag & Drop Zone -->
            <div class="drop-zone" id="mediaDropZone" onclick="triggerFileInputClick()">
              <div style="font-size: 2rem; margin-bottom: 8px;">📁</div>
              <div style="font-weight: 700; font-size: 1.05rem;">Drag &amp; drop images (JPG, PNG, WebP, SVG) or videos (MP4) here</div>
              <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">Or click anywhere in this zone to browse from your computer</div>
            </div>

            <!-- Media Grid -->
            <div class="media-grid" id="mediaVaultGrid">
              <!-- Rendered dynamically -->
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 8: INQUIRIES & RFQ LEADS CRM -->
        <!-- =================================================================== -->
        <div id="tab_inquiries_crm" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>📥 Inquiries &amp; Buyer RFQ Lead CRM</h2>
                <div class="header-desc">Every website inquiry is stored here permanently and routed to <strong>amy@widewaygroup.com</strong>.</div>
              </div>
              <div style="display: flex; gap: 10px;">
                <button class="btn btn-secondary btn-sm" onclick="exportInquiriesCsv()">
                  <span>📊 Export CSV</span>
                </button>
                <button class="btn btn-primary btn-sm" onclick="loadInquiriesList()">
                  <span>🔄 Refresh Inquiries</span>
                </button>
              </div>
            </div>

            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Inquiry ID / Date</th>
                    <th>Buyer &amp; Company</th>
                    <th>Contact Channels</th>
                    <th>Product &amp; Volume</th>
                    <th>Status</th>
                    <th style="width: 160px; text-align: right;">Quick Actions</th>
                  </tr>
                </thead>
                <tbody id="inquiriesTableBody">
                  <!-- Rendered dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 9: GLOBAL CONTACT & SALES DESK -->
        <!-- =================================================================== -->
        <div id="tab_contact_channels" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>📞 Global Contact Channels &amp; Sales Desk</h2>
                <div class="header-desc">Manage all public phone numbers, WhatsApp, WeChat, email dispatch routing, and factory addresses.</div>
              </div>
              <button class="btn btn-primary" onclick="saveContactChannels()">
                <span>💾 Save &amp; Recompile</span>
              </button>
            </div>

            <div class="grid-2">
              <div class="input-group">
                <label>Company Name (English)</label>
                <input type="text" id="cfgNameEn" class="input-field">
              </div>
              <div class="input-group">
                <label>Company Name (Chinese)</label>
                <input type="text" id="cfgNameZh" class="input-field">
              </div>
              <div class="input-group">
                <label>Unified Phone / WhatsApp / WeChat Number</label>
                <input type="text" id="cfgPhone" class="input-field" placeholder="+86 185 0595 9266">
              </div>
              <div class="input-group">
                <label>Inquiry Dispatch Target Email (Mandatory)</label>
                <input type="email" id="cfgEmail" class="input-field" placeholder="amy@widewaygroup.com">
              </div>
              <div class="input-group">
                <label>Secondary / Backup Email</label>
                <input type="email" id="cfgEmailSecondary" class="input-field" placeholder="kelly@widewaygroup.com">
              </div>
              <div class="input-group">
                <label>Export Sea Port</label>
                <input type="text" id="cfgPort" class="input-field" placeholder="Xiamen Port / Quanzhou Port">
              </div>
              <div class="input-group" style="grid-column: span 2;">
                <label>Chendai Manufacturing Plant Address</label>
                <input type="text" id="cfgAddress" class="input-field">
              </div>
              <div class="input-group" style="grid-column: span 2;">
                <label>Registered Export Office Address</label>
                <input type="text" id="cfgRegisteredAddress" class="input-field">
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 10: SEO & GEO AI COMMAND CENTER -->
        <!-- =================================================================== -->
        <div id="tab_seo_geo_command" class="tab-panel">
          <div class="card">
            <div class="card-header">
              <div>
                <h2>🌐 SEO &amp; GEO AI Search Command Center</h2>
                <div class="header-desc">Search engine metadata, AI crawler permissions, and machine-readable llms.txt knowledge graphs.</div>
              </div>
              <button class="btn btn-primary" onclick="saveSeoGeoSettings()">
                <span>💾 Save &amp; Sync Sitemaps</span>
              </button>
            </div>

            <div class="grid-2">
              <div class="input-group">
                <label>Primary Footwear SEO Keyword</label>
                <input type="text" id="cfgPrimaryKeyword" class="input-field">
              </div>
              <div class="input-group">
                <label>Brand Slogan (Hero Tagline)</label>
                <input type="text" id="cfgSlogan" class="input-field">
              </div>
              <div class="input-group" style="grid-column: span 2;">
                <label>Global Meta Description (For Google &amp; AI Search Indexing)</label>
                <textarea id="cfgMetaDescription" class="input-field"></textarea>
              </div>
              <div class="input-group" style="grid-column: span 2;">
                <label>Secondary Keywords (Comma-separated)</label>
                <input type="text" id="cfgSecondaryKeywords" class="input-field">
              </div>
            </div>

            <div style="background: rgba(0, 122, 255, 0.08); border: 1px solid rgba(0, 122, 255, 0.2); border-radius: var(--radius-md); padding: 18px; margin-top: 10px;">
              <h3 style="font-size: 0.95rem; font-weight: 700; color: #60a5fa; margin-bottom: 8px;">🤖 2026 AI Search Engine (GEO) Readiness Checklist</h3>
              <div style="display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.85rem;">
                <div>✅ <strong>GPTBot (OpenAI)</strong>: Permitted &amp; Indexed</div>
                <div>✅ <strong>PerplexityBot</strong>: Citation Ready</div>
                <div>✅ <strong>ClaudeBot (Anthropic)</strong>: Structure Verified</div>
                <div>✅ <strong>Google-Extended (Gemini)</strong>: Sitemaps Synced</div>
                <div>✅ <strong>llms.txt &amp; llms-full.txt</strong>: Active (296 Lines)</div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 11: AI COPYWRITING & MULTI-LANGUAGE STUDIO -->
        <!-- =================================================================== -->
        <div id="tab_ai_copywriting" class="tab-panel">
          <div class="grid-2">
            <div class="card">
              <div class="card-header">
                <div>
                  <h2>🪄 B2B Copywriting &amp; Polish Studio</h2>
                  <div class="header-desc">AI powered technical copywriting optimizer for footwear manufacturing.</div>
                </div>
              </div>
              <div class="input-group">
                <label>Input Text / Product Description</label>
                <textarea id="aiInputText" class="input-field" style="min-height: 120px;" placeholder="Paste text to polish or optimize..."></textarea>
              </div>
              <div class="input-group">
                <label>Optimization Goal</label>
                <select id="aiGoalSelect" class="input-field">
                  <option value="Make it technical, authoritative, and highlighting SATRA & ISO 9001 standards">🔬 Technical Manufacturing Authority</option>
                  <option value="High-converting B2B wholesale sales copy with Low MOQ call to action">💼 High-Converting Sourcing Pitch</option>
                  <option value="Concise product bullet points focusing on EVA rebound and flyknit breathability">👟 Sneaker Feature Highlights</option>
                  <option value="SEO optimized meta description with Jinjiang supply chain keywords">🌐 SEO Meta Description</option>
                </select>
              </div>
              <button class="btn btn-primary btn-block" onclick="runAiPolish()">
                <span>✨ Optimize with AI</span>
              </button>
              <div class="input-group" style="margin-top: 16px;">
                <label>AI Output</label>
                <textarea id="aiOutputText" class="input-field" style="min-height: 120px;" placeholder="AI optimized copy will appear here..."></textarea>
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <div>
                  <h2>🌐 8-Language Neural Translator</h2>
                  <div class="header-desc">Translate marketing copy to top export target languages.</div>
                </div>
              </div>
              <div class="input-group">
                <label>Source Copy (English)</label>
                <textarea id="translateInputText" class="input-field" style="min-height: 120px;" placeholder="Enter English text to translate..."></textarea>
              </div>
              <div class="input-group">
                <label>Target Language</label>
                <select id="translateLangSelect" class="input-field">
                  <option value="es">🇪🇸 Spanish (Español - Latin America / Spain)</option>
                  <option value="de">🇩🇪 German (Deutsch - Germany / Austria / Swiss)</option>
                  <option value="ar">🇸🇦 Arabic (العربية - Middle East / GCC)</option>
                  <option value="vi">🇻🇳 Vietnamese (Tiếng Việt)</option>
                  <option value="fr">🇫🇷 French (Français)</option>
                  <option value="ru">🇷🇺 Russian (Русский)</option>
                  <option value="pt">🇧🇷 Portuguese (Português)</option>
                  <option value="ja">🇯🇵 Japanese (日本語)</option>
                </select>
              </div>
              <button class="btn btn-primary btn-block" onclick="runAiTranslate()">
                <span>🌐 Neural Translate</span>
              </button>
              <div class="input-group" style="margin-top: 16px;">
                <label>Localized Output</label>
                <textarea id="translateOutputText" class="input-field" style="min-height: 120px;" placeholder="Translation result..."></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- =================================================================== -->
        <!-- TAB 12: PRODUCTION DEPLOYMENT & DEVOPS -->
        <!-- =================================================================== -->
        <div id="tab_system_devops" class="tab-panel">
          <div class="grid-2">
            <!-- Deploy Card -->
            <div class="card">
              <div class="card-header">
                <div>
                  <h2>☁️ Production Server Synchronizer</h2>
                  <div class="header-desc">Deploy updated web bundle to <strong>43.130.32.54:2222</strong> via secure SFTP.</div>
                </div>
              </div>
              <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px;">
                Clicking the button below will automatically package all HTML pages, CSS, JS, and media assets, upload them to the production server root (<code>/var/www/widewayfootwear.com</code>), apply file permissions, and reload Nginx.
              </p>
              <button class="btn btn-brand-red btn-block" style="padding: 14px;" onclick="triggerProductionDeploy()">
                <span>🚀 Deploy Live to 43.130.32.54</span>
              </button>
            </div>

            <!-- Password Change Card -->
            <div class="card">
              <div class="card-header">
                <div>
                  <h2>🔒 Change Master Admin Password</h2>
                  <div class="header-desc">Update the authorization key for this admin console.</div>
                </div>
              </div>
              <form onsubmit="handleChangePasswordSubmit(event)">
                <div class="input-group">
                  <label>Current Master Password</label>
                  <input type="password" id="pwCurrent" class="input-field" required>
                </div>
                <div class="input-group">
                  <label>New Master Password</label>
                  <input type="password" id="pwNew" class="input-field" required minlength="8">
                </div>
                <button type="submit" class="btn btn-secondary btn-block">
                  <span>Update Password</span>
                </button>
              </form>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- MODALS -->
  <!-- ===================================================================== -->

  <!-- 0. Replace Media Asset Modal (Direct In-Place Replacement) -->
  <div id="replaceMediaModal" class="modal-overlay modal-overlay-picker" style="z-index: 20000;">
    <div class="modal-dialog modal-lg" style="width: 950px; max-width: 95%;">
      <div class="modal-header">
        <h3>🔄 直接更换媒体文件 / In-Place Media Replacement</h3>
        <button class="modal-close-btn" onclick="closeReplaceMediaModal()">✕</button>
      </div>
      
      <!-- Replacement Specifications & Best Practice Card -->
      <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px 18px; margin-bottom: 16px;">
        <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 8px; color: #60a5fa; display: flex; align-items: center; gap: 6px;">
          <span>📋 替换图片/视频具体要求与建议规范</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.8rem; color: #cbd5e1; line-height: 1.5;">
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #3b82f6;">
            <strong>📁 支持格式：</strong><br>JPG / PNG / WebP / SVG / GIF (图片)；MP4 / WebM (视频)
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #10b981;">
            <strong>📏 尺寸与比例：</strong><br>强烈建议使用与原图<strong>相同长宽比</strong>（请参考下方原图尺寸），防止网页拉伸变形
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #f59e0b;">
            <strong>⚖️ 文件大小建议：</strong><br>网页图片建议 <strong>300KB ~ 3MB</strong>（服务器已支持最大 100MB），以确保海外秒开
          </div>
          <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #8b5cf6;">
            <strong>⚡️ 全站即时生效：</strong><br>直接覆盖原文件，全站所有引用页面<strong>自动重新编译并更新</strong>
          </div>
        </div>
      </div>

      <!-- Dynamic Error / Warning Box -->
      <div id="replaceModalErrorAlert" style="display: none; background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: var(--radius-md); padding: 14px 16px; margin-bottom: 16px; color: #fca5a5; font-size: 0.88rem; line-height: 1.6;">
        <div style="font-weight: 700; color: #f87171; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
          <span>❌ 替换操作遇到错误</span>
        </div>
        <div id="replaceModalErrorDetail">错误详情将在此显示</div>
        <div id="replaceModalErrorSuggestion" style="margin-top: 6px; color: #fed7aa; font-size: 0.82rem;"></div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
        <!-- Left Column: Current Asset -->
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px; display: flex; flex-direction: column;">
          <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-main); display: flex; align-items: center; justify-content: space-between;">
            <span>📸 当前线上原图</span>
            <span class="badge" style="background: rgba(148, 163, 184, 0.2); color: #cbd5e1;">当前在用</span>
          </div>
          <div style="width: 100%; height: 210px; background: #000; border-radius: var(--radius-sm); overflow: hidden; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; border: 1px solid var(--border); position: relative;">
            <img id="replaceCurrentPreviewImg" src="" style="max-width: 100%; max-height: 100%; object-fit: contain; display: block;" onload="handleOriginalImageLoaded(this)">
            <video id="replaceCurrentPreviewVideo" src="" controls style="max-width: 100%; max-height: 100%; display: none;" onloadedmetadata="handleOriginalVideoLoaded(this)"></video>
            <div id="replaceCurrentDimBadge" style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.75); color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-family: monospace;">测量中...</div>
          </div>
          <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.7; background: rgba(15, 23, 42, 0.4); padding: 10px; border-radius: 6px;">
            <div><strong>文件名称:</strong> <span id="replaceCurrentNameText" style="color: #60a5fa; word-break: break-all;">-</span></div>
            <div><strong>原图尺寸 (长宽):</strong> <span id="replaceCurrentDimText" style="color: #34d399; font-weight: 700;">测量中...</span></div>
            <div><strong>原图比例 (Ratio):</strong> <span id="replaceCurrentRatioText" style="color: #fde047;">-</span></div>
            <div><strong>文件大小:</strong> <span id="replaceCurrentSizeText" style="color: #cbd5e1;">-</span></div>
            <div><strong>相对路径:</strong> <span id="replaceCurrentPathText" style="color: #94a3b8; word-break: break-all;">-</span></div>
          </div>
        </div>

        <!-- Right Column: New Replacement Asset -->
        <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px; display: flex; flex-direction: column;">
          <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-main); display: flex; align-items: center; justify-content: space-between;">
            <span>✨ 待替换的新图/视频</span>
            <span id="replaceNewStatusBadge" class="badge" style="background: rgba(234, 179, 8, 0.2); color: #fde047;">等待选择文件</span>
          </div>
          
          <div id="replaceDropZone" class="drop-zone" style="min-height: 210px; padding: 15px; margin-bottom: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; position: relative;" onclick="triggerReplaceModalFileSelect()">
            <div id="replaceUploadPrompt">
              <div style="font-size: 2.2rem; margin-bottom: 6px;">📥</div>
              <div style="font-weight: 600; font-size: 0.92rem;">点击选择或拖放新图片到此处</div>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">支持 JPG, PNG, WebP, SVG, MP4 (最大 100MB)</div>
            </div>
            <div id="replaceNewPreviewContainer" style="display: none; width: 100%; height: 190px; align-items: center; justify-content: center;">
              <img id="replaceNewPreviewImg" src="" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 4px;" onload="handleNewImageLoaded(this)">
              <video id="replaceNewPreviewVideo" src="" controls style="max-width: 100%; max-height: 100%; display: none; border-radius: 4px;" onloadedmetadata="handleNewVideoLoaded(this)"></video>
              <div id="replaceNewDimBadge" style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.75); color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-family: monospace;">-</div>
            </div>
          </div>
          <input type="file" id="replaceModalFileInput" style="display: none;" accept="image/*,video/*" onchange="handleReplaceModalFileChange(this)">

          <div id="replaceNewMetaInfo" style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.7; background: rgba(15, 23, 42, 0.4); padding: 10px; border-radius: 6px; display: none;">
            <div><strong>所选新文件:</strong> <span id="replaceNewNameText" style="color: #60a5fa; word-break: break-all;">-</span></div>
            <div><strong>新图尺寸 (长宽):</strong> <span id="replaceNewDimText" style="color: #34d399; font-weight: 700;">-</span></div>
            <div><strong>新图比例 (Ratio):</strong> <span id="replaceNewRatioText" style="color: #fde047;">-</span></div>
            <div><strong>新文件大小:</strong> <span id="replaceNewSizeText" style="color: #cbd5e1;">-</span></div>
            <!-- Match Comparison Badge -->
            <div id="replaceMatchEvalBox" style="margin-top: 6px; padding: 6px 10px; border-radius: 4px; font-size: 0.78rem; line-height: 1.4;"></div>
          </div>
          <div id="replaceNoFileHint" style="font-size: 0.82rem; color: var(--text-muted); text-align: center; margin-top: auto;">
            请点击上方区域选择要替换的新图片
          </div>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 16px;">
        <button class="btn btn-secondary" onclick="closeReplaceMediaModal()">取消 (Cancel)</button>
        <div style="display: flex; gap: 10px;">
          <button class="btn btn-secondary btn-sm" onclick="triggerReplaceModalFileSelect()">
            <span>📂 重新选择文件</span>
          </button>
          <button id="btnConfirmReplaceMedia" class="btn btn-primary" disabled onclick="executeMediaReplacement()">
            <span>⚡️ 确认立即替换并全站发布</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 1. Media Asset Selector Modal -->
  <div id="mediaPickerModal" class="modal-overlay modal-overlay-picker" style="z-index: 20000;">
    <div class="modal-dialog modal-lg">
      <div class="modal-header">
        <h3>🖼️ Select Asset from Media Vault</h3>
        <button class="modal-close-btn" onclick="closeMediaPickerModal()">✕</button>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <input type="text" id="mediaPickerSearch" class="input-field" style="width: 260px;" placeholder="Search asset name..." onkeyup="filterMediaPickerGrid()">
        <button class="btn btn-primary btn-sm" onclick="triggerPickerFileInput()">
          <span>📤 Upload New Asset</span>
        </button>
        <input type="file" id="mediaPickerFileInput" style="display: none;" accept="image/*,video/*" onchange="handlePickerFileUpload(this)">
      </div>
      <div class="media-grid" id="mediaPickerGrid" style="max-height: 480px; overflow-y: auto;">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>

  <!-- 2. Product Edit / Add Modal (Shopify-Style Dual Column Master Editor) -->
  <div id="productEditModal" class="modal-overlay">
    <div class="modal-dialog modal-xl" style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:24px 28px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.85);">
      <div class="modal-header" style="border-bottom:1px solid #1e293b; padding-bottom:16px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:12px;">
          <span style="font-size:1.5rem;">👟</span>
          <div>
            <h3 id="productModalTitle" style="font-size:1.25rem; font-weight:700; color:#f8fafc; margin:0;">Edit Footwear SKU</h3>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">Shopify-Style Master Product Editor with Full Attribute Control &amp; SEO/GEO Engine</div>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <a id="btnLivePreviewSku" href="#" target="_blank" class="btn btn-secondary btn-sm" style="background:rgba(255,255,255,0.05); color:#93c5fd; border:1px solid #3b82f6; text-decoration:none; font-size:0.78rem; display:inline-flex; align-items:center; gap:6px;">
            <span>🌐 Live Product View</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </a>
          <button type="button" class="modal-close-btn" onclick="closeProductEditModal()" style="font-size:1.3rem; color:#94a3b8;">✕</button>
        </div>
      </div>

      <form id="productEditForm" onsubmit="handleSaveProductSubmit(event)">
        <input type="hidden" id="pEditIndex">

        <!-- Shopify 2-Column Responsive Layout -->
        <div style="display:grid; grid-template-columns: 1.8fr 1.2fr; gap:24px; align-items:start;">
          
          <!-- LEFT MAIN COLUMN -->
          <div style="display:flex; flex-direction:column; gap:20px;">
            
            <!-- Card 1: Title, Code & Full Description -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>📝</span> Product Title &amp; Laboratory Description
              </div>
              <div style="display:grid; grid-template-columns: 1.2fr 1fr; gap:12px; margin-bottom:14px;">
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Product Display Name *</label>
                  <input type="text" id="pEditName" class="input-field" required placeholder="e.g. WOMEN'S WD2500222" oninput="handleProductNameChange(this.value)">
                </div>
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Model Code / SKU *</label>
                  <input type="text" id="pEditCode" class="input-field" required placeholder="e.g. WD2500222">
                </div>
              </div>
              <div class="input-group" style="margin-bottom:4px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Product Description &amp; Lab Engineering Overview *</label>
                  <span id="pEditDescCount" style="font-size:0.7rem; color:#94a3b8;">0 chars</span>
                </div>
                <textarea id="pEditDescription" class="input-field" rows="4" required style="font-size:0.85rem; line-height:1.5; resize:vertical;" placeholder="Engineered by WIDEWAY footwear lab, the WOMEN'S WD2500222 combines ergonomic arch support, high-elastic cushioning outsoles, and durable wear-resistant materials..." oninput="updateDescCharCount(this.value)"></textarea>
                <div style="font-size:0.72rem; color:#94a3b8; margin-top:4px;">
                  💡 <strong>前台展示位置：</strong>此段落将完整呈现在产品详情页的主标题下方，并作为 Google / 必应等搜索引擎的默认摘要介绍。
                </div>
              </div>
            </div>

            <!-- Card 2: Visual Media & Gallery Assets -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>📸</span> Media &amp; Visual Assets (Shopify-Style Gallery)
              </div>
              
              <!-- Main Image -->
              <div class="input-group" style="margin-bottom:16px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Main Cover Thumbnail Image *</label>
                <div style="display:flex; gap:8px; align-items:center;">
                  <input type="text" id="pEditImage" class="input-field" required placeholder="images/products/women-s-wd2500222_1.jpg" style="font-family:var(--font-mono); font-size:0.82rem;" oninput="updateMainImagePreview(this.value)">
                  <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('pEditImage')" style="white-space:nowrap;">Choose Vault</button>
                </div>
                <div id="pEditMainImagePreviewBox" style="margin-top:8px; display:flex; align-items:center; gap:10px; padding:8px; background:rgba(0,0,0,0.25); border-radius:6px; border:1px solid #334155;">
                  <img id="pEditMainImagePreview" src="" alt="Main Preview" style="width:60px; height:50px; object-fit:cover; border-radius:4px; background:#0f172a;" onerror="this.src='images/sneakers_running.jpg'">
                  <span style="font-size:0.75rem; color:#94a3b8;">Primary cover image displayed across catalog and product cards.</span>
                </div>
              </div>

              <!-- Gallery Multi-Angles -->
              <div class="input-group" style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Additional Gallery Angles &amp; Colorways (1 URL per line)</label>
                  <button type="button" class="btn btn-secondary btn-sm" onclick="appendGalleryAngleFromVault()" style="font-size:0.7rem; padding:2px 8px;">+ Pick Angle</button>
                </div>
                <textarea id="pEditGallery" class="input-field" rows="3" placeholder="images/products/women-s-wd2500222_1.jpg&#10;images/products/women-s-wd2500222_2.jpg" style="font-family:var(--font-mono); font-size:0.8rem; line-height:1.4;" oninput="renderGalleryThumbnails(this.value)"></textarea>
                <div id="pEditGalleryThumbsContainer" style="display:flex; gap:8px; margin-top:8px; overflow-x:auto; padding-bottom:4px;"></div>
              </div>

              <!-- 4K Video Section -->
              <div style="background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.25); border-radius:8px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                  <label style="font-weight:600; color:#fff; margin-bottom:0; font-size:0.82rem;">🎬 4K / 1080P Product Showcase Video</label>
                  <span style="font-size:0.7rem; color:#60a5fa; background:rgba(59,130,246,0.15); padding:2px 8px; border-radius:10px; font-weight:600;">Max: 50MB</span>
                </div>
                
                <div style="font-size:0.75rem; color:#94a3b8; line-height:1.4; margin-bottom:8px;">
                  限制 <strong>50MB</strong> 以内，推荐 MP4/WebM/MOV。配置后前台详情页自动启用高清视频播放器与 360° 实测展厅。
                </div>

                <div style="display:flex; gap:8px; align-items:center;">
                  <input type="text" id="pEditVideo" class="input-field" placeholder="images/products/video.mp4 or URL" style="font-family:var(--font-mono); font-size:0.82rem;">
                  <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('pEditVideo')" style="white-space:nowrap; font-size:0.78rem;">Vault</button>
                  <button type="button" class="btn btn-primary" onclick="document.getElementById('productVideoFileInput').click()" style="background:#2563eb; white-space:nowrap; font-size:0.78rem;">🎥 Upload (&le;50MB)</button>
                  <button type="button" class="btn btn-danger" onclick="removeProductVideo()" title="Clear Video" style="white-space:nowrap; font-size:0.78rem;">✕</button>
                  <input type="file" id="productVideoFileInput" accept="video/mp4,video/webm,video/quicktime" style="display:none;" onchange="handleProductVideoFileSelect(this)">
                </div>

                <div id="pEditVideoUploadProgress" style="display:none; margin-top:8px; padding:6px 10px; background:rgba(37,99,235,0.15); border:1px dashed #3b82f6; border-radius:4px; font-size:0.75rem; color:#93c5fd;">
                  ⏳ Uploading product video... please wait.
                </div>

                <div id="pEditVideoPreviewContainer" style="display:none; margin-top:8px; padding:8px; background:rgba(0,0,0,0.3); border:1px solid #334155; border-radius:6px;">
                  <div style="font-size:0.72rem; color:#94a3b8; margin-bottom:4px; display:flex; justify-content:space-between;">
                    <span>Live Video Preview:</span>
                    <span id="pEditVideoStatus" style="color:#34d399;">✓ Video Attached</span>
                  </div>
                  <video id="pEditVideoPreview" controls style="width:100%; max-height:180px; border-radius:4px; background:#000;"></video>
                </div>
              </div>
            </div>

            <!-- Card 3: Footwear Specs -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>⚙️</span> Footwear Technical Specifications &amp; Materials
              </div>
              <div class="grid-2" style="gap:12px;">
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Upper Material</label>
                  <input type="text" id="pEditUpper" class="input-field" placeholder="Lightweight Breathable Flyknit Upper">
                </div>
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Outsole / Midsole</label>
                  <input type="text" id="pEditOutsole" class="input-field" placeholder="MD Midsole + High-Traction Rubber Outsole">
                </div>
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Lining / Insole</label>
                  <input type="text" id="pEditLining" class="input-field" placeholder="Breathable Mesh + Cushioned OrthoLite Insole">
                </div>
                <div class="input-group" style="margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Size Range</label>
                  <input type="text" id="pEditSizes" class="input-field" placeholder="EU 36-45 / US 5-11">
                </div>
                <div class="input-group" style="grid-column: span 2; margin-bottom:0;">
                  <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Customization / OEM Capabilities</label>
                  <input type="text" id="pEditCustomization" class="input-field" placeholder="Custom Logo, Colors, Upper Materials &amp; Packaging">
                </div>
              </div>
            </div>

          </div>

          <!-- RIGHT SIDEBAR COLUMN -->
          <div style="display:flex; flex-direction:column; gap:20px;">
            
            <!-- Card 4: Categorization & Tags -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>🏷️</span> Categorization &amp; Badges
              </div>
              <div class="input-group" style="margin-bottom:12px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Category *</label>
                <select id="pEditCat" class="input-field" required>
                  <option value="sport-outdoor-shoes">Sport &amp; Outdoor Shoes</option>
                  <option value="casual-shoes">Custom Casual Shoes</option>
                  <option value="mens-shoes">Men's Sneakers</option>
                  <option value="womens-shoes">Women's Trainers</option>
                  <option value="slides-sandals">Slides, Sandals &amp; Slippers</option>
                  <option value="bags-sportswear">Sport Bags &amp; Accessories</option>
                </select>
              </div>
              <div class="input-group" style="margin-bottom:12px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Feature Tag / Badge</label>
                <input type="text" id="pEditTag" class="input-field" placeholder="e.g. Wideway Sports Shoes, Anti-slip, OEM/ODM">
              </div>
              <div class="input-group" style="margin-bottom:0;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Search Keywords (Comma-separated)</label>
                <input type="text" id="pEditKeywords" class="input-field" placeholder="Wideway Sports Shoes, Breathable, Anti-slip">
              </div>
            </div>

            <!-- Card 5: B2B Sourcing Terms -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
                <span>📦</span> B2B Sourcing Terms
              </div>
              <div class="input-group" style="margin-bottom:12px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">MOQ (Minimum Order Quantity)</label>
                <input type="text" id="pEditMoq" class="input-field" placeholder="500 Pairs / Color">
              </div>
              <div class="input-group" style="margin-bottom:0;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Production Lead Time</label>
                <input type="text" id="pEditLeadTime" class="input-field" placeholder="30-45 Days (Samples 7-10 Days)">
              </div>
            </div>

            <!-- Card 6: Search Engine Listing & GEO Engine (Shopify-Style SERP Card) -->
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px;">
              <div style="font-weight:700; color:#f8fafc; font-size:0.95rem; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                <span>🌍</span> Search Engine Listing (SEO &amp; GEO)
              </div>
              <div style="font-size:0.72rem; color:#94a3b8; margin-bottom:12px;">
                Customize Google/Baidu ranking snippet and international GEO export trade tags.
              </div>

              <div class="input-group" style="margin-bottom:10px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">URL Slug / Handle *</label>
                <input type="text" id="pEditSlug" class="input-field" required placeholder="women-s-wd2500222" style="font-family:var(--font-mono); font-size:0.8rem;" oninput="updateSerpPreview()">
              </div>

              <div class="input-group" style="margin-bottom:10px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Page SEO Title</label>
                <input type="text" id="pEditSeoTitle" class="input-field" placeholder="WOMEN'S WD2500222 | WIDEWAY GROUP Footwear" oninput="updateSerpPreview()">
              </div>

              <div class="input-group" style="margin-bottom:10px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">Page Meta Description</label>
                <textarea id="pEditSeoDesc" class="input-field" rows="2" placeholder="Wholesale &amp; OEM/ODM manufacturing for WOMEN'S WD2500222. Breathable flyknit upper..." style="font-size:0.8rem;" oninput="updateSerpPreview()"></textarea>
              </div>

              <div class="input-group" style="margin-bottom:10px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">GEO Target Export Markets</label>
                <input type="text" id="pEditGeoMarkets" class="input-field" placeholder="North America, Europe, Middle East, Southeast Asia" oninput="updateSerpPreview()">
              </div>

              <div class="input-group" style="margin-bottom:12px;">
                <label style="font-size:0.78rem; font-weight:600; color:#cbd5e1;">GEO Manufacturing Cluster Origin</label>
                <input type="text" id="pEditGeoOrigin" class="input-field" placeholder="Jinjiang Footwear Industrial Cluster, Fujian, China" oninput="updateSerpPreview()">
              </div>

              <!-- Live SERP Preview Box -->
              <div style="background:#ffffff; color:#202124; padding:12px 14px; border-radius:6px; border:1px solid #dadce0; font-family:arial,sans-serif;">
                <div style="font-size:0.72rem; color:#202124; display:flex; align-items:center; gap:6px; margin-bottom:3px;">
                  <span style="background:#e8f0fe; color:#1a73e8; padding:1px 4px; border-radius:3px; font-weight:700; font-size:0.65rem;">GEO</span>
                  <span id="serpPreviewUrl" style="color:#202124; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:0.72rem;">https://www.widewayfootwear.com/product-detail?id=women-s-wd2500222</span>
                </div>
                <div id="serpPreviewTitle" style="color:#1a0dab; font-size:0.98rem; font-weight:500; line-height:1.25; margin-bottom:3px; cursor:pointer;">WOMEN'S WD2500222 | WIDEWAY GROUP Footwear</div>
                <div id="serpPreviewDesc" style="color:#4d5156; font-size:0.76rem; line-height:1.35; max-height:48px; overflow:hidden;">Engineered by WIDEWAY footwear lab...</div>
                <div style="margin-top:6px; font-size:0.68rem; color:#70757a; border-top:1px dashed #e8eaed; padding-top:4px;">
                  📍 Origin: <span id="serpPreviewOrigin">Jinjiang, Fujian, China</span> | 🌐 Target: <span id="serpPreviewMarkets">North America, Europe</span>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- Bottom Action Bar -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:24px; padding-top:18px; border-top:1px solid #1e293b;">
          <div style="font-size:0.78rem; color:#94a3b8;">
            💾 Changes will automatically compile static pages and update live B2B catalog instantly.
          </div>
          <div style="display:flex; gap:10px;">
            <button type="button" class="btn btn-secondary" onclick="closeProductEditModal()">Cancel</button>
            <button type="submit" class="btn btn-primary" style="background:#2563eb; padding:10px 24px; font-weight:700;">⚡️ Save Product &amp; Sync Across Site</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <!-- 3. News Article Edit / Add Modal -->
  <div id="newsEditModal" class="modal-overlay">
    <div class="modal-dialog modal-lg">
      <div class="modal-header">
        <h3 id="newsModalTitle">📰 Write / Edit News Article</h3>
        <button class="modal-close-btn" onclick="closeNewsEditModal()">✕</button>
      </div>
      <form id="newsEditForm" onsubmit="handleSaveNewsSubmit(event)">
        <input type="hidden" id="nEditIndex">
        <input type="hidden" id="nEditFilename">
        <div class="grid-2">
          <div class="input-group" style="grid-column: span 2;">
            <label>Article Title</label>
            <input type="text" id="nEditTitle" class="input-field" required>
          </div>
          <div class="input-group">
            <label>Category</label>
            <select id="nEditCat" class="input-field" required>
              <option value="⚙️ Product News">⚙️ Product News</option>
              <option value="🌿 Industry News">🌿 Industry News</option>
              <option value="🏭 Factory Updates">🏭 Factory Updates</option>
              <option value="🌿 ESG &amp; Sustainability">🌿 ESG &amp; Sustainability</option>
              <option value="🤝 Brand Partnerships">🤝 Brand Partnerships</option>
            </select>
          </div>
          <div class="input-group">
            <label>Publish Date (YYYY-MM-DD)</label>
            <input type="date" id="nEditDate" class="input-field" required>
          </div>
          <div class="input-group" style="grid-column: span 2;">
            <label>Cover Image URL</label>
            <div style="display: flex; gap: 8px;">
              <input type="text" id="nEditImage" class="input-field" required>
              <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('nEditImage')">Choose</button>
            </div>
          </div>
          <div class="input-group" style="grid-column: span 2;">
            <label>Executive Summary (For List &amp; Meta Description)</label>
            <textarea id="nEditSummary" class="input-field" style="min-height: 80px;" required></textarea>
          </div>
          <div class="input-group" style="grid-column: span 2;">
            <label>Full HTML Body</label>
            <textarea id="nEditBody" class="input-field" style="min-height: 200px; font-family: var(--font-mono); font-size: 0.85rem;" required></textarea>
          </div>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
          <button type="button" class="btn btn-secondary" onclick="closeNewsEditModal()">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Article</button>
        </div>
      </form>
    </div>
  </div>

  <!-- 4. Production Deployment Terminal Output Modal -->
  <div id="deployConsoleModal" class="modal-overlay">
    <div class="modal-dialog modal-lg">
      <div class="modal-header">
        <h3>🚀 Production Deployment Console</h3>
        <button class="modal-close-btn" onclick="closeDeployConsoleModal()">✕</button>
      </div>
      <div style="margin-bottom: 14px; font-size: 0.9rem; color: var(--text-muted);">
        Destination: <strong>43.130.32.54:2222</strong> | Target: <code>/var/www/widewayfootwear.com</code>
      </div>
      <div class="terminal-console" id="deployConsoleOutput">Connecting to server and deploying assets...</div>
      <div style="display: flex; justify-content: flex-end; margin-top: 18px;">
        <button class="btn btn-secondary" onclick="closeDeployConsoleModal()">Close Console</button>
      </div>
    </div>
  </div>

  <!-- 5. Visual Live Studio: Element Click-to-Edit Modal / Drawer -->
  <div id="visualElementEditorModal" class="modal-overlay">
    <div class="modal-dialog" style="width: 780px; max-width: 95%; background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.85);">
      <div class="modal-header" style="border-bottom: 1px solid #1e293b; padding-bottom: 14px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <h3 style="margin: 0; font-size: 1.15rem; color: #f8fafc;">✏️ Visual Element Editor</h3>
          <span id="vEditTypeBadge" style="background: #2563eb; color: #ffffff; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">TEXT</span>
        </div>
        <button type="button" class="modal-close-btn" onclick="closeVisualElementEditor()" style="font-size: 1.3rem; color: #94a3b8;">✕</button>
      </div>

      <form id="visualElementEditForm" onsubmit="event.preventDefault(); saveVisualElementEdit();">
        <input type="hidden" id="vEditPage">
        <input type="hidden" id="vEditType">
        <input type="hidden" id="vEditSelector">
        <input type="hidden" id="vEditOldVal">
        <input type="hidden" id="vEditAttr">

        <div style="background: rgba(30, 41, 59, 0.5); padding: 10px 14px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 16px; font-size: 0.8rem; color: #94a3b8; display: flex; justify-content: space-between;">
          <div>Target Page: <strong id="vEditPageLabel" style="color: #60a5fa; font-family: var(--font-mono);">index.html</strong></div>
          <div>Target Node: <code id="vEditSelectorLabel" style="color: #cbd5e1;">H2</code></div>
        </div>

        <!-- 1. Text / Content Editor Section -->
        <div id="vEditTextSection" style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <label style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin: 0;">Text / HTML Content</label>
            <div style="display: flex; gap: 6px;">
              <button type="button" class="btn btn-secondary btn-sm" onclick="polishVisualTextWithAi()" style="padding: 2px 8px; font-size: 0.75rem;">✨ AI Polish</button>
              <button type="button" class="btn btn-secondary btn-sm" onclick="translateVisualTextWithAi()" style="padding: 2px 8px; font-size: 0.75rem;">🌐 Translate</button>
            </div>
          </div>
          <textarea id="vEditTextContent" class="input-field" rows="4" style="font-size: 0.9rem; line-height: 1.5; font-family: var(--font-sans);" oninput="updateVisualCharCount()"></textarea>
          <div style="font-size: 0.72rem; color: #64748b; text-align: right; margin-top: 3px;">
            <span id="vEditCharCount">0</span> characters
          </div>
        </div>

        <!-- 2. Image Media Section (Shown if element is IMG or background) -->
        <div id="vEditImageSection" style="display: none; margin-bottom: 16px; background: #1e293b; padding: 14px; border-radius: 8px; border: 1px solid #334155;">
          <label style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; display: block; margin-bottom: 8px;">Image Asset &amp; Media Vault</label>
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 90px; height: 90px; border-radius: 6px; overflow: hidden; background: #0b1120; border: 1px solid #475569; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              <img id="vEditImagePreview" src="" alt="Preview" style="max-width: 100%; max-height: 100%; object-fit: cover;" onerror="this.src='https://via.placeholder.com/90x90?text=No+Img'">
            </div>
            <div style="flex: 1;">
              <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <input type="text" id="vEditImageSrc" class="input-field" placeholder="images/banner_factory.jpg" oninput="document.getElementById('vEditImagePreview').src = this.value">
                <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('vEditImageSrc')" style="white-space: nowrap;">🖼️ Choose Vault</button>
              </div>
              <div style="display: flex; gap: 8px; align-items: center;">
                <button type="button" class="btn btn-secondary btn-sm" onclick="triggerVisualImageUpload()" style="font-size: 0.8rem;">📤 Upload New Image</button>
                <input type="file" id="visualImageFileInput" accept="image/*" style="display: none;" onchange="handleVisualImageUpload(this)">
                <span id="vEditImageInfo" style="font-size: 0.72rem; color: #94a3b8;">PNG, JPG, WebP, SVG</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Video Media Section (Shown if element is VIDEO) -->
        <div id="vEditVideoSection" style="display: none; margin-bottom: 16px; background: #1e293b; padding: 14px; border-radius: 8px; border: 1px solid #334155;">
          <label style="font-size: 0.85rem; font-weight: 600; color: #cbd5e1; display: block; margin-bottom: 8px;">4K HD Video Asset (Limit: 50MB)</label>
          <div style="margin-bottom: 10px;">
            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
              <input type="text" id="vEditVideoSrc" class="input-field" placeholder="images/video_sole_cementing.mp4" oninput="updateVisualVideoPreview(this.value)">
              <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('vEditVideoSrc')" style="white-space: nowrap;">🎬 Choose Vault</button>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <button type="button" class="btn btn-secondary btn-sm" onclick="triggerVisualVideoUpload()" style="font-size: 0.8rem;">🎥 Upload Video (&le;50MB)</button>
              <input type="file" id="visualVideoFileInput" accept="video/mp4,video/webm,video/quicktime" style="display: none;" onchange="handleVisualVideoUpload(this)">
              <span style="font-size: 0.72rem; color: #38bdf8;">Max 50MB, MP4/WebM</span>
            </div>
          </div>
          <div id="vEditVideoPreviewContainer" style="display: none; background: #000; border-radius: 6px; overflow: hidden; max-height: 160px; border: 1px solid #475569;">
            <video id="vEditVideoPreview" controls style="width: 100%; max-height: 160px;"></video>
          </div>
        </div>

        <!-- 4. Link / Button Target Section (Shown if element is A or Button) -->
        <div id="vEditLinkSection" style="display: none; margin-bottom: 16px;">
          <div class="grid-2">
            <div class="input-group">
              <label style="font-size: 0.82rem; font-weight: 600; color: #cbd5e1;">Button / Link Text</label>
              <input type="text" id="vEditLinkText" class="input-field" placeholder="Request Factory Quote">
            </div>
            <div class="input-group">
              <label style="font-size: 0.82rem; font-weight: 600; color: #cbd5e1;">Target URL / Page</label>
              <input type="text" id="vEditLinkHref" class="input-field" placeholder="/contact">
            </div>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1e293b; padding-top: 16px; margin-top: 20px;">
          <button type="button" class="btn btn-secondary" onclick="closeVisualElementEditor()">Cancel</button>
          <div style="display: flex; gap: 10px;">
            <button type="button" class="btn btn-secondary" onclick="openRawHtmlEditorModal(document.getElementById('vEditPage').value)">📝 Edit Page Raw HTML</button>
            <button type="submit" class="btn btn-primary" style="background: #2563eb; font-weight: 700;">💾 Apply &amp; Save Live</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <!-- 6. Raw HTML & Code Editor Modal -->
  <div id="rawHtmlEditorModal" class="modal-overlay">
    <div class="modal-dialog modal-xl" style="width: 1200px; max-width: 96%; height: 90vh; display: flex; flex-direction: column; background: #0b1120; border: 1px solid #334155; border-radius: 12px; padding: 20px 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.95);">
      <div class="modal-header" style="border-bottom: 1px solid #1e293b; padding-bottom: 12px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <h3 style="margin: 0; font-size: 1.15rem; color: #f8fafc;">📝 Page Raw HTML &amp; Code Editor</h3>
          <select id="rawHtmlPageSelector" class="input-field" style="padding: 4px 10px; width: 280px; font-size: 0.82rem;" onchange="loadRawHtmlPage(this.value)">
            <!-- Populated dynamically -->
          </select>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <button type="button" class="btn btn-secondary btn-sm" onclick="toggleRawCodeWrap()" id="btnCodeWrap">Wrap: ON</button>
          <button type="button" class="modal-close-btn" onclick="closeRawHtmlEditorModal()" style="font-size: 1.3rem; color: #94a3b8;">✕</button>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.78rem; color: #94a3b8;">
        <div>Editing: <strong id="rawHtmlFilenameLabel" style="color: #38bdf8; font-family: var(--font-mono);">index.html</strong> | <span id="rawHtmlFileSize">0 KB</span></div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <input type="text" id="rawHtmlSearchInput" class="input-field" placeholder="Search in code (Ctrl+F)..." style="padding: 2px 8px; font-size: 0.75rem; width: 180px;" onkeyup="searchInRawHtml(this.value)">
          <span id="rawHtmlLineCount">0 lines</span>
        </div>
      </div>

      <div style="flex: 1; position: relative; min-height: 0; margin-bottom: 14px;">
        <textarea id="rawHtmlCodeTextarea" spellcheck="false" style="width: 100%; height: 100%; background: #030712; color: #e2e8f0; font-family: 'JetBrains Mono', Consolas, Monaco, monospace; font-size: 0.85rem; line-height: 1.5; padding: 14px; border: 1px solid #1e293b; border-radius: 8px; resize: none; outline: none; white-space: pre-wrap;" oninput="updateRawHtmlStats()"></textarea>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1e293b; padding-top: 12px;">
        <div style="font-size: 0.75rem; color: #64748b;">
          💡 Direct changes will be written directly to the page file and trigger site recompilation.
        </div>
        <div style="display: flex; gap: 10px;">
          <button type="button" class="btn btn-secondary" onclick="closeRawHtmlEditorModal()">Close</button>
          <button type="button" class="btn btn-primary" onclick="saveRawHtmlPage()" style="background: #2563eb; font-weight: 700;">💾 Save HTML &amp; Recompile Site</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toastContainer"></div>

  <!-- ===================================================================== -->
  <!-- JAVASCRIPT ENGINE -->
  <!-- ===================================================================== -->
  <script>
    // Global State
    let SITE_DATA = null;
    let MEDIA_LIST = [];
    let INQUIRIES_LIST = [];
    let CURRENT_PICKER_TARGET_INPUT_ID = null;

    // Initialize on load
    document.addEventListener('DOMContentLoaded', () => {
      checkExistingSession();
    });

    // Toast Helper
    function showToast(msg, type = 'success') {
      const container = document.getElementById('toastContainer');
      const item = document.createElement('div');
      item.className = `toast-item ${type}`;
      item.innerHTML = `<span>${type === 'success' ? '✅' : (type === 'error' ? '❌' : 'ℹ️')}</span> <span>${msg}</span>`;
      container.appendChild(item);
      setTimeout(() => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        setTimeout(() => item.remove(), 300);
      }, 3500);
    }

    // Session Verification
    async function checkExistingSession() {
      const token = localStorage.getItem('wideway_admin_token');
      if (!token) {
        showLoginScreen();
        return;
      }
      try {
        const res = await fetch('/api/verify-token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token })
        });
        const data = await res.json();
        if (data.valid) {
          hideLoginScreen();
          initAdminApp();
        } else {
          showLoginScreen();
        }
      } catch (err) {
        showLoginScreen();
      }
    }

    function showLoginScreen() {
      document.getElementById('loginScreen').style.display = 'flex';
      document.getElementById('adminApp').style.display = 'none';
    }

    function hideLoginScreen() {
      document.getElementById('loginScreen').style.display = 'none';
      document.getElementById('adminApp').style.display = 'flex';
    }

    function toggleLoginPasswordVisibility() {
      const input = document.getElementById('loginPasswordInput');
      if (!input) return;
      input.type = input.type === 'password' ? 'text' : 'password';
    }

    // Login Form
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const password = document.getElementById('loginPasswordInput').value.trim();
      try {
        const res = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password })
        });
        const data = await res.json();
        if (data.status === 'success' && data.session_token) {
          localStorage.setItem('wideway_admin_token', data.session_token);
          hideLoginScreen();
          initAdminApp();
          showToast('Welcome back, Administrator!');
        } else {
          showToast(data.message || 'Authentication failed: Please check password', 'error');
        }
      } catch (err) {
        showToast('Login request error: ' + err.message, 'error');
      }
    }

    function handleLogout() {
      localStorage.removeItem('wideway_admin_token');
      showLoginScreen();
      showToast('Logged out successfully');
    }

    // Initialize CMS App Data
    async function initAdminApp() {
      await loadContentDatabase();
      await loadMediaList();
      await loadInquiriesList();
      renderDashboardOverview();
      loadSelectedPageBlocks();
    }

    async function loadContentDatabase() {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/content', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          SITE_DATA = await res.json();
          populateGeneralSettings();
          renderProductsTable();
          renderNewsTable();
        }
      } catch (e) {
        console.error('Failed to load content database:', e);
      }
    }

    // Tab Switching
    function switchTab(tabId) {
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));

      const targetPanel = document.getElementById(`tab_${tabId}`);
      if (targetPanel) targetPanel.classList.add('active');

      const clickedNavItem = Array.from(document.querySelectorAll('.nav-item')).find(el => el.getAttribute('onclick')?.includes(tabId));
      if (clickedNavItem) clickedNavItem.classList.add('active');

      const titles = {
        'dashboard': 'Dashboard Overview',
        'global_search': 'Search & Batch Replace',
        'page_blocks': 'Pages & Block Master',
        'visual_studio': 'Visual Live Studio',
        'products_matrix': 'Products Matrix (115+ SKUs)',
        'newsroom': 'Newsroom & AI Scheduler',
        'media_vault': 'Media & Video Vault',
        'inquiries_crm': 'Inquiries & RFQ Leads CRM',
        'contact_channels': 'Global Contact Desk',
        'seo_geo_command': 'SEO & GEO AI Command',
        'ai_copywriting': 'AI Multi-Language Studio',
        'system_devops': 'Production Deployment & DevOps'
      };
      document.getElementById('topPageTitle').textContent = titles[tabId] || 'Dashboard Overview';

      if (tabId === 'media_vault') {
        loadMediaList();
      } else if (tabId === 'inquiries_crm') {
        loadInquiriesList();
      }
    }

    // ------------------------------------------------------------------------
    // DASHBOARD & STATS
    // ------------------------------------------------------------------------
    function renderDashboardOverview() {
      if (!SITE_DATA) return;
      document.getElementById('statTotalProducts').textContent = (SITE_DATA.products || []).length;
      document.getElementById('badgeProductCount').textContent = (SITE_DATA.products || []).length;
      document.getElementById('statTotalNews').textContent = (SITE_DATA.news || []).length;
      document.getElementById('badgeNewsCount').textContent = (SITE_DATA.news || []).length;
      document.getElementById('statTotalInquiries').textContent = INQUIRIES_LIST.length;
      document.getElementById('badgeInquiryCount').textContent = INQUIRIES_LIST.length;
      document.getElementById('statTotalMedia').textContent = MEDIA_LIST.length;
    }

    // ------------------------------------------------------------------------
    // GLOBAL SEARCH & BATCH REPLACE
    // ------------------------------------------------------------------------
    function executeGlobalSearch() {
      const q = document.getElementById('globalSearchInput').value.trim().toLowerCase();
      const container = document.getElementById('globalSearchResultsContainer');
      if (!q || !SITE_DATA) {
        container.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--text-muted); border: 1px dashed var(--border); border-radius: var(--radius-md);">Type any text or keyword above to see all matching pages, products, news articles, and blocks in real time.</div>`;
        return;
      }

      const matches = [];

      // Search Company Info
      for (const [k, v] of Object.entries(SITE_DATA.company_info || {})) {
        if (typeof v === 'string' && v.toLowerCase().includes(q)) {
          matches.push({ loc: `General Settings > ${k}`, val: v });
        }
      }

      // Search Pages Content
      if (SITE_DATA.pages_content) {
        for (const [page, sections] of Object.entries(SITE_DATA.pages_content)) {
          for (const [sec, content] of Object.entries(sections)) {
            if (typeof content === 'string' && content.toLowerCase().includes(q)) {
              matches.push({ loc: `Page [${page}] > Section [${sec}]`, val: content });
            } else if (typeof content === 'object') {
              for (const [subk, subv] of Object.entries(content)) {
                if (typeof subv === 'string' && subv.toLowerCase().includes(q)) {
                  matches.push({ loc: `Page [${page}] > [${sec}] > ${subk}`, val: subv });
                }
              }
            }
          }
        }
      }

      // Search Products
      (SITE_DATA.products || []).forEach(p => {
        const str = `${p.name} ${p.code} ${p.upper} ${p.outsole} ${p.customization}`.toLowerCase();
        if (str.includes(q)) {
          matches.push({ loc: `Product SKU [${p.code}] - ${p.name}`, val: `Upper: ${p.upper || ''} | Outsole: ${p.outsole || ''} | MOQ: ${p.moq || ''}` });
        }
      });

      // Search News
      (SITE_DATA.news || []).forEach(n => {
        const str = `${n.title} ${n.summary} ${n.category}`.toLowerCase();
        if (str.includes(q)) {
          matches.push({ loc: `News [${n.date}] - ${n.title}`, val: n.summary });
        }
      });

      if (matches.length === 0) {
        container.innerHTML = `<div style="padding: 30px; text-align: center; color: var(--warning);">No occurrences found for "${q}".</div>`;
        return;
      }

      let html = `<div style="margin-bottom: 12px; font-weight: 700; color: var(--success);">Found ${matches.length} matches for "${q}":</div>`;
      html += `<div style="display: flex; flex-direction: column; gap: 8px; max-height: 450px; overflow-y: auto;">`;
      matches.forEach(m => {
        html += `
          <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px;">
            <div style="font-size: 0.78rem; font-weight: 700; color: var(--primary); text-transform: uppercase;">${escapeHtml(m.loc)}</div>
            <div style="font-size: 0.88rem; color: var(--text); margin-top: 4px; word-break: break-all;">${highlightMatch(m.val, q)}</div>
          </div>
        `;
      });
      html += `</div>`;
      container.innerHTML = html;
    }

    function highlightMatch(text, query) {
      if (!text || !query) return escapeHtml(text || '');
      const escaped = escapeHtml(text);
      const reg = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      return escaped.replace(reg, '<span style="background: rgba(245, 158, 11, 0.4); color: #fff; font-weight: 700; padding: 0 4px; border-radius: 2px;">$1</span>');
    }

    async function executeBatchReplace() {
      const search_str = document.getElementById('globalSearchInput').value.trim();
      const replace_str = document.getElementById('globalReplaceInput').value;
      if (!search_str) {
        showToast('Please enter a search string', 'error');
        return;
      }
      if (!confirm(`Are you sure you want to replace all occurrences of "${search_str}" with "${replace_str}" across the entire website?`)) {
        return;
      }

      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/batch-replace', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ search_str, replace_str, case_sensitive: false })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(`Successfully replaced ${data.replace_count} occurrences!`);
          await loadContentDatabase();
          executeGlobalSearch();
        } else {
          showToast(data.message || 'Replace failed', 'error');
        }
      } catch (err) {
        showToast('Error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // PAGES & BLOCK MASTER EDITOR
    // ------------------------------------------------------------------------
    function openRawHtmlForCurrentPageBlock() {
      const pageKey = document.getElementById('pageSelectDropdown').value;
      const pageMap = {
        'home': 'index.html',
        'about': 'about.html',
        'oem_odm': 'oem-odm.html',
        'contact': 'contact.html',
        'sport_outdoor_shoes': 'sport-outdoor-shoes-wholesale.html',
        'casual_shoes': 'casual-shoes-oem-manufacturer.html',
        'mens_sneakers': 'mens-sneakers-bulk-supplier.html',
        'womens_sneakers': 'womens-sneakers-oem-factory.html',
        'slides_sandals': 'slides-sandals-slippers-manufacturer.html',
        'bags_sportswear': 'bags-sportswear-accessories-wholesale.html',
        'production_capacity': 'production-capacity.html',
        'quality_control': 'quality-control.html',
        'certifications': 'certifications.html',
        'sustainability': 'sustainability.html',
        'heritage_footwear': 'heritage-footwear-reproduction.html',
        'brand_identity': 'brand-identity.html',
        'case_studies': 'case-studies.html',
        'videos': 'videos.html',
        'knowledge_base': 'knowledge-base.html',
        'whitepapers': 'whitepapers.html',
        'glossary': 'glossary.html'
      };
      const fname = pageMap[pageKey] || `${pageKey}.html`;
      openRawHtmlEditorModal(fname);
    }

    function loadSelectedPageBlocks() {
      const pageKey = document.getElementById('pageSelectDropdown').value;
      const container = document.getElementById('pageBlockEditorContainer');
      if (!SITE_DATA || !SITE_DATA.pages_content || !SITE_DATA.pages_content[pageKey]) {
        container.innerHTML = `
          <div style="padding: 40px; text-align: center; color: var(--text-muted); background: rgba(15,23,42,0.4); border-radius: 8px; border: 1px dashed var(--border);">
            <div style="font-size: 1.1rem; color: #f8fafc; margin-bottom: 8px;">📄 Direct HTML Page Editing</div>
            <div style="margin-bottom: 16px; font-size: 0.88rem;">This page is ready for full-code live customization or visual click-to-edit inspection.</div>
            <button type="button" class="btn btn-primary" onclick="openRawHtmlForCurrentPageBlock()">
              <span>📝 Open Page in Raw HTML Editor</span>
            </button>
          </div>
        `;
        return;
      }

      const pageData = SITE_DATA.pages_content[pageKey];
      let html = '';

      for (const [secKey, secVal] of Object.entries(pageData)) {
        const secTitle = secKey.replace(/_/g, ' ').toUpperCase();
        html += `
          <div class="block-accordion">
            <div class="accordion-header" onclick="toggleAccordion(this)">
              <span>📦 Section: ${secTitle}</span>
              <span>▾</span>
            </div>
            <div class="accordion-content open">
              ${renderSectionFormFields(pageKey, secKey, secVal)}
            </div>
          </div>
        `;
      }

      container.innerHTML = html;
    }

    function toggleAccordion(headerEl) {
      const content = headerEl.nextElementSibling;
      content.classList.toggle('open');
    }

    function renderSectionFormFields(pageKey, secKey, secVal) {
      let fieldsHtml = '<div class="grid-2">';
      if (typeof secVal === 'object' && !Array.isArray(secVal)) {
        for (const [k, v] of Object.entries(secVal)) {
          const fieldId = `field_${pageKey}_${secKey}_${k}`;
          const isImgOrVideo = k.includes('image') || k.includes('poster') || k.includes('video') || k.includes('banner');
          const isLongText = typeof v === 'string' && (v.length > 80 || k.includes('body') || k.includes('desc') || k.includes('summary') || k.includes('lead') || k.includes('subtitle') || k.includes('headline'));

          fieldsHtml += `
            <div class="input-group" style="${isLongText ? 'grid-column: span 2;' : ''}">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label style="margin-bottom: 0;">${k.replace(/_/g, ' ')}</label>
                <div style="display: flex; gap: 6px;">
                  <button type="button" class="btn btn-secondary btn-sm" onclick="polishFieldWithAi('${fieldId}')" style="padding: 2px 7px; font-size: 0.75rem;">✨ Polish</button>
                  <button type="button" class="btn btn-secondary btn-sm" onclick="translateFieldWithAi('${fieldId}')" style="padding: 2px 7px; font-size: 0.75rem;">🌐 Translate</button>
                </div>
              </div>
          `;

          if (isImgOrVideo) {
            fieldsHtml += `
              <div style="display: flex; gap: 8px;">
                <input type="text" id="${fieldId}" class="input-field" value="${escapeHtml(v || '')}" data-page="${pageKey}" data-sec="${secKey}" data-key="${k}">
                <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('${fieldId}')">Choose</button>
              </div>
            `;
          } else if (isLongText) {
            fieldsHtml += `
              <textarea id="${fieldId}" class="input-field" data-page="${pageKey}" data-sec="${secKey}" data-key="${k}">${escapeHtml(v || '')}</textarea>
            `;
          } else {
            fieldsHtml += `
              <input type="text" id="${fieldId}" class="input-field" value="${escapeHtml(v || '')}" data-page="${pageKey}" data-sec="${secKey}" data-key="${k}">
            `;
          }
          fieldsHtml += `</div>`;
        }
      } else if (Array.isArray(secVal)) {
        fieldsHtml = `<div style="grid-column: span 2;">`;
        secVal.forEach((item, idx) => {
          fieldsHtml += `
            <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 12px;">
              <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary); margin-bottom: 10px;">Item #${idx + 1}</div>
              <div class="grid-2">
          `;
          for (const [ik, iv] of Object.entries(item)) {
            const arrFieldId = `field_${pageKey}_${secKey}_${idx}_${ik}`;
            const isImg = ik.includes('image') || ik.includes('poster');
            fieldsHtml += `
              <div class="input-group">
                <label>${ik.replace(/_/g, ' ')}</label>
            `;
            if (isImg) {
              fieldsHtml += `
                <div style="display: flex; gap: 8px;">
                  <input type="text" id="${arrFieldId}" class="input-field" value="${escapeHtml(iv || '')}" data-page="${pageKey}" data-sec="${secKey}" data-idx="${idx}" data-key="${ik}">
                  <button type="button" class="btn btn-secondary" onclick="openMediaPickerForInput('${arrFieldId}')">Choose</button>
                </div>
              `;
            } else {
              fieldsHtml += `
                <input type="text" id="${arrFieldId}" class="input-field" value="${escapeHtml(iv || '')}" data-page="${pageKey}" data-sec="${secKey}" data-idx="${idx}" data-key="${ik}">
              `;
            }
            fieldsHtml += `</div>`;
          }
          fieldsHtml += `</div></div>`;
        });
        fieldsHtml += `</div>`;
      }
      fieldsHtml += '</div>';
      return fieldsHtml;
    }

    async function savePageBlocks() {
      const pageKey = document.getElementById('pageSelectDropdown').value;
      if (!SITE_DATA || !SITE_DATA.pages_content || !SITE_DATA.pages_content[pageKey]) return;

      const inputs = document.querySelectorAll(`[data-page="${pageKey}"]`);
      inputs.forEach(input => {
        const sec = input.getAttribute('data-sec');
        const key = input.getAttribute('data-key');
        const idx = input.getAttribute('data-idx');
        const val = input.value;

        if (idx !== null && idx !== undefined) {
          if (SITE_DATA.pages_content[pageKey][sec] && SITE_DATA.pages_content[pageKey][sec][idx]) {
            SITE_DATA.pages_content[pageKey][sec][idx][key] = val;
          }
        } else {
          if (SITE_DATA.pages_content[pageKey][sec]) {
            SITE_DATA.pages_content[pageKey][sec][key] = val;
          }
        }
      });

      await saveContentAndRebuild();
    }

    // ------------------------------------------------------------------------
    // GENERAL / CONTACT / SEO SETTINGS
    // ------------------------------------------------------------------------
    function populateGeneralSettings() {
      if (!SITE_DATA || !SITE_DATA.company_info) return;
      const c = SITE_DATA.company_info;
      document.getElementById('cfgNameEn').value = c.name_en || '';
      document.getElementById('cfgNameZh').value = c.name_zh || '';
      document.getElementById('cfgPhone').value = c.phone || '+86 185 0595 9266';
      document.getElementById('cfgEmail').value = c.email || 'amy@widewaygroup.com';
      document.getElementById('cfgEmailSecondary').value = c.email_secondary || 'kelly@widewaygroup.com';
      document.getElementById('cfgPort').value = c.port || '';
      document.getElementById('cfgAddress').value = c.address || '';
      document.getElementById('cfgRegisteredAddress').value = c.registered_address || '';

      document.getElementById('cfgPrimaryKeyword').value = c.primary_keyword || '';
      document.getElementById('cfgSlogan').value = c.slogan || '';
      document.getElementById('cfgMetaDescription').value = c.meta_description || '';
      document.getElementById('cfgSecondaryKeywords').value = (c.secondary_keywords || []).join(', ');
    }

    async function saveContactChannels() {
      if (!SITE_DATA || !SITE_DATA.company_info) return;
      SITE_DATA.company_info.name_en = document.getElementById('cfgNameEn').value;
      SITE_DATA.company_info.name_zh = document.getElementById('cfgNameZh').value;
      SITE_DATA.company_info.phone = document.getElementById('cfgPhone').value;
      SITE_DATA.company_info.mobile = document.getElementById('cfgPhone').value;
      SITE_DATA.company_info.whatsapp = document.getElementById('cfgPhone').value;
      SITE_DATA.company_info.wechat = document.getElementById('cfgPhone').value;
      SITE_DATA.company_info.email = document.getElementById('cfgEmail').value;
      SITE_DATA.company_info.email_secondary = document.getElementById('cfgEmailSecondary').value;
      SITE_DATA.company_info.port = document.getElementById('cfgPort').value;
      SITE_DATA.company_info.address = document.getElementById('cfgAddress').value;
      SITE_DATA.company_info.registered_address = document.getElementById('cfgRegisteredAddress').value;

      await saveContentAndRebuild();
    }

    async function saveSeoGeoSettings() {
      if (!SITE_DATA || !SITE_DATA.company_info) return;
      SITE_DATA.company_info.primary_keyword = document.getElementById('cfgPrimaryKeyword').value;
      SITE_DATA.company_info.slogan = document.getElementById('cfgSlogan').value;
      SITE_DATA.company_info.meta_description = document.getElementById('cfgMetaDescription').value;
      SITE_DATA.company_info.secondary_keywords = document.getElementById('cfgSecondaryKeywords').value.split(',').map(s => s.trim()).filter(Boolean);

      await saveContentAndRebuild();
    }

    // ------------------------------------------------------------------------
    // PRODUCTS MANAGER (115+ SKUs)
    // ------------------------------------------------------------------------
    function renderProductsTable(filteredList = null) {
      const tbody = document.getElementById('productsTableBody');
      const list = filteredList || (SITE_DATA?.products || []);
      if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding:30px; color:var(--text-muted);">No products found matching criteria.</td></tr>`;
        return;
      }

      let html = '';
      list.forEach((p, idx) => {
        const realIdx = (SITE_DATA?.products || []).indexOf(p);
        const hasVideo = !!(p.video && p.video.trim() !== '');
        const descPreview = p.description ? p.description.substring(0, 90) + '...' : 'No description set';
        html += `
          <tr>
            <td>
              <img src="${p.image || 'images/sneakers_running.jpg'}" alt="${p.code || ''}" style="width:50px; height:50px; object-fit:cover; border-radius:6px; border:1px solid var(--border);" onerror="this.src='https://via.placeholder.com/50x50?text=Shoe'">
            </td>
            <td>
              <strong style="color:var(--primary); font-family:var(--font-mono);">${escapeHtml(p.code || p.name || 'SKU')}</strong>
              <div style="display:flex; gap:4px; flex-wrap:wrap; margin-top:3px;">
                ${hasVideo ? '<span style="background:rgba(37,99,235,0.18); color:#60a5fa; font-size:0.65rem; padding:1px 5px; border-radius:4px; font-weight:600; border:1px solid rgba(59,130,246,0.35);">🎬 4K Video</span>' : ''}
                <span style="background:rgba(16,185,129,0.15); color:#34d399; font-size:0.65rem; padding:1px 5px; border-radius:4px; font-weight:600; border:1px solid rgba(16,185,129,0.3);">🌍 GEO Ready</span>
              </div>
            </td>
            <td>
              <div style="font-weight:600; color:#f8fafc;">${escapeHtml(p.name || '')}</div>
              <div style="font-size:0.75rem; color:var(--text-dim); margin-top:1px;">${p.category || 'Footwear'}</div>
              <div style="font-size:0.75rem; color:#94a3b8; margin-top:3px; max-width:280px; line-height:1.3; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${escapeHtml(p.description || '')}">
                📝 ${escapeHtml(descPreview)}
              </div>
            </td>
            <td><div style="font-size:0.82rem;">${escapeHtml(p.upper || 'Flyknit / Mesh')}</div></td>
            <td><div style="font-size:0.82rem;">${escapeHtml(p.outsole || 'EVA / Rubber')}</div></td>
            <td><span class="badge-status" style="background:rgba(255,255,255,0.06);">${p.moq || '500 Pairs'}</span></td>
            <td><span style="font-size:0.82rem; color:var(--text-muted);">${p.lead_time || '30-45 Days'}</span></td>
            <td style="text-align: right; white-space:nowrap;">
              <a href="/product-detail?id=${encodeURIComponent(p.id || p.name)}" target="_blank" class="btn btn-secondary btn-sm" style="font-size:0.75rem; padding:4px 8px; margin-right:4px;" title="View on Frontend">↗</a>
              <button class="btn btn-secondary btn-sm" onclick="openEditProductModal(${realIdx})">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="deleteProduct(${realIdx})">✕</button>
            </td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    }

    function filterProductsTable() {
      if (!SITE_DATA || !SITE_DATA.products) return;
      const q = document.getElementById('productSearchInput').value.trim().toLowerCase();
      const cat = document.getElementById('productCategoryFilter').value;

      const filtered = SITE_DATA.products.filter(p => {
        const matchQ = !q || (p.name || '').toLowerCase().includes(q) || (p.code || '').toLowerCase().includes(q) || (p.upper || '').toLowerCase().includes(q) || (p.description || '').toLowerCase().includes(q);
        const matchCat = (cat === 'all') || (p.category === cat) || (p.category && p.category.includes(cat));
        return matchQ && matchCat;
      });
      renderProductsTable(filtered);
    }

    function updateDescCharCount(val) {
      const len = (val || '').length;
      const countEl = document.getElementById('pEditDescCount');
      if (countEl) countEl.textContent = `${len} chars`;
      updateSerpPreview();
    }

    function updateMainImagePreview(url) {
      const img = document.getElementById('pEditMainImagePreview');
      if (img) {
        img.src = url || 'images/sneakers_running.jpg';
      }
    }

    function renderGalleryThumbnails(text) {
      const container = document.getElementById('pEditGalleryThumbsContainer');
      if (!container) return;
      container.innerHTML = '';
      if (!text) return;
      const urls = text.split(/[\n,]/).map(s => s.trim()).filter(Boolean);
      urls.forEach((url, i) => {
        const div = document.createElement('div');
        div.style.position = 'relative';
        div.style.flexShrink = '0';
        div.innerHTML = `
          <img src="${url}" alt="Angle ${i+1}" style="width:45px; height:40px; object-fit:cover; border-radius:4px; border:1px solid #334155; background:#0f172a;" onerror="this.src='images/sneakers_running.jpg'">
          <span style="position:absolute; top:-4px; right:-4px; background:#ef4444; color:#fff; font-size:9px; border-radius:50%; width:14px; height:14px; display:flex; align-items:center; justify-content:center; cursor:pointer;" onclick="removeGalleryAngle(${i})" title="Remove Angle">✕</span>
        `;
        container.appendChild(div);
      });
    }

    function removeGalleryAngle(index) {
      const textarea = document.getElementById('pEditGallery');
      if (!textarea) return;
      let urls = textarea.value.split(/[\n,]/).map(s => s.trim()).filter(Boolean);
      urls.splice(index, 1);
      textarea.value = urls.join('\n');
      renderGalleryThumbnails(textarea.value);
    }

    function appendGalleryAngleFromVault() {
      openMediaPickerForInput('pEditGallery');
    }

    function handleProductNameChange(val) {
      const slugInput = document.getElementById('pEditSlug');
      const seoTitleInput = document.getElementById('pEditSeoTitle');
      const descInput = document.getElementById('pEditDescription');
      
      const slugVal = (val || '').toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '');
      if (document.getElementById('pEditIndex').value === '-1' || !slugInput.value) {
        slugInput.value = slugVal;
      }
      if (document.getElementById('pEditIndex').value === '-1' || !seoTitleInput.value) {
        seoTitleInput.value = `${val} | WIDEWAY GROUP Footwear`;
      }
      if (document.getElementById('pEditIndex').value === '-1' && (!descInput.value || descInput.value.trim() === '')) {
        descInput.value = `Engineered by WIDEWAY footwear lab, the ${val} combines ergonomic arch support, high-elastic cushioning outsoles, and durable wear-resistant materials. Designed for high-volume OEM/ODM export orders with customized branding, colorways, and full size runs.`;
        updateDescCharCount(descInput.value);
      }
      updateSerpPreview();
    }

    function updateSerpPreview() {
      const name = document.getElementById('pEditName')?.value || 'Footwear Model';
      const slug = document.getElementById('pEditSlug')?.value || 'product-slug';
      const seoTitle = document.getElementById('pEditSeoTitle')?.value || `${name} | WIDEWAY GROUP Footwear`;
      const seoDesc = document.getElementById('pEditSeoDesc')?.value || document.getElementById('pEditDescription')?.value || 'Detailed specifications, materials, and OEM/ODM private label options for WIDEWAY footwear.';
      const geoMarkets = document.getElementById('pEditGeoMarkets')?.value || 'North America, Europe, Middle East, Southeast Asia';
      const geoOrigin = document.getElementById('pEditGeoOrigin')?.value || 'Jinjiang, Fujian, China';

      const urlEl = document.getElementById('serpPreviewUrl');
      const titleEl = document.getElementById('serpPreviewTitle');
      const descEl = document.getElementById('serpPreviewDesc');
      const originEl = document.getElementById('serpPreviewOrigin');
      const marketsEl = document.getElementById('serpPreviewMarkets');

      if (urlEl) urlEl.textContent = `https://www.widewayfootwear.com/product-detail?id=${slug}`;
      if (titleEl) titleEl.textContent = seoTitle;
      if (descEl) descEl.textContent = seoDesc;
      if (originEl) originEl.textContent = geoOrigin.split('(')[0].trim();
      if (marketsEl) marketsEl.textContent = geoMarkets;
    }

    function openAddProductModal() {
      document.getElementById('productModalTitle').textContent = '➕ Add Footwear SKU (Shopify Editor)';
      document.getElementById('pEditIndex').value = '-1';
      document.getElementById('productEditForm').reset();
      
      const liveBtn = document.getElementById('btnLivePreviewSku');
      if (liveBtn) liveBtn.style.display = 'none';

      document.getElementById('pEditGallery').value = '';
      document.getElementById('pEditVideo').value = '';
      document.getElementById('pEditVideoPreviewContainer').style.display = 'none';
      document.getElementById('pEditVideoPreview').src = '';
      document.getElementById('pEditVideoUploadProgress').style.display = 'none';

      document.getElementById('pEditGeoMarkets').value = 'North America, European Union, United Kingdom, Middle East, Australia, Southeast Asia';
      document.getElementById('pEditGeoOrigin').value = 'Jinjiang Footwear Industrial Cluster, Fujian, China (SATRA & BSCI Certified Facility)';
      document.getElementById('pEditMoq').value = '500 Pairs / Color';
      document.getElementById('pEditLeadTime').value = '30-45 Days (Samples 7-10 Days)';
      document.getElementById('pEditCustomization').value = 'Custom Logo, Colors, Upper Materials & Packaging';

      updateMainImagePreview('');
      renderGalleryThumbnails('');
      updateDescCharCount('');
      updateSerpPreview();
      document.getElementById('productEditModal').classList.add('active');
    }

    function openEditProductModal(idx) {
      const p = SITE_DATA.products[idx];
      if (!p) return;
      document.getElementById('productModalTitle').textContent = `👟 Edit SKU: ${p.code || p.name}`;
      document.getElementById('pEditIndex').value = idx;
      
      const liveBtn = document.getElementById('btnLivePreviewSku');
      if (liveBtn) {
        liveBtn.style.display = 'inline-flex';
        liveBtn.href = `/product-detail?id=${encodeURIComponent(p.id || p.name)}`;
      }

      document.getElementById('pEditCode').value = p.code || p.name || '';
      document.getElementById('pEditName').value = p.name || '';
      document.getElementById('pEditCat').value = p.category || 'sport-outdoor-shoes';
      document.getElementById('pEditImage').value = p.image || '';
      document.getElementById('pEditVideo').value = p.video || '';
      
      const descVal = p.description || `Engineered by WIDEWAY footwear lab, the ${p.name || 'product'} combines ergonomic arch support, high-elastic cushioning outsoles, and durable wear-resistant materials. Designed for high-volume OEM/ODM export orders with customized branding, colorways, and full size runs.`;
      document.getElementById('pEditDescription').value = descVal;
      updateDescCharCount(descVal);

      // Gallery
      const galleryList = Array.isArray(p.gallery) && p.gallery.length > 0 ? p.gallery : (p.image ? [p.image] : []);
      document.getElementById('pEditGallery').value = galleryList.join('\n');
      renderGalleryThumbnails(document.getElementById('pEditGallery').value);

      document.getElementById('pEditUpper').value = p.upper || '';
      document.getElementById('pEditOutsole').value = p.outsole || '';
      document.getElementById('pEditLining').value = p.lining || '';
      document.getElementById('pEditSizes').value = p.sizes || 'EU 36-45 / US 5-11';
      document.getElementById('pEditMoq').value = p.moq || '500 Pairs / Color';
      document.getElementById('pEditLeadTime').value = p.lead_time || '30-45 Days (Samples 7-10 Days)';
      document.getElementById('pEditCustomization').value = p.customization || 'Custom Logo, Colors, Upper Materials & Packaging';

      document.getElementById('pEditTag').value = p.tag || 'Wideway Footwear';
      document.getElementById('pEditKeywords').value = p.keywords || `${p.name}, Breathable, Anti-slip`;

      // SEO & GEO
      document.getElementById('pEditSlug').value = p.id || (p.code || p.name || '').toLowerCase().replace(/[^a-z0-9_-]+/g, '-');
      document.getElementById('pEditSeoTitle').value = p.seo_title || `${p.name} | WIDEWAY GROUP Footwear`;
      document.getElementById('pEditSeoDesc').value = p.seo_description || (p.description ? p.description.substring(0, 160) : '');
      document.getElementById('pEditGeoMarkets').value = p.geo_markets || 'North America, European Union, United Kingdom, Middle East, Australia, Southeast Asia';
      document.getElementById('pEditGeoOrigin').value = p.geo_origin || 'Jinjiang Footwear Industrial Cluster, Fujian, China (SATRA & BSCI Certified Facility)';

      updateMainImagePreview(p.image || '');

      const previewCont = document.getElementById('pEditVideoPreviewContainer');
      const videoPreview = document.getElementById('pEditVideoPreview');
      const statusSpan = document.getElementById('pEditVideoStatus');
      const progressEl = document.getElementById('pEditVideoUploadProgress');
      if (progressEl) progressEl.style.display = 'none';

      if (p.video && p.video.trim() !== '') {
        previewCont.style.display = 'block';
        videoPreview.src = p.video;
        if (statusSpan) statusSpan.textContent = '✓ Video Attached';
      } else {
        previewCont.style.display = 'none';
        videoPreview.src = '';
      }

      updateSerpPreview();
      document.getElementById('productEditModal').classList.add('active');
    }

    function closeProductEditModal() {
      document.getElementById('productEditModal').classList.remove('active');
      const videoPreview = document.getElementById('pEditVideoPreview');
      if (videoPreview) {
        videoPreview.pause();
        videoPreview.src = '';
      }
    }

    function handleProductVideoFileSelect(input) {
      const file = input.files && input.files[0];
      if (!file) return;

      const MAX_VIDEO_SIZE = 50 * 1024 * 1024; // 50MB
      if (file.size > MAX_VIDEO_SIZE) {
        const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
        alert(`【上传拦截】视频文件过大！\n\n当前选择视频大小：${sizeMb} MB\n系统最大允许限制：50.00 MB\n\n该视频超过了 50MB 限制，系统已自动拒绝上传。请使用剪辑压缩工具将视频转码或压缩至 50MB 以内后再上传。`);
        showToast(`❌ 视频大小 (${sizeMb} MB) 超过 50MB 限制！已自动拦截`, 5000);
        input.value = '';
        return;
      }

      uploadProductVideoFile(file, input);
    }

    async function uploadProductVideoFile(file, inputElement = null) {
      const progressEl = document.getElementById('pEditVideoUploadProgress');
      const previewCont = document.getElementById('pEditVideoPreviewContainer');
      const videoPreview = document.getElementById('pEditVideoPreview');
      const statusSpan = document.getElementById('pEditVideoStatus');
      const videoInput = document.getElementById('pEditVideo');

      if (progressEl) {
        progressEl.style.display = 'block';
        progressEl.textContent = `⏳ Uploading video "${file.name}" (${(file.size / (1024 * 1024)).toFixed(2)} MB)... please wait.`;
      }

      try {
        const formData = new FormData();
        formData.append('file', file, file.name);

        const res = await fetch('/api/upload-media', {
          method: 'POST',
          body: formData
        });

        const data = await res.json();
        if (data.status === 'success') {
          videoInput.value = data.url;
          if (previewCont) previewCont.style.display = 'block';
          if (videoPreview) {
            videoPreview.src = data.url;
            videoPreview.load();
          }
          if (statusSpan) {
            statusSpan.textContent = `✓ Uploaded (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
          }
          showToast(`🎬 Video uploaded successfully (${(file.size / (1024 * 1024)).toFixed(2)} MB)!`);
        } else {
          throw new Error(data.message || 'Upload failed');
        }
      } catch (err) {
        alert('视频上传失败：' + err.message);
        showToast('❌ Video upload failed: ' + err.message, 5000);
      } finally {
        if (progressEl) progressEl.style.display = 'none';
        if (inputElement) inputElement.value = '';
      }
    }

    function removeProductVideo() {
      document.getElementById('pEditVideo').value = '';
      const previewCont = document.getElementById('pEditVideoPreviewContainer');
      const videoPreview = document.getElementById('pEditVideoPreview');
      if (previewCont) previewCont.style.display = 'none';
      if (videoPreview) {
        videoPreview.pause();
        videoPreview.src = '';
      }
      showToast('Product video removed');
    }

    async function handleSaveProductSubmit(e) {
      e.preventDefault();
      const idx = parseInt(document.getElementById('pEditIndex').value);
      const existing = (idx >= 0 && SITE_DATA.products && SITE_DATA.products[idx]) ? SITE_DATA.products[idx] : {};

      const nameVal = document.getElementById('pEditName').value.trim();
      const codeVal = document.getElementById('pEditCode').value.trim();
      const slugVal = document.getElementById('pEditSlug').value.trim();
      const imageVal = document.getElementById('pEditImage').value.trim();
      const videoVal = document.getElementById('pEditVideo').value.trim();
      const descVal = document.getElementById('pEditDescription').value.trim();

      // Safe ID / Slug generation
      let safeId = slugVal;
      if (!safeId) {
        safeId = (codeVal || nameVal || `product-${Date.now()}`)
          .toLowerCase()
          .replace(/[^a-z0-9_-]+/g, '-')
          .replace(/^-+|-+$/g, '');
      }

      // Safe gallery parsing
      const galleryRaw = document.getElementById('pEditGallery').value;
      let galleryList = galleryRaw.split(/[\n,]/).map(s => s.trim()).filter(Boolean);
      if (galleryList.length === 0 && imageVal) {
        galleryList = [imageVal];
      }
      if (imageVal && !galleryList.includes(imageVal)) {
        galleryList.unshift(imageVal);
      }

      const productObj = {
        ...existing,
        id: safeId,
        name: nameVal,
        code: codeVal,
        category: document.getElementById('pEditCat').value,
        image: imageVal,
        gallery: galleryList,
        video: videoVal,
        description: descVal,
        tag: document.getElementById('pEditTag').value.trim() || 'Wideway Footwear',
        keywords: document.getElementById('pEditKeywords').value.trim() || `${nameVal}, Breathable, Anti-slip`,
        upper: document.getElementById('pEditUpper').value.trim(),
        outsole: document.getElementById('pEditOutsole').value.trim(),
        lining: document.getElementById('pEditLining').value.trim(),
        sizes: document.getElementById('pEditSizes').value.trim() || 'EU 36-45 / US 5-11',
        moq: document.getElementById('pEditMoq').value.trim() || '500 Pairs / Color',
        lead_time: document.getElementById('pEditLeadTime').value.trim() || '30-45 Days (Samples 7-10 Days)',
        customization: document.getElementById('pEditCustomization').value.trim() || 'Custom Logo, Colors, Upper Materials & Packaging',
        seo_title: document.getElementById('pEditSeoTitle').value.trim() || `${nameVal} | WIDEWAY GROUP Footwear`,
        seo_description: document.getElementById('pEditSeoDesc').value.trim() || (descVal.substring(0, 160)),
        geo_markets: document.getElementById('pEditGeoMarkets').value.trim() || 'North America, European Union, United Kingdom, Middle East, Australia, Southeast Asia',
        geo_origin: document.getElementById('pEditGeoOrigin').value.trim() || 'Jinjiang Footwear Industrial Cluster, Fujian, China (SATRA & BSCI Certified Facility)'
      };

      if (idx === -1) {
        SITE_DATA.products.unshift(productObj);
      } else {
        SITE_DATA.products[idx] = productObj;
      }

      closeProductEditModal();
      await saveContentAndRebuild();
      renderProductsTable();
      showToast('Product, SEO/GEO attributes, and description saved successfully!');
    }

    async function deleteProduct(idx) {
      if (!confirm('Are you sure you want to delete this product SKU?')) return;
      SITE_DATA.products.splice(idx, 1);
      await saveContentAndRebuild();
      renderProductsTable();
      showToast('Product deleted');
    }

    // ------------------------------------------------------------------------
    // NEWSROOM & AUTO-SCHEDULER
    // ------------------------------------------------------------------------
    function renderNewsTable() {
      const tbody = document.getElementById('newsTableBody');
      const list = SITE_DATA?.news || [];
      if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">No news articles found.</td></tr>`;
        return;
      }

      let html = '';
      list.forEach((n, idx) => {
        const isPublished = n.status !== 'scheduled';
        html += `
          <tr>
            <td>
              <img src="${n.image || 'images/banner_factory.jpg'}" alt="${n.title || ''}" style="width:45px; height:45px; object-fit:cover; border-radius:6px;" onerror="this.src='https://via.placeholder.com/45x45?text=News'">
            </td>
            <td>
              <div style="font-weight:600; max-width:380px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(n.title || '')}</div>
              <div style="font-size:0.75rem; color:var(--text-dim);">${escapeHtml(n.filename || '')}</div>
            </td>
            <td><span class="badge-status" style="background:rgba(255,255,255,0.06);">${n.category || 'News'}</span></td>
            <td><span style="font-family:var(--font-mono); font-size:0.82rem;">${n.publish_date || n.sitemap_date || n.date || ''}</span></td>
            <td>
              <span class="badge-status ${isPublished ? 'published' : 'scheduled'}">
                ${isPublished ? 'Published' : 'Scheduled'}
              </span>
            </td>
            <td style="text-align: right;">
              ${!isPublished ? `<button class="btn btn-brand-red btn-sm" onclick="publishArticleNow('${n.filename}')" title="Publish immediately">Publish Now</button>` : ''}
              <button class="btn btn-secondary btn-sm" onclick="openEditNewsModal(${idx})">Edit</button>
            </td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    }

    function openAddNewsModal() {
      document.getElementById('newsModalTitle').textContent = '➕ Write News Article';
      document.getElementById('nEditIndex').value = '-1';
      document.getElementById('nEditFilename').value = `news-${Date.now()}.html`;
      document.getElementById('newsEditForm').reset();
      document.getElementById('nEditDate').value = new Date().toISOString().split('T')[0];
      document.getElementById('newsEditModal').classList.add('active');
    }

    function openEditNewsModal(idx) {
      const n = SITE_DATA.news[idx];
      if (!n) return;
      document.getElementById('newsModalTitle').textContent = `📰 Edit Article: ${n.title}`;
      document.getElementById('nEditIndex').value = idx;
      document.getElementById('nEditFilename').value = n.filename || '';
      document.getElementById('nEditTitle').value = n.title || '';
      document.getElementById('nEditCat').value = n.category || '⚙️ Product News';
      document.getElementById('nEditDate').value = n.publish_date || n.sitemap_date || new Date().toISOString().split('T')[0];
      document.getElementById('nEditImage').value = n.image || '';
      document.getElementById('nEditSummary').value = n.summary || '';
      document.getElementById('nEditBody').value = n.body || '';
      document.getElementById('newsEditModal').classList.add('active');
    }

    function closeNewsEditModal() {
      document.getElementById('newsEditModal').classList.remove('active');
    }

    async function handleSaveNewsSubmit(e) {
      e.preventDefault();
      const idx = parseInt(document.getElementById('nEditIndex').value);
      const filename = document.getElementById('nEditFilename').value;
      const pubDate = document.getElementById('nEditDate').value;
      const displayDate = new Date(pubDate).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

      const newsObj = {
        filename: filename,
        title: document.getElementById('nEditTitle').value,
        category: document.getElementById('nEditCat').value,
        publish_date: pubDate,
        sitemap_date: pubDate,
        date: displayDate,
        image: document.getElementById('nEditImage').value,
        summary: document.getElementById('nEditSummary').value,
        body: document.getElementById('nEditBody').value,
        status: new Date(pubDate) <= new Date() ? 'published' : 'scheduled'
      };

      if (idx === -1) {
        SITE_DATA.news.unshift(newsObj);
      } else {
        SITE_DATA.news[idx] = Object.assign(SITE_DATA.news[idx] || {}, newsObj);
      }

      closeNewsEditModal();
      await saveContentAndRebuild();
      renderNewsTable();
      showToast('Article saved and site rebuilt!');
    }

    async function publishArticleNow(filename) {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/scheduler/publish-now', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ filename })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(`Article ${filename} published immediately!`);
          await loadContentDatabase();
        } else {
          showToast(data.message || 'Failed', 'error');
        }
      } catch (err) {
        showToast('Error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // MEDIA & VIDEO ASSET VAULT
    // ------------------------------------------------------------------------
    async function loadMediaList() {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/media-list', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          MEDIA_LIST = data.media || [];
          renderMediaVaultGrid();
        }
      } catch (e) {
        console.error('Failed to load media list:', e);
      }
    }

    function renderMediaVaultGrid(filtered = null) {
      const container = document.getElementById('mediaVaultGrid');
      const list = filtered || MEDIA_LIST;
      if (list.length === 0) {
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">No media assets found. Upload images or videos above.</div>`;
        return;
      }

      let html = '';
      const cacheBust = Date.now();
      list.forEach(m => {
        const displayUrl = `${m.url}?v=${cacheBust}`;
        html += `
          <div class="media-card">
            <div class="media-thumb-container">
              ${m.is_video ? `
                <video src="${displayUrl}" preload="metadata"></video>
                <span class="video-play-badge">▶ MP4</span>
              ` : `
                <img src="${displayUrl}" alt="${m.name}" loading="lazy">
              `}
            </div>
            <div class="media-meta">
              <div class="media-name" title="${m.name}">${m.name}</div>
              <div class="media-size">${m.size_kb} KB &bull; ${m.date_str}</div>
            </div>
            <div class="media-actions" style="display: flex; gap: 6px; flex-wrap: wrap;">
              <button class="btn btn-primary btn-sm" style="flex: 1; padding: 5px 8px; font-size: 0.78rem; background: #2563eb; justify-content: center;" onclick="openReplaceMediaModal('${m.name}', '${m.url}', ${m.is_video})" title="直接更换/替换此文件并全站发布">
                <span>🔄 更换${m.is_video ? '视频' : '图片'}</span>
              </button>
              <button class="btn btn-secondary btn-sm" style="padding: 5px 8px; font-size: 0.78rem;" onclick="copyToClipboard('${m.url}')" title="复制相对路径">📋 复制</button>
              <button class="btn btn-danger btn-sm" style="padding: 5px 8px; font-size: 0.78rem;" onclick="deleteMediaAsset('${m.name}')" title="删除文件">✕</button>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function filterMediaGrid() {
      const q = document.getElementById('mediaSearchInput').value.trim().toLowerCase();
      const type = document.getElementById('mediaTypeFilter').value;

      const filtered = MEDIA_LIST.filter(m => {
        const matchQ = !q || m.name.toLowerCase().includes(q);
        const matchType = (type === 'all') || (type === 'videos' && m.is_video) || (type === 'images' && !m.is_video);
        return matchQ && matchType;
      });
      renderMediaVaultGrid(filtered);
    }

    function triggerFileInputClick() {
      document.getElementById('mediaVaultFileInput').click();
    }

    async function handleMediaVaultUpload(inputEl) {
      if (!inputEl.files || inputEl.files.length === 0) return;
      const files = Array.from(inputEl.files);
      const token = localStorage.getItem('wideway_admin_token');

      showToast(`Uploading ${files.length} file(s)...`, 'info');

      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        try {
          const res = await fetch('/api/upload-media', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
          });
          const data = await res.json();
          if (data.status === 'success') {
            showToast(`Uploaded ${file.name}!`);
          } else {
            showToast(`Failed to upload ${file.name}: ${data.message}`, 'error');
          }
        } catch (err) {
          showToast(`Upload error for ${file.name}: ${err.message}`, 'error');
        }
      }

      inputEl.value = '';
      await loadMediaList();
    }

    async function deleteMediaAsset(filename) {
      if (!confirm(`Are you sure you want to permanently delete "${filename}" from images directory?`)) return;
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/delete-media', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ filename })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('Media file deleted');
          await loadMediaList();
        } else {
          showToast(data.message || 'Delete failed', 'error');
        }
      } catch (err) {
        showToast('Error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // IN-PLACE MEDIA REPLACEMENT LOGIC
    // ------------------------------------------------------------------------
    let CURRENT_REPLACE_TARGET_FILENAME = '';
    let CURRENT_REPLACE_FILE_OBJ = null;
    let CURRENT_REPLACE_FILE_BASE64 = '';

    let CURRENT_ORIGINAL_W = 0;
    let CURRENT_ORIGINAL_H = 0;
    let CURRENT_ORIGINAL_RATIO = '';
    let CURRENT_NEW_W = 0;
    let CURRENT_NEW_H = 0;
    let CURRENT_NEW_RATIO = '';

    function calculateRatioDesc(w, h) {
      if (!w || !h) return '-';
      const dec = w / h;
      if (Math.abs(dec - 16/9) < 0.05) return '16:9 (标准宽屏)';
      if (Math.abs(dec - 4/3) < 0.05) return '4:3 (标准画幅)';
      if (Math.abs(dec - 1) < 0.04) return '1:1 (正方形)';
      if (Math.abs(dec - 3/2) < 0.05) return '3:2 (单反比例)';
      if (Math.abs(dec - 9/16) < 0.05) return '9:16 (竖版短视频)';
      if (Math.abs(dec - 21/9) < 0.08) return '21:9 (超宽Banner)';
      return `${dec.toFixed(2)}:1 (${dec > 1 ? '横版' : '竖版'})`;
    }

    function handleOriginalImageLoaded(imgEl) {
      if (!imgEl || !imgEl.naturalWidth) return;
      CURRENT_ORIGINAL_W = imgEl.naturalWidth;
      CURRENT_ORIGINAL_H = imgEl.naturalHeight;
      CURRENT_ORIGINAL_RATIO = calculateRatioDesc(CURRENT_ORIGINAL_W, CURRENT_ORIGINAL_H);

      const dimText = `${CURRENT_ORIGINAL_W} × ${CURRENT_ORIGINAL_H} px`;
      document.getElementById('replaceCurrentDimText').textContent = dimText;
      document.getElementById('replaceCurrentRatioText').textContent = CURRENT_ORIGINAL_RATIO;
      document.getElementById('replaceCurrentDimBadge').textContent = dimText;
      evaluateImageMatch();
    }

    function handleOriginalVideoLoaded(vidEl) {
      if (!vidEl || !vidEl.videoWidth) return;
      CURRENT_ORIGINAL_W = vidEl.videoWidth;
      CURRENT_ORIGINAL_H = vidEl.videoHeight;
      CURRENT_ORIGINAL_RATIO = calculateRatioDesc(CURRENT_ORIGINAL_W, CURRENT_ORIGINAL_H);

      const dimText = `${CURRENT_ORIGINAL_W} × ${CURRENT_ORIGINAL_H} px`;
      document.getElementById('replaceCurrentDimText').textContent = dimText;
      document.getElementById('replaceCurrentRatioText').textContent = CURRENT_ORIGINAL_RATIO;
      document.getElementById('replaceCurrentDimBadge').textContent = dimText;
      evaluateImageMatch();
    }

    function handleNewImageLoaded(imgEl) {
      if (!imgEl || !imgEl.naturalWidth) return;
      CURRENT_NEW_W = imgEl.naturalWidth;
      CURRENT_NEW_H = imgEl.naturalHeight;
      CURRENT_NEW_RATIO = calculateRatioDesc(CURRENT_NEW_W, CURRENT_NEW_H);

      const dimText = `${CURRENT_NEW_W} × ${CURRENT_NEW_H} px`;
      document.getElementById('replaceNewDimText').textContent = dimText;
      document.getElementById('replaceNewRatioText').textContent = CURRENT_NEW_RATIO;
      document.getElementById('replaceNewDimBadge').textContent = dimText;
      evaluateImageMatch();
    }

    function handleNewVideoLoaded(vidEl) {
      if (!vidEl || !vidEl.videoWidth) return;
      CURRENT_NEW_W = vidEl.videoWidth;
      CURRENT_NEW_H = vidEl.videoHeight;
      CURRENT_NEW_RATIO = calculateRatioDesc(CURRENT_NEW_W, CURRENT_NEW_H);

      const dimText = `${CURRENT_NEW_W} × ${CURRENT_NEW_H} px`;
      document.getElementById('replaceNewDimText').textContent = dimText;
      document.getElementById('replaceNewRatioText').textContent = CURRENT_NEW_RATIO;
      document.getElementById('replaceNewDimBadge').textContent = dimText;
      evaluateImageMatch();
    }

    function evaluateImageMatch() {
      const box = document.getElementById('replaceMatchEvalBox');
      if (!box || !CURRENT_NEW_W || !CURRENT_ORIGINAL_W) {
        if (box) box.style.display = 'none';
        return;
      }

      box.style.display = 'block';
      const origDec = CURRENT_ORIGINAL_W / CURRENT_ORIGINAL_H;
      const newDec = CURRENT_NEW_W / CURRENT_NEW_H;
      const ratioDiff = Math.abs(origDec - newDec) / origDec;

      let matchHtml = '';
      if (ratioDiff < 0.06) {
        matchHtml += `<div style="color: #34d399; font-weight: 600;">✅ 比例完美匹配（与原图均为 ${CURRENT_ORIGINAL_RATIO}）</div>`;
        box.style.background = 'rgba(16, 185, 129, 0.15)';
        box.style.border = '1px solid rgba(16, 185, 129, 0.4)';
      } else {
        matchHtml += `<div style="color: #fde047; font-weight: 600;">⚠️ 比例差异提示：原图 [${CURRENT_ORIGINAL_RATIO}] vs 新图 [${CURRENT_NEW_RATIO}]</div><div style="color: #cbd5e1; font-size: 0.76rem; margin-top: 2px;">比例差异可能会改变页面该区域的排版高度或引起自动裁剪，若符合您的预期可直接替换。</div>`;
        box.style.background = 'rgba(234, 179, 8, 0.15)';
        box.style.border = '1px solid rgba(234, 179, 8, 0.4)';
      }

      box.innerHTML = matchHtml;
    }

    function showReplacementError(title, detail, suggestion) {
      const alertBox = document.getElementById('replaceModalErrorAlert');
      const detailEl = document.getElementById('replaceModalErrorDetail');
      const suggEl = document.getElementById('replaceModalErrorSuggestion');
      if (alertBox) {
        alertBox.style.display = 'block';
        detailEl.innerHTML = `<strong>${title}</strong><br><span style="color: #cbd5e1;">${detail}</span>`;
        suggEl.innerHTML = `💡 <strong>排查与解决建议：</strong>${suggestion}`;
        alertBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      showToast(title, 'error');
    }

    function openReplaceMediaModal(filename, currentUrl, isVideo = false) {
      CURRENT_REPLACE_TARGET_FILENAME = filename;
      CURRENT_REPLACE_FILE_OBJ = null;
      CURRENT_REPLACE_FILE_BASE64 = '';
      CURRENT_ORIGINAL_W = 0;
      CURRENT_ORIGINAL_H = 0;
      CURRENT_ORIGINAL_RATIO = '';
      CURRENT_NEW_W = 0;
      CURRENT_NEW_H = 0;
      CURRENT_NEW_RATIO = '';

      // Hide previous error alert
      document.getElementById('replaceModalErrorAlert').style.display = 'none';

      document.getElementById('replaceCurrentNameText').textContent = filename;
      document.getElementById('replaceCurrentPathText').textContent = currentUrl;
      document.getElementById('replaceCurrentDimText').textContent = '测量中...';
      document.getElementById('replaceCurrentRatioText').textContent = '分析中...';
      document.getElementById('replaceCurrentDimBadge').textContent = '测量中...';

      // Find file size and dimensions from MEDIA_LIST
      const foundMeta = MEDIA_LIST.find(m => m.name === filename);
      const fileSizeStr = foundMeta ? `${foundMeta.size_kb} KB (${foundMeta.ext || 'Media'})` : '已在服务器部署';
      document.getElementById('replaceCurrentSizeText').textContent = fileSizeStr;

      if (foundMeta && foundMeta.width && foundMeta.height) {
        CURRENT_ORIGINAL_W = foundMeta.width;
        CURRENT_ORIGINAL_H = foundMeta.height;
        CURRENT_ORIGINAL_RATIO = calculateRatioDesc(foundMeta.width, foundMeta.height);
        const dimStr = `${foundMeta.width} × ${foundMeta.height} px`;
        document.getElementById('replaceCurrentDimText').textContent = dimStr;
        document.getElementById('replaceCurrentRatioText').textContent = CURRENT_ORIGINAL_RATIO;
        document.getElementById('replaceCurrentDimBadge').textContent = dimStr;
      }

      const cacheBustUrl = currentUrl.includes('?') ? currentUrl : `${currentUrl}?v=${Date.now()}`;
      const curImg = document.getElementById('replaceCurrentPreviewImg');
      const curVid = document.getElementById('replaceCurrentPreviewVideo');

      if (isVideo) {
        curImg.style.display = 'none';
        curVid.style.display = 'block';
        curVid.src = cacheBustUrl;
      } else {
        curVid.style.display = 'none';
        curImg.style.display = 'block';
        curImg.src = cacheBustUrl;
        if (curImg.complete && curImg.naturalWidth > 0) {
          handleOriginalImageLoaded(curImg);
        }
      }

      // Reset new file preview
      document.getElementById('replaceUploadPrompt').style.display = 'block';
      document.getElementById('replaceNewPreviewContainer').style.display = 'none';
      document.getElementById('replaceNewPreviewImg').src = '';
      document.getElementById('replaceNewPreviewVideo').src = '';
      document.getElementById('replaceNewMetaInfo').style.display = 'none';
      document.getElementById('replaceNoFileHint').style.display = 'block';
      document.getElementById('replaceMatchEvalBox').style.display = 'none';
      
      const badge = document.getElementById('replaceNewStatusBadge');
      badge.style.background = 'rgba(234, 179, 8, 0.2)';
      badge.style.color = '#fde047';
      badge.textContent = '等待选择文件';
      
      const confirmBtn = document.getElementById('btnConfirmReplaceMedia');
      confirmBtn.disabled = true;
      confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';

      document.getElementById('replaceModalFileInput').value = '';
      document.getElementById('replaceMediaModal').classList.add('active');

      setupReplaceDropZone();
    }

    function closeReplaceMediaModal() {
      document.getElementById('replaceMediaModal').classList.remove('active');
    }

    function triggerReplaceModalFileSelect() {
      document.getElementById('replaceModalFileInput').click();
    }

    function handleReplaceModalFileChange(inputEl) {
      if (!inputEl.files || inputEl.files.length === 0) return;
      processReplacementFile(inputEl.files[0]);
    }

    function processReplacementFile(file) {
      document.getElementById('replaceModalErrorAlert').style.display = 'none';
      CURRENT_REPLACE_FILE_OBJ = file;
      const isVideo = file.type.startsWith('video/') || Boolean(file.name.match(/\.(mp4|webm)$/i));

      // Client-side file size check (50MB warning)
      const sizeMB = file.size / (1024 * 1024);
      if (sizeMB > 50) {
        showReplacementError(
          `文件过大警告 (${sizeMB.toFixed(1)} MB)`,
          '上传的文件超过了 50MB 推荐上限。过大的图片会导致海外客户访问变慢，甚至超出浏览器上传内存。',
          '请先使用图片压缩软件或在线压缩工具（如 TinyPNG）处理后再试。'
        );
      }

      document.getElementById('replaceUploadPrompt').style.display = 'none';
      const container = document.getElementById('replaceNewPreviewContainer');
      container.style.display = 'flex';
      const previewImg = document.getElementById('replaceNewPreviewImg');
      const previewVid = document.getElementById('replaceNewPreviewVideo');

      const reader = new FileReader();
      reader.onload = (e) => {
        CURRENT_REPLACE_FILE_BASE64 = e.target.result;
        if (isVideo) {
          previewImg.style.display = 'none';
          previewVid.style.display = 'block';
          previewVid.src = CURRENT_REPLACE_FILE_BASE64;
        } else {
          previewVid.style.display = 'none';
          previewImg.style.display = 'block';
          previewImg.src = CURRENT_REPLACE_FILE_BASE64;
        }
      };
      reader.readAsDataURL(file);

      const sizeStr = file.size < 1024 * 1024 
        ? `${(file.size / 1024).toFixed(1)} KB` 
        : `${(file.size / (1024 * 1024)).toFixed(2)} MB`;

      document.getElementById('replaceNewNameText').textContent = file.name;
      document.getElementById('replaceNewSizeText').textContent = `${sizeStr} (${file.type || 'Media'})`;
      document.getElementById('replaceNewDimText').textContent = '测量中...';
      document.getElementById('replaceNewRatioText').textContent = '分析中...';
      document.getElementById('replaceNewMetaInfo').style.display = 'block';
      document.getElementById('replaceNoFileHint').style.display = 'none';

      const badge = document.getElementById('replaceNewStatusBadge');
      badge.style.background = 'rgba(16, 185, 129, 0.2)';
      badge.style.color = '#34d399';
      badge.textContent = '新文件已就绪';

      const confirmBtn = document.getElementById('btnConfirmReplaceMedia');
      confirmBtn.disabled = false;
    }

    function setupReplaceDropZone() {
      const dropZone = document.getElementById('replaceDropZone');
      if (!dropZone || dropZone.dataset.setupDone) return;
      dropZone.dataset.setupDone = 'true';

      ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropZone.style.borderColor = 'var(--primary)';
          dropZone.style.background = 'rgba(37, 99, 235, 0.1)';
        }, false);
      });
      ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropZone.style.borderColor = 'var(--border)';
          dropZone.style.background = '';
        }, false);
      });
      dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
          processReplacementFile(files[0]);
        }
      }, false);
    }

    async function executeMediaReplacement() {
      if (!CURRENT_REPLACE_TARGET_FILENAME || !CURRENT_REPLACE_FILE_BASE64) {
        showReplacementError('未选择新文件', '请先在右侧区域选择或拖入要替换的新图片/视频。', '点击右侧虚线框浏览本地文件。');
        return;
      }

      const confirmBtn = document.getElementById('btnConfirmReplaceMedia');
      confirmBtn.disabled = true;
      confirmBtn.innerHTML = '<span>⏳ 正在替换并重新编译全站...</span>';

      const token = localStorage.getItem('wideway_admin_token');
      const sizeStr = CURRENT_REPLACE_FILE_OBJ 
        ? (CURRENT_REPLACE_FILE_OBJ.size < 1024 * 1024 
            ? (CURRENT_REPLACE_FILE_OBJ.size / 1024).toFixed(1) + ' KB' 
            : (CURRENT_REPLACE_FILE_OBJ.size / (1024*1024)).toFixed(2) + ' MB') 
        : '未知大小';

      try {
        const res = await fetch('/api/replace-media', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            target_filename: CURRENT_REPLACE_TARGET_FILENAME,
            file_base64: CURRENT_REPLACE_FILE_BASE64,
            new_filename: CURRENT_REPLACE_FILE_OBJ ? CURRENT_REPLACE_FILE_OBJ.name : ''
          })
        });

        if (res.status === 413) {
          showReplacementError(
            '上传失败：文件体积过大 (HTTP 413 Request Entity Too Large)',
            `所选文件体积为 ${sizeStr}，超出了服务器单次传输限制。`,
            '建议：使用 TinyPNG (https://tinypng.com) 压缩图片，或将图片转为 WebP/JPG 格式后再试。'
          );
          confirmBtn.disabled = false;
          confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';
          return;
        }

        if (res.status === 401) {
          showReplacementError(
            '上传失败：管理员会话失效 (HTTP 401 Unauthorized)',
            '您的管理认证凭据已过期或无效。',
            '建议：请退出登录并重新输入管理密码进入后台后再执行替换。'
          );
          confirmBtn.disabled = false;
          confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';
          return;
        }

        let data;
        const responseText = await res.text();
        try {
          data = JSON.parse(responseText);
        } catch (jsonErr) {
          showReplacementError(
            `上传失败：服务器未返回预期数据 (HTTP ${res.status} ${res.statusText})`,
            `服务器响应内容: ${responseText.slice(0, 300)}`,
            '建议：请检查服务器 Nginx 与 Python 后台服务运行状态。'
          );
          confirmBtn.disabled = false;
          confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';
          return;
        }

        if (res.ok && data.status === 'success') {
          showToast(`🎉 成功替换 ${CURRENT_REPLACE_TARGET_FILENAME} 并更新全站！`, 'info');
          closeReplaceMediaModal();
          
          // Bust image cache in entire document
          const cacheBuster = Date.now();
          document.querySelectorAll('img, video').forEach(el => {
            const src = el.getAttribute('src');
            if (src && src.includes(CURRENT_REPLACE_TARGET_FILENAME)) {
              const base = src.split('?')[0];
              el.setAttribute('src', `${base}?v=${cacheBuster}`);
            }
          });

          await loadMediaList();
          await loadContentDatabase();
        } else {
          showReplacementError(
            `替换失败 (错误码: ${res.status})`,
            data.message || '未知错误，服务器未返回具体原因。',
            '建议：请确认目标文件名格式正确（支持 JPG, PNG, WebP, SVG, MP4），且服务器磁盘有足够的写入权限。'
          );
          confirmBtn.disabled = false;
          confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';
        }
      } catch (err) {
        showReplacementError(
          '网络传输或连接错误 (Network Connection Error)',
          err.message || '与服务器通信中断，可能是上传大文件导致超时或网络波动。',
          '建议：请检查网络连接状态，或压缩图片减小上传数据量后再试。'
        );
        confirmBtn.disabled = false;
        confirmBtn.innerHTML = '<span>⚡️ 确认立即替换并全站发布</span>';
      }
    }

    // Media Picker Modal (For choosing asset into any input field)
    function openMediaPickerForInput(inputId) {
      CURRENT_PICKER_TARGET_INPUT_ID = inputId;
      renderMediaPickerGrid();
      document.getElementById('mediaPickerModal').classList.add('active');
    }

    function closeMediaPickerModal() {
      document.getElementById('mediaPickerModal').classList.remove('active');
    }

    function renderMediaPickerGrid(filtered = null) {
      const container = document.getElementById('mediaPickerGrid');
      const list = filtered || MEDIA_LIST;
      let html = '';
      list.forEach(m => {
        html += `
          <div class="media-card" style="cursor: pointer;" onclick="selectAssetIntoInput('${m.url}')">
            <div class="media-thumb-container">
              ${m.is_video ? `<video src="${m.url}"></video>` : `<img src="${m.url}" alt="${m.name}">`}
            </div>
            <div class="media-meta">
              <div class="media-name">${m.name}</div>
              <div class="media-size">${m.size_kb} KB</div>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function filterMediaPickerGrid() {
      const q = document.getElementById('mediaPickerSearch').value.trim().toLowerCase();
      const filtered = MEDIA_LIST.filter(m => !q || m.name.toLowerCase().includes(q));
      renderMediaPickerGrid(filtered);
    }

    function selectAssetIntoInput(url) {
      if (CURRENT_PICKER_TARGET_INPUT_ID) {
        const targetInput = document.getElementById(CURRENT_PICKER_TARGET_INPUT_ID);
        if (targetInput) {
          if (CURRENT_PICKER_TARGET_INPUT_ID === 'pEditGallery') {
            let existing = targetInput.value.split(/[\n,]/).map(s => s.trim()).filter(Boolean);
            if (!existing.includes(url)) {
              existing.push(url);
              targetInput.value = existing.join('\n');
            }
            renderGalleryThumbnails(targetInput.value);
          } else {
            targetInput.value = url;
            if (CURRENT_PICKER_TARGET_INPUT_ID === 'pEditImage') {
              updateMainImagePreview(url);
            } else if (CURRENT_PICKER_TARGET_INPUT_ID === 'pEditVideo') {
              const prevContainer = document.getElementById('pEditVideoPreviewContainer');
              const prevVideo = document.getElementById('pEditVideoPreview');
              if (prevContainer && prevVideo) {
                prevVideo.src = url;
                prevContainer.style.display = 'block';
              }
            } else if (CURRENT_PICKER_TARGET_INPUT_ID === 'vEditImageSrc') {
              const vImg = document.getElementById('vEditImagePreview');
              if (vImg) vImg.src = url;
            } else if (CURRENT_PICKER_TARGET_INPUT_ID === 'vEditVideoSrc') {
              if (typeof updateVisualVideoPreview === 'function') {
                updateVisualVideoPreview(url);
              }
            }
          }
          showToast(`Selected asset: ${url}`);
        }
      }
      closeMediaPickerModal();
    }

    function triggerPickerFileInput() {
      document.getElementById('mediaPickerFileInput').click();
    }

    async function handlePickerFileUpload(inputEl) {
      if (!inputEl.files || inputEl.files.length === 0) return;
      const file = inputEl.files[0];
      const token = localStorage.getItem('wideway_admin_token');
      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('/api/upload-media', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        });
        const data = await res.json();
        if (data.status === 'success' && data.url) {
          await loadMediaList();
          selectAssetIntoInput(data.url);
        } else {
          showToast(data.message || 'Upload failed', 'error');
        }
      } catch (err) {
        showToast('Upload error: ' + err.message, 'error');
      }
      inputEl.value = '';
    }

    // ------------------------------------------------------------------------
    // INQUIRIES & RFQ LEADS CRM
    // ------------------------------------------------------------------------
    async function loadInquiriesList() {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/inquiries', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          INQUIRIES_LIST = await res.json();
          renderInquiriesTable();
          renderDashboardInquiries();
        }
      } catch (e) {
        console.error('Failed to load inquiries:', e);
      }
    }

    function renderInquiriesTable() {
      const tbody = document.getElementById('inquiriesTableBody');
      if (INQUIRIES_LIST.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">No inquiries received yet. All new RFQ forms submitted from the website will appear here in real time.</td></tr>`;
        return;
      }

      let html = '';
      INQUIRIES_LIST.slice().reverse().forEach(item => {
        const st = (item.status || 'New').toLowerCase();
        html += `
          <tr>
            <td>
              <div style="font-family:var(--font-mono); font-weight:700; color:var(--primary); font-size:0.8rem;">${item.id || 'RFQ'}</div>
              <div style="font-size:0.75rem; color:var(--text-dim); margin-top:2px;">${item.timestamp || ''}</div>
            </td>
            <td>
              <div style="font-weight:700;">${escapeHtml(item.name || 'Anonymous Buyer')}</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">${escapeHtml(item.company || 'Private Buyer')} (${escapeHtml(item.country || 'Global')})</div>
            </td>
            <td>
              <div><a href="mailto:${item.email}" style="color:#60a5fa; text-decoration:none;">${escapeHtml(item.email || '')}</a></div>
              <div style="font-size:0.8rem; color:var(--success); margin-top:2px;">📞 ${escapeHtml(item.phone || 'N/A')}</div>
            </td>
            <td>
              <div style="font-weight:600;">${escapeHtml(item.product_interest || 'Footwear OEM')}</div>
              <div style="font-size:0.75rem; color:var(--text-muted);">Qty: ${escapeHtml(item.volume || '500+ pairs')}</div>
            </td>
            <td>
              <select class="input-field" style="padding:4px 8px; font-size:0.78rem; width:110px;" onchange="updateInquiryStatus('${item.id}', this.value)">
                <option value="New" ${st === 'new' ? 'selected' : ''}>New</option>
                <option value="Contacted" ${st === 'contacted' ? 'selected' : ''}>Contacted</option>
                <option value="Quoting" ${st === 'quoting' ? 'selected' : ''}>Quoting</option>
                <option value="Sample" ${st === 'sample' ? 'selected' : ''}>Sample Sent</option>
                <option value="Won" ${st === 'won' ? 'selected' : ''}>Deal Won</option>
              </select>
            </td>
            <td style="text-align: right;">
              ${item.phone ? `<a href="https://wa.me/${item.phone.replace(/[^0-9]/g, '')}" target="_blank" class="btn btn-success btn-sm" style="padding:4px 8px;" title="Chat on WhatsApp">💬 WA</a>` : ''}
              <a href="mailto:${item.email}?subject=RE: Footwear Sourcing Inquiry - Jinjiang Wideway (WIDEWAY GROUP)" class="btn btn-secondary btn-sm" style="padding:4px 8px;" title="Send Email">✉️ Email</a>
              <button class="btn btn-danger btn-sm" style="padding:4px 8px;" onclick="deleteInquiryRecord('${item.id}')">✕</button>
            </td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    }

    function renderDashboardInquiries() {
      const container = document.getElementById('dashInquiriesList');
      if (INQUIRIES_LIST.length === 0) {
        container.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:30px;">No buyer inquiries logged yet.</div>`;
        return;
      }
      let html = '';
      INQUIRIES_LIST.slice(-5).reverse().forEach(inq => {
        html += `
          <div style="background:rgba(15,23,42,0.6); border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700; font-size:0.88rem;">${escapeHtml(inq.name || 'Buyer')} (${escapeHtml(inq.company || 'B2B')})</div>
              <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(inq.product_interest || 'Footwear')} &bull; ${inq.timestamp || ''}</div>
            </div>
            <a href="mailto:${inq.email}" class="btn btn-secondary btn-sm" style="padding:4px 8px;">Reply</a>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    async function updateInquiryStatus(id, newStatus) {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/inquiry/update-status', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ id, status: newStatus })
        });
        if (res.ok) {
          showToast(`Inquiry status updated to ${newStatus}`);
          await loadInquiriesList();
        }
      } catch (e) {
        showToast('Failed to update status: ' + e.message, 'error');
      }
    }

    async function deleteInquiryRecord(id) {
      if (!confirm('Permanently delete this inquiry record?')) return;
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/inquiry/delete', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ id })
        });
        if (res.ok) {
          showToast('Inquiry deleted');
          await loadInquiriesList();
        }
      } catch (e) {
        showToast('Error: ' + e.message, 'error');
      }
    }

    function exportInquiriesCsv() {
      if (INQUIRIES_LIST.length === 0) {
        showToast('No inquiries to export', 'error');
        return;
      }
      let csv = 'Inquiry ID,Date & Time,Name,Company,Email,Phone/WhatsApp,Country,Product Interest,Volume,Message,Client IP\n';
      INQUIRIES_LIST.forEach(i => {
        csv += `"${i.id || ''}","${i.timestamp || ''}","${(i.name || '').replace(/"/g, '""')}","${(i.company || '').replace(/"/g, '""')}","${i.email || ''}","${i.phone || ''}","${i.country || ''}","${(i.product_interest || '').replace(/"/g, '""')}","${i.volume || ''}","${(i.message || '').replace(/"/g, '""')}","${i.client_ip || ''}"\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `wideway_inquiries_${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
    }

    // ------------------------------------------------------------------------
    // VISUAL LIVE STUDIO & IN-IFRAME INSPECTOR ENGINE
    // ------------------------------------------------------------------------
    let VISUAL_EDIT_MODE = true;
    let CURRENT_INSPECTED_ELEMENT = null;
    let ALL_PAGES_LIST = [];

    function setVisualEditMode(isEdit) {
      VISUAL_EDIT_MODE = isEdit;
      const btnEdit = document.getElementById('btnVisualEditMode');
      const btnBrowse = document.getElementById('btnVisualBrowseMode');
      const banner = document.getElementById('visualModeBanner');

      if (isEdit) {
        if (btnEdit) btnEdit.className = 'btn btn-primary btn-sm';
        if (btnBrowse) btnBrowse.className = 'btn btn-secondary btn-sm';
        if (banner) {
          banner.style.display = 'flex';
          banner.innerHTML = `<div>💡 <strong>Click-to-Edit Mode Active:</strong> Move your mouse over any text, heading, image, video, or button on the page below and click directly to edit, replace, or polish!</div><div style="font-size:0.75rem; color:#60a5fa;">Live DOM &amp; File Sync</div>`;
        }
      } else {
        if (btnEdit) btnEdit.className = 'btn btn-secondary btn-sm';
        if (btnBrowse) btnBrowse.className = 'btn btn-primary btn-sm';
        if (banner) {
          banner.style.display = 'flex';
          banner.innerHTML = `<div>🌐 <strong>Browse Mode Active:</strong> Clicking links navigates the website normally. Switch back to Click-to-Edit to modify content.</div>`;
        }
      }
    }

    function updateVisualIframeSrc() {
      const picker = document.getElementById('visualPagePicker');
      const iframe = document.getElementById('visualPreviewIframe');
      if (iframe && picker) {
        iframe.src = picker.value;
      }
    }

    function reloadVisualIframe() {
      const iframe = document.getElementById('visualPreviewIframe');
      if (iframe) {
        iframe.src = iframe.src;
        showToast('Preview refreshed', 'info');
      }
    }

    function openLiveVisualPage() {
      const picker = document.getElementById('visualPagePicker');
      const url = picker ? picker.value : '/';
      window.open(url, '_blank');
    }

    function setVisualDevice(width, btnEl) {
      document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');
      document.getElementById('visualPreviewIframe').style.width = width;
    }

    // Attach click-to-edit inspector to iframe content
    function attachVisualInspector(iframe) {
      try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        if (!doc) return;

        // Inject Inspector CSS
        let style = doc.getElementById('ww-inspector-css');
        if (!style) {
          style = doc.createElement('style');
          style.id = 'ww-inspector-css';
          style.textContent = `
            .ww-hover-target {
              outline: 2px dashed #2563eb !important;
              outline-offset: 3px !important;
              cursor: pointer !important;
              box-shadow: 0 0 12px rgba(37, 99, 235, 0.4) !important;
              transition: outline 0.1s ease !important;
            }
          `;
          doc.head.appendChild(style);
        }

        let hoveredEl = null;

        doc.addEventListener('mouseover', (e) => {
          if (!VISUAL_EDIT_MODE) return;
          const target = e.target.closest('h1, h2, h3, h4, h5, h6, p, span, a, button, img, video, li, td, th, blockquote, figcaption');
          if (!target) return;
          if (hoveredEl && hoveredEl !== target) {
            hoveredEl.classList.remove('ww-hover-target');
          }
          hoveredEl = target;
          target.classList.add('ww-hover-target');
        }, true);

        doc.addEventListener('mouseout', (e) => {
          if (!VISUAL_EDIT_MODE) return;
          if (hoveredEl) {
            hoveredEl.classList.remove('ww-hover-target');
            hoveredEl = null;
          }
        }, true);

        doc.addEventListener('click', (e) => {
          if (!VISUAL_EDIT_MODE) return;
          const target = e.target.closest('h1, h2, h3, h4, h5, h6, p, span, a, button, img, video, li, td, th, blockquote, figcaption');
          if (!target) return;

          e.preventDefault();
          e.stopPropagation();

          CURRENT_INSPECTED_ELEMENT = target;

          // Determine current page filename
          let pagePath = iframe.contentWindow.location.pathname;
          if (pagePath === '/' || pagePath === '') pagePath = 'index.html';
          if (pagePath.startsWith('/')) pagePath = pagePath.substring(1);
          if (!pagePath.endsWith('.html')) pagePath += '.html';

          const tagName = target.tagName.toUpperCase();
          const isImg = tagName === 'IMG';
          const isVideo = tagName === 'VIDEO';
          const isLink = tagName === 'A' || tagName === 'BUTTON';

          let editType = 'text';
          if (isImg) editType = 'image';
          else if (isVideo) editType = 'video';
          else if (isLink) editType = 'link';
          else if (tagName.startsWith('H')) editType = 'heading';

          const textContent = (target.innerText || target.textContent || '').trim();
          const imageSrc = isImg ? target.getAttribute('src') : '';
          const videoSrc = isVideo ? (target.getAttribute('src') || (target.querySelector('source') ? target.querySelector('source').getAttribute('src') : '')) : '';
          const linkHref = isLink ? (target.getAttribute('href') || '') : '';

          openVisualElementEditor({
            page: pagePath,
            type: editType,
            tagName: tagName,
            text: textContent,
            imageSrc: imageSrc,
            videoSrc: videoSrc,
            linkHref: linkHref,
            element: target
          });
        }, true);

      } catch (err) {
        console.warn('Cross-origin or iframe inspector load note:', err);
      }
    }

    function openVisualElementEditor(info) {
      document.getElementById('vEditPage').value = info.page;
      document.getElementById('vEditPageLabel').innerText = info.page;
      document.getElementById('vEditType').value = info.type;
      document.getElementById('vEditTypeBadge').innerText = info.tagName || info.type.toUpperCase();
      document.getElementById('vEditSelectorLabel').innerText = info.tagName;
      
      const textSec = document.getElementById('vEditTextSection');
      const imgSec = document.getElementById('vEditImageSection');
      const vidSec = document.getElementById('vEditVideoSection');
      const linkSec = document.getElementById('vEditLinkSection');

      // Reset visibility
      textSec.style.display = 'block';
      imgSec.style.display = 'none';
      vidSec.style.display = 'none';
      linkSec.style.display = 'none';

      // Set text content
      const textArea = document.getElementById('vEditTextContent');
      textArea.value = info.text || '';
      document.getElementById('vEditOldVal').value = info.text || '';
      document.getElementById('vEditAttr').value = '';
      updateVisualCharCount();

      if (info.type === 'image' || info.tagName === 'IMG') {
        imgSec.style.display = 'block';
        document.getElementById('vEditImageSrc').value = info.imageSrc || '';
        document.getElementById('vEditImagePreview').src = info.imageSrc || '';
        document.getElementById('vEditOldVal').value = info.imageSrc || '';
        document.getElementById('vEditAttr').value = 'src';
      } else if (info.type === 'video' || info.tagName === 'VIDEO') {
        vidSec.style.display = 'block';
        document.getElementById('vEditVideoSrc').value = info.videoSrc || '';
        updateVisualVideoPreview(info.videoSrc || '');
        document.getElementById('vEditOldVal').value = info.videoSrc || '';
        document.getElementById('vEditAttr').value = 'src';
      } else if (info.type === 'link' || info.tagName === 'A' || info.tagName === 'BUTTON') {
        linkSec.style.display = 'block';
        document.getElementById('vEditLinkText').value = info.text || '';
        document.getElementById('vEditLinkHref').value = info.linkHref || '';
      }

      document.getElementById('visualElementEditorModal').classList.add('active');
    }

    function closeVisualElementEditor() {
      document.getElementById('visualElementEditorModal').classList.remove('active');
      CURRENT_INSPECTED_ELEMENT = null;
    }

    function updateVisualCharCount() {
      const val = document.getElementById('vEditTextContent').value || '';
      document.getElementById('vEditCharCount').innerText = val.length;
    }

    function updateVisualVideoPreview(url) {
      const vContainer = document.getElementById('vEditVideoPreviewContainer');
      const vPreview = document.getElementById('vEditVideoPreview');
      if (url && url.trim() !== '') {
        vPreview.src = url;
        vContainer.style.display = 'block';
      } else {
        vContainer.style.display = 'none';
        vPreview.src = '';
      }
    }

    function triggerVisualImageUpload() {
      document.getElementById('visualImageFileInput').click();
    }

    async function handleVisualImageUpload(inputEl) {
      if (!inputEl.files || inputEl.files.length === 0) return;
      const file = inputEl.files[0];
      const formData = new FormData();
      formData.append('file', file);

      showToast(`Uploading ${file.name}...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/upload-media', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        });
        const data = await res.json();
        if (data.status === 'success' && data.url) {
          document.getElementById('vEditImageSrc').value = data.url;
          document.getElementById('vEditImagePreview').src = data.url;
          showToast('Image uploaded and set!');
        } else {
          showToast(data.message || 'Upload failed', 'error');
        }
      } catch (err) {
        showToast('Upload error: ' + err.message, 'error');
      }
    }

    function triggerVisualVideoUpload() {
      document.getElementById('visualVideoFileInput').click();
    }

    async function handleVisualVideoUpload(inputEl) {
      if (!inputEl.files || inputEl.files.length === 0) return;
      const file = inputEl.files[0];

      // 50MB check
      if (file.size > 50 * 1024 * 1024) {
        showToast(`❌ Video size (${(file.size/1024/1024).toFixed(1)}MB) exceeds 50MB limit!`, 'error');
        alert(`❌ 视频文件过大（${(file.size/1024/1024).toFixed(1)} MB），超过 50MB 限制！\\n请使用压缩工具或选择 50MB 以内的视频。`);
        inputEl.value = '';
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      showToast(`Uploading video ${(file.size/1024/1024).toFixed(1)}MB...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/upload-media', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        });
        const data = await res.json();
        if (data.status === 'success' && data.url) {
          document.getElementById('vEditVideoSrc').value = data.url;
          updateVisualVideoPreview(data.url);
          showToast('Video uploaded and attached!');
        } else {
          showToast(data.message || 'Upload failed', 'error');
        }
      } catch (err) {
        showToast('Video upload error: ' + err.message, 'error');
      }
    }

    async function polishVisualTextWithAi() {
      const text = document.getElementById('vEditTextContent').value;
      if (!text) {
        showToast('Text is empty', 'error');
        return;
      }
      showToast('Polishing with AI...', 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/edit-text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, prompt: 'Make it compelling, professional B2B export footwear copy' })
        });
        const data = await res.json();
        if (data.status === 'success' && data.text) {
          document.getElementById('vEditTextContent').value = data.text;
          updateVisualCharCount();
          showToast('Text polished with AI!');
        }
      } catch (err) {
        showToast('AI error: ' + err.message, 'error');
      }
    }

    async function translateVisualTextWithAi() {
      const lang = prompt('Translate to language code (e.g. es, de, ar, vi, fr, ru, pt, ja):', 'es');
      if (!lang) return;
      const text = document.getElementById('vEditTextContent').value;
      if (!text) return;
      showToast(`Translating to ${lang.toUpperCase()}...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, lang })
        });
        const data = await res.json();
        if (data.status === 'success' && data.text) {
          document.getElementById('vEditTextContent').value = data.text;
          updateVisualCharCount();
          showToast('Text translated!');
        }
      } catch (err) {
        showToast('Translation error: ' + err.message, 'error');
      }
    }

    async function saveVisualElementEdit() {
      const page = document.getElementById('vEditPage').value;
      const type = document.getElementById('vEditType').value;
      const oldVal = document.getElementById('vEditOldVal').value;
      const attr = document.getElementById('vEditAttr').value;

      let newVal = '';
      if (type === 'image') {
        newVal = document.getElementById('vEditImageSrc').value;
      } else if (type === 'video') {
        newVal = document.getElementById('vEditVideoSrc').value;
      } else if (type === 'link') {
        newVal = document.getElementById('vEditLinkHref').value;
        const linkText = document.getElementById('vEditLinkText').value;
        if (CURRENT_INSPECTED_ELEMENT) {
          CURRENT_INSPECTED_ELEMENT.innerText = linkText;
          CURRENT_INSPECTED_ELEMENT.setAttribute('href', newVal);
        }
      } else {
        newVal = document.getElementById('vEditTextContent').value;
      }

      if (!newVal && type !== 'video') {
        showToast('Content cannot be empty', 'error');
        return;
      }

      // Update live in iframe immediately
      if (CURRENT_INSPECTED_ELEMENT) {
        if (type === 'image') {
          CURRENT_INSPECTED_ELEMENT.setAttribute('src', newVal);
        } else if (type === 'video') {
          CURRENT_INSPECTED_ELEMENT.setAttribute('src', newVal);
          const srcTag = CURRENT_INSPECTED_ELEMENT.querySelector('source');
          if (srcTag) srcTag.setAttribute('src', newVal);
        } else if (type !== 'link') {
          CURRENT_INSPECTED_ELEMENT.innerText = newVal;
        }
      }

      showToast('Saving and publishing changes...', 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/visual-edit-element', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ page, type, old_val: oldVal, new_val: newVal, attr })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(`🎉 Saved & Published to ${page}!`);
          closeVisualElementEditor();
          await loadContentDatabase();
        } else {
          showToast(data.message || 'Save failed', 'error');
        }
      } catch (err) {
        showToast('Save error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // RAW HTML PAGE CODE EDITOR
    // ------------------------------------------------------------------------
    async function fetchPagesList() {
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/pages-list', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        if (data.status === 'success' && data.pages) {
          ALL_PAGES_LIST = data.pages;
          populateRawHtmlPageSelector();
        }
      } catch (e) {}
    }

    function populateRawHtmlPageSelector() {
      const sel = document.getElementById('rawHtmlPageSelector');
      if (!sel) return;
      sel.innerHTML = '';
      
      const groups = {};
      ALL_PAGES_LIST.forEach(p => {
        const cat = p.category || 'General';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(p);
      });

      for (const [catName, list] of Object.entries(groups)) {
        const grp = document.createElement('optgroup');
        grp.label = catName;
        list.forEach(p => {
          const opt = document.createElement('option');
          opt.value = p.filename;
          opt.innerText = `${p.filename} (${p.title})`;
          grp.appendChild(opt);
        });
        sel.appendChild(grp);
      }
    }

    async function openRawHtmlEditorModal(initialFilename = null) {
      if (ALL_PAGES_LIST.length === 0) {
        await fetchPagesList();
      }

      let targetFile = initialFilename;
      if (!targetFile) {
        const picker = document.getElementById('visualPagePicker');
        let pickerVal = picker ? picker.value : '/';
        if (pickerVal === '/' || pickerVal === '') {
          targetFile = 'index.html';
        } else {
          if (pickerVal.startsWith('/')) pickerVal = pickerVal.substring(1);
          targetFile = pickerVal.endsWith('.html') ? pickerVal : pickerVal + '.html';
        }
      }

      if (!targetFile.endsWith('.html')) targetFile += '.html';

      document.getElementById('rawHtmlEditorModal').classList.add('active');
      const sel = document.getElementById('rawHtmlPageSelector');
      if (sel) sel.value = targetFile;

      await loadRawHtmlPage(targetFile);
    }

    function closeRawHtmlEditorModal() {
      document.getElementById('rawHtmlEditorModal').classList.remove('active');
    }

    async function loadRawHtmlPage(filename) {
      document.getElementById('rawHtmlFilenameLabel').innerText = filename;
      const ta = document.getElementById('rawHtmlCodeTextarea');
      ta.value = 'Loading source code from server...';

      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch(`/api/page-content?file=${encodeURIComponent(filename)}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        if (data.status === 'success') {
          ta.value = data.html || '';
          updateRawHtmlStats();
        } else {
          ta.value = `<!-- Error: ${data.message} -->`;
        }
      } catch (err) {
        ta.value = `<!-- Error loading page: ${err.message} -->`;
      }
    }

    function updateRawHtmlStats() {
      const ta = document.getElementById('rawHtmlCodeTextarea');
      const val = ta.value || '';
      const lines = val.split('\\n').length;
      const sizeKb = (new Blob([val]).size / 1024).toFixed(1);
      document.getElementById('rawHtmlLineCount').innerText = `${lines} lines`;
      document.getElementById('rawHtmlFileSize').innerText = `${sizeKb} KB`;
    }

    function toggleRawCodeWrap() {
      const ta = document.getElementById('rawHtmlCodeTextarea');
      const btn = document.getElementById('btnCodeWrap');
      if (ta.style.whiteSpace === 'pre-wrap') {
        ta.style.whiteSpace = 'pre';
        btn.innerText = 'Wrap: OFF';
      } else {
        ta.style.whiteSpace = 'pre-wrap';
        btn.innerText = 'Wrap: ON';
      }
    }

    function searchInRawHtml(term) {
      if (!term) return;
      const ta = document.getElementById('rawHtmlCodeTextarea');
      const idx = ta.value.toLowerCase().indexOf(term.toLowerCase());
      if (idx !== -1) {
        ta.focus();
        ta.setSelectionRange(idx, idx + term.length);
      }
    }

    async function saveRawHtmlPage() {
      const filename = document.getElementById('rawHtmlFilenameLabel').innerText;
      const html = document.getElementById('rawHtmlCodeTextarea').value;

      if (!html) {
        showToast('HTML content cannot be empty', 'error');
        return;
      }

      showToast(`Saving ${filename} and recompiling site...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/save-page', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ filename, html, rebuild: true })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(`✅ ${filename} saved & recompiled successfully!`);
          reloadVisualIframe();
          await loadContentDatabase();
        } else {
          showToast(data.message || 'Save failed', 'error');
        }
      } catch (err) {
        showToast('Save error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // AI MARKETING STUDIO & HELPERS
    // ------------------------------------------------------------------------
    async function polishFieldWithAi(fieldId) {
      const inputEl = document.getElementById(fieldId);
      if (!inputEl) return;
      const text = inputEl.value;
      if (!text) {
        showToast('Field is empty', 'error');
        return;
      }
      showToast('Polishing with AI...', 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/edit-text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, prompt: 'Make it technical, professional, and optimized for footwear manufacturing export' })
        });
        const data = await res.json();
        if (data.status === 'success' && data.text) {
          inputEl.value = data.text;
          showToast('Field polished with AI!');
        }
      } catch (err) {
        showToast('AI error: ' + err.message, 'error');
      }
    }

    async function translateFieldWithAi(fieldId) {
      const lang = prompt('Translate to language code (e.g. es, de, ar, vi, fr, ru, pt, ja):', 'es');
      if (!lang) return;
      const inputEl = document.getElementById(fieldId);
      if (!inputEl) return;
      const text = inputEl.value;
      if (!text) return;
      showToast(`Translating to ${lang.toUpperCase()}...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, lang })
        });
        const data = await res.json();
        if (data.status === 'success' && data.text) {
          inputEl.value = data.text;
          showToast('Field translated!');
        }
      } catch (err) {
        showToast('Translation error: ' + err.message, 'error');
      }
    }

    async function runAiPolish() {
      const text = document.getElementById('aiInputText').value;
      const prompt = document.getElementById('aiGoalSelect').value;
      if (!text) return;
      showToast('Generating AI copy...', 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/edit-text', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, prompt })
        });
        const data = await res.json();
        if (data.status === 'success') {
          document.getElementById('aiOutputText').value = data.text;
          showToast('AI optimization ready!');
        }
      } catch (err) {
        showToast('AI error: ' + err.message, 'error');
      }
    }

    async function runAiTranslate() {
      const text = document.getElementById('translateInputText').value;
      const lang = document.getElementById('translateLangSelect').value;
      if (!text) return;
      showToast(`Translating to ${lang}...`, 'info');
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/ai/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ text, lang })
        });
        const data = await res.json();
        if (data.status === 'success') {
          document.getElementById('translateOutputText').value = data.text;
          showToast('Translation completed!');
        }
      } catch (err) {
        showToast('Translate error: ' + err.message, 'error');
      }
    }

    // ------------------------------------------------------------------------
    // BUILD, DEPLOY & SAVE CORE
    // ------------------------------------------------------------------------
    async function saveContentAndRebuild() {
      if (!SITE_DATA) return;
      const token = localStorage.getItem('wideway_admin_token');
      showToast('Saving database & compiling static site...', 'info');
      try {
        const res = await fetch('/api/save-content', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(SITE_DATA)
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('Site compiled successfully! ✨');
          reloadVisualIframe();
        } else {
          showToast(data.message || 'Save error', 'error');
        }
      } catch (err) {
        showToast('Save request error: ' + err.message, 'error');
      }
    }

    async function triggerRebuildSite() {
      await saveContentAndRebuild();
    }

    function triggerProductionDeployModal() {
      document.getElementById('deployConsoleModal').classList.add('active');
      document.getElementById('deployConsoleOutput').textContent = 'Initiating production bundle build and deployment to 43.130.32.54:2222...\n';
      triggerProductionDeploy();
    }

    function closeDeployConsoleModal() {
      document.getElementById('deployConsoleModal').classList.remove('active');
    }

    async function triggerProductionDeploy() {
      const consoleEl = document.getElementById('deployConsoleOutput');
      consoleEl.textContent = '🚀 1. Running site rebuild with fresh database content...\n📦 2. Packing web assets into dist_bundle.tar.gz...\n🔑 3. Connecting to production server 43.130.32.54:2222 via SSH/SFTP...\n';
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/deploy-production', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await res.json();
        consoleEl.textContent += `\n${data.log || ''}\n\n${data.status === 'success' ? '🎉 DEPLOYMENT SUCCESSFUL! All production pages are live.' : '❌ DEPLOYMENT FAILED.'}`;
        if (data.status === 'success') {
          showToast('Production deployment complete!');
        } else {
          showToast('Deployment failed', 'error');
        }
      } catch (err) {
        consoleEl.textContent += `\nError: ${err.message}`;
        showToast('Deploy error: ' + err.message, 'error');
      }
    }

    function downloadContentBackup() {
      window.location.href = '/api/backup-download';
      showToast('Downloading site content backup JSON...');
    }

    async function handleChangePasswordSubmit(e) {
      e.preventDefault();
      const current_password = document.getElementById('pwCurrent').value;
      const new_password = document.getElementById('pwNew').value;
      const token = localStorage.getItem('wideway_admin_token');
      try {
        const res = await fetch('/api/change-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ current_password, new_password })
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('Master password updated successfully!');
          document.getElementById('pwCurrent').value = '';
          document.getElementById('pwNew').value = '';
        } else {
          showToast(data.message || 'Incorrect password', 'error');
        }
      } catch (err) {
        showToast('Password change error: ' + err.message, 'error');
      }
    }

    // Utility Helpers
    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied: ${text}`);
      });
    }

    function handleQuickSearch(e) {
      const q = e.target.value.trim();
      if (e.key === 'Enter' && q) {
        switchTab('global_search');
        document.getElementById('globalSearchInput').value = q;
        executeGlobalSearch();
      }
    }

    // Keyboard Shortcuts (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('quickSearchInput');
        if (searchInput) searchInput.focus();
      }
    });
  </script>
</body>
</html>
'''

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html_content)

print(f"Successfully generated master admin.html ({len(admin_html_content)} bytes)")
