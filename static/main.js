// Open and close sidebar
var open = false;
function openNav() {
  if (!open) {
    
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main-content").style.transform='translateX(250px)';
  
  open = true;
  }
  else {
    closeNav();
  }
}

function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main-content").style.transform = 'translateX(0)';
  open = false;
}

// Image preview and diagnosis function
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const imageDisplay = document.getElementById("imageDisplay");
const imageText = document.getElementById("imageText");
const diagnosisMessage = document.getElementById("diagnosisMessage");

imageInput.addEventListener("change", function() {
  const file = this.files[0];

  if (file) {
    const reader = new FileReader();
    imageText.style.display = "none";
    imageDisplay.style.display = "block";

    reader.addEventListener("load", function() {
      imageDisplay.setAttribute("src", this.result);
    });

    reader.readAsDataURL(file);
  } else {
    imageText.style.display = "block";
    imageDisplay.style.display = "none";
  }
});

function diagnoseImage() {
  const file = imageInput.files[0];

  if (!file) {
    diagnosisMessage.textContent = "Please select an image first.";
  } else {
    diagnosisMessage.textContent = "Diagnosing... (mock result: Smallpox)";
  }
}