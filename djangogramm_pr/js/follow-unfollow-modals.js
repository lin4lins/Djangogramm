function followModal(username, csrf_token) {
  fetch(`/follow/${username}/create`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 201) {
      setUnfollowModalButton(username, csrf_token);
    }
  }).catch((error) => {
    console.log(error)
  })
}

function unfollowModal(username, csrf_token) {
  fetch(`/follow/${username}/delete`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 204) {
      setFollowModalButton(username, csrf_token);
    }
  }).catch((error) => {
    console.log(error)
  })
}


function setFollowModalButton(username, csrf_token) {
  var old_button = document.getElementById(`unfollow-modal-button-${username}`);
  var new_button = `<button id="follow-modal-button-${username}" type="button" class="btn btn-dark" onClick="followModal('${username}', '${csrf_token}')">Follow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}

function setUnfollowModalButton(username, csrf_token) {
  var old_button = document.getElementById(`follow-modal-button-${username}`);
  var new_button = `<button id="unfollow-modal-button-${username}" type="button" class="btn btn-outline-dark" onClick="unfollowModal('${username}', '${csrf_token}')">Unfollow</button>`
  if(old_button.outerHTML) {
    old_button.outerHTML = new_button;
  }
}