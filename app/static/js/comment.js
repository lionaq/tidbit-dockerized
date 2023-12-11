let commentBody = document.getElementById("commentBody");
let postComment = document.getElementById("postComment");
let cancelComment = document.getElementById("cancelComment");
let textArea = document.getElementsByClassName("textArea");


document.addEventListener("DOMContentLoaded", function () {
    for (let i = 0; i < textArea.length; i++) {
        textArea[i].style.height = 0;
        textArea[i].style.height = textArea[i].scrollHeight + "px";
    }

});

commentBody.addEventListener("focus", function () {
    commentBody.classList.remove("plainline");
    commentBody.classList.add("underline");
    postComment.style.display = "inline";
    cancelComment.style.display = "inline";
});

commentBody.addEventListener("blur", function () {
    commentBody.classList.remove("underline");
    commentBody.classList.add("plainline");
});

cancelComment.addEventListener("click", function () {
    console.log("CANCEL");
    postComment.style.display = "none";
    cancelComment.style.display = "none";
    commentBody.value = "";
    commentBody.style.height = 0;
});

commentBody.oninput = function() {
    commentBody.style.height = "";
    commentBody.style.height = commentBody.scrollHeight + "px"
    if(commentBody.value.trim().length == 0){
        postComment.disabled = true;
    }else{
        postComment.disabled = false;
    }
};

function toggleEdit(comment_id, user_id){
    const commentBodyEdit = document.getElementById('body-'+comment_id+'-'+user_id);
    const commentConfirmEdit = document.getElementById('editConfirm-'+comment_id+'-'+user_id);
    const commentCancelEdit = document.getElementById('editCancel-'+comment_id+'-'+user_id);

    initText = commentBodyEdit.value

    commentBodyEdit.oninput = null
    commentBodyEdit.readOnly = false;
    commentBodyEdit.classList.add("underline");
    commentBodyEdit.selectionStart = commentBodyEdit.selectionEnd = commentBodyEdit.value.length;
    commentBodyEdit.focus();

    commentConfirmEdit.style.display = "inline";
    commentCancelEdit.style.display = "inline";

    commentBodyEdit.oninput = function() {
        commentBodyEdit.style.height = 0;
        commentBodyEdit.style.height = commentBodyEdit.scrollHeight + "px"
        if(commentBodyEdit.value.trim().length == 0 || commentBodyEdit.value.trim() == initText.trim()){
            commentConfirmEdit.disabled = true;
        }else{
            commentConfirmEdit.disabled = false;
        }
    };

    toggleEdit.cancelEdit = function () {
        // Your cancelation code goes here
        commentBodyEdit.readOnly = true;
        console.log("Edit canceled");
        commentConfirmEdit.style.display = "none";
        commentCancelEdit.style.display = "none";
        commentBodyEdit.classList.remove("underline");
        commentBodyEdit.value = initText;
        commentBodyEdit.style.height = 0;
        commentBodyEdit.style.height = commentBodyEdit.scrollHeight + "px"
        
    };
}

