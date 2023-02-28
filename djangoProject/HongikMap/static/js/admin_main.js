// 이 부분은 사이드 바 txt 클릭했을때 iframe url 변경해준다
$(document).ready(function(e) {
/* a요소를 클릭 했을 시 */
    $('.link').click(function(){
/* iframe 요소의 src 속성값을 a 요소의 data-url 속성값으로 변경 */
        $('#iframe').attr('src',$(this).attr('data-url'));
        })
});