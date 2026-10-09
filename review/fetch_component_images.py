"""Fetch public product photos and public listing metadata for the BOM report."""
from pathlib import Path
import requests, json, re, html
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
PHOTOS = OUT/'images'
PHOTOS.mkdir(exist_ok=True)
PRODUCTS = {
 'n20_motor':'https://robocraze.com/products/robocraze-dc6v-100rpm-gm12-n20-miniature-gear-motor-with-metal-gear',
 'drv8833':'https://robocraze.com/products/drv8833-2-channel-dc-motor-driver',
 'tof':'https://robocraze.com/products/vl53l0x-laser-ranging-sensor',
 'esp32_camera':'https://robocraze.com/products/esp32-camera-module',
 'lfp_6ah':'https://elbotics.com/products/12-8v-6ah-lifepo4-battery-smart-bms-76-8wh',
 'wattnine_6ah':'https://quartzcomponents.com/products/12v-6ah-lithium-battery-lifepo4-battery',
 'small_wheel':'https://kitsguru.com/products/car-wheel-tyre-44mm-n20-dc-gear-motor-wheel',
 'mdd10a':'https://evelta.com/mdd10a-10amp-5v-30v-dc-motor-driver-2-channels/',
 'esp32s3':'https://evelta.com/7semi-esp32-s3-devkitc-1-esp32-s3-wroom-wi-fi-bluetooth-5-ble-development-board/',
 'pololu_37d':'https://www.pololu.com/product/4755',
 'jgb37':'https://www.engineerstoy.com/product/dc-geared-motor-with-encoder-jgb37-520-12v/',
 'large_wheel':'https://www.hiwonder.com/products/100mm-high-load-bearing-and-wear-resistant-tire',
 'bonka_3s':'https://robocraze.com/products/bonka-2200mah-35c-3s1p-11-1v-lipo-battery',
 'small_battery':'https://fioparts.com/products/gnb-2s-850mah-80c-xt30-lipo',
}
def fetch(item):
    key,url=item
    result={'key':key,'source_page':url,'checked_utc':datetime.now(timezone.utc).isoformat()}
    try:
        headers={'User-Agent':'Mozilla/5.0'}
        is_shopify = '/products/' in url
        r=requests.get(url+'.js' if is_shopify else url,headers=headers,timeout=25)
        r.raise_for_status()
        if is_shopify:
            p=r.json()
            result.update(title=p['title'],variants=[{k:v.get(k) for k in ('title','price','available','sku')} for v in p.get('variants',[])],description_text=re.sub('<[^>]+>',' ',p.get('description','')))
            img=p.get('featured_image') or (p.get('images') or [None])[0]
        else:
            body=r.text
            (OUT/(key+'_source.html')).write_text(body)
            match=re.search(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)',body,re.I)
            if not match: match=re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image',body,re.I)
            img=html.unescape(match.group(1)) if match else None
        if img:
            img=urljoin(url,img)
            photo=requests.get(img,headers=headers,timeout=25)
            photo.raise_for_status()
            content_type=photo.headers.get('content-type','')
            if not content_type.startswith('image/'): raise ValueError('Non-image response: '+content_type)
            ext={'image/jpeg':'.jpg','image/png':'.png','image/webp':'.webp','image/avif':'.avif'}.get(content_type.split(';')[0],'.jpg')
            rel='images/'+key+ext
            (OUT/rel).write_bytes(photo.content)
            result.update(image_source=img,local_image=rel)
        else: result['image_error']='No product image found'
    except Exception as exc: result['error']=str(exc)[:250]
    print(json.dumps({k:v for k,v in result.items() if k not in ('description_text',)},ensure_ascii=False))
    return result
existing_file=OUT/'component_sources.json'
existing=json.loads(existing_file.read_text()) if existing_file.exists() else []
already={x['key'] for x in existing if x.get('local_image')}
with ThreadPoolExecutor(max_workers=6) as pool:
    fresh=list(pool.map(fetch,((k,v) for k,v in PRODUCTS.items() if k not in already)))
updated={x['key']:x for x in existing}
updated.update({x['key']:x for x in fresh})
results=list(updated.values())
(OUT/'component_sources.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
