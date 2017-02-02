update res_partner set display_name = name||', '|| CASE when city is not Null THEN city||', ' ELSE '' END || ref ;
