UPDATE ir_config_parameter SET value = 's3' WHERE value = 's3://' AND key = 'ir_attachment.location';
