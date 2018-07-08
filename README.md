# tornado-exercise
This is a simple webpage coded in Python and utilizing the Tornado and Jinja2 frameworks to create web content.  From
this page there are a few navigatible pages as outlined below.

1) "/" page is a splash page that demonstrates the working of a basic webpage created by Tornado and a
    Python coded app handler.  This page also demonstrates the ability to read parameters directly from the 
    url bar.
    
2) "/form" page is a simple form that requests a user for me to contact them.  This page uses Amazon Web Services,
    Simple Email Services (SES) to send an email to me upon submittal of the form.  This was accomplished through the
    use of the AWS Boto3 Software Development Kit.  The concept learned here was how to use AWS SES to send emails 
    within my own sandbox.  Upon submission, the user is redirect to a "success page".
    
    Since this does require authentication, I did also make use of Environmental Variables located in a protected .env file
    to prevent access to my personal account information.
    
3) "/tip_calc" is a simple form that will calculate tip based off a bill total and the quality of service provided.  This
    was a simple exercise that was added to the site for demonstration purposes only.
    
4) The fourth menu option is a blog page, which was implemented separatly in its own app, so I will detail in that ReadMe.