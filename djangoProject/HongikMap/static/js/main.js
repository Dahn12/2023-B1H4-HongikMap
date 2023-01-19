const bookBtn = document.querySelector('.bookmark-btt');
const section = document.querySelector('section');
const label = document.querySelector('label');

// 이부분이 발생시키기
bookBtn.addEventListener('click', function(){
	section.style.left = 0;
	label.style.opacity = 0;
})

//이부분이 없애기
bookBtn.addEventListener('blur',function(){
	section.style.left = '-200px';
	label.style.opacity = 1;
})
