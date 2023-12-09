function like(postId){
    console.log("im in");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const likeCount = document.getElementById('like-count-'+postId);
    const likebutton = document.getElementById('like-icon-'+postId);

    fetch('/like/'+postId, 
      { method:'POST',
        headers: {
        'X-CSRFToken': csrfToken
      }})
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            likeCount.innerHTML = data["likes"];
            if(data['liked'] == true){
                likebutton.className = "fa-solid fa-heart fa-2xl";
            }else{
                likebutton.className = "fa-regular fa-heart fa-2xl";
            }
        });

}