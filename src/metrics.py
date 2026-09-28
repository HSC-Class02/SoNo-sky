ACCOUNT_ALIASES={"revenue":["매출액","영업수익","수익(매출액)"],"cogs":["매출원가"],"gross_profit":["매출총이익","매출총손익"],"operating_income":["영업이익","영업이익(손실)"],"net_income":["당기순이익","당기순이익(손실)","당기순손익"],"assets":["자산총계"],"liabilities":["부채총계"],"equity":["자본총계"],"current_assets":["유동자산"],"current_liabilities":["유동부채"],"cash":["현금및현금성자산","현금 및 현금성자산"],"receivables":["매출채권","매출채권및기타채권","매출채권 및 기타채권"],"inventory":["재고자산"],"borrowings":["단기차입금","장기차입금","차입금","사채"],"operating_cash_flow":["영업활동으로 인한 현금흐름","영업활동현금흐름"],"capex":["유형자산의 취득","유형자산 취득","유형자산의 증가"]}
PEERS=[{"name":"아이마켓코리아","ticker":"122900","note":"MRO/기업소모성자재 구매"},{"name":"현대리바트","ticker":"079430","note":"리빙·가구 유통"},{"name":"코웨이","ticker":"021240","note":"렌탈·생활가전"},{"name":"SK네트웍스","ticker":"001740","note":"렌탈·유통/서비스"}]
def pick(rows,aliases):
 for a in aliases:
  for r in rows:
   if (r.get("account_nm") or "").strip()==a:return r
 for r in rows:
  if any(a in (r.get("account_nm") or "") for a in aliases):return r
 return None
def num(v):
 if v in (None,"","-"):return None
 try:return float(str(v).replace(",",""))
 except:return None
def extract_metrics(rows,period):
 out={}
 for k,aliases in ACCOUNT_ALIASES.items():
  r=pick(rows,aliases)
  if not r:out[k]=None;continue
  f="thstrm_add_amount" if period in ("half","q1","q3") and r.get("sj_div") in ("IS","CIS","CF") else "thstrm_amount"
  out[k]=num(r.get(f))
 return out
def div(a,b):return None if a is None or b in (None,0) else a/b
def calculate_ratios(m):return {"operating_margin":div(m.get("operating_income"),m.get("revenue")),"net_margin":div(m.get("net_income"),m.get("revenue")),"roe":div(m.get("net_income"),m.get("equity")),"roa":div(m.get("net_income"),m.get("assets")),"debt_ratio":div(m.get("liabilities"),m.get("equity")),"current_ratio":div(m.get("current_assets"),m.get("current_liabilities")),"asset_turnover":div(m.get("revenue"),m.get("assets"))}
