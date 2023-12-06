document.addEventListener("DOMContentLoaded", function () {
    const lazyLoadPosts = document.querySelectorAll('.lazy-post');

    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: .3
    };

    const observer = new IntersectionObserver(callback, observerOptions);

    lazyLoadPosts.forEach(post => {
      observer.observe(post);
    });

    function callback(entries, observer) {
      entries.forEach(entry => {
        const intersecting = entry.isIntersecting
        if (intersecting) {
          entry.target.style.opacity = '1'
          observer.unobserve(entry.target);
        }
      });
    }
  });

function like(postId){
    console.log("im in")
    const likeCount = document.getElementById('like-count-'+postId);
    const likebutton = document.getElementById('like-icon-'+postId);

    fetch('/like/'+postId, {method: "GET"})
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            likeCount.innerHTML = data["likes"];
            if(data['liked'] == true){
                likebutton.className = "fa-solid fa-heart fa-2xl";
            }else{
                likebutton.className = "fa-regular fa-heart fa-2xl";
            }
        })

}