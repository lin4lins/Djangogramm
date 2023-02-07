function follow(username, csrf_token) {
  fetch(`/follow/${username}/create`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 201) {
      setUnfollowButton(username, csrf_token);
      addFollowerToCounter();
    }
  }).catch((error) => {
    console.log(error)
  })
}

function unfollow(username, csrf_token) {
  fetch(`/follow/${username}/delete`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 204) {
      setFollowButton(username, csrf_token);
      subtractFollowerFromCounter();
    }
  }).catch((error) => {
    console.log(error)
  })
}


function setFollowButton(username, csrf_token) {
  var old_button = document.getElementById(`unfollow-button-${username}`);
  var new_button = `<button id="follow-button-${username}" type="button" class="btn btn-dark" onClick="follow('${username}', '${csrf_token}')">Follow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}

function addFollowerToCounter() {
  var counter = document.getElementById('followers_count');
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value + 1;
}

function setUnfollowButton(username, csrf_token) {
  var old_button = document.getElementById(`follow-button-${username}`);
  var new_button = `<button id="unfollow-button-${username}" type="button" class="btn btn-outline-dark" onClick="unfollow('${username}', '${csrf_token}')">Unfollow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}

function subtractFollowerFromCounter() {
  var counter = document.getElementById('followers_count');
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value - 1;
}