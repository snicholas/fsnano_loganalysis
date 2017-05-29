# Log analysys project

The main scope is to answer 3 questions:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors? 

## Usage
To run the program you need python 3 (tested with version 3.5.2) and the new database from the [Fullstack Nanodegree Virtual machine](https://github.com/udacity/fullstack-nanodegree-vm) .

Inside the virtual machine running `python3 logAnalysis.py` will show usage message.
There are 4 possible paramaters to pass:
* -a : will print results for all the 3 questions
* -getMostPopular3Articles : will print the 3 most popular articles of all time
* -getMostPopularAuthors : will print authors ordered, most popular first
* -getDaysWithMore1PercError : will print days on which more than 1% of request lead to error

To simplify python code various views has been created:

```
create view authorsarticles as
    SELECT authors.name,
            concat('/article/', articles.slug) AS path
    FROM articles,authors
    WHERE articles.author = authors.id
    GROUP BY articles.author, authors.name, articles.slug
    ORDER BY articles.author;

create view authorviews as
    SELECT ll.name, sum(ll.numviews) AS totalviews
    FROM ( SELECT authorsarticles.name,
                  count(log.path) AS numviews
           FROM log, authorsarticles
           WHERE log.path = authorsarticles.path
           GROUP BY log.path, authorsarticles.name
           ORDER BY authorsarticles.name) AS ll
    GROUP BY ll.name
    ORDER BY (sum(ll.numviews)) DESC;

create view errorrequest as
    SELECT date(log."time") AS data,
            count(*) AS totalrequest
    FROM log
    WHERE log.status <> '200 OK'::text
    GROUP BY (date(log."time"))
    ORDER BY (date(log."time"));

create view errorrequestperc as
	SELECT err.data,
    err.totalrequest::double precision / totreq.totalrequest::double precision * 100::double precision AS perc
    FROM errorrequest err, totalrequest totreq
    WHERE err.data = totreq.data;

create view mostviewedpath as 
	SELECT log.path, count(log.path) AS numviews
    FROM log, articles
    WHERE log.path = concat('/article/', articles.slug)
    GROUP BY log.path
    ORDER BY (count(log.path)) DESC
    LIMIT 3;


create view totalrequest as 
    SELECT date(log."time") AS data, count(*) AS totalrequest
    FROM log
    GROUP BY (date(log."time"))
    ORDER BY (date(log."time"));


```
