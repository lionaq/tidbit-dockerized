document.addEventListener("DOMContentLoaded", function () {
  console.log("lazyLoad initialized")
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

  // Select the target node
var targetNode = document.getElementById('contentContainer');

// Options for the observer (which mutations to observe)
var config = { childList: true };

// Callback function to execute when mutations are observed
var callback = function (mutationsList, observer) {
    for (var mutation of mutationsList) {
        if (mutation.type === 'childList') {
            // Check if nodes have been added
            if (mutation.addedNodes.length > 0) {
                // Do something, as a div has been appended
                console.log('Div has been appended!');
            }
        }
    }
};

// Create an observer instance linked to the callback function
var observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(targetNode, config);