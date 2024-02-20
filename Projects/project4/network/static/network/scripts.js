document.addEventListener('DOMContentLoaded', function() {

  const followButton = document.querySelector('#follow_button');
  const total_followers = document.querySelector('#total_followers');

  followButton.onclick = function(){
    
    const userId = this.dataset.userId;
    const isFollowing = this.dataset.following;
    
    fetch(`/api/follow/${userId}/`, {
      method: 'POST',
      body: JSON.stringify({
        is_following: isFollowing,
      }),
    })
    .then(response => response.json())
    .then(data => {
      followButton.textContent = data.is_following ? 'Unfollow' : 'Follow';
      let n = parseInt(total_followers.textContent);
      total_followers.textContent = data.is_following ? ++n : --n;
    })
    .catch(error => {
      console.error('Erro:', error);
    });
  }
});