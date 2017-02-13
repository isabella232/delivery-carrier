update res_partner set display_name = name||', '|| CASE when city is not Null THEN city||', ' ELSE '' END || '(' || ref || ')' ;
update account_invoice set income_partner_id = (
select case when part.is_company = 't' then part.id else part.parent_id end from sale_order as so,res_partner as part
 where so.id in (select sol.order_id from sale_order_line as sol
    where sol.id in (select soli.order_line_id from sale_order_line_invoice_rel as soli
     where soli.invoice_line_id in (select il.id from account_invoice_line as il where il.invoice_id = account_invoice.id) ) ) and part.id = so.partner_id limit 1);