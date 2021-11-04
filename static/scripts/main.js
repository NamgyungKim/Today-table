// $.ajax({
//     type: 'GET',
//     url: '/main',
//     data:{},
//     success: function (response) {
//         alert("ajax success")	//연결을 확인한다
//         let items = JSON.parse('{{ items | tojson | safe}}');
//         // console.log(response)
//         console.log(items)
//     }
// })

function toggle_like(food_num, type) {
  let $a_like = $(`#${food_num} a[aria-label='heart']`);
  let $i_like = $a_like.find("i");
  if ($i_like.hasClass("fa-heart")) {
    $.ajax({
      type: "POST",
      url: "/update_like",
      data: {
        food_num_give: food_num,
        type_give: type,
        action_give: "unlike",
      },
      success: function (response) {
        $i_like.addClass("fa-heart-o").removeClass("fa-heart");
        $a_like.find("span.like-num").text(response["count"]);
      },
    });
  } else {
    $.ajax({
      type: "POST",
      url: "/update_like",
      data: {
        food_num_give: food_num,
        type_give: type,
        action_give: "like",
      },
      success: function (response) {
        $i_like.addClass("fa-heart").removeClass("fa-heart-o");
        $a_like.find("span.like-num").text(response["count"]);
      },
    });
  }
}

function sign_out() {
  $.removeCookie("mytoken", { path: "/" });
  alert("정상적으로 로그아웃 되었습니다.");
  window.location.href = "/";
}

function nav_show() {
  if ($(".nav").css("display") == "none") {
    $(".nav").show();
    $(".nav").addClass("show");
  } else {
    $(".nav").hide();
    $(".nav").removeClass("show");
  }
}

function show_modal() {
  $(".modal").removeClass("hidden");
}

function hide_modal() {
  $(".modal").addClass("hidden");
}

$(document).ready(function () {
  // get_list();
});

// 프로필클릭시 로그아웃버튼 show
$('.user').click(function(){
  if($(".nav").hasClass("show")){
    $(".nav").removeClass("show");
  }else{
    $(".nav").addClass("show");
  }
})
//top버튼 클릭시 위로스크롤
$( '#top-btn' ).click( function() {
  $( 'html, body' ).animate( { scrollTop : 0 }, 400 );
  return false;
} );
//top버튼 스트롤200부터 보임
$( window ).scroll( function() {
  if ( $( this ).scrollTop() > 200 ) {
    $( '#top-btn' ).fadeIn();
  } else {
    $( '#top-btn' ).fadeOut();
  }
} );

function get_list() {
  $.ajax({
    type: "GET",
    crossDomain: true,
    url: "http://openapi.foodsafetykorea.go.kr/api/sample/COOKRCP01/json/1/5",
    data: {},
    success: function (response) {
      let dishes = response["COOKRCP01"]["row"];

      dishes.forEach((dish, idx) => {
        let dishName = dish["RCP_NM"];
        let kind = dish["RCP_PAT2"];
        let url = dish["ATT_FILE_NO_MAIN"];

        console.log(dishName, kind, url);
        if (idx < 3) {
          let temp_html_rc = `<img src="${url}" alt="dish-image"/>`;
          $(".image-container").append(temp_html_rc);
        }

        let temp_html = `<div class="dish">
                                    <img src="${url}" alt="dish-image"/>
                                    <h3 class="title">${kind} ${dishName} </h3>
                                </div>`;

        $(".dish-lists").append(temp_html);
      });
    },
  });
}



//// 추천 요리 크기변경
//// 중간 라인 삭제
//// input form 색 디테일에 있는 댓글 폼과 변경
//// 요리 이름 한줄 처리
//// 미디어 쿼리 적용
//// 로고 url 홈페이지로 이동
//// 요리 description 불투명 처리
// 모달
// tab키 포커스 확인

// 검색 기능
