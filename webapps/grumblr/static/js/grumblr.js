function populateList() {
    $.get("/grumblr/get_posts")
        .done(function(data) {
            var list = $("#post");
            // var userList = $("#user");
            list.data('max-time', data['max-time']);
            list.html('')
            for (var i = data.posts.length - 1; i >= 0; i--) {
                post = data.posts[i];
                // alert(data.comments);
                // alert(post);
                comment_list = data.comments[i];
                // alert(data.posts);
                // if (comments == null) {
                //     alert("null");
                // }
                // if (comments != null) {
                //     alert("enter");
                // }
                // alert(comment_list.comment_list.length);

                var new_post = $(post.html);
                var new_user = $(post.user);
                new_post.data("post-id", post.id);
                new_post.data("user-id", post.user);
                // var new_comment = $("#comment");
                // var new_button = $("#add-comment");
                // new_user.data("post-id", post.id);
                list.append(new_post);
                list.append("<p>Comments:</p>");
                list.append("<p id=total_"+post.id+"></p>");
                // if(post.id==38) {

                //     alert(comment_list.comment_list[0].html);
                //     alert(comment_list.comment_list[1]);
                //     alert(comment_list.comment_list[2]);
                // }
                if (comment_list.comment_list.length != 0) {

                    for (var j = comment_list.comment_list.length - 1; j >= 0; j--) {  
                    // if(post.id==38) {
                    //     alert(j);
                    // } 
                        comment = comment_list.comment_list[j];

                        var new_comment = $(comment.html);
                        if (new_comment != null) {
                          list.append(new_comment);
                        }
                        

                        new_comment.data("comment-id", comment.id);
                    }
                }


                // list.append(commentList);
                // list.append(new_comment);
                // list.append(new_button);
                // list.append("<input id='comment' value=''>");
                // list.append("<button id='add-comment class='add-comment'>Comment</button>");
                list.append("<hr class='featurette-divider'>");

                // list.append("<input id='comment' value="">");


                // userList.append(new_user);
            }
        });
}

function getProfile(e) {
    var id = $(e.target).data("user-id");
    $(e.target).attr("href", "/profile/" + id);
}

function addPost() {
    var postField = $('#post-field');

    $.post("/grumblr/add_post", { post: postField.val() })
        .done(function(data) {


            getUpdates();
            postField.val("").focus();



        });
}

function addComment(e) {
    getUpdates();
    var post_key = $(e.target).data("post-id");

    var commentField = $("#comment_post_" + post_key);

    $.post("/grumblr/add_comment", { comment: commentField.val(), post: post_key })
        .done(function(data) {          
            var list = $("#total_"+post_key);
            list.prepend(data.comment_list[0].html);
            
            commentField.val("");

        })
}

function getUpdates() {
    var list = $("#post");
    var max_time = list.data("max-time")
    $.get("/grumblr/get_changes/" + max_time)
        .done(function(data) {
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                var new_post = $(post.html);
                new_post.data("post-id", post.id);

                list.prepend("<hr class='featurette-divider'>");
                list.prepend("<p id=total_"+post.id+"></p>");
                list.prepend("<p>Comments:</p>");
                
                
                list.prepend(new_post);
                
            }


        });
}


$(document).ready(function() {
    $('#post-form').on('submit', function(e){
        e.preventDefault();
        addPost();
    });
    // $("#add-btn").click(addPost);
    $("#post-field").keypress(function(e) {
        if (e.which == 13) addPost(); });
     $("#post").click(addComment);
    // $(".add-comment").click(addComment);
    $("#comment").keypress(function(e) {
        if (e.which == 13) addComment(); });
$('#comment-form').on('submit', function(e){
    e.preventDefault();
    addComment();
});
    populateList();
    $("#post-field").focus();

    window.setInterval(getUpdates, 5000);

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });


});