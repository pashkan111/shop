 import $ from 'jquery';

const comment_form = $('.post_comment');
const btn = $("[data-button]");
comment_form.classList.add('hide');

function open_comment() {
    comment_form.classList.add('show')
    comment_form.classList.remove('hide')
    btn.innerHTML = '<p>Свернуть</p>'
    btn.style.cssText = `
    display: block;
    margin: 0;
    `
};

function close_comment() {
    comment_form.classList.add('hide')
    comment_form.classList.remove('show')
    btn.innerHTML = '<p>Оставить отзыв</p>'
    btn.style.cssText = `
    display: block;
    margin: 0;
    `
};

btn.addEventListener('click', () => {
  if (comment_form.classList.contains('hide')) {
      open_comment();
  } else 
       close_comment();
});


