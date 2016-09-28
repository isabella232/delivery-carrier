FROM camptocamp/odoo-project:9.0-1.5.0
MAINTAINER Camptocamp

COPY requirements.txt /opt/odoo/requirements.txt
RUN pip install -r /opt/odoo/requirements.txt

COPY ./features /opt/odoo/features

COPY oerpscenario /opt/odoo/oerpscenario
COPY bin/oerpscenario /opt/odoo/bin/oerpscenario

ENV ADDONS_PATH="/opt/odoo/local-src, \
    /opt/odoo/external-src/enterprise, \
    /opt/odoo/external-src/server-tools, \
    /opt/odoo/external-src/account-financial-reporting, \
    /opt/odoo/external-src/account-financial-tools, \
    /opt/odoo/external-src/account-payment, \
    /opt/odoo/external-src/bank-payment, \
    /opt/odoo/external-src/bank-statement-reconcile, \
    /opt/odoo/external-src/carrier-delivery, \
    /opt/odoo/external-src/department, \
    /opt/odoo/external-src/l10n-switzerland, \
    /opt/odoo/external-src/manufacture, \
    /opt/odoo/external-src/partner-contact, \
    /opt/odoo/external-src/product-attribute, \
    /opt/odoo/external-src/project, \
    /opt/odoo/external-src/reporting-engine, \
    /opt/odoo/external-src/stock-logistics-warehouse, \
    /opt/odoo/external-src/stock-logistics-workflow, \
    /opt/odoo/external-src/web, \
    /opt/odoo/src/addons" \
    LIMIT_TIME_CPU=86400 \
    LIMIT_TIME_REAL=86400 \
    LIMIT_MEMORY_SOFT=1342177280 \
    LIMIT_MEMORY_HARD=1610612736
