function followModalMe(username, csrf_token) {
  fetch(`/follow/${username}/create`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 201) {
      setUnfollowModalMeButton(username, csrf_token);
      addFollowingToCounter();
    }
  }).catch((error) => {
    console.log(error)
  })
}

function unfollowModalMe(username, csrf_token) {
  fetch(`/follow/${username}/delete`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 204) {
      setFollowModalMeButton(username, csrf_token);
      subtractFollowingFromCounter();
    }
  }).catch((error) => {
    console.log(error)
  })
}


function setFollowModalMeButton(username, csrf_token) {
  var old_button = document.getElementById(`unfollow-modal-button-${username}`);
  var new_button = `<button id="follow-modal-button-${username}" type="button" class="btn btn-dark" onClick="followModalMe('${username}', '${csrf_token}')">Follow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}

function addFollowingToCounter() {
  var counter = document.getElementById('following_count');
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value + 1;
}

function setUnfollowModalMeButton(username, csrf_token) {
  var old_button = document.getElementById(`follow-modal-button-${username}`);
  var new_button = `<button id="unfollow-modal-button-${username}" type="button" class="btn btn-outline-dark" onClick="unfollowModalMe('${username}', '${csrf_token}')">Unfollow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}

function subtractFollowingFromCounter() {
  var counter = document.getElementById('following_count');
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value - 1;
}