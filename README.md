# 🛳 5조 미니1프로젝트 S.A

<br />

### 👥 조원

팀장: 오규화

팀원: 김남경, 유지수, 이재정

<br />

## 🎯 프로젝트 명

제목:

내용:

<br />

## 📑 와이어 프레임

![와이어프레임](./static/imgs/와이어프레임.png)

<br />

## 👀 API 설계

| 기능                        | Method | URL                    | request                                                               | response                                                                                                                                                                  | 간략 설명                                                                                                                                                 |
| --------------------------- | ------ | ---------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [로그인 페이지]             |        | /                      | {'token' : token}                                                     | {'userInfo' : userInfo,<br />'foods' : allFoods}                                                                                                                          | - token이 존재할 경우 main 페이지로 이동 <br />- token이 없을 경우 로그인 페이지 노출                                                                     |
| 회원가입 - 아이디 중복 체크 | POST   | /api/sign_up/check_dup | {'username' : username}                                               | {'exists' : True / False}                                                                                                                                                 | - username 중복 확인                                                                                                                                      |
| 회원가입                    |        | /api/sign_up           |                                                                       |                                                                                                                                                                           | - user가 입력한 username /pw를 받고 pw를 암호화 한 후 DB에 저장                                                                                           |
| 로그인                      |        | /api/sign_in           |                                                                       | {'token' : token}                                                                                                                                                         | - user가 입력한 username / pw를 DB에서 확인 후, 일치하면 로그인 완료! 서버에서는 토큰을 발급하고, 클라이언트는 발급된 토큰을 쿠키에 저장 후 메인으로 이동 |
| [Main 페이지]               |        | /main                  |                                                                       | {'foods' : allFoods}                                                                                                                                                      | - DB에 있는 음식들을 노출하고, 검색 기능을 제공하는 페이지                                                                                                |
| 음식리스트                  |        | /main                  |                                                                       | {'foods' : allFoods}                                                                                                                                                      | 음식들을 노출한다.                                                                                                                                        |
| 검색                        |        | /api/search_foods      | {'inputKeyword' : keyword}                                            | {'foodsList' : list}                                                                                                                                                      | 검색한 키워드에 맞는 음식 결과를 노출한다.                                                                                                                |
| [Detail 페이지]             |        | /detail/<keyword>      |                                                                       | {'foodInfo' : foodInfo, <br />'foodImg' : foodImg, <br />'foodManual' : foodManual, <br />'comments' : comments, <br />'username' : username, <br />'nickname : nickname} | - main페이지에서 음식 Num을 받아서 이동. <br />- 음식의 상세 정보를 보여주고, 음식에 대한 코멘트를 작성/ 확인할 수 있는 페이지                            |
| 코멘트 - 저장               | POST   | /api/save_comment      | {'comment' : comment,<br /> 'foodNum' : foodNum,<br /> 'time' : time} | {'msg' : msg}                                                                                                                                                             | - user가 입력한 comment와 함께 해당 food의 num, 입력한 시간을 받아서 DB에 저장한다.                                                                       |
| 코멘트 - 불러오기           | POST   | /api/get_comments      | {'foodNum' : foodNum}                                                 | { 'commentsList' : list}                                                                                                                                                  | - Detail 페이지 내의 댓글 기능이므로, 해당하는 음식의 Number을 요청받고 DB에서 해당 음식에 대한 댓글만 가져온다.                                          |
| 코멘트 - 삭제               | POST   | /api/delete_comment    | {'username' : username, <br />'comment' : comment}                    | {'msg' : msg}                                                                                                                                                             | - DB에서 해당하는 username과 comment가 일치하는 것을 찾아, 삭제한다.                                                                                      |
