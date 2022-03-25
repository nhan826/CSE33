// TODO : MAKE SURE EMAIL DISPLAY SHOWS THE RIGHT INFO AND ADD LABELS


let fetchedEmails = [];

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');

    document.querySelector('#compose-form').onsubmit = () => {
        event.preventDefault();
        // saves the values from the compose email form
        const recipient = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;
        fetch('/emails', {
                // sends the email — makes a POST request to /emails
                method: 'POST',
                body: JSON.stringify({
                    recipients: recipient,
                    subject: subject,
                    body: body
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
        // loads the user's sent mailbox once the email has been sent
        load_mailbox('sent');

    };

});

function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#emails-content').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#display-email').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#emails-content').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#display-email').style.display = 'none';


    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // reference : https://stackoverflow.com/questions/42236578/create-a-list-for-each-object-in-a-json-array
    fetch('/emails/' + mailbox) // request to get a mailbox's emails
        .then(response => response.json())
        .then(emails => {
            fetchedEmails = emails; // saves emails in an empty list
            let emailSection = "";
            emails.forEach(function(item) {
                //  appends to list — creates a div for each email   
                //  displayEmail function is called when the email in the mailbox is clicked 
                emailSection += `<div id = ${item.id} onclick = "displayEmail(${item.id})">` + item.recipients + "<br>" + item.subject + "<br>" + item.timestamp + "</div>";
            });
            // modifies the html with the string created  
            document.getElementById('emails-content').innerHTML = emailSection;
        });

}

function displayEmail(id) {
    // Shows the single email — hides the other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#emails-content').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#display-email').style.display = 'block';
    let email = [];
    // finds the email by id
    fetchedEmails.forEach(function(item) {
        if (parseInt(item.id) === id) {
            email = item;
        }
    });

    // creates HTML for email's contents
    const singleEmail = "<div>" + email.sender + "<br>" + email.subject + "<br>" + "<p>" + email.body + "</p>" + email.timestamp + "</div>";
    // modifies html document to display the single email
    document.getElementById('display-email').innerHTML = singleEmail;
}