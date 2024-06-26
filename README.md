프로젝트
 - 팀원의 정보를 입력하여 사용자에게 정보를 노출 해주는 사이트 제작

사용하는 기술
 - Flask
 - render_template
 - request
 - redirect
 - url_for
 - SQLAlchemy
 - Jquery
 - html
 - css

기능 상세
  - bootstrap 제공하고 있는 modal 이용 하여 이름, 한 줄 소개, mbti, 장점, 협업 스타일, 우리팀의 약속,블로그 주소 입력 받아 DB에 저장
  - 디자인을 하기 어려워 bootstrap에서 제공하는 템플릿 중 Album 사용 이후 필요 없는 버튼삭제 및 footer 수정
  - 리스트 : 추가 된 멤버는 메인에 리스트로 출력
  - 추가 : 메인 페이지에 있는 버튼으로 통해 멤버를 추가 할 수 있음.
  - 상세 : 메인 페이지에서 선택한 팀원의 상세 정보를 보여주는 페이지 제작
  - 수정 : 메인 페이지에서 선택한 팀원의 정보를 수정하여 DB에 저장하는 페이지 및 BackEnd 코드 제작
  - 삭제 : 메인 페이지에서 선택한 팀원의 정보를 선택하여 DB에 선택한 팀원의 정보를 삭제 하는 페이지 및 BackEnd 코드 제작

데이터 베이스 구조
  - id        primary_key
  - name      이름
  - oneline   한줄소개
  - mbti      mbti
  - good      장점
  - about     협업 스타일 소개
  - promise   우리 팀의 약속
  - blogurl    블로그 주소

API
  - 메인          /
  - 멤버 추가     /user/create/          Get
  - 멤버 상세     /document/<ind:id>     Get
  - 멤버 수정     /update/<int:user_id>  Post
  - 멤버 삭제     /user/del/<int:id>     Get


설치 방법
git clone https://github.com/SHY-89/MiniProject.git .
pip install -r requirements.txt
