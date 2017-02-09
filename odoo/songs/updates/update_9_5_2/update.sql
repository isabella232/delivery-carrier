update res_partner set display_name = name||', '|| CASE when city is not Null THEN city||', ' ELSE '' END || '(' || ref || ')' ;
update account_invoice set income_partner_id = (
select so.partner_id from sale_order as so
 where so.id in (select sol.order_id from sale_order_line as sol
    where sol.id in (select soli.order_line_id from sale_order_line_invoice_rel as soli
     where soli.invoice_line_id in (select il.id from account_invoice_line as il where il.invoice_id = account_invoice.id) ) ) limit 1);

