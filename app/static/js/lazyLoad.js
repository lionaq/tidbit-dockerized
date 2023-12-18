function startIntersectionObserver(elements, options) {
  const observer = new IntersectionObserver(callback, options);

  elements.forEach(element => {
    observer.observe(element);
  });

  function callback(entries, observer) {
    entries.forEach(entry => {
      const intersecting = entry.isIntersecting;
      if (intersecting) {
        entry.target.style.opacity = '1';
        observer.unobserve(entry.target);
      }
    });
  }
}
