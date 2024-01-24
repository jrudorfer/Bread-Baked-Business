# BREAD BAKED BUSINESS
#### Video demo: https://youtu.be/Wxf9JbGXH0M
#### Description:


For my project, I have created a web app using Python, HTML and Javascript. The purpose of the web app is to serve as a promotion website as well as preorder system for a local bakery. The main idea is to have customer pre-order break for a particular day so that the baker knows in the early morning how many breads to prepare.

The main page opens op on a preorder already to incentivise user to directly go to order. When clicked, we are redirect to another page with a form. First, we are too choose one of three types of bread that we would like to order. Then quantity, name, surname and email, as well as the date. For the date, I have used bootstrap calendar picker and limited it to only be able to select day in the future (not today and in the past). Yhe email field has to include a @ sign and all the fields need to be filled in to submit the form.

Once the form is filled, we are redirected to another page. This serves as a temporary subsitute. In the back end, the form is currently held in a variable called session. I imagine that here would be a payment process incorporated. In this case, we just click Zaplaceno and we are taken to another page. This page is the summary of our order. We see the type of bread, how much etc. We are also able to print the order as pdf. In case of an actual server, I would like for an email confirmation to be sent out to the user as well.

Now, for other funcionalities of the web app, we can do to offer, where we can see cards for three different types of bread product. Depending on which one we like, we can click Objednat and we are back at the order form and the type of bread is prefilled based on user selection. The user now just needs to fill in the rest.

Gallery is simply to share pictures of the business.

Change order is not for user that have made a reservation of the bread. Here, they can use their unique reference (program has been written to user the date of the order and random 4 symbols after, ensuring perfect uniqueness given the size of the operation assumed here (small business). When a user submits the reference, the app autmatically checks for when the orders is for and if the order has been for today or in the past, it gives user a flash warning explaning that the order cannot be adjusted anymore. If the order does not exist, the user recieves flash error message as well. If the order is existing and in the future, the order details are filled in the form and the user can decided which part of the order he would like to change. I have build a dynamic query update form, so whether the user wants to adjust the quantity or all the fields does not matter. The reference cannot be changed. In this case, the field for email is checked first whether is empty or not before checking if @ is included.

Lastly, there is a contact page with basic information as well as instagram link. User can fill in the form to contact the business. I was unable to pip install the required packages to make this work but would like to test it out in the future outside of the CS50 Virtual space.

The business would then be able to receive emails with the amount of orders to be made for the next/same day. Order cutoff for the next day is at midnight, because the orders are prepared early in the morning
