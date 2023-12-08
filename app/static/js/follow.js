// follow.js
function follow(user_id) {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const followButton = document.getElementById('follow-button-' + user_id);
    const unfollowButton = document.getElementById('unfollow-button-' + user_id);
    fetch('/follow/' + user_id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
    });
    unfollowButton.style.display = "inline";
    followButton.style.display="none";
}

function unfollow(user_id) {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const followButton = document.getElementById('follow-button-' + user_id);
    const unfollowButton = document.getElementById('unfollow-button-' + user_id);
    fetch('/unfollow/' + user_id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
    });
    unfollowButton.style.display = "none";
    followButton.style.display="inline";
}
