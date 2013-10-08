/*review rank*/
update Review r set r.rank = (select count(distinct c.Userid) from Comment c where c.Reviewid=r.Reviewid);

/*makeup rank*/
update Makeup m set m.rank = (select count(*) from Review r where m.Makeupid=r.Makeupid);

/*brand rank*/
update Brand b set b.rank = ( (select count(*) from Makeup m where b.Brandid=m.Brandid)*0.3 +  (select count(*) from Review r join Makeup m on r.Makeupid=m.Makeupid where b.Brandid=m.Brandid)*0.7 );
