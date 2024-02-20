document.addEventListener('DOMContentLoaded', function() {

  //“Follow” or “Unfollow” button
  
  const follow_Button = document.querySelector('#follow_button');
  const total_followers = document.querySelector('#total_followers');
  if(follow_Button){ 
    follow_Button.onclick = function(){
      
      const userId = this.dataset.userId;
      
      fetch(`/api/follow/${userId}/`)
      .then(response => response.json())
      .then(data => {
        follow_Button.textContent = data.is_following ? 'Unfollow' : 'Follow';
        let n = parseInt(total_followers.textContent);
        total_followers.textContent = data.is_following ? ++n : --n;
      })
      .catch(error => {
        console.error('Erro:', error);
      });
    }
  }
  
  //“Edit” link
  const editLinks = document.querySelectorAll('.edit-post');
  
  editLinks.forEach(function(editLink) {
    editLink.addEventListener('click', function(event) {
      event.preventDefault();
      
      const postBox = event.target.parentElement;
      const postContent = postBox.querySelector('.post-content');
      const editContent = postBox.querySelector('.edit-content');
      const saveButton = postBox.querySelector('.save-edit');
      const postId = postBox.dataset.postId;
      
      postContent.style.display = 'none';
      editContent.style.display = 'block';
      saveButton.style.display = 'block';
      editContent.focus();
      
      saveButton.addEventListener('click', function() {
        const newContent = editContent.value;
        postContent.textContent = newContent;
        
        fetch(`/api/edit/${postId}`, {
          method: 'PUT',
          body: JSON.stringify({
            content: newContent
          })
        })
        .catch(error =>{
          console.log('Error:', error)
        });
  
        editContent.style.display = 'none';
        saveButton.style.display = 'none';
        postContent.style.display = 'block';
      });
    });
  });

  //“Like” and “Unlike”
  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach(function(button) {
    button.addEventListener('click', function() {

      const postBox = button.parentElement;
      const postId = postBox.dataset.postId;
      
      const likesNumber = parseInt(postBox.querySelector('.likes-number'));

      fetch(`/api/like_unlike/${postId}`)
      .then(response => response.json())
      .then(data => {
        const likesNumber = postBox.querySelector('.likes-number');
        likesNumber.textContent = data.likes_count;
      })
      .catch(error =>{
        console.log('Error:', error)
      });
    });
  });
});