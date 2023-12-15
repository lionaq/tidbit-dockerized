// follow.js

const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
const current_user_id = document.querySelector('meta[name="current_user_id"]').content;

function follow(user_id) {
    const user_prof_id = document.getElementById('user_prof_id')
    const followButton = document.getElementsByClassName('follow-button-' + user_id);
    const unfollowButton = document.getElementsByClassName('unfollow-button-' + user_id);

    //handles follower/following count in user profile
    const followingCount = document.getElementById('userFollowing');
    const followerCount = document.getElementById('userFollowers');

    const followers_count_in_search = document.getElementById('followers-count-in-search-'+user_id)

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

            if(followingCount && current_user_id == user_prof_id.value){ //makes sure following count & user_prof_id elements exists in the page etc.
                console.log("following count in profile changed!");
                followingCount.innerHTML = data['following_count'];
            }

            if(followerCount && current_user_id != user_prof_id.value && user_prof_id.value == user_id){
                console.log("followerCount")
                followerCount.innerHTML = data['following_followers'];
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
    const user_prof_id = document.getElementById('user_prof_id')
    const followButton = document.getElementsByClassName('follow-button-' + user_id);
    const unfollowButton = document.getElementsByClassName('unfollow-button-' + user_id);

    //handles follower/following count in user profile
    const followingCount = document.getElementById('userFollowing');
    const followerCount = document.getElementById('userFollowers');

    const followers_count_in_search = document.getElementById('followers-count-in-search-'+user_id)

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
            
            if(followingCount && current_user_id == user_prof_id.value){
                console.log("following count in profile changed!");
                followingCount.innerHTML = data['following_count'];
            }
            if(followerCount && current_user_id != user_prof_id.value && user_prof_id.value == user_id){
                followerCount.innerHTML = data['following_followers'];
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
