# Commerce
This project is developed in Django and is similar to e-commerce website. It uses Django models for storing information.
The user can do following tasks:
* **Sign in/Sign up:** The users can create accounts and using that they can login and create listings.
* **Create Listing:**
Users are be able to visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
* **Watchlist:** 
Users who are signed in are able to visit a Watchlist page, which would display all of the 
listings that a user has added to their watchlist. Clicking on any of those listings will take the user to that listing’s page.
* **Categories:** 
Users are able to visit a page that displays a list of all listing categories. Clicking on the name of any category will 
take the user to a page that displays all of the active listings in that category.
* **Django Admin Interface:**
Via the Django admin interface, a site administrator will be able to view, add, edit, and delete any listings, comments, and bids made on the site.
* **Comments:**
Users can also post comments in the listings.
<br>
The Following video shows the project Demonstration: <br>
https://www.youtube.com/watch?v=0VifMoLvbnU

# Mail
This project is developed in Django. It uses Django as back-end and javascript as front-end. It also utilizes API. The user can create accounts and login as specified before.
## Specifications:
* **Send Mail:** When a user submits the email composition form, JavaScript code to send the email by making POST request to /emails, passing in values for recipients, subject, and body.Once the email has been sent, it load the user’s sent mailbox.
* **Mailbox:** When a user visits their Inbox, Sent mailbox, or Archive, it loads the appropriate mailbox by making a GET request to /emails/<mailbox> to request the emails for a particular mailbox
  * When a mailbox is visited, the application first query the API for the latest emails in that mailbox.
  * When a mailbox is visited, the name of the mailbox will appear at the top of the page.
  * Each email is then be rendered in its own box (e.g. as a div with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.   If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.
* **View Email** When a user clicks on an email, the user will be taken to a view where they see the content of that email by making a GET request to /emails/<email_id> to    request the email. 
  * The aation will show the email’s sender, recipients, subject, timestamp, and body.
  * Once the email has been clicked on, it will mark the email as read by sending a PUT request to /emails/<email_id> to update whether an email is read or not.
* **Archive and Unarchive:** It allows the users to archive and unarchive emails that they have received.
  * When viewing an Inbox email, the user will be presented with a button that lets them archive the email. When viewing an Archive email, the user will be presented with a     button that lets them unarchive the email. This requirement does not apply to emails in the Sent mailbox.
  * It will send a PUT request to /emails/<email_id> to mark an email as archived or unarchived.
  * Once an email has been archived or unarchived, the application will load the user’s inbox.
* **Reply:** The application allow the users to reply to an email.
  * When viewing an email, the user will be presented with a “Reply” button that lets them reply to the email.
  * When the user clicks the “Reply” button, they will be taken to the email composition form.
  * The application will Pre-fill the composition form with the recipient field set to whoever sent the original email.
  * The application will also Pre-fill the subject line. If the original email had a subject line of foo, the new subject line should be Re: foo. (If the subject line already     begins with Re: , it will not add subject again)
  * The application will also Pre-fill the body of the email with a line like "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.
