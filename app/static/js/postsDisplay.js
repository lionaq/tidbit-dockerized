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