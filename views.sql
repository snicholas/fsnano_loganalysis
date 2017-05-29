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

