# Eigen

# Working Notes/Approach

### Problem 
    We’ve attached a few documents, each of which has lots of words 
    and sentences. For this task, produce a list of the most 
    frequent interesting words, along with a summary table showing 
    where those words appear (sentences and documents).

### Initial Proposed Solution

Django Rest API that returns a JSON response containing 
the above information using Postgres Free Text search. 
I can then work out the presentation layer later.

First task is to set up a Django Project and App. Then I need to configure a postgres instance inside docker. (Note to self, make sure to document how to set this up on someone elses machine) 

Then my test 
framework so that I can test drive my changes. Once this is set up I will test drive my 
API features in the following order:
1) I can perform a get with a single word. The response contains sentences that contain the word.
1) I can perform a get with a single word. The response contains sentences that contain the word. Along with references to the documents. (Probably via foreign key on sentence)
1) I can perform a get with many words. The response contains a list where each entry contains the corresponding sentences and documents.

My main assumption I'm making here is that storing *sentences* rather than full documents here is the correct approach. I'm very aware that I'm restricting myself to a relational database here but there's a conscious choice here to stick to what I know in this instance.   

I'm using a front-to-back approach because as a working approach I believe its most efficient.

This means that my import script will be lead by my database structure which will be lead by my API which will be lead by my tests. (Which in practice would be lead by the needs of a client).

Once the API has been test driven as above, I will test drive some endpoints for saving these documents. I'm thinking the cleanest way to do this is hooking into the save function on the model and destructuring the document as it is saved.
The import will then occur via the API over a network (That way the DB is completely wrapped with this API with no back doors)

My final e2e test will be manual: Import the data, hit my api, and observe if I get the expected result.

