// follow.js
function follow(user_id) {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const current_user_id = document.querySelector('meta[name="current_user_id"]').content;
    console.log(current_user_id)
    const followButton = document.getElementsByClassName('follow-button-' + user_id);
    const unfollowButton = document.getElementsByClassName('unfollow-button-' + user_id);
    const followingCount = document.getElementById('userFollowing');

    fetch('/follow/' + user_id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data)
        if(data['following'] == false){
            console.log("Followed");
            for (let i = 0; i < followButton.length; i++) {
                followButton[i].style.display = "none";
            }
            for(let i = 0; i < unfollowButton.length; i++){
                unfollowButton[i].style.display = "block";
            }

            if(followingCount && current_user_id == user_id){
                console.log("following count in profile changed!");
                followingCount.innerHTML = data['following_count'];
            }
        }
        else{
            console.log("Already Following")
            for (let i = 0; i < followButton.length; i++) {
                followButton[i].style.display = "none";
            }
            for(let i = 0; i < unfollowButton.length; i++){
                unfollowButton[i].style.display = "block";
            }
        }
    });
}

function unfollow(user_id) {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const current_user_id = document.querySelector('meta[name="current_user_id"]').content;
    const followButton = document.getElementsByClassName('follow-button-' + user_id);
    const unfollowButton = document.getElementsByClassName('unfollow-button-' + user_id);
    const followingCount = document.getElementById('userFollowing');

    fetch('/unfollow/' + user_id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data)
        if(data['following'] == true){
            console.log("Unfollowed")
            for (let i = 0; i < followButton.length; i++) {
                followButton[i].style.display="inline";
            }
            for(let i = 0; i < unfollowButton.length; i++){
                unfollowButton[i].style.display = "none";
            }
            
            if(followingCount && current_user_id == user_id){
                console.log("following count in profile changed!");
                followingCount.innerHTML = data['following_count'];
            }
        }
        else{
            console.log("Already unfollowed")
            for (let i = 0; i < followButton.length; i++) {
                followButton[i].style.display="inline";
            }
            for(let i = 0; i < unfollowButton.length; i++){
                unfollowButton[i].style.display = "none";
            }
        }
    });
}
