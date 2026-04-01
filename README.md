# DTX Web Converter (정적 브라우저 배포 버전)

파이썬 환경이나 서버 사이드 백엔드를 거치지 않고 오로지 100% 웹 브라우저(`Javascript`)만을 사용하여 DTX 파일들을 최신 규칙으로 변환하고 `.zip`으로 다운로드할 수 있도록 제작된 정적 웹 애플리케이션입니다.

## ✨ 주요 기능

- **서버 무설치**: 백엔드 코드나 앱 컨테이너(Docker, 파이썬 등)가 전혀 필요 없습니다. 오로지 Github Pages 만으로 전세계 어디서든 무료로 즉각 서비스할 수 있습니다.
- **클라이언트 사이드 파일 변환**: `JSZip` 및 Javascript File FileReader를 사용하여 내부 텍스트를 파싱하고 즉시 변환합니다. 모든 작업은 브라우저에서 수행되므로 개인정보(Data)가 외부 서버로 유출되지 않으며 속도 또한 비약적으로 빠릅니다.
- **최신식 디자인 적용**: 다크 모드(Dark Mode), 미려한 폰트, Drop Zone, Button Animation 등을 지원합니다.
- **통계 자동 누적 (Firebase)**: 파이어베이스를 연동할 수 있도록 코드가 구성되어 있습니다.

## 🚀 배포 방법 (Github Pages) 

1. 현재 변경 사항이 모두 Github의 `master` 브랜치에 저장되었습니다.
2. Github 레포지토리([yskim032/COR_MTF](https://github.com/yskim032/COR_MTF))의 **"Settings" > "Pages"** 로 이동합니다.
3. **Build and deployment** 섹션의 Source 속성을 `Deploy from a branch`로 맞춥니다.
4. **Branch**를 `master` (또는 `main`) 로 지정한 후 `/(root)` 를 설정하고 **Save**를 누릅니다.
5. 1~2분 뒤에 제공되는 github.io URL로 누구나 접속하여 사용할 수 있습니다!

## 💾 Firebase 통계 연동 방법

접속자 수 기록(IP) 및 당일 횟수 조회 기능을 되살리기 위해 **Firebase Firestore** 서버리스 데이터베이스를 연동합니다.

1. [파이어베이스 콘솔 (https://console.firebase.google.com/)](https://console.firebase.google.com/)에 구글 아이디로 로그인 후 무료 프로젝트를 생성합니다.
2. Firestore Database 메뉴에서 데이터베이스를 만들고, **테스트 모드 (Test mode)** 로 생성합니다. 
   - (경고가 뜨면 `rules` 탭에서 `allow read, write: if true;` 로 두어 개발 및 테스트가 가능하게 합니다.)
3. "프로젝트 설정 (Project Settings)" 으로 가셔서 **웹앱 추가 (`</>`)** 모양의 아이디콘을 클릭하여 앱을 추가 후, 앱의 `firebaseConfig` 값을 확인합니다.
4. 이 코드(레포지토리)의 **`index.html`** 파일을 에디터로 연 후, 하단 `<script>` 부분의 `firebaseConfig` 영역을 본인의 API 키로 바꿔치기 해주세요!
5. 다시 Github에 커밋하면 자동으로 통계가 Cloud에 쌓이는 배포가 완료됩니다.
