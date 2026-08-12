console.log("Index")

const uploadButton = document.querySelector('input[type="file"]');

uploadButton.addEventListener('click', async () => {
  const file = uploadButton.file()
  if (!file) return alert("Please select a file");
  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: file
    });
    if (response.ok) {
      alert("Upload successful")
    } else {
      alert("Upload failed")
    }
  } catch (error) { 
    alert("Error")
  }
});