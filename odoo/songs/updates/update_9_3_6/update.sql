UPDATE res_partner set customer='t' where parent_id in (select id from res_partner where customer='t');
UPDATE res_partner set supplier='t' where parent_id in (select id from res_partner where supplier='t');

