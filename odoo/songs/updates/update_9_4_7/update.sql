UPDATE stock_warehouse_orderpoint set name='OP/'||lpad(id::text,5,'0') ;
UPDATE ir_sequence set number_next=(select max(id) from stock_warehouse_orderpoint) + 1 where code='stock.orderpoint';
UPDATE res_partner set ref=((select max(ref::int) from res_partner)::int  + id)::text where ref is null;
UPDATE ir_sequence set number_next=(select max(ref::int) from res_partner) + 1 where code='res.partner';
