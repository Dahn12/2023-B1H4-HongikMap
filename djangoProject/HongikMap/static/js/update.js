// csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function preprocessingSubmit(e) {
    // 어떤 버튼인지 구분
    if (e.target.id == "buildingButton") {
        // 전체인지 건물하나인지 구분
        if ($('#buildingName').val() == 'ALL') {
            $.ajax({
                url: 'good',
                type: 'POST',
                datatype: 'json',
                data: {
                    'input_val': '111', //대문자 변환해서 소문자도 검색가능
                    'csrfmiddlewaretoken': csrftoken,
                },
                success: function (data) {
                    if (data == "success") {
                        alert('DB저장완료')
                    }

                }
            });
        } else {
            txtName = $('#buildingName').val() + '.txt'
        }


    } else if (e.target.id == "XtoXButton") {

    } else if (e.target.id == "externalNodeButton") {

    }
}
