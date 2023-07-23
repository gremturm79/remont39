'use strict';

/* edit_account */
let editbut = document.getElementById('edit_account')
let edit = document.getElementById('edit') /* блок формы редактирования */
console.log(edit)
console.log(editbut)
editbut.addEventListener('click', opentEditAccount);

function opentEditAccount() {
    edit.style.display = 'block'
}
let editclose = document.querySelector('.edit_close')
editclose.addEventListener('click', closeEditAccount)
function closeEditAccount() {
    edit.style.display = 'none'
}

let imagefavourite = document.querySelector('image-window')
let butimage = document.getElementById('close-block-{{ image.id }}')
imagefavourite.addEventListener('click', clouseImageFavourite)
function clouseImageFavourite() {
    butimage.style.display = 'none'
}



let leavereview = document.getElementById('leave_review')
let formreviewpersonal = document.getElementById('main_review_personal')
leavereview.addEventListener('click', openFormReview)

function openFormReview() {
    formreviewpersonal.style.display = 'flex'
}
let closereviews = document.getElementById('review_close')
closereviews.addEventListener('click', closeFormReviews)

function closeFormReviews() {
    formreviewpersonal.style.display = 'none'
}

/* setTimeout(function () {
    document.getElementsByClassName('warning').style.display = 'none';
}, 5000); */

/* форма отзыва на странице отзыва */
let openreview = document.getElementById('open_review')
let reviewform = document.getElementById('review_form')
openreview.addEventListener('click', openReview)

function openReview() {
    reviewform.style.display = 'flex'
}

let reviewsclose = document.getElementById('reviews_close')
reviewsclose.addEventListener('click', closeReviews)
function closeReviews() {
    reviewform.style.display = 'none'
}
const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
    myInput.focus()
})
/* убрать информационное окно */

$('.add-favourite').on('click', function () {

    let image_id = $(this).data('id');

    $.ajax({

        url: '/add-favourite/',

        type: 'GET',

        data: {

            'image_id': image_id

        },

        success: function (data) {

            alert('Image added to favourites!');

        }

    });

});

