var tests = {
      filereader: typeof FileReader != 'undefined',
      formdata: !!window.FormData,
      progress: "upload" in new XMLHttpRequest
    }, 
    support = {
      filereader: document.getElementById('filereader'),
      formdata: document.getElementById('formdata'),
      progress: document.getElementById('progress')
    },
    infoDom = document.getElementById('info');
    progress = document.getElementById('process'),
    progressDom = document.getElementById('uploadprogress'),
    fileupload = document.getElementById('upload');
    mask = document.getElementById('mask');
    maskText = document.getElementById('maskText');

"filereader formdata progress".split(' ').forEach(function (api) {
  if (tests[api] === false) {
    support[api].className = 'fail';
  } else {
    support[api].className = 'hidden';
  }
}); 

function previewFile(file) {
    var fileName = file.name;
    var fileSize = Math.floor((file.size)/1024); 
    var fileType = file.type; 
    console.log(fileName + "; " + fileType.slice(0,5)) + "; " + fileSize;
    if(fileType.slice(0,5) == 'video') {
        var videoPath = window.URL.createObjectURL(file);
        var str = "<video id='videoPreview' src='"+videoPath+"' controls autoplay='autoplay'></video>"; 
        holder.innerHTML = str;         
    } else {
        alert('Type unsupported!');
        return false;          
    }
}

function uploadFiles(formData) {
        //use ajax to send the video
    if (tests.formdata) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/classify_upload');
        xhr.onload = function() {
            progressDom.value = progressDom.innerHTML = 100;
        };
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                console.log(xhr.responseText);
                mask.style.opacity = 0;
                visualize(xhr.responseText);
        }
    };

      if (tests.progress) {
        progress.style.opacity = 1;
        xhr.upload.onprogress = function (event) {
          if (event.lengthComputable) {
            var complete = (event.loaded / event.total * 100 | 0);
            progressDom.value = progressDom.innerHTML = complete;
            maskText.innerHTML = "uploading " + complete + "% ...";
            if(complete == 100) {
                maskText.innerHTML = "processing ...";
            } 
          }
        }
      }

      xhr.send(formData);
    } 
}
function handleFiles(files) {
    var formData = tests.formdata ? new FormData() : null;
    for (var i = 0; i < files.length; i++) {
        if (tests.formdata) formData.append('videofile', files[i]);
        previewFile(files[i]);
    }
    uploadFiles(formData);
  
}


var checker = 1;
setInterval(function(){
    if(checker == 1){
        maskText.style.transform = 'scale(1.1,1.1)';
        checker = 0;
    }else {
        maskText.style.transform = 'scale(1,1)';
        checker = 1;
    }
},1800);  

if ('draggable' in document.createElement('span')) {
    var holder = document.getElementById('holder');
    holder.ondragover = function() {
        this.className = 'hover';
        return false;
    };
    holder.ondragend = function() {
        this.className = '';
        return false;
    };
    holder.ondrop = function(event) {
        event.preventDefault();
        this.className = '';
        var files = event.dataTransfer.files;
        console.log('hello');
        maskText.innerHTML = "upLoading ..."
        // handle files
        handleFiles(files);
    };
} else {
    fileupload.className = 'hidden';
    fileupload.querySelector('input').onchange = function () {
        readfiles(this.files);
    };
}