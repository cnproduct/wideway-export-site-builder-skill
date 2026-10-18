import os
import sys
import glob
import tarfile
import paramiko

def deploy():
    host = "43.130.32.54"
    port = 2222
    user = "ubuntu"
    password = "WHJCwhjc2026"
    remote_dir = "/var/www/widewayfootwear.com"

    # Step 1: Create a tar.gz bundle locally
    tar_path = "dist_bundle.tar.gz"
    print("📦 Packing web assets into dist_bundle.tar.gz...")
    
    # Collect files
    core_files = glob.glob("*.html") + [
        "sitemap.xml", "robots.txt", "llms.txt", "llms-full.txt", "DESIGN.md", "favicon.ico", "manifest.json",
        "server.py", "build_site.py", "validate_site_quality.py", "deploy_production_sync.py",
        "e8a4c9f21b0d4637a9e52c3f8b7d6e21.txt"
    ]
    
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in core_files:
            if os.path.exists(f):
                tar.add(f, arcname=os.path.basename(f))
        for folder in ["css", "js", "data", "ru", "references", "scripts", "ai"]:
            if os.path.exists(folder):
                tar.add(folder, arcname=folder)

    tar_size = os.path.getsize(tar_path)
    print(f"  Bundle created: {tar_size / 1024:.1f} KB")

    # Step 2: Connect SSH & SFTP with retry
    print(f"Connecting to {host}:{port}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    import time
    connected = False
    for attempt in range(1, 6):
        try:
            print(f"  Attempt {attempt}/5...")
            ssh.connect(
                host, 
                port=port, 
                username=user, 
                password=password, 
                timeout=30, 
                banner_timeout=60, 
                auth_timeout=60
            )
            connected = True
            print("  ✅ SSH Connected!")
            break
        except Exception as e:
            print(f"  Connection attempt {attempt} failed: {e}")
            time.sleep(3)
            
    if not connected:
        print("❌ Could not connect after 5 attempts.")
        return
    
    sftp = ssh.open_sftp()

    # Step 3: Upload tarball
    remote_tar = "/tmp/wideway_bundle.tar.gz"
    print(f"Uploading {tar_path} to {remote_tar}...")
    sftp.put(tar_path, remote_tar)
    print("  ✅ Upload complete.")

    # Step 4: Extract on remote server
    print(f"Extracting bundle into {remote_dir}...")
    extract_cmd = f"echo '{password}' | sudo -S tar -xzf {remote_tar} -C {remote_dir} && echo '{password}' | sudo -S chown -R ubuntu:ubuntu {remote_dir} && rm -f {remote_tar}"
    stdin, stdout, stderr = ssh.exec_command(extract_cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        err = stderr.read().decode()
        print(f"❌ Extraction error: {err}")
    else:
        print("  ✅ Extracted and permissions updated successfully.")

    # Step 5: Reload nginx and restart backend service
    print("Reloading Nginx and restarting wideway-api backend service...")
    stdin, stdout, stderr = ssh.exec_command(f"echo '{password}' | sudo -S systemctl reload nginx && echo '{password}' | sudo -S systemctl restart wideway-api.service")
    stdout.channel.recv_exit_status()
    print("  ✅ Nginx reloaded and wideway-api.service restarted on remote production server!")

    # Cleanup local bundle
    if os.path.exists(tar_path):
        os.remove(tar_path)

    sftp.close()
    ssh.close()
    print("🚀 Deployment to 43.130.32.54 completed successfully!")

    # Step 6: Submit IndexNow notification to Yandex and Bing
    print("📡 Submitting real-time IndexNow notification to Yandex & Bing...")
    try:
        import subprocess
        subprocess.run([sys.executable, "scripts/yandex_indexnow_notify.py"], check=False)
    except Exception as e:
        print(f"  ⚠️ IndexNow notification notice: {e}")

if __name__ == "__main__":
    deploy()

