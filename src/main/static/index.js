// Function to handle the file upload form submission event and send it for processing.
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const input = document.querySelector('[type="file"]');
    if (!input.files.length) return;

    // Send data using Fetch API
    let formData = new FormData();
    formData.append("memory_dump", input.files[0]);

    fetch('/process_memory_dump', { 
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Handle the received data after processing
        console.log('Processing result:', data);
    }).catch(error => {
        console.error('Error during memory dump upload and view process', error);
    });
});

// Function to fetch a specific page of your processed file.
function fetchMemoryDumpPage() {
  const selectedFileName = 'your_processed_file_name'; // Replace with the actual name
  const currentPageNumber = document.getElementById('pageNumber').value;

  let formData = new FormData();
  if (currentPageNumber) formData.append("file", selectedFileName);
  formData.append("_page", currentPageNumber);

  fetch('/view_memory_dump_page', { 
    method: 'POST',
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
      // Display the result in your memory viewer container
      document.getElementById('result').textContent = data;
  }).catch(error => {
      console.error('Error during fetching a page of memory dump', error);
  });
}