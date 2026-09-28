# SoNo-sky DART Financial Agent

[![🔗 대시보드 바로가기](https://img.shields.io/badge/%F0%9F%94%97-%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C%20%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0-155EEF?style=for-the-badge)](https://hsc-class02.github.io/SoNo-sky/)

DART(OpenDART)에서 SoNo-sky 관련 정기보고서의 재무정보를 수집하고 주요 재무비율을 계산해 GitHub Pages 대시보드로 제공하는 자동화 프로젝트입니다.

## 🔗 대시보드
https://hsc-class02.github.io/SoNo-sky/

상단에는 매출·영업이익·순이익 추이와 수익성 지표, 하단에는 **Annual / Half-year / Quarterly** 3개 표와 국내 Peer Firms 표를 제공합니다.

## API / 자동 업데이트
1. OpenDART에서 인증키를 발급합니다: https://opendart.fss.or.kr/
2. GitHub → **Settings → Secrets and variables → Actions → New repository secret**
3. Name: `DART_API_KEY`
4. Value: 발급받은 OpenDART 인증키
5. **Actions → DART Monthly Update → Run workflow**로 최초 수집합니다.

`.github/workflows/update_data.yml`이 매월 1일 UTC 00:17(한국시간 09:17)에 실행되며 수동 실행도 지원합니다. API key는 코드에 저장하지 않습니다.

## 데이터 범위
- Annual: 사업보고서
- Half-year: 반기보고서
- Quarterly: 1분기보고서, 3분기보고서
- 요청 범위: 2010년부터

OpenDART 단일회사 전체 재무제표 API는 공식 제공범위상 2015년 이후를 구조화 데이터로 처리합니다. 2010–2014는 DART 정기공시 목록을 별도로 조회하고 접수번호를 보존하는 fallback 구조를 사용합니다. 임의의 숫자로 과거 구간을 채우지 않습니다.

## 주요 지표
매출액, 매출원가, 매출총이익, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 유동자산, 유동부채, 현금및현금성자산, 매출채권, 재고자산, 차입금, 영업활동현금흐름, 유형자산 취득액 및 영업이익률, 순이익률, ROA, ROE, 부채비율, 유동비율, 자산회전율을 제공합니다.

## 국내 Peer Firms
사업부문 유사성을 참고한 비교군이며 1:1 동종기업을 의미하지 않습니다.

| Peer | 종목코드 | 비교 근거 |
|---|---:|---|
| 아이마켓코리아 | 122900 | MRO / 기업소모성자재 구매 |
| 현대리바트 | 079430 | 리빙·가구 유통 |
| 코웨이 | 021240 | 렌탈·생활가전 |
| SK네트웍스 | 001740 | 렌탈·유통/서비스 |

## GitHub Pages
`pages.yml`이 main push 때 GitHub Pages를 배포합니다. 저장소 **Settings → Pages → Build and deployment → Source**에서 **GitHub Actions**를 한 번 선택하면 됩니다.

> 재무 데이터 원천: 금융감독원 DART / OpenDART.