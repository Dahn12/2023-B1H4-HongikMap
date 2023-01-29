//##선그리기

//테스트케이스
let pathResult = [[207,538],[240,490],[294,436],[445,225],[401,210],[461,79],];
//canvas 엘리먼트를 취득한다.
const canvas = document.getElementById('myCanvas');
// 2d모드의 그리기 객체를 취득한다. => 이 객체를 통해 canvas에 그림을 그릴 수 있다.
const ctx = canvas.getContext("2d");
//색깔
ctx.strokeStyle = '#FF5A5A';
//굵기
ctx.lineWidth = 6;

//선긋는 함수 pathResult에 경로좌표리스트
function drawLine(pathResult){
    //선 초기화
    ctx.clearRect(0, 0, 1300, 700);
    //새 선 그리기
    ctx.beginPath();
    // 출발점 지정
    ctx.moveTo(pathResult[0][0], pathResult[0][1]);

    for(var i=0; i<pathResult.length-1; i++){
        //도착점 지정
        ctx.lineTo(pathResult[i+1][0], pathResult[i+1][1]);
        //실선 그리기
        ctx.stroke();
    }
    
}

//임시 함수 실행. 리스트 받으면 호출되어야함
drawLine(pathResult);

//클릭하면 콘솔에 좌표 출력
canvas.onclick = function(event){

    const x = event.clientX - ctx.canvas.offsetLeft; 

    const y = event.clientY - ctx.canvas.offsetTop; 
    console.log(x, y);
}



//##편의시설 아이콘띄우기
function convenienceIcon(name){
    document.getElementById('cafe').style.display="none";
    document.getElementById('convi').style.display="none";
    document.getElementById('food').style.display="none";
    document.getElementById('hosp').style.display="none";
    document.getElementById('study').style.display="none";
    if(name == 'cafe'){ 
        document.getElementById("cafe").style.display="block";
    } else if(name == 'convi'){
        document.getElementById("convi").style.display="block";
    } else if(name == 'food'){
        document.getElementById("food").style.display="block";
    } else if(name == 'hosp'){
        document.getElementById("hosp").style.display="block";
    } else if(name == 'study'){
        document.getElementById("study").style.display="block";
    }
    
}




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
let receivedList =[];

//데이터 보내기, setautocomplete함수밑에서 보내는 동작 구현
function sendingData(inp){ //inp는 input객체

    $.ajax({
        url: 'recommend',
        type: 'POST',
        data: {'input_val':inp.value.toUpperCase(), //대문자 변환해서 소문자도 검색가능
        'csrfmiddlewaretoken':csrftoken,
        },
        datatype: 'json',
        success: function(data){
            receivedList = data['recommendations'];
            autocomplete.setAutocomplete(inp, receivedList); //autocomplete함수를 input객체를 받아 실행
            console.log(receivedList);
        }
    });
}

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
        _inp.addEventListener("keyup", inputEvent);
        _inp.addEventListener("keydown", keydownEvent);

    }

    let inputEvent = function (e) {
        //화살표 및 엔터면 출력된 자동완성 초기화 안한다
        if (e.keyCode == 40 || e.keyCode == 38 || e.keyCode == 13) {
            return false;
        }
        var a, b, i, val = this.value;//a,b,i는 지정되지않고 val만 입력값으로 저장
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
        a.setAttribute("id", this.id + "autocomplete-list");//속성주기
        // css 적용 
        a.setAttribute("class", "autocomplete-items");

        // input 아래의 div 붙이기.
        this.parentNode.appendChild(a);

        // autocomplet할 요소 찾기
        for (i = 0; i < _arr.length; i++) {
            // 배열의 요소를 현재 input의 value의 값만큼 자른 후, 같으면 추가한다.
            if (_arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                b = document.createElement("DIV");
                // value의 값 만큼 굵게 표시 
                b.innerHTML = "<strong>" + _arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += _arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + _arr[i] + "'>";

                // 생성된 div에서 이벤트 발생시 hidden으로 생성된 input안의 value의 값을 autocomplete할 요소에 넣기
                b.addEventListener("click", function (e) {
                    _inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });

                // autocomplete 리스트를 붙이기.
                a.appendChild(b);
            }
        }
    }

    let keydownEvent = function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        // 선택할 요소 없으면 null ,
        if (x) {
            // 태그 네임을 가지는 엘리먼트의 유요한 html 컬렉션을 반환.
            // div의 값을 htmlCollection의 값으로 받아옴.
            x = x.getElementsByTagName("div");
        }

        if (e.keyCode == 40) {
            // down
            // 현재위치 증가
            _currentFocus++;
            // 현재위치의 포커스 나타내기
            addActive(x);
        } else if (e.keyCode == 38) {
            // up
            // 현재위치 감소
            _currentFocus--;
            // 현재위치의 포커스 나타내기
            addActive(x);
        } else if (e.keyCode == 13) {
            // enter
            e.preventDefault();
            // 현재위치가 아이템 선택창내에 있는 경우
            if (_currentFocus > -1) {
                // 현재 위치의 값 클릭
                if (x) x[_currentFocus].click();
            }
        }
    }
    //바깥 클릭하면 자동완성 사라짐
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });


    let addActive = function (x) {
        if (!x) return false;
        removeActive(x);
        if (_currentFocus >= x.length) _currentFocus = 0;
        if (_currentFocus < 0) _currentFocus = (x.length - 1);
        x[_currentFocus].classList.add("autocomplete-active");
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
    }

})();






//##결과경로표시
//테스트케이스
var textList = {
    "elevatorUse":[10, ['I101','I102','I103','I104']],
    "elevatorNoUse":[13,['I105','I106','I107','I108']]
};


let ElevUsePageDiv = document.getElementById("ElevUsePage");
let ElevNoUsePageDiv = document.getElementById("ElevNoUsePage");
function ElevUsePage(){
    //Elev체크했을때 div표시
    ElevUsePageDiv.style.display="block";
    ElevNoUsePageDiv.style.display="none";


    ElevUsePageDiv.replaceChildren();
    //최소 주기
    let timeText = document.createElement('div');
    timeText.setAttribute("id", "timeText");//속성주기
    timeText.innerHTML="최소";
    ElevUsePageDiv.appendChild(timeText);

    //시간주기
    let newDivTime = document.createElement('div');
    newDivTime.setAttribute("id", "time");//속성주기
    newDivTime.innerHTML=textList["elevatorUse"][0]+"분";
    ElevUsePageDiv.appendChild(newDivTime);

    for (var i=0; i<textList["elevatorUse"][1].length;i++){
        let newDiv = document.createElement('div');
        newDiv.innerHTML=textList["elevatorUse"][1][i];
        ElevUsePageDiv.appendChild(newDiv);
    }


}

function ElevNoUsePage(){
    ElevUsePageDiv.style.display="none";
    ElevNoUsePageDiv.style.display="block";

    //자식모두지우고 받은리스트 추가
    ElevNoUsePageDiv.replaceChildren();

     //최소 주기
    let timeText = document.createElement('div');
    timeText.setAttribute("id", "timeText");//속성주기
    timeText.innerHTML="최소";
    ElevNoUsePageDiv.appendChild(timeText);

    //시간주기
    let newDivTime = document.createElement('div');
    newDivTime.setAttribute("id", "time");//속성주기
    newDivTime.innerHTML=textList["elevatorNoUse"][0]+"분";
    ElevNoUsePageDiv.appendChild(newDivTime);

    for (var i=0; i<textList["elevatorNoUse"][1].length;i++){
        let newDiv = document.createElement('div');
        newDiv.innerHTML=textList["elevatorNoUse"][1][i];
        ElevNoUsePageDiv.appendChild(newDiv);
    }
}




// 경로표시

//위 리스트를 돌려보면서 input이 있는지 체크
function find(inp){
  for (const key in receivedList){  

    if (inp==receivedList[key]){
      return true;
    }
  }
  return false;
}
//리스트에 둘 다 있으면 true
function submitCheck(event) {
    //submit될 때 페이지 리로드 방지
    event.preventDefault();

    var departure = document.getElementById("autoInput").value;
    var destination = document.getElementById("autoInput1").value;
    departure = departure.toUpperCase();//소문자 대문자 변환
    destination = destination.toUpperCase();

    if (find(departure) && find(destination)) {
    document.getElementById("showRoute").style.visibility="visible";
    return true;

    } else{
      return false;
    }
}
