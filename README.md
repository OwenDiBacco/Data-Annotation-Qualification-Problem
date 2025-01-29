**Introduction**

As part of a qualification exam for DataAnnotation, I was instructed to read cells from the Google Doc table. Each row in the table was composed of three cells, containing an x-coordinate, a y-coordinate, and a character that would be used accordingly to map the character to a specific index in a grid. The code will then be revealed when the grid is logged. 

**Approach**

The approach I used to find this solution was to use a Google Docs API-enabled Service Account from the Google Cloud Console. A Service Account allows applications to communicate. In this scenario, the Service Account will allow our application to collect or send data, based on the provided permissions, to a specific Google Doc file. To connect to the Google Doc, however, we must share the Google Doc with the Service Account’s ‘client_email.’ We should configure the scope, which are permissions that define what actions our application can perform on specific resources, to have read-only access for Google Docs, based on the principle of least privilege.

 We can extract credentials from our service account. Credentials are used with APIs to authenticate and identify the application or user making a request. 

The get_document_cells() function first calls the connect_to_document() function and passes the Google Doc id as an argument. The connect_to_documen() function retrieves the credentials from the get_credentails() function to create a Google Docs Service Object. A Service Object acts as an intermediary between your application and the Google Docs API, for handling authentication and providing methods for API calls. The function then extracts the document associated with the Google Doc ID using the Service Object. 

The get_document_cells() function then takes the document produced from the Service Object and extracts all the content from the body of the document. The function uses the extracted content to locate the table object.To read the content from each cell, the script reveals all the necessary attributes embedded within other attributes, to locate the content of the cell, and then appends each cell’s content to an array. Once finished iterating over the table’s cells, the function removes the first three indexes of the table because these are headers. 

The array containing the content from each cell of the table is passed into the display_code() function. This function finds the largest x and y-coordinates from the table and initializes the array to their size. The function then proceeds to iterate over each row of the table and map the characters to the grid based on their corresponding x and y-coordinates.  

The code can be properly displayed using the print_code() function. 
