// TO DO: fix send inbox refresh
// check about styling

let currentMailbox = null;
let currentEmail = null;

document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
  document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
  document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");

  document.querySelector("#compose-form").onsubmit = () => {
    event.preventDefault();
    // saves the values from the compose email form
    const recipient = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    fetch("/emails", {
      // sends the email — makes a POST request to /emails
      method: "POST",
      body: JSON.stringify({
        recipients: recipient,
        subject: subject,
        body: body,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
      });

    // loads the user's sent mailbox once the email has been sent

    // I had trouble getting this view to refresh — I tried changing the code in the load_mailbox function
    // to include code within the fetch request, but still had this issue

    // While this isn't very good design, I was able to resolve this by calling the load_mail function twice:
    load_mailbox("sent");
    load_mailbox("sent");
  };
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#emails-content").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#display-email").style.display = "none";
  document.querySelector("#archiveBtn").style.display = "none";
  document.querySelector("#unarchiveBtn").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#emails-content").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#display-email").style.display = "none";
  document.querySelector("#archiveBtn").style.display = "none";
  document.querySelector("#unarchiveBtn").style.display = "none";
  document.querySelector("#replyBtn").style.display = "none";

  // global variable — saves current mailbox
  currentMailbox = mailbox;

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // reference : https://stackoverflow.com/questions/42236578/create-a-list-for-each-object-in-a-json-array
  fetch("/emails/" + mailbox) // request to get a mailbox's emails
    .then((response) => response.json())
    .then((emails) => {
      let emailSection = "";
      emails.forEach(function (item) {
        //  appends to string — creates a div for each email
        //  displayEmail function is called when the email in the mailbox is clicked
        //  if email is read, background color is set to gray
        //  if email is unread, background color is set to white
        if (item.read === true) {
          emailSection +=
            `<div id = ${item.id} style="background-color:#d9d9d9;" onclick = "displayEmail(${item.id})">` +
            "From: " +
            item.sender +
            "<br>" +
            "To: " +
            item.recipients +
            "<br>" +
            "<h5>" +
            "Subject: "+
            item.subject +
            "</h5>" +
            item.timestamp +
            "</div>";
        }
        if (item.read === false) {
          emailSection +=
            `<div id = ${item.id} style="background-color:#FFFFFF;" onclick = "displayEmail(${item.id})">` +
            "From: " +
            item.sender +
            "<br>" +
            "To: " +
            item.recipients +
            "<br>" +
            "<h5>" +
            item.subject +
            "</h5>" +
            item.timestamp +
            "</div>";
        }
      });
      // modifies the html with the string created
      document.getElementById("emails-content").innerHTML = emailSection;
    });
}

function displayEmail(id) {
  // Shows the single email — hides the other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#emails-content").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#display-email").style.display = "block";

  // displays buttons depending on the mailbox:

  if (currentMailbox === "inbox") {
    document.querySelector("#archiveBtn").style.display = "block";
  }

  if (currentMailbox === "archive") {
    document.querySelector("#unarchiveBtn").style.display = "block";
  }

  if (currentMailbox !== "sent") {
    document.querySelector("#replyBtn").style.display = "block";
  }

  // runs function to archive email when button is pressed
  document.querySelector("#archiveBtn").addEventListener("click", function () {
    archiveCurrentEmail(true);
  });

  // runs function to unarchive email when button is pressed
  document.querySelector("#unarchiveBtn").addEventListener("click", function () {
      archiveCurrentEmail(false);
  });

  document.querySelector("#replyBtn").addEventListener("click", function () {
    // when the reply button is clicked, the compose email view is displayed
    compose_email();
    // pre-fills recipient field with the original email's sender
    document.getElementById("compose-recipients").value = currentEmail.sender;
    let subject = currentEmail.subject;

    // Adds prefix "RE:" to the subject line if the subject doesn't already begin with "RE"
    if (!currentEmail.subject.startsWith("Re:")) {
      subject = "Re: " + currentEmail.subject;
    }
    document.getElementById("compose-subject").value = subject;

    // pre-fills the body section of the form with content from the original email
    document.getElementById("compose-body").value =
      "On " +
      currentEmail.timestamp +
      " " +
      currentEmail.sender +
      " wrote: " +
      "\n" +
      currentEmail.body +
      "\n" +
      "-------------------------------" +
      "\n";
  });

  // fetches the email by id
  fetch("/emails/" + id)
    .then((response) => response.json())
    .then((email) => {
      // global variable — saves current email being viewed
      currentEmail = email;
      // creates HTML with email's contents
      const singleEmail =
        "<div>" +
        "From: " +
        email.sender +
        "<br>" +
        "To: " +
        email.recipients +
        "<br>" +
        "Subject: " +
        email.subject +
        "<br>" +
        email.timestamp +
        "<br>" +
        "<hr>" +
        "<p>" +
        email.body +
        "</p>" +
        "</div>";
      // modifies HTML DOC to display the single email
      document.getElementById("display-email").innerHTML = singleEmail;
    });
  fetch("/emails/" + id, {
    // Marks email as read when clicked
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function archiveCurrentEmail(status) {
  // changes archived status
  fetch("/emails/" + currentEmail.id, {
    method: "PUT",
    body: JSON.stringify({
      archived: status,
    }),
  });
  // returns to inbox view
  load_mailbox("inbox");
}
