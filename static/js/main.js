/** Dropzone allows to drag and drop files for upload
  * https://www.dropzonejs.com/#configuration
*/
jQuery(document).ready(function ($) {

const submitButton = document.getElementById('submitul');
const downloadButton = document.getElementById('download-btn');
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const removeButton = document.getElementById('remove_btn');
const uploadLogo = document.getElementById('upload_image');
const loadingSpinner = document.getElementById('loading-spinner');
const downloadButtonAnime = document.querySelector('.button')
let errorAlert = false;
let clickable = false;


// Create a new instance of Dropzone
let myDropzone = new Dropzone("#uploadfile", { 
    url: "/api/upload/",
    autoProcessQueue: true,
    uploadMultiple: false,
    parallelUploads: 1,
    maxFiles: 1,
    acceptedFiles: 'video/.mkv,.webm,.gif,.vob,.3gp,.wmv,.flv,.avi,.mov,.mp4,.mpg,.mpeg',
  });


myDropzone.on('error', function(file, errorMessage, xhr) {
    this.removeFile(file);
    const uploadFileFormat = file.name.split('.').pop();
    const displayError = uploadFileFormat + " file format not supported."
    showAlert(displayError, {file: false});
    errorAlert = true;
});

// When a file is added to the dropzone, send it to the server
// See success and error ajax callbacks for what happens next
myDropzone.on("addedfile", file => {
    setTimeout(function() {
    if (errorAlert === false) {
    const formData = new FormData();
    const uploadFile = file
    const fileName = file.name
    const fileType = '.'+file.name.split('.').pop(); // Get file type
    const selectobject = document.getElementById("output_format");
    for (let i=0; i<selectobject.length; i++) { // Remove file type from output format options
    if (selectobject.options[i].value == fileType)
        selectobject.remove(i);
    }
    const outputFormat = selectobject.value;
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('video', uploadFile, fileName);
    formData.append('output_format', outputFormat);
    uploadLogo.style.display = 'none';
    
    $.ajax({
        url: 'api/upload/', // See video_upload in views.py for the view that handles this call
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
        // Hide upload logo // 
            console.log(data);
            setTimeout(function() {
                localStorage.setItem('upFileName', data.file); // Store uploaded file name for use in submit button event listener
                allowToSubmit();
            });
        },
        error: function(data) {
            console.log(data);
        }
    });


    // Remove file from dropzone when X is clicked
    removeButton.addEventListener('click', function(e) {
        var _myDropzone = myDropzone
        e.preventDefault();
        e.stopPropagation();
        _myDropzone.removeFile(file); // Remove file from dropzone
        const formData = new FormData();
        formData.append('file_name', localStorage.getItem('upFileName'));
        $.ajax({
            url: 'api/delete/', // See delete_video in views.py for the view that handles this call
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                revertToDefault();
            },
            error: function(data) {
                console.log(data.file);
            }
        });
    });
}
    else if (errorAlert === true) {
        errorAlert = false; }
}, 50);});


// When the submit button is clicked, send the file to the server for conversion
submitButton.addEventListener('click', function(e) {
    e.preventDefault()
    const outputFormat = document.getElementById('output_format').value;
    if (outputFormat === 'Choose conversion format') {
            showAlert('Please select an output format', {file: true});
    }
    else if (outputFormat !== 'Choose conversion format' ) 
    {
    uploadInProgress();
    const formData = new FormData();
    const fileName = localStorage.getItem('upFileName'); 
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('file_name', fileName);
    formData.append('output_format', outputFormat);
    $.ajax({
        url: 'api/convert/', // See convert_video in views.py for the view that handles this call
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            localStorage.setItem('upFileName', data.file); // Store converted file name for uses in download button event listener
            allowToDownload();
        },
        error: function(data) {
            console.log(data);
        }
    })
    };
});


function showAlert(message, file) {
    $(".alert").removeClass("hide");
    $('.alert').addClass("show");
    let alertMessage = document.querySelector('.msg')
    let alertBox = document.querySelector('.alert')
    if (file.file !== true) {
        alertBox.style.top = "61.7%"
    }
    alertMessage.innerHTML = `${message}`;
    if (clickable === true) {
        submitButton.style.backgroundColor = "grey"; // Hide submit button
        submitButton.style.pointerEvents = "none";
    }
    setTimeout(function() {
        clickable = true
        $(".alert").removeClass("show");
        $('.alert').addClass("hide");
        submitButton.style.backgroundColor = "transparent";
        submitButton.style.pointerEvents = "auto" // Hide submit button
    }, 2000);
}


function allowToSubmit () {
    submitButton.style.display = 'block'; // Display submit button
    removeButton.style.display = 'block'; // Display 'X' remove button
    uploadLogo.style.display = 'none'; // Hide upload logo
}

function uploadInProgress () {
    submitButton.style.display = 'none'; // Hide submit button
    loadingSpinner.style.display = 'block'; // Hide loading spinner
    removeButton.style.display = 'none' // Hide 'X' remove button
}

function allowToDownload () {
    downloadButton.style.display = 'flex'; // Display download button
    loadingSpinner.style.display = 'none'; // Hide loading spinner
}

// Download the converted file
downloadButton.addEventListener('click', () => {
    const fileName = localStorage.getItem('upFileName') // Get file name from local storage
    window.location.href = 'media/uploads/videos/' + fileName // Download file
    
});

downloadButtonAnime.addEventListener('click', () => {
    downloadButtonAnime.classList.add('active');
})

function revertToDefault() {
    submitButton.style.display = 'none'; // Hide submit button
    loadingSpinner.style.display = 'none'; // Hide loading spinner
    removeButton.style.display = 'none' // Hide 'X' remove button
    downloadButton.style.display = 'none'; // Hide download button
    uploadLogo.style.display = 'block'; // Display upload logo
}

$('.trigger').click(function() {
    $(this).parents('.page-about').toggleClass('show-info');
  });

});
