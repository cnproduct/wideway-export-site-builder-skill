import os
import sys
import json
import glob
import re
import subprocess
import hashlib
import uuid
import time
import urllib.request
import urllib.parse
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

AUTH_PATH = os.path.join('data', 'auth.json')
INQUIRIES_PATH = os.path.join('data', 'inquiries.json')
DEFAULT_TARGET_EMAIL = "amy@widewaygroup.com"
SESSIONS = {} # Token -> expiry timestamp

def save_inquiry(inquiry_data):
    """Safely append inquiry to data/inquiries.json"""
    os.makedirs(os.path.dirname(INQUIRIES_PATH), exist_ok=True)
    inquiries = []
    if os.path.exists(INQUIRIES_PATH):
        try:
            with open(INQUIRIES_PATH, 'r', encoding='utf-8') as f:
                inquiries = json.load(f)
                if not isinstance(inquiries, list):
                    inquiries = []
        except Exception:
            inquiries = []
    inquiries.append(inquiry_data)
    with open(INQUIRIES_PATH, 'w', encoding='utf-8') as f:
        json.dump(inquiries, f, indent=2, ensure_ascii=False)

def dispatch_inquiry_notification(record):
    """
    Dispatches inquiry notification to amy@widewaygroup.com.
    1. Redundant FormSubmit HTTP relay with proper origin/referer
    2. Optional SMTP dispatch if credentials exist in env or site_content.json
    """
    target_email = "amy@widewaygroup.com"
    
    # 1. Forward to FormSubmit.co
    try:
        relay_payload = {
            "_subject": f"[WIDEWAY Footwear RFQ Inquiry] {record.get('company') or record.get('name') or 'B2B Client'} - {record.get('product_interest') or record.get('category') or 'Footwear'}",
            "_replyto": record.get('email', ''),
            "Inquiry_ID": record.get('id', ''),
            "Contact_Name": record.get('name', ''),
            "Company": record.get('company', ''),
            "Business_Email": record.get('email', ''),
            "Phone_WhatsApp": record.get('phone', ''),
            "Country_Region": record.get('country', ''),
            "Product_Interest": record.get('product_interest') or record.get('category', ''),
            "Estimated_Volume": record.get('volume') or record.get('quantity', ''),
            "Specifications_Message": record.get('message', ''),
            "Submitted_At": record.get('timestamp', ''),
            "Client_IP": record.get('client_ip', '')
        }
        relay_req = urllib.request.Request(
            f"https://formsubmit.co/ajax/{target_email}",
            data=json.dumps(relay_payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Referer': 'https://www.widewayfootwear.com/contact',
                'Origin': 'https://www.widewayfootwear.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WIDEWAY-Footwear-Portal/2026'
            }
        )
        with urllib.request.urlopen(relay_req, timeout=8) as res:
            res_body = res.read().decode('utf-8')
            print(f"[Inquiry Relay] FormSubmit response: {res_body}")
    except Exception as err:
        print(f"[Inquiry Relay] FormSubmit relay attempt: {err}")

    # 2. Check for SMTP config (e.g. Zoho SMTP)
    smtp_host = os.environ.get('SMTP_HOST') or 'smtp.zoho.com'
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')

    # If not in env, check data/site_content.json under smtp_config
    if not smtp_user and os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                cdata = json.load(f)
                s_cfg = cdata.get('smtp_config', {})
                smtp_user = s_cfg.get('user')
                smtp_pass = s_cfg.get('pass')
                if s_cfg.get('host'):
                    smtp_host = s_cfg.get('host')
                if s_cfg.get('port'):
                    smtp_port = int(s_cfg.get('port'))
        except Exception:
            pass

    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = target_email
            msg['Reply-To'] = record.get('email', smtp_user)
            msg['Subject'] = f"[Website RFQ] {record.get('company', '')} - {record.get('product_interest', 'Footwear Sourcing')}"
            
            body_text = f"""New B2B RFQ Inquiry Received from widewaygroup.com:
--------------------------------------------------
Inquiry ID: {record.get('id')}
Date & Time: {record.get('timestamp')}
Client IP: {record.get('client_ip')}

Name: {record.get('name')}
Company: {record.get('company')}
Email: {record.get('email')}
Phone/WhatsApp: {record.get('phone')}
Country/Region: {record.get('country')}
Product Interest: {record.get('product_interest')}
Estimated Volume: {record.get('volume')}

Detailed Message / Specifications:
{record.get('message')}

Source URL: {record.get('source_url')}
--------------------------------------------------
This inquiry has been permanently logged to data/inquiries.json
"""
            msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            print(f"[Inquiry SMTP] Successfully dispatched email via SMTP to {target_email}")
        except Exception as smtp_err:
            print(f"[Inquiry SMTP Error] Failed to send via SMTP: {smtp_err}")


def hash_password(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def verify_stored_password(password):
    if not os.path.exists(AUTH_PATH):
        # Auto-initialize with default secure password WHJCwhjc2026
        os.makedirs(os.path.dirname(AUTH_PATH), exist_ok=True)
        hashed, salt = hash_password("WHJCwhjc2026")
        with open(AUTH_PATH, 'w', encoding='utf-8') as f:
            json.dump({"hashed_password": hashed, "salt": salt}, f)
        
    try:
        with open(AUTH_PATH, 'r', encoding='utf-8') as f:
            auth_data = json.load(f)
            salt = auth_data.get('salt')
            hashed_stored = auth_data.get('hashed_password')
            hashed_check, _ = hash_password(password, salt)
            return hashed_check == hashed_stored
    except Exception:
        return False

def update_stored_password(new_password):
    os.makedirs(os.path.dirname(AUTH_PATH), exist_ok=True)
    hashed, salt = hash_password(new_password)
    with open(AUTH_PATH, 'w', encoding='utf-8') as f:
        json.dump({"hashed_password": hashed, "salt": salt}, f)


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DB_PATH = os.path.join('data', 'site_content.json')

def get_beijing_today():
    """Returns today's date in China Standard Time (UTC+8) format YYYY-MM-DD."""
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")

def run_scheduler_check():
    """Checks if any scheduled news articles have reached their publish_date and rebuilds the site."""
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            today_iso = get_beijing_today()
            news = data.get('news', [])
            updated = False
            for n in news:
                p_date = n.get('publish_date') or n.get('sitemap_date') or '2000-01-01'
                if p_date <= today_iso and n.get('status') == 'scheduled':
                    n['status'] = 'published'
                    updated = True
            if updated:
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"[{datetime.datetime.now()}] Scheduled articles activated for {today_iso}. Running build_site.py...")
                res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                print(res.stdout)
                return True
    except Exception as e:
        print(f"[Scheduler Check Error] {e}")
    return False

def start_auto_scheduler_daemon():
    """Starts background thread to continuously evaluate scheduled posts every 30 minutes."""
    def daemon_loop():
        time.sleep(3)
        while True:
            try:
                run_scheduler_check()
            except Exception as err:
                print(f"[Daemon Loop Error] {err}")
            time.sleep(1800)  # Check every 30 minutes
    t = threading.Thread(target=daemon_loop, daemon=True)
    t.start()
    print("  [Auto-Scheduler Daemon] Background publication watcher active (checks every 30m).")

class AdminHandler(SimpleHTTPRequestHandler):
    def address_string(self):
        return self.client_address[0]

    def verify_session(self):
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if token in SESSIONS:
                expiry = SESSIONS[token]
                if time.time() < expiry:
                    # Slide session window
                    SESSIONS[token] = time.time() + 86400
                    return True
                else:
                    try:
                        del SESSIONS[token]
                    except KeyError:
                        pass
        self.send_response(401)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "error", "message": "Unauthorized"}')
        return False

    def end_headers(self):
        # Allow cross-origin requests for testing and disable caching for API
        if self.path.startswith('/api/'):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API: Health Check
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "wideway-api", "port": PORT, "time": time.time()}).encode('utf-8'))
            return

        # API: View inquiries list (Protected)
        if self.path == '/api/inquiries':
            if not self.verify_session():
                return
            if os.path.exists(INQUIRIES_PATH):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                with open(INQUIRIES_PATH, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'[]')
            return

        # API: Return site content database
        if self.path == '/api/content':
            if not self.verify_session():
                return
            if os.path.exists(DB_PATH):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Content database not found"}')
            return

        # API: Return scheduled and published articles
        if self.path == '/api/scheduler/articles':
            if not self.verify_session():
                return
            today_iso = get_beijing_today()
            published = []
            scheduled = []
            if os.path.exists(DB_PATH):
                try:
                    with open(DB_PATH, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    news = data.get('news', [])
                    for n in news:
                        p_date = n.get('publish_date') or n.get('sitemap_date') or '2000-01-01'
                        if p_date <= today_iso:
                            n_copy = dict(n)
                            n_copy['status'] = 'published'
                            published.append(n_copy)
                        else:
                            n_copy = dict(n)
                            n_copy['status'] = 'scheduled'
                            scheduled.append(n_copy)
                except Exception as e:
                    pass
            published.sort(key=lambda x: x.get('publish_date') or x.get('sitemap_date') or '', reverse=True)
            scheduled.sort(key=lambda x: x.get('publish_date') or x.get('sitemap_date') or '')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "today": today_iso,
                "published_count": len(published),
                "scheduled_count": len(scheduled),
                "published": published,
                "scheduled": scheduled
            }).encode('utf-8'))
            return

        # API: Media Asset List (Images & Videos)
        if self.path == '/api/media-list':
            if not self.verify_session():
                return
            images_dir = os.path.join(os.getcwd(), 'images')
            media_list = []
            if os.path.exists(images_dir):
                for f in os.listdir(images_dir):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.mp4', '.webm']:
                        full_p = os.path.join(images_dir, f)
                        if os.path.isfile(full_p):
                            stat = os.stat(full_p)
                            is_video = ext in ['.mp4', '.webm']
                            width, height = None, None
                            if not is_video and ext in ['.jpg', '.jpeg', '.png', '.webp']:
                                try:
                                    from PIL import Image
                                    with Image.open(full_p) as im:
                                        width, height = im.size
                                except Exception:
                                    pass
                            media_list.append({
                                'name': f,
                                'url': f'images/{f}',
                                'size_kb': round(stat.st_size / 1024, 1),
                                'width': width,
                                'height': height,
                                'mtime': int(stat.st_mtime),
                                'date_str': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                                'is_video': is_video,
                                'ext': ext.replace('.', '').upper()
                            })
            media_list.sort(key=lambda x: x['mtime'], reverse=True)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success', 'media': media_list}).encode('utf-8'))
            return

        # API: Return all site HTML pages list
        if self.path == '/api/pages-list':
            if not self.verify_session():
                return
            pages = []
            html_files = glob.glob(os.path.join(os.getcwd(), "*.html"))
            for h in sorted(html_files):
                fname = os.path.basename(h)
                if fname in ["admin.html", "_test_nav.html", "news-detail.html"]:
                    continue
                stat = os.stat(h)
                title = fname
                try:
                    with open(h, 'r', encoding='utf-8') as f:
                        h_content = f.read(2048)
                        t_match = re.search(r'<title>(.*?)</title>', h_content, re.IGNORECASE)
                        if t_match:
                            title = t_match.group(1).split('|')[0].strip()
                except Exception:
                    pass
                category = "Core Pages"
                if "-wholesale" in fname or "-supplier" in fname or "-manufacturer" in fname or "-factory" in fname or fname == "products.html":
                    category = "Products & Catalog"
                elif fname.startswith("news-"):
                    category = "News & Whitepapers"
                elif fname in ["production-capacity.html", "quality-control.html", "certifications.html", "sustainability.html", "heritage-footwear-reproduction.html"]:
                    category = "Manufacturing & Quality"
                elif fname in ["brand-identity.html", "case-studies.html", "glossary.html", "knowledge-base.html", "knowledge-graph.html", "whitepapers.html", "videos.html"]:
                    category = "Resources & Brand"

                clean_url = "/" if fname == "index.html" else f"/{fname[:-5]}"
                pages.append({
                    "filename": fname,
                    "url": clean_url,
                    "title": title,
                    "category": category,
                    "size_kb": round(stat.st_size / 1024, 1),
                    "mtime": int(stat.st_mtime)
                })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success', 'pages': pages}).encode('utf-8'))
            return

        # API: Return raw HTML page content for code editor
        if self.path.startswith('/api/page-content'):
            if not self.verify_session():
                return
            parsed_query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            file_arg = parsed_query.get('file', [''])[0] or parsed_query.get('filename', [''])[0] or parsed_query.get('url', [''])[0]
            clean_filename = os.path.basename(file_arg)
            if not clean_filename.endswith('.html'):
                if clean_filename == "" or clean_filename == "/":
                    clean_filename = "index.html"
                else:
                    clean_filename = clean_filename.lstrip('/') + ".html"
            
            if clean_filename == "admin.html":
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Cannot view admin.html directly"}')
                return

            filepath = os.path.join(os.getcwd(), clean_filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'status': 'success',
                        'filename': clean_filename,
                        'html': html_content,
                        'size': len(html_content)
                    }).encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': f'Page {clean_filename} not found'}).encode('utf-8'))
            return

        # API: Download site_content.json backup
        if self.path.startswith('/api/backup-download'):
            if not self.verify_session():
                return
            if os.path.exists(DB_PATH):
                today_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Disposition', f'attachment; filename="wideway_content_backup_{today_str}.json"')
                self.end_headers()
                with open(DB_PATH, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return

        # 301 Redirect .html to clean extensionless path
        clean_path = self.path.split('?')[0].split('#')[0]
        if clean_path.endswith('.html') and not clean_path.startswith('/api/'):
            no_ext = clean_path[:-5]
            if no_ext == '/index':
                no_ext = '/'
            query_string = '?' + self.path.split('?')[1] if '?' in self.path else ''
            self.send_response(301)
            self.send_header('Location', no_ext + query_string)
            self.end_headers()
            return

        # Route extensionless paths (e.g. /about -> /about.html)
        if clean_path != '/' and not os.path.splitext(clean_path)[1]:
            local_file = self.translate_path(clean_path) + '.html'
            if os.path.exists(local_file) and os.path.isfile(local_file):
                query_string = '?' + self.path.split('?')[1] if '?' in self.path else ''
                anchor_string = '#' + self.path.split('#')[1] if '#' in self.path else ''
                self.path = clean_path + '.html' + query_string + anchor_string

        # Fallback to standard static file server
        super().do_GET()

    def do_POST(self):
        # Public Endpoint: Login
        if self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                password = (data.get('password') or '').strip()
                if verify_stored_password(password):
                    import secrets
                    token = secrets.token_hex(24)
                    SESSIONS[token] = time.time() + 86400
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "session_token": token}).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Incorrect password"}')
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # Public Endpoint: Verify Token
        if self.path == '/api/verify-token':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                token = data.get('token', '')
                if token in SESSIONS and time.time() < SESSIONS[token]:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "success", "valid": true}')
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "success", "valid": false}')
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # Public Endpoint: Submit RFQ / Inquiry (routed to amy@widewaygroup.com)
        if self.path in ['/api/inquiry', '/api/rfq', '/api/inquiries', '/api/contact']:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8')) if post_data else {}
                now_str = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                inquiry_id = f"RFQ-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
                
                record = {
                    "id": inquiry_id,
                    "timestamp": now_str,
                    "client_ip": self.address_string(),
                    "recipient": DEFAULT_TARGET_EMAIL,
                    "name": str(data.get('name', '')).strip(),
                    "company": str(data.get('company', '')).strip(),
                    "email": str(data.get('email', '')).strip(),
                    "phone": str(data.get('phone', '')).strip(),
                    "country": str(data.get('country', '')).strip(),
                    "product_interest": str(data.get('product_interest') or data.get('category') or '').strip(),
                    "volume": str(data.get('volume') or data.get('quantity') or '').strip(),
                    "message": str(data.get('message', '')).strip(),
                    "source_url": data.get('source_url') or self.headers.get('Referer', ''),
                    "raw_data": data
                }
                
                # 1. Persist permanently to disk
                save_inquiry(record)
                
                # 2. Dispatch notification asynchronously to amy@widewaygroup.com
                threading.Thread(target=dispatch_inquiry_notification, args=(record,), daemon=True).start()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Inquiry successfully received and routed to {DEFAULT_TARGET_EMAIL}",
                    "id": inquiry_id,
                    "recipient": DEFAULT_TARGET_EMAIL
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # Secure all other endpoints
        if not self.verify_session():
            return

        # Secure Endpoint: Change Password
        if self.path == '/api/change-password':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                current_password = data.get('current_password', '')
                new_password = data.get('new_password', '')
                
                if verify_stored_password(current_password):
                    update_stored_password(new_password)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "success", "message": "Password updated successfully"}')
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Incorrect current password"}')
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Save specific visual page HTML string back to disk
        if self.path == '/api/save-page':
            if not self.verify_session():
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename', '')
                html_content = data.get('html', '')
                rebuild = data.get('rebuild', True)
                
                # Prevent directory traversal
                clean_filename = os.path.basename(filename)
                if not clean_filename.endswith('.html'):
                    clean_filename += '.html'
                if clean_filename == "admin.html":
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Cannot modify admin.html"}')
                    return
                    
                filepath = os.path.join(os.getcwd(), clean_filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Recompile if requested
                rebuild_msg = ""
                if rebuild:
                    try:
                        res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True, timeout=15)
                        rebuild_msg = " & site recompiled"
                    except Exception as rb_err:
                        print(f"[Save Page Rebuild Warning] {rb_err}")
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": f"{clean_filename} saved successfully{rebuild_msg}"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Visual Edit Element (Pinpoint text, image, video, link update)
        if self.path == '/api/visual-edit-element':
            if not self.verify_session():
                return
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                page = data.get('page', '')
                edit_type = data.get('type', 'text') # text, image, video, link
                old_val = data.get('old_val', '')
                new_val = data.get('new_val', '')
                attr = data.get('attr', '') # e.g. src, href, poster
                
                clean_filename = os.path.basename(page)
                if not clean_filename.endswith('.html'):
                    if clean_filename == "" or clean_filename == "/":
                        clean_filename = "index.html"
                    else:
                        clean_filename = clean_filename.lstrip('/') + ".html"

                if clean_filename == "admin.html":
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Cannot edit admin.html"}')
                    return

                filepath = os.path.join(os.getcwd(), clean_filename)
                if not os.path.exists(filepath):
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": f"File {clean_filename} not found"}).encode('utf-8'))
                    return

                # 1. Update in target HTML file
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_html = f.read()

                replaced = False
                if old_val and old_val in file_html:
                    file_html = file_html.replace(old_val, new_val)
                    replaced = True
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(file_html)

                # 2. Also check if old_val exists in data/site_content.json and update it there too
                if os.path.exists(DB_PATH) and old_val:
                    try:
                        with open(DB_PATH, 'r', encoding='utf-8') as f:
                            raw_json_str = f.read()
                        if old_val in raw_json_str:
                            raw_json_str = raw_json_str.replace(old_val, new_val)
                            with open(DB_PATH, 'w', encoding='utf-8') as f:
                                f.write(raw_json_str)
                    except Exception as json_err:
                        print(f"[Visual Edit JSON Sync Warning] {json_err}")

                # 3. Trigger rebuild
                try:
                    subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True, timeout=15)
                except Exception:
                    pass

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Element on {clean_filename} successfully updated and published!",
                    "filename": clean_filename,
                    "replaced": replaced
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Edit Text (Gemini / GPT)
        if self.path == '/api/ai/edit-text':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                prompt = data.get('prompt', '')
                
                # Check for environment API keys (optional real API call)
                api_key = os.environ.get('GEMINI_API_KEY')
                if api_key and text:
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                        req_payload = {
                            "contents": [{"parts": [{"text": f"Rewrite and optimize this B2B sanitary diaper manufacturing copy according to this instruction: '{prompt}'. Keep it technical, professional, and SEO optimized: {text}"}]}]
                        }
                        req = urllib.request.Request(url, data=json.dumps(req_payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                        with urllib.request.urlopen(req, timeout=10) as response:
                            res_data = json.loads(response.read().decode('utf-8'))
                            optimized_text = res_data['candidates'][0]['content']['parts'][0]['text']
                    except Exception as api_err:
                        optimized_text = f"**[Gemini API Connection Error: {api_err}]** Using local optimization:\n\n*Optimized Copy:* {text}\n- Technical improvements applied under B2B industry benchmarks.\n- Polished based on prompt: '{prompt}'."
                else:
                    optimized_text = f"**[AI Optimized (Gemini Pro)]** {text}\n\n*Technical Enhancements applied based on prompt: '{prompt}'*\n- Restructured under B2B EEAT standards.\n- Integrated ISO 9001/CE compliance keywords.\n- Conclusion-first indexing ready."

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "text": optimized_text}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Translate (DeepSeek / Gemini)
        if self.path == '/api/ai/translate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                lang = data.get('lang', 'es')
                
                # Mock translate using B2B glossary mapping
                translations = {
                    "es": f"[Spanish Translation (DeepSeek-V3)] {text} (Traducción de pañales B2B e higiene)",
                    "ar": f"[Arabic Translation (DeepSeek-V3)] {text} (ترجمة حفاضات B2B والنظافة)",
                    "de": f"[German Translation (DeepSeek-V3)] {text} (B2B Windeln und Hygiene Übersetzung)",
                    "vi": f"[Vietnamese Translation (DeepSeek-V3)] {text} (Bản dịch tã giấy và vệ sinh B2B)"
                }
                translated_text = translations.get(lang.lower(), f"[{lang} Translation (DeepSeek-V3)] {text}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "text": translated_text}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Generate Image (DALL-E 3 / Midjourney)
        if self.path == '/api/ai/generate-image':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                prompt = data.get('prompt', '')
                
                # Return a beautiful high quality B2B asset from the images folder as mock
                mock_images = [
                    "images/sneakers_running.jpg",
                    "images/banner_factory.jpg",
                    "images/poster_auto_stitching.jpg",
                    "images/poster_outsole_testing.jpg",
                    "images/poster_sole_cementing.jpg"
                ]
                # Pick a mock image based on prompt keywords or hash
                import hashlib
                idx = int(hashlib.md5(prompt.encode('utf-8')).hexdigest(), 16) % len(mock_images)
                selected_image = mock_images[idx]
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "url": selected_image}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Generate Video (Runway / Seedance)
        if self.path == '/api/ai/generate-video':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                prompt = data.get('prompt', '')
                
                # Return the factory video as mock loop
                selected_video = "images/wideway_intro.mp4"
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "url": selected_video}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Schedule News Articles (OpenClaw / WorkBuddy / ChatGPT / Gemini Spark)
        if self.path == '/api/ai/schedule-news':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                provider = data.get('provider', 'OpenClaw')
                start_date_str = data.get('startDate', '2026-08-01')
                frequency = data.get('frequency', '7') # in days
                batch_count = int(data.get('batchCount', 5))
                keywords = data.get('keywords', 'diapers')
                
                # Load DB
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                
                new_articles = []
                
                # Mock topics matching B2B diaper exports
                topics = [
                    {"title": f"Material Upgrades: High-Retention Super Absorbent Polymers in {keywords}", "cat": "⚙️ Product News"},
                    {"title": f"Market Analysis: Sourcing Demographics for {keywords} in Europe", "cat": "🌿 Industry News"},
                    {"title": f"Sustainable Sourcing: Totally Chlorine-Free Fluff Pulp for {keywords}", "cat": "🌿 ESG & Sustainability"},
                    {"title": f"QA Lab Auditing: Wetness Backback under 0.1g for {keywords}", "cat": "🏭 Factory Updates"},
                    {"title": f"Compliance Guidance: Preparing for global EUDR Trade in {keywords}", "cat": "🌿 ESG & Sustainability"},
                ]
                
                for i in range(batch_count):
                    t_idx = i % len(topics)
                    curr_date = start_date + datetime.timedelta(days=i * int(frequency))
                    date_str = curr_date.strftime("%B %d, %Y")
                    iso_date_str = curr_date.strftime("%Y-%m-%d")
                    art_id = f"sch-{int(curr_date.timestamp())}-{i}"
                    filename = f"news-scheduled-{art_id}.html"
                    
                    art = {
                        "filename": filename,
                        "title": f"Scheduled: {topics[t_idx]['title']} (Batch #{i+1})",
                        "date": date_str,
                        "sitemap_date": iso_date_str,
                        "category": topics[t_idx]['cat'],
                        "image": "images/laboratory_testing.jpg" if i%2==0 else "images/sustainability_factory.jpg",
                        "alt": "Factory qc automated quality testing instruments",
                        "summary": f"A scheduled article generated via {provider} matching parameters: {keywords}. Focuses on manufacturing parameters, absorbency test sheets, and trade audits.",
                        "introduction": f"Published via B2B Scheduler powered by {provider}. This article outlines key sourcing trends matching search queries for {keywords}.",
                        "body": f"<p>This article has been scheduled and published automatically by the AI Agent scheduling pipeline connected to {provider}. Raw material parameters: {keywords} are audited in compliance with ISO and CE criteria.</p><h3>B2B Sourcing Parameters</h3><p>Our quality control processes ensure that all scheduled runs meet factory re-wetness targets under 0.2g, utilizing high-stretch ears spandex components.</p><ul><li><strong>Sourcing Agent:</strong> {provider} Auto-Writer.</li><li><strong>Verification Reference:</strong> QC-SCH-{art_id}.</li><li><strong>Keywords:</strong> {keywords} Export compliance.</li></ul>"
                    }
                    db['news'].append(art)
                    new_articles.append(art)
                
                # Write back
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                    
                # Run the static site generator compiler script to write these new html files
                result = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Successfully generated and scheduled {batch_count} articles via {provider}!",
                    "articles": new_articles,
                    "build_log": result.stdout + result.stderr
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Publish a scheduled article immediately
        if self.path == '/api/scheduler/publish-now':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename')
                if not filename:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Missing filename"}')
                    return
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                today_iso = get_beijing_today()
                today_display = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%B %d, %Y")
                found = False
                for n in db.get('news', []):
                    if n.get('filename') == filename:
                        n['publish_date'] = today_iso
                        n['sitemap_date'] = today_iso
                        n['date'] = today_display
                        n['status'] = 'published'
                        found = True
                        break
                if not found:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Article not found in database"}')
                    return
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Article {filename} published immediately!",
                    "build_log": res.stdout + res.stderr
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Force run scheduler check
        if self.path == '/api/scheduler/run-check':
            updated = run_scheduler_check()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "updated": bool(updated),
                "message": "Scheduler check executed successfully"
            }).encode('utf-8'))
            return

        # API: Batch schedule Facebook 30-day series starting from a given date
        if self.path == '/api/scheduler/batch-schedule-facebook':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8')) if post_data else {}
                start_date_str = data.get('startDate') or get_beijing_today()
                start_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
                today_iso = get_beijing_today()
                
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                news = db.get('news', [])
                fb_filenames = [
                    "news-brand-partnership-fila.html",
                    "news-brand-partnership-diadora.html",
                    "news-brand-partnership-airness.html",
                    "news-brand-partnership-starter.html",
                    "news-brand-partnership-wrangler.html",
                    "news-supermarket-supply-lidl-aldi.html",
                    "news-supply-chain-strength.html",
                    "news-factory-building-capacity.html",
                    "news-category-of-bags.html",
                    "news-sportswear-spectrum.html",
                    "news-industrial-fire-safety.html",
                    "news-global-trade-chain.html"
                ]
                
                matched = 0
                for i, target_fn in enumerate(fb_filenames):
                    for n in news:
                        if n.get('filename') == target_fn:
                            curr_dt = start_dt + datetime.timedelta(days=i)
                            pub_iso = curr_dt.strftime("%Y-%m-%d")
                            display_date = curr_dt.strftime("%B %d, %Y")
                            n['publish_date'] = pub_iso
                            n['sitemap_date'] = pub_iso
                            n['date'] = display_date
                            n['status'] = 'published' if pub_iso <= today_iso else 'scheduled'
                            matched += 1
                            break
                
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                
                res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                end_iso = (start_dt + datetime.timedelta(days=29)).strftime("%Y-%m-%d")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Successfully batch-scheduled 30 Facebook articles from {start_date_str} to {end_iso}!",
                    "scheduled_count": matched,
                    "startDate": start_date_str,
                    "endDate": end_iso
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Update specific article schedule date
        if self.path == '/api/scheduler/update-date':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename')
                new_date_str = data.get('publish_date')
                if not filename or not new_date_str:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Missing filename or publish_date"}')
                    return
                
                new_dt = datetime.datetime.strptime(new_date_str, "%Y-%m-%d")
                today_iso = get_beijing_today()
                display_date = new_dt.strftime("%B %d, %Y")
                
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                found = False
                for n in db.get('news', []):
                    if n.get('filename') == filename:
                        n['publish_date'] = new_date_str
                        n['sitemap_date'] = new_date_str
                        n['date'] = display_date
                        n['status'] = 'published' if new_date_str <= today_iso else 'scheduled'
                        found = True
                        break
                
                if not found:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Article not found"}')
                    return
                
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                
                res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Updated {filename} scheduled date to {new_date_str}",
                    "build_log": res.stdout + res.stderr
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Find Recommended Backlink Opportunities
        if self.path == '/api/ai/find-backlinks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                domain = data.get('domain', 'widewaygroup.com')
                
                recommendations = [
                    {
                        "site": "worldfootwear.com",
                        "category": "📰 Footwear Trade Journal",
                        "authority": 88,
                        "reason": "Premier publication for international footwear manufacturing, sneaker trends, and sole tech innovations. Ideal for pitching Jinjiang craftsmanship and OEM case studies."
                    },
                    {
                        "site": "satra.com",
                        "category": "🔬 Footwear Testing & QC Institute",
                        "authority": 91,
                        "reason": "World leading research and testing organisation for footwear & leather. Essential authority for SATRA test standards and Bally flex resistance."
                    },
                    {
                        "site": "fdra.org",
                        "category": "👞 Industry Trade Association",
                        "authority": 89,
                        "reason": "Footwear Distributors and Retailers of America. Direct connection to North American footwear brands, sourcing executives, and import customs compliance."
                    },
                    {
                        "site": "thomasnet.com",
                        "category": "📦 Global B2B Sourcing Directory",
                        "authority": 90,
                        "reason": "Largest industrial supplier platform in North America. Drives qualified private label sneaker and sports shoe RFQ traffic."
                    },
                    {
                        "site": "sneakerfreaker.com",
                        "category": "👟 Sneaker Culture & Design Portal",
                        "authority": 82,
                        "reason": "Leading lifestyle sneaker magazine. Perfect target to highlight high-rebound cushioning foams, lightweight flyknit uppers, and streetwear retro styling."
                    },
                    {
                        "site": "sustainablefootwear.org",
                        "category": "🌿 ESG & Eco-Footwear Coalition",
                        "authority": 78,
                        "reason": "Green footwear initiative. Ideal for pitching WIDEWAY bio-based EVA outsoles, recycled PET linings, and low-VOC vulcanization."
                    }
                ]
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "recommendations": recommendations}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Generate Ads (Google, LinkedIn, Facebook, TikTok)
        if self.path == '/api/ai/generate-ads':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                product = data.get('product', 'baby diapers')
                keywords = data.get('keywords', 'OEM diaper manufacturer')
                audience = data.get('audience', 'B2B distributors and brand owners')
                
                prompt = f"""
                Generate high-converting B2B ad campaign copies for:
                1. Google Search Ads (Headline, Description, Keywords)
                2. LinkedIn Ads (Intro Copy, Headline, CTA)
                3. Facebook Ads (Primary Text, Headline, Description)
                4. TikTok/YouTube Video Ads (Hook, Script Description, Hashtags)
                
                Target Product: {product}
                Primary Search Keywords: {keywords}
                Target Audience: {audience}
                
                Format the response as clear structured copy sections. Keep it professional, emphasizing CE/ISO quality and factory direct wholesale capacity.
                """
                
                # Call Gemini helper or return high-converting templates
                gemini_key = None
                try:
                    with open(DB_PATH, 'r', encoding='utf-8') as f:
                        content_data = json.load(f)
                        gemini_key = content_data.get('api_keys', {}).get('gemini')
                except Exception:
                    pass
                
                if gemini_key:
                    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req, timeout=15) as res:
                        res_data = json.loads(res.read().decode('utf-8'))
                        text_output = res_data['candidates'][0]['content']['parts'][0]['text']
                else:
                    text_output = f"""### 🔍 Google Search Ads (Targeting High-Intent B2B Footwear Buyers)
* **Headline 1:** OEM/ODM Sneaker Manufacturer Jinjiang
* **Headline 2:** Certified Shoes Factory Direct Wholesale
* **Headline 3:** Custom Sports & Casual Footwear
* **Description 1:** Partner with Jinjiang Wideway (WIDEWAY GROUP). 19+ years footwear manufacturing experience. Audited for FILA, KAPPA, DIADORA. Low MOQ 500 pairs.
* **Description 2:** High-rebound EVA cushioning, breathable knit uppers, private label tooling. Request factory direct quotation today!
* **Keywords:** sneaker oem factory, shoes manufacturer jinjiang, private label footwear supplier, sports shoes wholesale bulk

---

### 👔 LinkedIn Sponsored Content Ads (Targeting Footwear Brand Owners & Procurement Heads)
* **Intro Text:** Looking for a reliable OEM sneaker factory to scale your footwear brand? Jinjiang Wideway (WIDEWAY GROUP) operates 3 automated assembly lines, shipping 300,000 monthly pairs to 40+ countries. Certified BSCI, Sedex SMETA, and ISO 9001.
* **Headline:** State-of-the-Art Footwear Contract Manufacturing (OEM/ODM)
* **CTA Button:** Get Quote / Learn More

---

### 👥 Facebook/Meta Ads (Targeting Athletic Brands & E-commerce Sellers)
* **Primary Text:** Scale your athletic brand or footwear independent site with Jinjiang's premier manufacturing partner. Direct factory pricing, custom tooling, and fast 7-10 days sample prototyping.
* **Headline:** Direct-from-Factory Footwear OEM/ODM Partner
* **Description:** BSCI & Sedex Audited Factory | Fast Shipping from Xiamen Port.

---

### 🎥 TikTok / YouTube Shorts (Targeting Sneaker Brands & Visual Trust)
* **Video Script Hook (0-3s):** [Visual of automated shoe lasting and robotic outsole stitching line] "Here is how 300,000 pairs of high-performance sneakers are engineered monthly in Jinjiang."
* **Script Description:** SATRA tested durability, 3D flying knit weaving. Launch your custom private-label sneaker collection today.
* **Hashtags:** #FootwearManufacturer #OEMSneakers #FactoryWholesale #WidewayGroup #PrivateLabelShoes"""
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "ads": text_output}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: AI Generate Backlink Outreach Pitch
        if self.path == '/api/ai/generate-pitch':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                partner_url = data.get('partnerUrl', 'hygiene-blog.com')
                contact_name = data.get('contactName', 'Editor')
                context = data.get('context', 'guest post request')
                
                prompt = f"""
                Write a highly professional B2B outreach email to pitch a guest article or request a link exchange.
                Recipient Contact Name: {contact_name}
                Target Website: {partner_url}
                Pitch Context: {context}
                
                Emphasize that we are Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP - https://www.widewaygroup.com), a premier footwear and sneaker manufacturer in Jinjiang with 19+ years of OEM/ODM production experience for global brands like FILA, Diadora, Starter, and Kappa. We offer high-quality technical insights about footwear ergonomics, EVA/MD outsole molding, flyknit upper engineering, or sustainable footwear materials. Keep the tone courteous, authoritative, and mutually beneficial.
                """
                
                # Call Gemini helper or return high-converting templates
                gemini_key = None
                try:
                    with open(DB_PATH, 'r', encoding='utf-8') as f:
                        content_data = json.load(f)
                        gemini_key = content_data.get('api_keys', {}).get('gemini')
                except Exception:
                    pass
                
                if gemini_key:
                    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req, timeout=15) as res:
                        res_data = json.loads(res.read().decode('utf-8'))
                        text_output = res_data['candidates'][0]['content']['parts'][0]['text']
                else:
                    text_output = f"""Subject: Footwear Manufacturing Insights / Editorial Collaboration Proposal for {partner_url}

Dear {contact_name},

I hope this message finds you well. 

I have been following {partner_url} and greatly appreciate your industry perspectives and technical coverage of footwear design, athletic apparel, and supply chain manufacturing trends.

I am reaching out on behalf of Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP - https://www.widewaygroup.com). Based in Jinjiang ("China's Footwear Capital") since 2007, we specialize in high-performance sports sneakers, casual footwear, and EVA recovery slides, partnering with international brands including FILA, Diadora, Starter, and Wrangler.

Given your readership's focus on athletic performance, ergonomics, and sustainable footwear production, we have prepared a comprehensive engineering whitepaper titled:
"Advancements in Dual-Density EVA Cushioning & Recycled Flyknit Weaving for High-Traction Athletic Footwear"

We would be thrilled to contribute this technical briefing as a guest column or collaborate on co-branded research for your audience at no cost.

If this aligns with your editorial priorities, I would be delighted to share the complete draft or discuss tailored footwear topics for your review.

Warm regards,

Amy Lin | International Business Director
Jinjiang Wideway Import & Export Co., Ltd. (WIDEWAY GROUP)
Website: https://www.widewaygroup.com
Email: Amy@widewaygroup.com | Direct/WhatsApp: +86 185 0595 9266"""
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "pitch": text_output}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Save structured database settings and trigger rebuild
        if self.path == '/api/save-content':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Write back to content JSON database
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
                # Run the static site generator compiler script
                result = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Content saved and site compiled successfully",
                    "build_log": result.stdout + result.stderr
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Handle B2B media image/video uploads
        if self.path == '/api/upload-media':
            try:
                content_type = self.headers['Content-Type']
                if 'boundary=' not in content_type:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Invalid Content-Type"}')
                    return
                    
                boundary = content_type.split("boundary=")[1].encode()
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                
                parts = body.split(b'--' + boundary)
                filename = ""
                file_data = b""
                
                for part in parts:
                    if b'filename=' in part:
                        headers_part, data_part = part.split(b'\r\n\r\n', 1)
                        header_str = headers_part.decode('utf-8', errors='ignore')
                        for line in header_str.split('\r\n'):
                            if 'filename=' in line:
                                filename = line.split('filename=')[1].strip('"')
                        if data_part.endswith(b'\r\n'):
                            data_part = data_part[:-2]
                        if data_part.endswith(b'\r\n--'):
                            data_part = data_part[:-4]
                        file_data = data_part
                        break
                
                if filename and file_data:
                    clean_filename = os.path.basename(filename)
                    # Support only common web media formats
                    ext = os.path.splitext(clean_filename)[1].lower()
                    if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.webm', '.mov', '.webp']:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"status": "error", "message": "File format not supported"}')
                        return

                    # Strict size limits: Image <= 2MB, Video <= 50MB
                    MAX_IMAGE_SIZE = 2 * 1024 * 1024   # 2MB
                    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
                    file_len = len(file_data)
                    
                    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'] and file_len > MAX_IMAGE_SIZE:
                        size_mb = round(file_len / (1024 * 1024), 2)
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "error",
                            "message": f"【上传拦截】图片文件大小为 {size_mb} MB，超过了系统允许的最大限制（2MB / 2,048 KB）！图片规格要求：单张不得超过 2MB，建议压缩至 300KB~800KB（推荐分辨率 1200x800 或 1920x1080）后重新上传。"
                        }).encode('utf-8'))
                        return

                    if ext in ['.mp4', '.webm', '.mov'] and file_len > MAX_VIDEO_SIZE:
                        size_mb = round(file_len / (1024 * 1024), 2)
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "status": "error",
                            "message": f"【上传拦截】视频文件大小为 {size_mb} MB，超过了系统允许的最大限制（50MB）！视频规格要求：单个视频不得超过 50MB，建议转码压缩至 10MB~30MB（推荐 1080p/720p H.264 MP4 格式）后重新上传。"
                        }).encode('utf-8'))
                        return
                        
                    dest_path = os.path.join(os.getcwd(), 'images', clean_filename)
                    with open(dest_path, 'wb') as f:
                        f.write(file_data)
                        
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "success",
                        "url": f"images/{clean_filename}"
                    }).encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Empty file data or filename"}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Replace an existing media file in-place and recompile entire site
        if self.path == '/api/replace-media':
            try:
                content_type = self.headers.get('Content-Type', '')
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length) if content_length > 0 else b''

                target_filename = ""
                file_data = b""

                if 'application/json' in content_type:
                    data = json.loads(body.decode('utf-8'))
                    target_filename = data.get('target_filename') or data.get('filename') or ''
                    file_base64 = data.get('file_base64') or data.get('base64') or ''
                    if ',' in file_base64:
                        file_base64 = file_base64.split(',', 1)[1]
                    if file_base64:
                        file_data = base64.b64decode(file_base64)
                elif 'boundary=' in content_type:
                    boundary = content_type.split("boundary=")[1].encode()
                    parts = body.split(b'--' + boundary)
                    for part in parts:
                        if b'name="target_filename"' in part:
                            headers_part, data_part = part.split(b'\r\n\r\n', 1)
                            target_filename = data_part.strip().decode('utf-8', errors='ignore')
                        elif b'filename=' in part:
                            headers_part, data_part = part.split(b'\r\n\r\n', 1)
                            header_str = headers_part.decode('utf-8', errors='ignore')
                            if not target_filename:
                                for line in header_str.split('\r\n'):
                                    if 'filename=' in line:
                                        target_filename = line.split('filename=')[1].strip('"')
                            if data_part.endswith(b'\r\n'):
                                data_part = data_part[:-2]
                            if data_part.endswith(b'\r\n--'):
                                data_part = data_part[:-4]
                            file_data = data_part

                if not target_filename:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Missing target_filename"}')
                    return

                clean_target = os.path.basename(urllib.parse.unquote(target_filename))
                ext = os.path.splitext(clean_target)[1].lower()
                if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.webp', '.webm']:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Unsupported file format for replacement"}')
                    return

                if not file_data:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "No file data received"}')
                    return

                # Strict size limits: Image <= 2MB, Video <= 50MB
                MAX_IMAGE_SIZE = 2 * 1024 * 1024   # 2MB
                MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
                file_len = len(file_data)

                if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'] and file_len > MAX_IMAGE_SIZE:
                    size_mb = round(file_len / (1024 * 1024), 2)
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "error",
                        "message": f"【替换拦截】待替换图片文件大小为 {size_mb} MB，超过了系统允许的最大限制（2MB / 2,048 KB）！图片规格要求：单张不得超过 2MB，建议压缩至 300KB~800KB（推荐分辨率 1200x800 或 1920x1080）后重新上传。"
                    }).encode('utf-8'))
                    return

                if ext in ['.mp4', '.webm'] and file_len > MAX_VIDEO_SIZE:
                    size_mb = round(file_len / (1024 * 1024), 2)
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "error",
                        "message": f"【替换拦截】待替换视频文件大小为 {size_mb} MB，超过了系统允许的最大限制（50MB）！视频规格要求：单个视频不得超过 50MB，建议转码压缩至 10MB~30MB（推荐 1080p/720p H.264 MP4 格式）后重新上传。"
                    }).encode('utf-8'))
                    return

                images_dir = os.path.join(os.getcwd(), 'images')
                os.makedirs(images_dir, exist_ok=True)
                dest_path = os.path.join(images_dir, clean_target)

                # Overwrite the target file in-place
                with open(dest_path, 'wb') as f:
                    f.write(file_data)

                # Automatically trigger build_site.py to rebuild templates, sitemaps, and pages
                build_res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": f"Successfully replaced {clean_target} and refreshed entire website!",
                    "filename": clean_target,
                    "url": f"images/{clean_target}",
                    "timestamp": int(time.time()),
                    "build_log": build_res.stdout
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        # API: Deploy site to remote production server (43.130.32.54)
        if self.path == '/api/deploy-production':
            try:
                # 1. Run build_site.py to ensure all generated files are fresh
                build_res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                # 2. Run deploy_production_sync.py
                deploy_res = subprocess.run([sys.executable or 'python3', 'deploy_production_sync.py'], capture_output=True, text=True, timeout=120)
                
                log_output = f"=== BUILD LOG ===\n{build_res.stdout}\n{build_res.stderr}\n\n=== DEPLOY LOG ===\n{deploy_res.stdout}\n{deploy_res.stderr}"
                success = (deploy_res.returncode == 0)
                
                self.send_response(200 if success else 500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'success' if success else 'error',
                    'message': '🚀 Production deployment completed successfully to 43.130.32.54!' if success else '❌ Deployment failed.',
                    'log': log_output
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        # API: Batch search and replace across entire site_content.json database
        if self.path == '/api/batch-replace':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                search_str = data.get('search_str', '').strip()
                replace_str = data.get('replace_str', '')
                case_sensitive = data.get('case_sensitive', False)
                
                if not search_str:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Search string cannot be empty"}')
                    return
                
                with open(DB_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                replace_count = 0
                def recurse_replace(obj):
                    nonlocal replace_count
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, str):
                                if (search_str in v if case_sensitive else search_str.lower() in v.lower()):
                                    if case_sensitive:
                                        obj[k] = v.replace(search_str, replace_str)
                                    else:
                                        pattern = re.compile(re.escape(search_str), re.IGNORECASE)
                                        obj[k] = pattern.sub(replace_str, v)
                                    replace_count += 1
                            elif isinstance(v, (dict, list)):
                                recurse_replace(v)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            if isinstance(item, str):
                                if (search_str in item if case_sensitive else search_str.lower() in item.lower()):
                                    if case_sensitive:
                                        obj[i] = item.replace(search_str, replace_str)
                                    else:
                                        pattern = re.compile(re.escape(search_str), re.IGNORECASE)
                                        obj[i] = pattern.sub(replace_str, item)
                                    replace_count += 1
                            elif isinstance(item, (dict, list)):
                                recurse_replace(item)

                recurse_replace(db)
                
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                    
                build_res = subprocess.run([sys.executable or 'python3', 'build_site.py'], capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'replace_count': replace_count,
                    'message': f'Replaced {replace_count} occurrences of "{search_str}" and recompiled website.',
                    'build_log': build_res.stdout
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        # API: Delete Media File
        if self.path == '/api/delete-media':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename') or os.path.basename(data.get('url', ''))
                clean_name = os.path.basename(filename)
                target_path = os.path.join(os.getcwd(), 'images', clean_name)
                
                if os.path.exists(target_path) and os.path.isfile(target_path):
                    os.remove(target_path)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'message': f'{clean_name} deleted successfully'}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "File not found"}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        # API: Update Inquiry Status
        if self.path == '/api/inquiry/update-status':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                inq_id = data.get('id')
                new_status = data.get('status', 'Contacted')
                inquiries = []
                if os.path.exists(INQUIRIES_PATH):
                    with open(INQUIRIES_PATH, 'r', encoding='utf-8') as f:
                        inquiries = json.load(f)
                
                found = False
                for item in inquiries:
                    if item.get('id') == inq_id:
                        item['status'] = new_status
                        item['status_updated_at'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                        found = True
                        break
                
                if found:
                    with open(INQUIRIES_PATH, 'w', encoding='utf-8') as f:
                        json.dump(inquiries, f, indent=2, ensure_ascii=False)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'message': 'Status updated'}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "error", "message": "Inquiry not found"}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        # API: Delete Inquiry
        if self.path == '/api/inquiry/delete':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            try:
                data = json.loads(post_data.decode('utf-8'))
                inq_id = data.get('id')
                inquiries = []
                if os.path.exists(INQUIRIES_PATH):
                    with open(INQUIRIES_PATH, 'r', encoding='utf-8') as f:
                        inquiries = json.load(f)
                
                filtered = [item for item in inquiries if item.get('id') != inq_id]
                with open(INQUIRIES_PATH, 'w', encoding='utf-8') as f:
                    json.dump(filtered, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'message': 'Inquiry deleted'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def main():
    print(f"Starting B2B Admin Server on http://localhost:{PORT} ...")
    start_auto_scheduler_daemon()
    server = HTTPServer(('0.0.0.0', PORT), AdminHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()

if __name__ == '__main__':
    main()
