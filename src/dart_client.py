import io,zipfile,xml.etree.ElementTree as ET,requests
BASE="https://opendart.fss.or.kr/api"
REPORT_CODES={"annual":"11011","half":"11012","q1":"11013","q3":"11014"}
class DartClient:
 def __init__(self,key):
  if not key:raise ValueError("DART_API_KEY is required")
  self.key=key;self.s=requests.Session();self.s.headers["User-Agent"]="SoNo-sky-DART-Agent/1.0"
 def get(self,endpoint,params):
  p=dict(params);p["crtfc_key"]=self.key;r=self.s.get(f"{BASE}/{endpoint}.json",params=p,timeout=60);r.raise_for_status();d=r.json()
  if str(d.get("status"))!="000":
   if str(d.get("status"))=="013":return {}
   raise RuntimeError(f"DART {d.get('status')}: {d.get('message')}")
  return d
 def corp_code(self,name="소노스퀘어",stock="007720"):
  r=self.s.get(f"{BASE}/corpCode.xml",params={"crtfc_key":self.key},timeout=60);r.raise_for_status()
  with zipfile.ZipFile(io.BytesIO(r.content)) as z:root=ET.fromstring(z.read("CORPCODE.xml"))
  fallback=None
  for x in root.findall("list"):
   n=(x.findtext("corp_name") or "").strip();st=(x.findtext("stock_code") or "").strip();c=(x.findtext("corp_code") or "").strip()
   if st==stock and c:return c
   if n==name:fallback=c
  if fallback:return fallback
  raise RuntimeError("corp code not found")
 def financials(self,corp,year,report,fs="CFS"):return self.get("fnlttSinglAcntAll",{"corp_code":corp,"bsns_year":str(year),"reprt_code":report,"fs_div":fs}).get("list",[])
 def disclosures(self,corp,start,end,detail):return self.get("list",{"corp_code":corp,"bgn_de":start,"end_de":end,"pblntf_ty":"A","pblntf_detail_ty":detail,"last_reprt_at":"Y","page_no":"1","page_count":"100"}).get("list",[])
 def legacy_discovery(self,corp,year,detail):return [{"year":year,"rcept_no":d.get("rcept_no"),"report_nm":d.get("report_nm"),"rcept_dt":d.get("rcept_dt")} for d in self.disclosures(corp,f"{year}0101",f"{year+1}0630",detail) if "보고서" in d.get("report_nm","")]
