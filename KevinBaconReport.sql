--Athena create table statement
--s3://kfred/movies/ is an S3 folder that just contains movies.txt in its original format.
CREATE EXTERNAL TABLE IF NOT EXISTS test1.movies (
 `col1` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
 'serialization.format' = '|',
 'field.delim' = '|',
 'collection.delim' = 'undefined',
 'mapkey.delim' = 'undefined'
) LOCATION 's3://kfred/movies/'
TBLPROPERTIES ('has_encrypted_data'='false');


--Which actor was in the most movies?
with num_fields as
(select col1,sequence(2,length(col1)-length(replace(col1,'/',''))+1,1)
idx from test1.movies),
MoviesActors as
(select split_part(col1,'/',1) as movie,split_part(col1,'/',n) as
actor from num_fields cross join unnest(idx) t(n))
select actor,count(actor) from MoviesActors group by actor order by 2 desc,1;
--Welker, Frank (never heard of him!)

--Which movie had the most actors?
with num_fields as
(select col1,sequence(2,length(col1)-length(replace(col1,'/',''))+1,1)
idx from test1.movies),
MoviesActors as
(select split_part(col1,'/',1) as movie,split_part(col1,'/',n) as
actor from num_fields cross join unnest(idx) t(n))
select movie,count(movie) from MoviesActors group by movie order by 2 desc,1;
--Around the World in Eighty Days (1956)

--Which movies was Kevin Bacon in?
with num_fields as
(select col1,sequence(2,length(col1)-length(replace(col1,'/',''))+1,1)
idx from test1.movies),
MoviesActors as
(select split_part(col1,'/',1) as movie,split_part(col1,'/',n) as
actor from num_fields cross join unnest(idx) t(n))
select actor,array_agg(movie) from MoviesActors where actor='Bacon, Kevin' group by actor ;
--[Animal House (1978), Apollo 13 (1995), Beauty Shop (2005), Diner (1982), Few Good Men, A (1992), Flatliners (1990), Footloose (1984), Friday the 13th (1980), He Said, She Said (1991), Hollow Man (2000), In the Cut (2003), JFK (1991), Murder in the First (1995), My Dog Skip (2000), Mystic River (2003), Novocaine (2001), Picture Perfect (1997), Planes, Trains & Automobiles (1987), River Wild, The (1994), She's Having a Baby (1988), Sleepers (1996), Stir of Echoes (1999), Trapped (2002), Tremors (1990), Where the Truth Lies (2005), Wild Things (1998), Woodsman, The (2004)]

--How many actors connected to Kevin Bacon?
with num_fields as
(select col1,sequence(2,length(col1)-length(replace(col1,'/',''))+1,1)
idx from test1.movies),
MoviesActors as
(select split_part(col1,'/',1) as movie,split_part(col1,'/',n) as
actor from num_fields cross join unnest(idx) t(n)),
KB0 as
(select *,'0' as KBIndex from MoviesActors where actor='Bacon, Kevin'),
KB1 as
(select *,'1' as KBIndex from MoviesActors where movie in (select
movie from KB0)),
KB2 as
(select * from MoviesActors where actor in (select actor from KB1)),
KB3 as
(select *,'2' as KBIndex from MoviesActors where movie in (select
movie from KB2)),
KB4 as
(select * from MoviesActors where actor in (select actor from KB3)),
KB5 as
(select *,'3' as KBIndex from MoviesActors where movie in (select
movie from KB4)),
KB6 as
(select * from MoviesActors where actor in (select actor from KB5)),
KB7 as
(select *,'4' as KBIndex from MoviesActors where movie in (select
movie from KB6)),
KB8 as
(select * from MoviesActors where actor in (select actor from KB7)),
KB9 as
(select *,'5' as KBIndex from MoviesActors where movie in (select
movie from KB8)),
--Doing any further iterations of this such as KB10, KB11,... doesn't add any results,
--so we can assume that the highest KBIndex is 5 and any remaining actors aren't
--connected to Kevin Bacon at all
big_union as
(select actor from KB0
 union
 select actor from KB1
 union
 select actor from KB3
 union
 select actor from KB5
 union
 select actor from KB7
 union
 select actor from KB9)
 select count(actor) from big_union
--Answer: 114620
