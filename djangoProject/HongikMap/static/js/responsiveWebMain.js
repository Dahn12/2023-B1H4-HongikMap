//첫시작 설정
window.onload= function (){
    if (screen.width < 500) {
        document.getElementById('navbarToggleExternalContent').classList.remove('collapse-horizontal');
    }

}
window.onresize = function () {
    if (screen.width < 500) {
        document.getElementById('navbarToggleExternalContent').classList.remove('collapse-horizontal');
    } else {
        document.getElementById('navbarToggleExternalContent').classList.add('collapse-horizontal');
    }
}



//변수선언
//##경로표시
let boolDepartureCheck = false;
let boolDestinationCheck = false;





//선그리기
let pathResult = [];
//canvas 엘리먼트를 취득한다.
const canvas = document.getElementById('myCanvas');
// 2d모드의 그리기 객체를 취득한다. => 이 객체를 통해 canvas에 그림을 그릴 수 있다.
const ctx = canvas.getContext("2d");
//색깔
ctx.strokeStyle = '#FF5A5A';
//굵기
ctx.lineWidth = 6;
//꺽인부분처리
ctx.lineCap = 'round';

//선긋는 함수 pathResult에 경로좌표리스트
function drawLine(pathResult) {
    //선 초기화
    ctx.clearRect(0, 0, 1300, 700);
    //새 선 그리기
    ctx.beginPath();

    for (var i = 0; i < pathResult.length - 1; i++) {
        if (pathResult[i].length == 0 || pathResult[i + 1].length == 0) {
            continue;
        }
        //시작점 지정
        ctx.moveTo(pathResult[i][0], pathResult[i][1]);
        //도착점 지정
        ctx.lineTo(pathResult[i + 1][0], pathResult[i + 1][1]);
        //실선 그리기
        ctx.stroke();

    }
}


//클릭하면 콘솔에 좌표 출력
canvas.onclick = function (event) {

    const x = event.clientX - ctx.canvas.offsetLeft;

    const y = event.clientY - ctx.canvas.offsetTop;
    console.log(x, y);
}

let number = 0;
let amenitiesName = 'cafe';


//##입력데이터 백으로 보내기 및 처리된 데이터 받기
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

//변수 선언
let receivedList = [];


//keycode가져오기
let nowKeyboardCode = 0;
$('#autoInput').bind('keydown', function (e) {
    nowKeyboardCode = e.keyCode;

})
$('#autoInput1').bind('keydown', function (e) {
    nowKeyboardCode = e.keyCode;
})

//데이터 보내기, setautocomplete함수밑에서 보내는 동작 구현
function sendingData(inp) { //inp는 input객체

    if (inp == document.getElementById('autoInput')) {
        boolDepartureCheck = false;
    } else {
        boolDestinationCheck = false;
    }
    $.ajax({
        url: 'recommend',
        type: 'POST',
        data: {
            'input_val': inp.value.toUpperCase(), //대문자 변환해서 소문자도 검색가능
            'csrfmiddlewaretoken': csrftoken,
        },
        datatype: 'json',
        success: function (data) {
            receivedList = data['recommendations'];
            autocomplete.setAutocomplete(inp, receivedList); //autocomplete함수를 input객체를 받아 실행
            autocomplete.inputEvent(nowKeyboardCode);
            autocomplete.keydownEvent(nowKeyboardCode);
            console.log(receivedList);
        }
    });
}


// // ##사이드바 햄버거버튼 누르면 그림자화
// let shadowingCheck = 0;
//
// function shadowing() {
//     // 화면 넓이를 측정해 500px이하일때 html 백그라운드와 지도가 밝기감소
//     if (screen.width < 500) {
//         if (shadowingCheck % 2 == 0) {
//             // 햄버거 바 버튼 누르면 shadowing
//             brightnessFromButton = document.getElementsByClassName('brightnessFromButton');
//
//             for (var i = 0; i < brightnessFromButton.length; i++) {
//                 $('#backgroundClick').css('background-color', 'rgba(0,0,0,0.5)');
//                 $('#total').css('background-color', 'rgba(0,0,0,0.5)');
//                 $(brightnessFromButton).css('filter', 'brightness(0.5)');
//
//             }
//
//         } else {
//             for (let i = 0; i < brightnessFromButton.length; i++) {
//                 $('#backgroundClick').css('background-color', 'rgba(0,0,0,0)');
//                 $('#total').css('background-color', 'rgba(0,0,0,0)');
//                 $(brightnessFromButton).css('filter', 'brightness(1)');
//             }
//         }
//         shadowingCheck++;
//     }
//
// }


//##자동완성
// autocomplete 부분을 생성
let autocomplete = (function () {

    let _inp = null;

    let _arr = [];

    let _currentFocus;

    let _setAutocomplete = function (inp, arr) {
        // autocomplete할 배열
        _arr = arr;


        // 기존의 input 값과 같지 않다면, 리스너 해제
        if (_inp === inp) {
            return;
        }

        // 기존 리스너해제
        _removeListener();

        // 새로운 input 의 리스너 추가.
        _inp = inp;
    }

    let inputEvent = function (keyCord) {
        //화살표 및 엔터면 출력된 자동완성 초기화 안한다
        if (keyCord == 40 || keyCord == 38 || keyCord == 13) {
            return false;
        }
        var a, b, i, val = _inp.value;//a,b,i는 지정되지않고 val만 입력값으로 저장
        // 이전 생성된 div 제거
        closeAllLists();

        // 요소 확인
        if (!val) {
            return false;
        }

        // 현재의 포커스의 위치는 없음.
        _currentFocus = -1;

        // autocomplet에서 항목을 보여줄 div 생성하고 이를 a에 준다.
        a = document.createElement("DIV");
        //
        a.setAttribute("id", _inp.id + "autocomplete-list");//속성주기
        // css 적용
        a.setAttribute("class", "autocomplete-items");

        // input 아래의 div 붙이기.
        _inp.parentNode.appendChild(a);

        // autocomplet할 요소 찾기
        for (i = 0; i < _arr.length; i++) {
            // 배열의 요소를 현재 input의 value의 값만큼 자른 후, 같으면 추가한다.

            b = document.createElement("DIV");
            // value의 값 만큼 굵게 표시
            b.innerHTML = "<strong>" + _arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += _arr[i].substr(val.length);
            b.innerHTML += "<input type='hidden' value='" + _arr[i] + "'>";

            // 생성된 div에서 이벤트 발생시 hidden으로 생성된 input안의 value의 값을 autocomplete할 요소에 넣기
            b.addEventListener("click", function (e) {
                if (_inp == document.getElementById('autoInput')) {
                    boolDepartureCheck = true;
                } else {
                    boolDestinationCheck = true;
                }
                _inp.value = this.getElementsByTagName("input")[0].value;
                closeAllLists();
            });

            // autocomplete 리스트를 붙이기.
            a.appendChild(b);

        }
    }
    let lastkeyCord=40;

    let keydownEvent = function (keyCord) {
        var x = document.getElementById(_inp.id + "autocomplete-list");
        // 선택할 요소 없으면 null ,
        if (x) {
            // 태그 네임을 가지는 엘리먼트의 유요한 html 컬렉션을 반환.
            // div의 값을 htmlCollection의 값으로 받아옴.
            x = x.getElementsByTagName("div");
        }

        if (keyCord == 40) {
            // down
            // 현재위치 증가
            _currentFocus++;
            // 현재위치의 포커스 나타내기
            addActive(x, keyCord, lastkeyCord);
        } else if (keyCord == 38) {
            // up
            // 현재위치 감소
            _currentFocus--;
            // 현재위치의 포커스 나타내기
            addActive(x, keyCord, lastkeyCord);
        } else if (keyCord == 13) {
            // enter
            if (_inp == document.getElementById('autoInput')) {
                boolDepartureCheck = true;
            } else {
                boolDestinationCheck = true;
            }
            // keyCord.preventDefault();
            // 현재위치가 아이템 선택창내에 있는 경우
            if (_currentFocus > -1) {
                // 현재 위치의 값 클릭
                if (x) x[_currentFocus].click();
            }
        }
        lastkeyCord=keyCord;
    }
    //바깥 클릭하면 자동완성 사라짐
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });


    let addActive = function (x, keyCode, lastkeyCord) {
        let now_keyCode = keyCode;
        let last_keyCode = lastkeyCord
        if (!x) return false;
        removeActive(x);
        if (_currentFocus >= x.length) _currentFocus = 0;
        if (_currentFocus < 0) _currentFocus = (x.length - 1);
        x[_currentFocus].classList.add("autocomplete-active");
        // 키다운이벤트 따라가기

        if(last_keyCode!=now_keyCode && _currentFocus%6==5){
            $('.autocomplete-items').scrollTop((_currentFocus-5) * 28);
        }

        if(_currentFocus%6==0 && now_keyCode==40)
        {
            $('.autocomplete-items').scrollTop(_currentFocus * 28);
        }
        else if (_currentFocus%6==0 && now_keyCode==38)
        {
            $('.autocomplete-items').scrollTop((_currentFocus-5) * 28);
        }

    }


    let removeActive = function (x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }


    let closeAllLists = function (elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != _inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }


    let _removeListener = function () {
        if (_inp !== null) {
            console.log(_inp)
            _inp.removeEventListener("keyup", inputEvent, false);
            _inp.removeEventListener("keydown", keydownEvent, false);
        }
    }
    return {

        setAutocomplete: function (inp, arr) {
            _setAutocomplete(inp, arr);
        },
        inputEvent: function (keyCode) {
            inputEvent(keyCode);
        },
        keydownEvent: function (keyCode) {
            keydownEvent(keyCode);
        }
    }

})();


//엘리베이터 사용 미사용과 경로 간략화에 관한 전역변수 페이지가 몇번 로드되는지에 대한 값을 저장
var checked = 0;

//##결과경로표시
//테스트케이스
var textList = {
    "elevatorUse": {'distance': 0, 'route': [], 'coordinates': []},
    "elevatorNoUse": {'distance': 0, 'route': [], 'coordinates': []}
};

var k;
var p;

function is_checked() {

    k = p;
    // 1. checkbox element를 찾습니다.
    const checkbox = document.getElementById('my_checkbox');

    // 2. checked 속성을 체크합니다.
    const is_checked = checkbox.checked;

    // 3. 결과를 출력합니다.
    if (is_checked) {
        checked = 1;
        ElevPage(k);
    } else {
        checked = 0;
        ElevPage(k);
    }
}

function ElevPage(name) {
    p = name;
    let show;
    let noShow;
    if (name == 'use') {
        show = document.getElementById("elevatorUse");
        noShow = document.getElementById("elevatorNoUse");
    } else {
        show = document.getElementById("elevatorNoUse");
        noShow = document.getElementById("elevatorUse");
    }
    show.style.display = "block";
    noShow.style.display = "none";
    show.style.textAlign = "center";

    show.replaceChildren();
    //최소 주기

    let timeText = document.createElement('div');
    timeText.setAttribute("id", "timeText");//속성주기
    timeText.innerHTML = "최소";
    show.appendChild(timeText);

    //시간주기
    const seconds = parseInt(textList[show.getAttribute('id')]["distance"]);
    var min = parseInt((seconds % 3600) / 60);
    var sec = seconds % 60;

    let newDivTime = document.createElement('div');
    newDivTime.setAttribute("id", "time");//속성주기
    if (min == 0) {
        newDivTime.innerHTML = sec + "초";
    } else {
        newDivTime.innerHTML = min + "분 " + sec + "초";
    }
    show.appendChild(newDivTime);

    var j = 1;


    //경로 총 길이
    const ways = textList[show.getAttribute('id')]['route'].length;

    //경로에 포함되는 건물들 배열
    var buildings_in_ways = [];

    for (var i = 0; i < textList[show.getAttribute('id')]['route'].length; i++) {
        //전체 경로 돌면서 각 경로의 첫번째 알파벳을 배열에 push
        var x = textList[show.getAttribute('id')]['route'][i];
        var y = x.charCodeAt(0);

        if (65 <= y && y < 90) {
            buildings_in_ways.push(x[0]+"동");
        }
        else if(y==90){ //z동만 예외 z1,z2,z3는 두글자 따와야됨
            buildings_in_ways.push(x[0]+x[1]+"동");

        }
        else{
            buildings_in_ways.push(x);
        }

    }

    var set = new Set(buildings_in_ways);
    var Set_buildings_in_ways = Array.from(set);

    console.log(Set_buildings_in_ways);

    for (var q = 0; q < Set_buildings_in_ways.length; q++) {
        Set_buildings_in_ways[q] = Set_buildings_in_ways[q];
    }


    if (checked == 1) //간략 경로
    {
        console.log("checked");

        for (var m = 0; m < Set_buildings_in_ways.length; m++) {
            let newDiv = document.createElement('div');
            newDiv.style.textAlign = "center";
            newDiv.innerHTML = Set_buildings_in_ways[m];
            show.appendChild(newDiv);

            if (m + 1 < Set_buildings_in_ways.length) {
                let arrow_image = document.createElement('i');
                arrow_image.setAttribute('class', 'bi bi-caret-down-fill');
                show.appendChild(arrow_image);
            }
        }
    } else // 상세 경로
    {
        console.log("not checked");

        for (var i = 0; i < textList[show.getAttribute('id')]['route'].length; i++) {
            let newDiv = document.createElement('div');
            newDiv.style.textAlign = "center";
            newDiv.innerHTML = textList[show.getAttribute('id')]['route'][i];
            show.appendChild(newDiv);

            if (i < textList[show.getAttribute('id')]['route'].length - 1) {
                let arrow_image = document.createElement('i');
                arrow_image.setAttribute('class', 'bi bi-caret-down-fill');
                show.appendChild(arrow_image);
            }
        }

    }

    show.appendChild(document.createElement('br'));
    drawLine(textList[show.getAttribute('id')]["coordinates"]);

    console.log(ways);

}




//출발지, 도착지가 옳은 형식인지 체크
function getDirectionCheck() {
    if (boolDepartureCheck && boolDestinationCheck) {
        return true;
    } else if (!boolDepartureCheck && boolDestinationCheck) {
        alert('출발지를 입력하세요.');
        return false;
    } else if (boolDepartureCheck && !boolDestinationCheck) {
        alert('도착지를 입력하세요.');
        return false;
    } else {
        alert('출발지, 도착지를 입력하세요.');
        return false;
    }
}



// 스피너 안보이게 
$("#mySpinner").hide();

// 길찾기 버튼 이벤트
function submitCheck(event) {
    //submit될 때 페이지 리로드 방지
    //event.preventDefault();

    var departure = document.getElementById("autoInput").value;
    var destination = document.getElementById("autoInput1").value;
    departure = departure.toUpperCase();//소문자 대문자 변환
    destination = destination.toUpperCase();

    //출발지 도착지형식이 참이면 백으로 출발지 도착지 보내기
    if (getDirectionCheck()) {
        //결과경로창 보이게끔

        $.ajax({
            url: 'place_submit',
            type: 'POST',
            data: {
                'departure': departure, 'destination': destination,
                'csrfmiddlewaretoken': csrftoken,
            },
            datatype: 'json',
            beforeSend : function(request){
                // Performed before calling Ajax
                $("#mySpinner").show();
                document.getElementById("showRoute").style.visibility = "hidden";
                document.getElementById("elevatorCheck").style.visibility = "hidden";
                document.getElementById("checkbox_check").style.visibility = "hidden";
              },
            success: function (data) {
                document.getElementById("showRoute").style.visibility = "visible";
                document.getElementById("elevatorCheck").style.visibility = "visible";
                document.getElementById("checkbox_check").style.visibility = "visible";
                $("#mySpinner").hide();
                textList = data;
                //엘리베이터 시간주기
                console.log(textList);
                elevTimePlus(textList);
                ElevPage('use');
                drawLine(textList["elevatorUse"]["coordinates"]);
            },

        });
    }
}


// 엘리베이터 실제시간주기
function elevTimePlus(textList) {
    let seconds = parseInt(textList["elevatorUse"]["distance"]);
    for (let i = 0; i < textList["elevatorUse"]["route"].length; i++) {
        if (textList["elevatorUse"]["route"][i].includes("엘리베이터")) {
            seconds += 60;//한번탈때 엘리베이터 두번주므로 120초를 두번에 나눠서 준다
        }
    }
    textList["elevatorUse"]["distance"] = seconds;
}

function amenitiesShow(name, e) {
    if (e.target.checked) {
        document.getElementById(name).style.visibility = 'visible';
    } else {
        document.getElementById(name).style.visibility = 'hidden';
    }
}

let amenitiesDic = {
    'cafe': [["R동 L층 카페나무", 193, 452], ["와우관 4층 카페나무", 443, 126], ["R동 2층 카페 그라찌에", 271, 439], ["R동 2층 다과점 파프리카", 260, 508], ["카페 캠퍼", 916, 529], ["A동 1층 카페드림", 904, 296], ["C동 8층 간이카페", 1005, 230], ["중앙도서관 2층 북카페", 511, 188], ['집가고싶다', 213, 578]],
    'convenienceStore': [["R동 B2 홍익대학서적", 234, 463], ["와우관 4층 편의점", 433, 126], ["R동 3층 편의점", 232, 444], ["R동 L층 한가람 문구센터", 276, 430], ["제2기숙사 지하1층 편의점", 944, 482],['집가고싶다', 213, 578]],
    'restaurant': [["제2기숙사 학생식당", 942, 486], ["향차이", 922, 543],['집가고싶다', 213, 578]],
    'medicalRoom': [["약국(원이 약국)", 922, 562], ["건강진료센터", 576, 271],['집가고싶다', 213, 578]],
    'readingRoom': [["T동 3,4층 열람실", 827, 511], ["R동 8층 열람실", 263, 543], ["중앙도서관 열람실", 527, 231],['집가고싶다', 213, 578]]
}

let amenitiesText = {
    'R동 L층 카페나무':['(평일, 학기중) 08:00 – 21:00', '(평일, 방학중) 08:30 – 20:30', '(주말, 학기중) 09:00 – 20:00', '(주말, 방학중) 09:00 – 19:30'],
    '와우관 4층 카페나무':['(평일, 학기중) 08:30 – 20:00', '(평일, 방학중) 08:30 – 19:30', '(주말/공휴일) 09:00 – 18:00'],
    'R동 2층 카페 그라찌에':['(평일) 08:00 – 20:00', '(주말) 09:00 – 18:00'],
    'R동 2층 다과점 파프리카':['am08:00 – pm08:00'],
    '카페 캠퍼':[],
    'A동 1층 카페드림':['학기중','(평일) 1층 08:00 – 20:00, 2층 08:00~23:00', '(주말) 1층 09:00 – 19:00, 2층 09:00~23:00','방학중','(평일) 1층 10:00~17:00, 2층 09:00~23:00','(주말) 1층 10:00~17:00, 2층 09:00~23:00'],
    'C동 8층 간이카페':['(평일, 학기중) 08:30 - 20:00','(평일, 방학중) 08:30 - 18:00','(일요일/공휴일) 휴무'],
    '중앙도서관 2층 북카페':['(평일, 학기중) 10:00 - 19:00','(평일, 방학중) 09:00 - 18:00','(일요일/공휴일) 휴무'],
    'R동 B2 홍익대학서적':['평일 : am09:00 - pm07:00 (학기중)','토요일 : am09:00 - pm02:00 (학기중)','일요일 및 공휴일 휴무'],
    '와우관 4층 편의점':['(평일, 학기중) 08:30 - 21:00','(평일, 방학중) 08:30 - 20:00','(주말/공휴일) 08:30 - 18:00'],
    'R동 3층 편의점':['(평일, 학기중) 08:00 - 21:00','(평일, 방학중) 08:00 - 18:00','(주말/공휴일) 휴무'],
    'R동 L층 한가람 문구센터':['평일 : am08:30 - pm8:30','주말 및 공휴일 : am10:00 - pm08:00'],
    '제2기숙사 지하1층 편의점':[],
    '제2기숙사 학생식당':['08:00~09:00(조식), 11:30~14:30(중식), 17:30~19:20(석식)','[방학중 주말/공휴일] 휴무'],
    '향차이':[],
    '약국(원이 약국)':['(평일) 08:30 - 23:00','(주말) 11:00 - 22:00'],
    '건강진료센터':[],
    'T동 3,4층 열람실':['06:00-23:00 연중무휴','(제4공학관 4층 일반열람실 24시간 개방)'],
    'R동 8층 열람실':['06:00-23:00 연중무휴'],
    '중앙도서관 열람실':['06:00-23:00 연중무휴'],
    '집가고싶다':['죽겠어요..'],
}

function amenitiesInMap() {
    //지도위 편의시설 전부 삭제
    $('#amenitiesOnMap div').empty();
    //위치조정
    //위치조정은 기본 1300*700px의 지도 위치를 기준으로 한다.
    //이 함수는 페이지 로드될 떄와 화면크기가 변할때 실행된다.

    //화면비율
    let widthRatio = document.getElementById('background').getBoundingClientRect().width / 1300;
    let heightRatio = document.getElementById('background').getBoundingClientRect().height / 700;
    for (let key in amenitiesDic) {
        for (let i = 0; i < amenitiesDic[key].length; i++) {
            //제이쿼리를 통해 img의 속성와 css를 주고 div안에 넣어준다
            if (amenitiesDic[key][i][0]=='집가고싶다') {
                $('<img>').attr('src', '../../static/logo/' + key + '.svg').attr('onclick', 'amenitiesTitle(event, this)').attr('title', amenitiesDic[key][i][0]).css('width', 32 * widthRatio + 'px').css('height', 32 * heightRatio + 'px').css('left', widthRatio * amenitiesDic[key][i][1]).css('top', heightRatio * amenitiesDic[key][i][2]).css('position', 'absolute').css('opacity', '0').css('z-index','3').appendTo(document.getElementById(key));

                continue;
            }
            $('<img>').attr('src', '../../static/logo/' + key + '.svg').attr('onclick', 'amenitiesTitle(event, this)').attr('title', amenitiesDic[key][i][0]).css('width', 32 * widthRatio + 'px').css('height', 32 * heightRatio + 'px').css('left', widthRatio * amenitiesDic[key][i][1]).css('top', heightRatio * amenitiesDic[key][i][2]).css('position', 'absolute').css('z-index','3').appendTo(document.getElementById(key));

        }
    }
}


amenitiesInMap();

//화면 크기 변할 때 편의시설 조정
window.onresize = function () {
    amenitiesInMap();
}



// 편의시설 카드띄우기
function amenitiesTitle(e, img) {
    let title = $(img).attr("title");

    let titleWithoutSpace = title.replace(/ /g, '_')
    console.log(titleWithoutSpace);
    // 카드 히든 제거
    $('.card').css('display', 'flex');
    // 이미지 넣어 주기
    $('.card-img-top').attr('src', '../../static/logo/amenitiespic/'+titleWithoutSpace+'.jpg');
    // 타이틀
    $('.card-title').html('<h3>'+title+'</h3>');
    let textWithList = '';
    // text 내용물 만드는 과정
    for (let list in amenitiesText[title]) {
        console.log(list);
        list = '<li>' + amenitiesText[title][list] +'</li>';
        textWithList += list ;
    }
    textWithList = '<ul>'+ textWithList +'</ul>';
    $('.card-text').html(textWithList);

}

$('#close').click(function () {
    document.getElementById('card').style.display = 'none'
});



// 뒷배경 누르면 사이드바사라짐
function backgroundClick(e) {

    document.getElementById('navbarToggleExternalContent').classList.remove('show');
    // shadowing();

}
// document.getElementById('backgroundClick').addEventListener("click", function (e) {
//
// });

