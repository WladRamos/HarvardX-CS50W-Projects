document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#selected-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //call function to send email when form is submitted
  document.querySelector('#compose-form').onsubmit = function(){
    const email_recipient = document.querySelector('#compose-recipients').value;
    const email_subject = document.querySelector('#compose-subject').value;
    const email_body = document.querySelector('#compose-body').value;
    send_email(email_recipient, email_subject, email_body);
  }
}

function send_email(email_recipient, email_subject, email_body){
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: email_recipient,
        subject: email_subject,
        body: email_body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    //load the user’s sent mailbox
    load_mailbox('sent')
  })
  .catch(error =>{
    console.log('Error:', error)
  });
  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#selected-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //load the appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    emails.forEach(email => {
      const element = document.createElement('div');
      element.classList.add('mail-box');
      if (email.read) {
        element.classList.add('read');
      } else {
        element.classList.add('unread');
      }
      element.setAttribute('data-email-id', email.id);
      element.innerHTML = `<strong>${email.sender}</strong> <span style="margin-left: 15px;">${email.subject}</span> <span style="float: right; color: #888;">${email.timestamp}</span>`;
      element.addEventListener('click', function(event) {

        //mark email as read
        const emailId = event.currentTarget.dataset.emailId;
        const clickedEmail = emails.find(email => email.id === parseInt(emailId));
        fetch(`/emails/${emailId}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
        .then(() => {
          // Take user to a view where he can see the content of that email
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector('#selected-email-view').style.display = 'block';
          
          const div1 = document.createElement('div');
          const div2 = document.createElement('div');
          const div3 = document.createElement('div');

          div1.innerHTML = `
            <strong>From:</strong> <span>${clickedEmail.sender}</span> <br>
            <strong>To:</strong> <span>${clickedEmail.recipients.join(', ')}</span> <br>
            <strong>Subject:</strong> <span>${clickedEmail.subject}</span> <br>
            <strong>Timestamp:</strong> <span>${clickedEmail.timestamp}</span> <br>
            <hr>
          `;

          div2.innerHTML = `<span>${clickedEmail.body}</span>`

          div3.innerHTML = '<hr>'
          
          if (mailbox !== 'sent') {
            const archiveButton = document.createElement('button');
            archiveButton.setAttribute('id', 'archive-button');
            archiveButton.setAttribute('type', 'button');
            archiveButton.classList.add('btn', 'btn-primary');
            div3.appendChild(archiveButton);
            
            archiveButton.addEventListener('click', function() {
              
              const isArchived = clickedEmail.archived;
        
              fetch(`/emails/${emailId}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: !isArchived
                })
              })
              .then(() => {
                load_mailbox('inbox')
              })
              .catch(error =>{
                console.log('Error:', error)
              });
            });
            archiveButton.textContent = clickedEmail.archived ? 'Unarchive' : 'Archive';
          }

          const replyButton = document.createElement('button');
          replyButton.setAttribute('id', 'archive-button');
          replyButton.setAttribute('type', 'button');
          replyButton.classList.add('btn', 'btn-primary');
          replyButton.style.marginLeft = '5px';
          replyButton.textContent = 'Reply';
          div3.appendChild(replyButton);
          
          replyButton.addEventListener('click', function() {
            reply(clickedEmail.sender, clickedEmail.subject, clickedEmail.body, clickedEmail.timestamp);
          });

          document.querySelector('#selected-email-view').innerHTML = '';
          document.querySelector('#selected-email-view').append(div1, div2, div3);
          
        })
        .catch(error =>{
          console.log('Error:', error)
        });
      });
      document.querySelector('#emails-view').append(element);
    });
  })
  .catch(error =>{
    console.log('Error:', error)
  });
}

function reply(sender, subject, body, timestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#selected-email-view').style.display = 'none';

  // Pre-fill fields
  let subjectReply = subject;
  if(!subject.startsWith('Re:')){
    subjectReply = 'Re: ' + subject;
  }
  document.querySelector('#compose-recipients').value = `${sender}`;
  document.querySelector('#compose-subject').value = `${subjectReply}`;
  document.querySelector('#compose-body').value = `"On ${timestamp} ${sender} wrote: ${body}"`;

  //call function to send email when form is submitted
  document.querySelector('#compose-form').onsubmit = function(){
    const email_recipient = document.querySelector('#compose-recipients').value;
    const email_subject = document.querySelector('#compose-subject').value;
    const email_body = document.querySelector('#compose-body').value;
    send_email(email_recipient, email_subject, email_body);
  }
}