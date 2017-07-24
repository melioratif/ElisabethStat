select compositor_name, count(*) as c from oeuvres group by compositor_name order by c desc limit 10
-- top concerto en finale
select compositor_name, count(*) as c from (select * from oeuvres where id  in (select oeuvre_id from activities 
where classement in ("Finale")) and oeuvre_name like "%Concerto%" ) group by compositor_name order by c desc limit 10

-- big view of everything.
select categories.instrument, compositors.name,oeuvre_name, oeuvre_id, count(*) as c 
from categories, activities,oeuvres,compositors where categories.annee = activities.annee 
and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id 
and classement in ("Finale","Demi-finale") group by categories.instrument, compositors.name,oeuvre_name ,oeuvre_id  order by c desc



select compositor_name, count(*) as c from oeuvres group by compositor_name order by c desc limit 10

-- top concerto en finale
select compositor_name, count(*) as c from (select * from oeuvres 
where id  in (select oeuvre_id from activities where classement in ("Finale")) and oeuvre_name like "%Concerto%" ) group by compositor_name order by c desc

select  field2 , count (*) as c from categories group by field2

select * from oeuvres where id  in (select oeuvre_id from activities where classement in ("Finale")) and oeuvre_name like "%Concerto%" and compositor_name = "Fryderyk Chopin"

select * from oeuvres where compositor_name  like "%Chopin" and oeuvre_name like "%Concert%"

select *  from oeuvres where id in ( select oeuvre_id from activities where annee) and oeuvre_name like "%Concerto%"  and compositor_name like "%Chopin%"

select * from activities, oeuvres where oeuvres.id = activities.oeuvre_id and compositor_name  like "%Chopin" 


select categories.instrument, compositors.name,oeuvre_name, oeuvre_id, count(*) as c from categories, activities,oeuvres,compositors 
where categories.annee = activities.annee and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id and classement in ("Première épreuve","Demi-finale","Finale") and instrument="Piano"
group by categories.instrument, compositors.name,oeuvre_name ,oeuvre_id  order by c desc


select categories.instrument, compositors.name,oeuvre_name, oeuvre_id, count(*) as c from categories, activities,oeuvres,compositors 
where categories.annee = activities.annee and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id and classement in ("Première épreuve") and instrument="Piano"
group by categories.instrument, compositors.name,oeuvre_name ,oeuvre_id  order by c desc

select categories.instrument, compositors.name,oeuvre_name, oeuvre_id, count(*) as c from categories, activities,oeuvres,compositors 
where categories.annee = activities.annee and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id and classement in ("Demi-finale")  and instrument="Piano"
group by categories.instrument, compositors.name,oeuvre_name ,oeuvre_id  order by c desc

select categories.instrument, compositors.name,oeuvre_name, oeuvre_id, count(*) as c from categories, activities,oeuvres,compositors 
where categories.annee = activities.annee and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id and classement not in ("Finale")  and instrument="Piano"
group by categories.instrument, compositors.name,oeuvre_name ,oeuvre_id  order by c desc

select  CAST(birth as INT) as b from categories, activities,oeuvres,compositors 
where categories.annee = activities.annee and activities.oeuvre_id = oeuvres.id  and oeuvres.compositor_id = compositors.id and classement in ("Première épreuve") and instrument="Piano"

select  oeuvre_name, compositor_name, birth, death from oeuvres, compositors where oeuvres.compositor_id = compositors.id order by  cast(birth as INT)

-- morceaux finaliste

