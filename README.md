# GMUC Tennis Watcher

광명도시공사 테니스 예약현황을 낮은 빈도로 조회하고, 조건에 맞는 빈 코트가 새로 나타나면 ntfy로 알립니다. 예약/결제는 자동화하지 않습니다.

## 감시 조건
- 화요일 18:00-20:00, 20:00-22:00
- 목요일 18:00-20:00, 20:00-22:00
- 토요일 08:00-10:00, 10:00-12:00
- 7번, 8번 코트 제외
- 오늘부터 14일 이내 대상일 조회
- GitHub Actions 약 10분 간격 실행

## Android 알림 설정
1. Android에 ntfy 앱을 설치합니다.
2. 추측하기 어려운 개인 토픽 이름을 하나 정하고 구독합니다.
3. GitHub 저장소 Settings > Secrets and variables > Actions > New repository secret에서
   Name: NTFY_TOPIC
   Value: 위에서 정한 토픽 이름
4. Actions 탭에서 Watch GMUC tennis를 열고 Run workflow로 1회 테스트합니다.

주의: ntfy.sh 공개 서버의 토픽 이름은 비밀번호가 아닙니다. 충분히 길고 임의적인 값을 사용하세요. GitHub 저장소에는 로그인 정보나 JSESSIONID를 저장하지 마세요.
