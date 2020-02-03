# Eigen

# Working Notes/Approach

### Problem 
    We’ve attached a few documents, each of which has lots of words 
    and sentences. For this task, produce a list of the most 
    frequent interesting words, along with a summary table showing 
    where those words appear (sentences and documents).

### Initial Proposed Solution

First module: A Django (DRF) API that returns a JSON response containing the above information using 
Postgres Free Textsearch under the hood. I've left making the output pretty for later (This README is a living document)

First task is to set up a Django Project and App. Then I need to configure a postgres container with docker. 
(Note to self, make sure to document how to set this up on someone elses machine) 

Then my will set up my test framework so that I can test drive my changes. Once this is set up I will test drive my 
API features in the following order:
1) I can perform a get with a single word. The response contains a list of sentences that contain the word.
(This first test will be extended rather than adding a new test, because the contract this test asserts on will change 
to invlude additional functionality, and I'm using this test to *drive* out being able to add documents to my system 
(which is a required step for adequate testing) AND retrieve search results. Since there is already a lot here I'm 
considering this test a 'steel thread' to build on later. Please ask me about steel threads later!

1) Extending the previous test. I can perform a get with a single word. The response contains sentences that contain 
the word. Along with references to the documents. (Probably via foreign key on sentence)
1) I can perform a get with many words. The response contains a list where each entry contains the corresponding 
sentences and documents.

My main assumption I'm making here is that storing *sentences* in their own table aswell as full documents here 
(linked via foreign key) is the "correct" approach. I will be using postgres' free text search functionality. 
I'm very aware that I'm restricting myself to a relational database here but there's a conscious choice here to stick 
to what I know in this instance. This way, free text searches are done on a per sentence basis (The other fields can then 
be populated in the serialiser level in django). I'm aware this is potentially a coupling of what is expected on the 
presentation layer all the way through to the data layer, and would love feedback on what approach would have been more 
appropriate.

Once the API has been test driven as above, I will test drive some endpoints for saving these documents. 
I'm thinking the cleanest way to do this is hooking into the save function on the model and destructuring the document as it is saved.
The import will then occur via the API over a network (That way the DB is completely wrapped with this API with no back doors)


NB: "MOST FREQUENT". There needs to be some kind of ranking to these results.

# Why I chose to build an API


# Installation and instructions
Your problem statement invited me to stretch myself, so I have built an API that will give you answers to the type of query you asked
me to perform in this challenge!

I used this API to generate my output for the pdf. I wanted to make something a bit more programmatic but I hoped the API
would be cool enough.

Follow these steps to try out the API:
1) Install the project and load the DB with docker:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
python -m nltk.downloader all
docker-compose up db
```

1) In a separate terminal, run `pytest`, just to make sure I haven't forgotten something! The tests will be passing on submission
1) Start the local server with ` python manage.py runserver`
1) To upload a document, navigate to localhost:8000/api/ and click on `http://localhost:8000/api/document/`. 
You can use the post form to upload a document with a title and content
1) Using postman or even your browser, you can now perform a GET query with the terms you are investigating for 
example `http://localhost:8000/api/search/?term=done` should tell you that all 6 documents contain this word. 
1) Please feel free to use several 'terms' in your search: All the info I used to generate 
my output file was queried in a single GET. For example:  `http://localhost:8000/api/search/?term=done&term=well` 

Remember to prune docker when you're happy! <sub><sup>(This can also be done when you're sad.)</sup></sub>

## Limitations
- Started to find limitations with using postgres free text search. Some words it just doesn't want to pick up. I did investigate, 
and it seemed like I could fix it by changing the postgres full text search setting to 'simple'. Unfortunately, I had no joy with this.

## Thank you
Thanks for setting my a great challenge with enough flexibility to allow me to put a lot of effort in. 
I had a lot of fun building this service from the ground up. I hope you find it demonstrates not only aptitude but passion.