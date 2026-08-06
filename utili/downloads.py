import os
import requests
from urllib.parse import urlparse


def download_via_requests(driver, url, dest_dir, timeout=60):
    os.makedirs(dest_dir, exist_ok=True)

    session = requests.Session()

    # Transfer cookies from Selenium driver to requests session
    for c in driver.get_cookies():
        session.cookies.set(c['name'], c.get('value', ''), domain=c.get('domain'))

    # Use driver's user agent if available
    try:
        ua = driver.execute_script('return navigator.userAgent')
        session.headers.update({'User-Agent': ua})
    except Exception:
        pass

    resp = session.get(url, stream=True, timeout=timeout)
    resp.raise_for_status()

    # Determine filename from Content-Disposition or URL
    filename = None
    cd = resp.headers.get('content-disposition')
    if cd and 'filename=' in cd:
        filename = cd.split('filename=')[-1].strip('"')
    if not filename:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or 'download.bin'

    dest_path = os.path.join(dest_dir, filename)
    with open(dest_path, 'wb') as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                fh.write(chunk)

    return dest_path
