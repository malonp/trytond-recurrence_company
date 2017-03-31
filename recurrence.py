##############################################################################
#
#    GNU Condo: The Free Management Condominium System
#    Copyright (C) 2016- M. Alonso <port02.server@gmail.com>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from trytond.model import ModelSQL, ModelView, fields, dualmethod
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


__all__ = ['RecurrenceEvent', 'RecurrenceEventCompany']


class RecurrenceEvent:
    __metaclass__ = PoolMeta
    __name__ = 'recurrence.event'
    companies = fields.Many2Many('recurrence.event-company.company', 'event', 'company',
            'Companies', help='Companies registered for this recurrence event')

    @dualmethod
    @ModelView.button
    def run_once(cls, events):
        pool = Pool()
        User = Pool().get('res.user')

        for event in events:
            if not event.companies:
                return super(RecurrenceEvent, cls).run_once([event])
            for company in event.companies:
                User.write([event.user], {
                        'company': company.id,
                        'main_company': company.id,
                        })
                with Transaction().set_context(company=company.id):
                    super(RecurrenceEvent, cls).run_once([event])
            User.write([event.user], {
                    'company': None,
                    'main_company': None,
                    })

    @staticmethod
    def default_companies():
        Company = Pool().get('company.company')
        return map(int, Company.search([]))


class RecurrenceEventCompany(ModelSQL):
    'RecurrenceEvent - Company'
    __name__ = 'recurrence.event-company.company'
    event = fields.Many2One('recurrence.event', 'Recurrence Event', ondelete='CASCADE',
            required=True, select=True)
    company = fields.Many2One('company.company', 'Company', ondelete='CASCADE',
            required=True, select=True)
