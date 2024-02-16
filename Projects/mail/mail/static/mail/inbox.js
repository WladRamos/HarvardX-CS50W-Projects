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

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //load the appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
  })
  .catch(error =>{
    console.log('Error:', error)
  });
}