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

function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('정상적으로 로그아웃 되었습니다.')
    window.location.href = "/"
}


function nav_show() {
    if ($(".nav").css("display") == "none") {
        $(".nav").show();
    } else {
        $(".nav").hide();
    }
}

function search_ingredients() {
    let value = $(".search-input").val();
    console.log(value);
}

function likeHeart() {
    console.log("ㅇㅇㅇ");
}

$(document).ready(function () {
    // get_list();
});

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
