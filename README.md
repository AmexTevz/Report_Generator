The script was initially created to be integrated into the AWS Lambda function. 
This version is rewritten for the local machine.
It will connect with Postgres, send a query, catch the output, and store it in format CSV, XLS, etc.
After that, it will attach the file to the email and send it to the provided list of recipients.
