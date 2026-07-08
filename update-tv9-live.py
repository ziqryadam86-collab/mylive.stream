import requests
import re
import base64

# 1. Link GitHub Pages abang yang simpan keys.txt (Kalis Block 429!)
KEY_URL = "https://ziqryadam86-collab.github.io/tv9keys/keys.txt"

# Fungsi tukar HEX ke Base64 URL-safe (ClearKey DRM Format)
def hex_to_base64(hex_str):
    clean_hex = re.sub(r'[^A-Fa-f0-9]', '', hex_str)
    bytes_data = bytes.fromhex(clean_hex)
    b64 = base64.b64encode(bytes_data).decode('utf-8')
    return b64.replace('=', '').replace('+', '-').replace('/', '_')

try:
    # 2. Ambil (curl/fetch) data dari GitHub Pages
    print(f"Mengambil kunci dari {KEY_URL}...")
    response = requests.get(KEY_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    
    if response.status_code == 200:
        key_data = response.text.strip()
        
        if ":" in key_data:
            KID_HEX, KEY_HEX = key_data.split(":")
            
            # 3. Tukar HEX ke Base64
            base64_kid = hex_to_base64(KID_HEX)
            base64_key = hex_to_base64(KEY_HEX)
            
            print(f"KID (Base64): {base64_kid}")
            print(f"KEY (Base64): {base64_key}")

            # 4. Template XML MPD TV9 (Dengan pautan segmen .dash yang sah)
            template_mpd = f"""<?xml version="1.0" encoding="utf-8"?>
<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:clearkey="http://dashif.org/guidelines/clearKey" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 DASH-MPD.xsd" profiles="urn:mpeg:dash:profile:isoff-live:2011" type="dynamic" minimumUpdatePeriod="PT5S" availabilityStartTime="2021-11-23T03:36:20Z" publishTime="2023-10-18T00:00:00Z" timeShiftBufferDepth="PT30S" maxSegmentDuration="PT9S">
  <Period id="p0" start="PT0S">
    <AdaptationSet id="0" contentType="video" segmentAlignment="true" bitstreamSwitching="true" maxWidth="1920" maxHeight="1080" maxFrameRate="25" par="16:9">
      <ContentProtection schemeIdUri="urn:uuid:e251367d-bb43-4d70-970f-5544af77c198" value="ClearKey">
        <clearkey:Laurl Lic_type="EME-CLEARKEY">data:application/json,{{"keys":[{{"kty":"oct","kid":"{base64_kid}","k":"{base64_key}"}}],"type":"temporary"}}</clearkey:Laurl>
      </ContentProtection>
      <SegmentTemplate timescale="1000" duration="8000" startNumber="1" initialization="https://ngtv-live-cbj.gcdn.co/Content/DASH/Live/channel(TV9)/init-video=$RepresentationID$.dash" media="https://ngtv-live-cbj.gcdn.co/Content/DASH/Live/channel(TV9)/media-video=$RepresentationID$-$Number$.dash"/>
      <Representation id="1" mimeType="video/mp4" codecs="avc1.64001f" width="1280" height="720" frameRate="25" sar="1:1" bandwidth="2200000"/>
      <Representation id="2" mimeType="video/mp4" codecs="avc1.640028" width="1920" height="1080" frameRate="25" sar="1:1" bandwidth="4500000"/>
    </AdaptationSet>
    <AdaptationSet id="1" contentType="audio" segmentAlignment="true" lang="ms">
      <ContentProtection schemeIdUri="urn:uuid:e251367d-bb43-4d70-970f-5544af77c198" value="ClearKey">
        <clearkey:Laurl Lic_type="EME-CLEARKEY">data:application/json,{{"keys":[{{"kty":"oct","kid":"{base64_kid}","k":"{base64_key}"}}],"type":"temporary"}}</clearkey:Laurl>
      </ContentProtection>
      <SegmentTemplate timescale="1000" duration="8000" startNumber="1" initialization="https://ngtv-live-cbj.gcdn.co/Content/DASH/Live/channel(TV9)/init-audio=$RepresentationID$.dash" media="https://ngtv-live-cbj.gcdn.co/Content/DASH/Live/channel(TV9)/media-audio=$RepresentationID$-$Number$.dash"/>
      <Representation id="1" mimeType="audio/mp4" codecs="mp4a.40.2" audioSamplingRate="48000" bandwidth="128000"/>
    </AdaptationSet>
  </Period>
</MPD>"""

            # 5. Tulis / Simpan fail tv9.mpd
            with open("tv9.mpd", "w", encoding="utf-8") as f:
                f.write(template_mpd)
                
            print("BERJAYA: Fail tv9.mpd telah dihasilkan!")
        else:
            print("RALAT: Format keys.txt tidak mengandungi ':'")
    else:
        print(f"RALAT: Gagal ambil keys.txt. Status Code: {response.status_code}")

except Exception as e:
    print(f"RALAT: {e}")
          
