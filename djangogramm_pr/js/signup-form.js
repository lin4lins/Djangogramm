function submitForm(token) {
  console.log("run");
  user_input_data = {
    'email': document.getElementById('email-input').value,
    'username': document.getElementById('username-input').value,
    'password1': document.getElementById('password1-input').value,
    'password2': document.getElementById('password2-input').value
  }
  console.log(user_input_data);
  fetch('/auth/signup/', {
  method: 'post',
  body: user_input_data,
  headers: {
    'X-CSRFToken': token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  }).then(
    function(response) {
      if (response.status === 200) {
        alert("Check your email");
        return;
      };
      response.json().then(function(data) {
        for (const [field, error] of Object.entries(data)) {
          var div = document.getElementById(`${field}-div`);
          var error_el = `<p class="text-danger">${error}</p>`;
          div.innerHTML += error_el;
        };
      });
    }
  ).catch((error) => {
    console.log(error)
  })
}


//{field_name: error_message[0]['message'] for field_name, error_message in form.errors.get_json_data().items()},
//            status=404)