// Get the CSRF token from the meta tag or a hidden input field
function openPopup() {
  document.getElementById('popupOverlay').style.display = 'flex';
}

function closePopup() {
  document.getElementById('popupOverlay').style.display = 'none';
}


function myFunction() {
  let userInput = prompt("Please enter your name:", "Guest");
    if (userInput !== null && userInput !== "") {
        console.log("User entered: " + userInput);
    } else {
        console.log("User canceled or entered nothing.");
    }
}

function submitForm() {
  let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let info = document.getElementById('infoInput').value;
  console.log(info);
  info={
    texto: info,
  }
  // Add further logic, e.g., send data to server

  fetch('mapa_info/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken // Include the CSRF token
    },
    body: JSON.stringify(info) // Convert JavaScript object to JSON string
  })
  .then(response => response.json()) // Parse the JSON response from Django
  .then(data => {
    console.log('Success:', data);
    // Handle the response from Django
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  closePopup();
}
