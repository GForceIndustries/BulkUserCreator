# Genesys Cloud Bulk User Creator

Script to bulk create users inside a Genesys Cloud CX org. Useful for scale testing where a large number of users need to be created.

## Features

Supports all commercial production regions, DCA and TCA.

Supports creating a variable number of users with randomised email aliases. Email domain can be specified or can also be generated randomly.

Includes throttling to avoid rate limiting and automatically retries failed requests if you do get rate limited.

Outputs the list of users created with their email addresses and user IDs.

Outputs the correlation ID for all user creation attempts.

## Setup

Create an [OAuth client](https://help.mypurecloud.com/articles/create-an-oauth-client/) in your Genesys Cloud org and select the Client Credentials grant type. Assign role(s) to the OAuth client that include the **Directory > User > Add** permission.

## Instructions

Requires Python 3.

Update the variables in the Configuration section near the top with your required settings.

* Update the **quantity** variable to determine the number of users to create.
* Update the **domain** variable to specify the email domain to use for the created users' email addresses. Leave this blank for the domain to be randomly generated.
* Update the **region** variable to specify the region of your Genesys Cloud org, using the syntax _us-east-1_, _eu-west-2_ etc.
* Update the **clientid** and **clientsecret** variables with the client ID and client secret of the OAuth client you created in your Genesys Cloud org.
* Update the **sleeptime** variable to adjust the delay between each user creation. Increase this if you find you are getting rate limited.
