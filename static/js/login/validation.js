

document.getElementById("loginForm").addEventListener("submit", function(event) {

  event.preventDefault(); // Prevent the form from submitting



  // Get username and password values

  var username = document.getElementById("username").value;

  var password = document.getElementById("password").value;



  // Reset error messages

  document.getElementById("errorMessages").innerHTML = "";



  // Check for empty fields and display error messages

  if (!username && !password) {

      document.getElementById("errorMessages").innerHTML = "Please enter username and password.";

  } else if (!username) {

      document.getElementById("errorMessages").innerHTML = "Please enter username.";

  } else if (!password) {

      document.getElementById("errorMessages").innerHTML = "Please enter password.";

  } else {

      // Submit the form if both fields are filled

      event.target.submit();

  }

});

