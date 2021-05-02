document.addEventListener('DOMContentLoaded', function () {

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
    document.querySelector('#msg').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

}


function load_email(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    mydiv = document.createElement('div');
    mydiv.id = "email";

    btn_reply = document.createElement('button');
    btn_reply.id = "reply-btn";
    btn_reply.innerHTML = "Reply";
    btn_reply.className = "btn btn-sm btn-primary";


    archive_btn = document.createElement('button');
    archive_btn.id = "archive-btn";
    archive_btn.className = "btn btn-sm btn-primary";

    // clearing the div before appending any data
    document.querySelector('#email-view').innerHTML = '';

    fetch('/emails/' + id)
        .then(response => response.json())
        .then(email => {
        console.log(email);
            if (email.archived == false) {
                archive_btn.innerHTML = "Add to Archive";
                archive_btn.addEventListener('click', function(){
                toggle_archive(email.id, email.archived);
                load_mailbox('inbox');
                    });
                }

            else if (email.archived == true) {
                archive_btn.innerHTML = "Remove From Archive";
                archive_btn.addEventListener('click', function(){
                toggle_archive(email.id, email.archived);
                load_mailbox('inbox');
                    });
                }

            if (email.recipients.length != 1)
            {
                var all_recipients = "";
                for (recipient of email.recipients) {
                    all_recipients = all_recipients + recipient + ',';
                }
            }
      mydiv.innerHTML = `<b>From</b>: ${email.sender}<br>
      <b>To</b>: ${email.recipients}<br>
      <b>Subject</b>: ${email.subject}<br>
      <b>Timestamp</b>: ${email.timestamp}<br>
      <b>Body: </b><br><br>
      <textarea class="form-control" disabled="disabled">${email.body}</textarea><br>`

            btn_reply.addEventListener('click', function () {
                compose_email();
                document.querySelector('#compose-recipients').value = email.sender;
                document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n<-- End of message-->`;
                if (document.querySelector('#compose-subject').value.includes("Re:")) {
                    document.querySelector('#compose-subject').value = email.subject;
                } else {
                    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
                }
            });

        });
    document.querySelector('#email-view').append(mydiv);
    document.querySelector('#email-view').append(btn_reply);
    document.querySelector('#email-view').append(archive_btn);

}

function toggle_archive(id, state){
    fetch('/emails/'+ id, {
        method: "PUT",
        body: JSON.stringify({
          archived: !state,
        }),
      });
}

function mark_read(id){
     fetch('/emails/' + id, {
     method: 'PUT',
     body: JSON.stringify({
           read: true
                })
            })
}


document.addEventListener(
  "DOMContentLoaded",
  function () {
    const form = document.querySelector("#compose-form");

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      to = document.querySelector("#compose-recipients");
      subject = document.querySelector("#compose-subject");
      body = document.querySelector("#compose-body");

      fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
          recipients: to.value,
          subject: subject.value,
          body: body.value,
        }),
      })
      .then ((response) => response.json())
      .then((result) => {
          console.log(result);
          if (result.message.includes("success")) {
            load_mailbox("sent");
          }
          else{
              document.querySelector('#msg').style.display = 'block';
              document.querySelector('#msg').innerHTML = result.error;
          }
        });

        });
false
    });




function iterate_over_emails(email, index) {

    // is email is unread and the sender is not current user
    if (email.read == false)  {
        var mydiv = document.createElement('div');
        mydiv.id = "email-unread";
        mydiv.innerHTML = `<span style="display: inline-block"><b>${email.sender}</b>&nbsp;&nbsp;&nbsp;${email.subject}</span>
        <span id="email-timestamp">${email.timestamp}</span>`;
        mydiv.addEventListener('click', function () {
            document.querySelector('#emails-view').style.display = 'none';
            mark_read(email.id);
            load_email(email.id);

        })
        document.querySelector('#emails-view').append(mydiv);
    } else if (email.read == true) {
        var mydiv = document.createElement('div');
        mydiv.id = "email-read";
        mydiv.innerHTML = `<span style="display: inline-block"><b>${email.sender}</b>&nbsp;&nbsp;&nbsp;${email.subject}</span>
        <span id="email-timestamp">${email.timestamp}</span>`;
        mydiv.addEventListener('click', function () {
            document.querySelector('#emails-view').style.display = 'none';
            // mark email as read
            mark_read(email.id);
            load_email(email.id);
        })
    console.log(email);
    document.querySelector('#emails-view').append(mydiv);
    }

}


function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#msg').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch('/emails/' + mailbox)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            // ... iterate over each email ...
            emails.forEach(iterate_over_emails);
        });

}
