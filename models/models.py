

from sqlalchemy import String, Column, Integer, Unicode, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FofExpenses(Base):
    __tablename__ = 'fof_expences'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    item = Column('item', String)
    subitem = Column('subitem', String)
    activity_type = Column('activity_type', String)
    activity_kind = Column('activity_kind', String)
    cost_type = Column('cost_type', String)
    code = Column('code', String)
    planfix_code = Column('planfix_code', String)


class IndustrialProjects(Base):
    __tablename__ = 'industrial_projects'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    project_id = Column('project_id', Integer)
    project_name = Column('project_name', String)
    description = Column('description', String)


class Expenses(Base):
    __tablename__ = "planfix_expenses_data"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    claim_name = Column('claim_name', String)
    claim_id = Column('claim_id', Integer)
    pay_date = Column('pay_date', Date)
    subitem = Column('subitem', String)
    turnover_date = Column('turnover_date', Date)
    currency = Column('currency', String)
    subitem_id = Column('subitem_id', String)
    amount_to_pay = Column('amount_to_pay', Integer)
    paid = Column('paid', Integer)
    acquisition_cost = Column('acquisition_cost', Integer)
    payment_type = Column('payment_type', String)
    project = Column('project', String)
    project_id = Column('project_id', Integer)
    organization = Column('organization', String)
    has_photo_confirmation = Column('has_photo_confirmation', Boolean)
    initiator = Column("initiator", String)
    # template_name = Column("template_name", String)
