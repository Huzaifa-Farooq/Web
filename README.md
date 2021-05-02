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
The user can:
* **Send Mail:** When a user submits the email composition form, JavaScript code to send the email by making POST request to /emails, passing in values for recipients, subject, and body.Once the email has been sent, it load the user’s sent mailbox.
* **Mailbox:** When a user visits their Inbox, Sent mailbox, or Archive, it loads the appropriate mailbox by making a GET request to /emails/<mailbox> to request the emails for a particular mailbox
  * When a mailbox is visited, the application first query the API for the latest emails in that mailbox.
  * When a mailbox is visited, the name of the mailbox will appear at the top of the page.
  * Each email is then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, what the subject line is, and the timestamp of the email. If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.
* **
