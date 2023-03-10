function like(post_id, csrf_token) {
  fetch(`/like/${post_id}/create`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 201) {
      set_liked_icon(post_id, csrf_token);
      add_like_to_counter(post_id);
    }
  }).catch((error) => {
    console.log(error)
  })
}

function dislike(post_id, csrf_token) {
  fetch(`/like/${post_id}/delete`, {
    method: 'post',
    headers: {
      'X-CSRFToken': csrf_token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then((res) => {
    if (res.status === 204) {
      set_disliked_icon(post_id, csrf_token);
      subtract_like_from_counter(post_id);
    }
  }).catch((error) => {
    console.log(error)
  })
}


function set_liked_icon(post_id, csrf_token) {
  var old_img = document.getElementById(`no-like-${post_id}`);
  var new_img = `<i id="like-${post_id}" class="bi bi-heart-fill" onclick="dislike(${post_id}, '${csrf_token}')" style="font-size: 1.9em;"></i>`;
  if(old_img.outerHTML) {
    old_img.outerHTML = new_img;
  }
}

function add_like_to_counter(post_id) {
  var counter = document.getElementById(`like-counter-${post_id}`);
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value + 1;
}

function set_disliked_icon(post_id, csrf_token) {
  var old_img = document.getElementById(`like-${post_id}`);
  var new_img = `<i id="no-like-${post_id}" class="bi bi-heart" onclick="like(${post_id}, '${csrf_token}')" style="font-size: 1.9em;"></i>`;
  if(old_img.outerHTML) {
    old_img.outerHTML = new_img;
  }
}

function subtract_like_from_counter(post_id) {
  var counter = document.getElementById(`like-counter-${post_id}`);
  var old_value = parseInt(counter.innerHTML);
  counter.innerHTML = old_value - 1;
}
