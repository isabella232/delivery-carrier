UPDATE res_partner set contacts_last_xprt='2016-12-01 01:00:00.000001'
WHERE ((write_date<'2016-12-01') OR (create_date<'2016-12-01'))
AND (parent_id IS NOT NULL)
AND (is_company IS False);

UPDATE res_partner SET adrs_lst_xprt='2016-12-01 01:00:00.000001'
WHERE ((write_date<'2016-12-01') OR (create_date<'2016-12-01'))
AND ((parent_id is NULL) OR (is_company is True));

UPDATE res_partner SET adrs_tags_lst_xprt='2016-12-01 01:00:00.000001'
WHERE ((write_date<'2016-12-01') OR (create_date<'2016-12-01'));
