let clearBtn = document.getElementById("clearFiles");
let defaultImg = document.getElementById("uploadIcon");
let filePreviewContainer = document.getElementById("filePreviews");

$(document).ready(function () {
    $("#clearFiles").on("click", function (e) {
        e.preventDefault();
        $("#content").val('');  // Clear the file input field
        clearFilePreview('<img id="imagePreview" src="static/img/UploadImg.png" alt="File Preview" class="img-thumbnail" style="width:600px; height:350px; opacity:0.2;">');
    });
});

document.getElementById("content").addEventListener("change", function (event) {
    let input = event.target;
    if(input.files.length == 0){return;}
    clearFilePreview(' ');
    let iterCount = 0;
    Array.from(input.files).forEach(function (file) {
        iterCount++;
        let reader = new FileReader();
        let preview = document.createElement('div');
        if (iterCount < 2){preview.className = 'carousel-item active';} else { preview.className = 'carousel-item';}
        preview.style.overflow = 'hidden'; // Hide overflow to maintain consistent size

        reader.onload = function () {
            if (file.type.startsWith('image/')) {
                // For image files
                let img = document.createElement('img');
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.objectFit = 'contain'; // Maintain aspect ratio for images
                img.src = reader.result;
                preview.appendChild(img);
            } else if (file.type.startsWith('video/')) {
                // For video files
                let video = document.createElement('video');
                video.style.width = '100%';
                video.style.height = '100%';
                video.style.objectFit = 'contain'; // Maintain aspect ratio for videos
                video.setAttribute('controls', 'false'); // Disable video controls
                video.setAttribute('disablePictureInPicture', 'true'); // Disable Picture-in-Picture mode
                let source = document.createElement('source');
                source.src = URL.createObjectURL(file);
                source.type = file.type;
                video.appendChild(source);
                preview.appendChild(video);
            }

            filePreviewContainer.appendChild(preview);
        };

        reader.readAsDataURL(file);
    });

    clearBtn.style.visibility = 'visible';
    filePreviewContainer.style.display = 'flex';
    defaultImg.style.visibility = 'hidden';
    uploadCaption.style.visibility = 'hidden';
});

function clearFilePreview(defaultPrev) {
    filePreviewContainer.innerHTML = defaultPrev; // Clear previous previews
    clearBtn.style.visibility = 'hidden';
    filePreviewContainer.style.display = 'block';
    defaultImg.style.visibility = 'visible';
    uploadCaption.style.visibility = 'visible';
}

