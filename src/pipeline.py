import json,os,time
from datetime import date
from pathlib import Path
from .dart_client import DartClient,REPORT_CODES
from .metrics import extract_metrics,calculate_ratios,PEERS
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"data";DATA.mkdir(exist_ok=True)
def collect(c,corp,y,p,code):
 rows=c.financials(corp,y,code,"CFS")
 if not rows:rows=c.financials(corp,y,code,"OFS")
 m=extract_metrics(rows,p);m.update(calculate_ratios(m))
 return {"year":y,"period":p,"report_code":code,"metrics":m,"rcept_no":rows[0].get("rcept_no") if rows else None,"currency":rows[0].get("currency") if rows else "KRW","fs_div":rows[0].get("fs_div") if rows else None}
def main():
 c=DartClient(os.environ.get("DART_API_KEY"));corp=c.corp_code();today=date.today().year;records=[]
 for y in range(2015,today+1):
  for p,code in REPORT_CODES.items():
   try:
    r=collect(c,corp,y,p,code)
    if any(v is not None for v in r["metrics"].values()):records.append(r)
   except Exception as e:print("skip",y,p,e)
   time.sleep(.15)
 legacy=[]
 for y in range(2010,2015):
  for detail in ("A001","A002","A003"):
   try:legacy+=c.legacy_discovery(corp,y,detail)
   except Exception as e:print("legacy",y,e)
 payload={"company":{"name":"소노스퀘어","legacy_name":"대명소노시즌","stock_code":"007720","corp_code":corp},"generated_at":date.today().isoformat(),"coverage":{"structured_from":2015,"requested_from":2010,"legacy_discovery":legacy},"records":records,"peers":PEERS}
 (DATA/"financial_data.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8");print("records:",len(records))
if __name__=="__main__":main()
