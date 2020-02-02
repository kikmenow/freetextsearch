# Eigen

# Working Notes/Approach

### Problem 
    We’ve attached a few documents, each of which has lots of words 
    and sentences. For this task, produce a list of the most 
    frequent interesting words, along with a summary table showing 
    where those words appear (sentences and documents).

### Initial Proposed Solution

First module: A Django (DRF) API that returns a JSON response containing the above information using Postgres Free Textsearch under the hood. I've left making the output pretty for later (This README is a living document)

First task is to set up a Django Project and App. Then I need to configure a postgres container with docker. (Note to self, make sure to document how to set this up on someone elses machine) 

Then my will set up my test framework so that I can test drive my changes. Once this is set up I will test drive my 
API features in the following order:
1) I can perform a get with a single word. The response contains a list of sentences that contain the word.(This first test will be extended rather than adding a new test, because the contract this test asserts on will change to invlude additional functionality, and I'm using this test to *drive* out being able to add documents to my system (which is a required step for adequate testing) AND retrieve search results. Since there is already a lot here I'm considering this test a 'steel thread' to build on later. Please ask me about steel threads later!

1) Extending the previous test. I can perform a get with a single word. The response contains sentences that contain the word. Along with references to the documents. (Probably via foreign key on sentence)
1) I can perform a get with many words. The response contains a list where each entry contains the corresponding sentences and documents.

My main assumption I'm making here is that storing *sentences* in their own table aswell as full documents here (linked via foreign key) is the "correct" approach. I will be using postgres' free text search functionality. I'm very aware that I'm restricting myself to a relational database here but there's a conscious choice here to stick to what I know in this instance. This way, free text searches are done on a per sentence basis (The other fields can then be populated in the serialiser level in django). I'm aware this is potentially a coupling of what is expected on the presentation layer all the way through to the data layer, and would love feedback on what approach would have been more appropriate.

Once the API has been test driven as above, I will test drive some endpoints for saving these documents. I'm thinking the cleanest way to do this is hooking into the save function on the model and destructuring the document as it is saved.
The import will then occur via the API over a network (That way the DB is completely wrapped with this API with no back doors)


NB: "MOST FREQUENT". There needs to be some kind of ranking to these results.

Started to find limitations with using postgres free text search. Some words it just doesn't want to pick up. Turns out that its a config somewhere inside postgres, I need to change the type of tsvector it generates

# Installation
generate pip env from requirements.txt

`source venv/bin/activate` 

`python -m nltk.downloader all`

-----------
When testing the count field I found that my count was case sensitive. Data needs to be cleaned on the way in. 