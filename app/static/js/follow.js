// follow.js
function follow(user_id, event) {
    event.preventDefault();  // Prevent the default form submission behavior

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const followButton = document.getElementById('follow-button-' + user_id);
    const followingCount = document.getElementById('following-count');

    fetch('/follow/' + user_id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data['following_count']) {
            followingCount.textContent = data['following_count'];
        }

        if (data['following']) {
            followButton.textContent = 'Following';
            followButton.classList.remove('btn-primary');
            followButton.classList.add('btn-secondary');
        } else {
            followButton.textContent = 'Follow';
            followButton.classList.remove('btn-secondary');
            followButton.classList.add('btn-primary');
        }
    });
}
