// function onReady(){
//     $("#forward").on("click", function(){
//         $("h1").text("Йеее! Мы поменяли текст заголовка!")
//     })
//
//     $("#backward").on("click", function(){
//         $("h1").text("Это Главная страница сайта")
//     })
// }
//
// $(document).ready(onReady);


function initBootstrapForms() {
    $("form.bootstrap-form").find("input,textarea").addClass("form-control");
    $("form.bootstrap-form").find("input[type='submit']").removeClass("form-control");
}

function initCommenting(){
    $(".comment-input").on("keyup", function(event){
        var input = $(this);
        if(event.keyCode === 13) {
            var comment = $(this).val().trim();
            var post_id = $(this).data("post-id");     // или post_id
            if (comment.length > 0) {
                $.ajax("/post-comment/", {
                    data: {
                        post_id: post_id,
                        comment: comment
                    },
                    success: function(html){
                        $("#comments-list-post-"+post_id).append(html);
                        $(input).val("");
                    }
                })
            }
            return false;
        }
    })
}

$(document).ready(function(){
    initBootstrapForms();
    initCommenting();
});