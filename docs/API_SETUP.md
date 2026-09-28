# API 설정

OpenDART 인증키 발급: https://opendart.fss.or.kr/

GitHub Settings → Secrets and variables → Actions → New repository secret
- Name: DART_API_KEY
- Value: OpenDART 40자리 인증키

그 다음 Actions → DART Monthly Update → Run workflow로 초기 수집을 실행합니다.

GitHub Pages는 Settings → Pages → Build and deployment → Source에서 GitHub Actions를 한 번 선택합니다.
월 1일 workflow는 UTC 00:17(한국시간 09:17)에 실행됩니다.
