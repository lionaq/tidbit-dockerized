function save(postId){
    console.log("im in");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    const saveButton = document.getElementById('save-icon-'+postId);

    fetch('/save/'+postId, 
      { method:'POST',
        headers: {
        'X-CSRFToken': csrfToken
      }})
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if(data['saved'] == true){
                saveButton.className = "fa-solid fa-bookmark fa-xl";
            }else{
                saveButton.className = "fa-regular fa-bookmark fa-xl";
            }
        });

}