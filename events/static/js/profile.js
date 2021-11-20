$(document).ready(function () {
    //change user's role at the profile page
    $('#submitButton').click(function () {
        confirm("Are you sure to change this user's role? ")
        var change_role_url = $(this).siblings('#role-options').attr('data-ajax-url');
        var user_id = $(this).siblings('#role-options').attr('data-user-id');
        var user_role = $(this).siblings('#role-options').val()
        $.ajax({
            url: change_role_url,
            data: {
                user_id: user_id,
                user_role: user_role,
            },
            // Whether this is a POST or GET request
            type: "POST",
            // The type of data we expect back
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            context: this
        })
            .done(function (json) {
                if (json.success === 'success') {
                    var new_role = json.user_role;
                    console.log(new_role);
                    $(this).siblings('ul').children('li').children('span#new-role').text(new_role);
                } else {
                    alert("Error: " + json.error)
                }
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
                console.log(user_id)
            })
    });

    //add/edit comment
    $('#submitCommentButton').click(function () {

        var add_comment_url = $(this).parent().attr('data-ajax-url');
        var username = $(this).parent().attr('data-user-name');
        var event_id = $(this).parent().attr('data-event-id');
        var text = $(this).siblings('#textEditor').val();
        var edit_or_add =  $(this).parent().attr('data-operation-type');
        var event_detail_url = "events/"+ event_id + "/edit"
        console.log(edit_or_add)
        console.log(username)
        console.log(event_id);
        console.log(text);
        $.ajax({
            url: add_comment_url,
            data: {
                username: username,
                event_id: event_id,
                text: text,
            },
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            context: this
        })
            .done(function () {
                if(edit_or_add === "add"){
                      location.reload()
                }
                else{
                    location.replace(document.referrer);
                }
            })
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
    });

    //delete a comment
    $('.deleteComment').click(function () {
        var approval = confirm("Do you want to delete");
        if(approval === true) {
            var delete_comment_url = $(this).parent().attr('data-ajax-url');
            var comment_id = $(this).parent().attr('data-comment-id');
            console.log(delete_comment_url)
            console.log(comment_id);
            $.ajax({
                url: delete_comment_url,
                data: {
                    comment_id: comment_id,
                },
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                context: this
            })
                .done(function () {
                    alert("you successfully delete a post")
                    location.reload();
                })
                .fail(function (xhr, status, errorThrown) {
                    alert("Sorry, there was a problem!");
                    console.log("Error: " + errorThrown);
                    console.log("Status: " + status);
                    console.dir(xhr);
                })
        }
    });


});