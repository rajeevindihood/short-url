from datetime import datetime
from email.policy import default

from importlib import import_module
import enum
from unittest.mock import DEFAULT

from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    DateTime,
    Date,
    Time,
    Text,
    Sequence,
    Enum,
    JSON,
    BLOB, FLOAT
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import FetchedValue
from sqlalchemy.sql.sqltypes import VARCHAR
# from sqlalchemy.sql.sqltypes import BLOB, BOOLEAN, Float, JSON
Base = declarative_base()

class Client(Base):
    __tablename__ = "journey_client"
    id = Column(Integer(), primary_key=True)
    name=Column(String(length=100))
    domain=Column(String(length=100))
    pg_type = Column(Enum('RAZORPAY','BILLDESK','NEFT','CASHFREE','DKGFS','APP-REDIRECT','SL-REDIRECT','ZP-REDIRECT'))
    contact_name=Column(String(length=100))
    contact_phone=Column(String(length=100))
    contact_email=Column(String(length=100))
    logo=Column(BLOB)
    created_by=Column(String(length=100))
    category=Column(Enum('NBFC','CC','BNPL'))
    creation_date=Column(DateTime(),server_default=func.now())
    last_update_time=Column(DateTime(),server_default=func.now())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Tranch(Base):
    __tablename__ = "journey_tranch"
    id = Column(Integer(), primary_key=True)
    name = Column(String(length=64))
    client_id = Column(Integer(), ForeignKey(column="journey_client.id", ondelete="CASCADE"))
    created_on = Column(DateTime(),default=datetime.now())
    campaign_type = Column(Enum('EMI','SETTLEMENT'))
    enable_emi_payment = Column(Boolean(), default=False)
    enable_emi_payment_date = Column(DateTime())
    enable_liveassist = Column(Boolean(), default=False)
    is_gupshupenabled  = Column(Boolean(),default=False)
    created_by=Column(String(length=30))


    # additional_features = Column(JSON)
    client = relationship ("Client")

    is_enabled = Column(Boolean, default=False) 
    telecalling_strategy=Column(Text)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Hash(Base):
    __tablename__ = "hash_keys"
    id = Column(Integer(), primary_key=True)
    original_key=Column(String(length=255), unique=True)
    hash_key=Column(String(length=8), unique=True)
    creation_date=Column(DateTime(),server_default=func.now(), default=func.now())
    last_visiting_time=Column(DateTime())
    is_enabled = Column(Boolean, default=True)
    tranch_id = Column(Integer(),ForeignKey(column="journey_tranch.id"))
    expiry_date=Column(DateTime())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Borrower(Base):
    __tablename__ = "journey_borrower"
    id = Column(
        Integer(), primary_key=True, unique=True, nullable=False, autoincrement=True
    )

    # LSQ ID
    Prospect_ID = Column(
        String(length=255), primary_key=False, unique=False, nullable=True
    )
    canpebid = Column(String(length=255))
    current_stage = Column(String(length=20))
    stage_change_dt = Column(DateTime())
    locked_option = Column(String(length=20))
    installments_paid = Column(String(length=20))
    channel = Column(String(length=20))
    offer_chosen_in_email = Column(String(length=100))
    borrower_engagement_score = Column(Integer(), default=0)
    borrower_leadscore = Column(Integer(), default=0)
    esign_status = Column(Integer())
    esign_url = Column(String(length=255))
    language = Column(String(length=255))
    initials = Column(String(length=255))
    disputed_fields = Column(String(length=255))
    disputed_note = Column(String(length=1000))
    session_key = Column(String(length=200))
    lastremark = Column(String(length=1000))
    status = Column(String(length=100))
    payment_date = Column(Date())
    payment_amount = Column(String(length=200))
    account_name = Column(String(length=255))
    lender_name = Column(String(length=255))
    dob = Column(Date())
    emailid = Column(String(length=255))
    phone = Column(String(length=255))
    secondary_phone = Column(String(length=255))
    tertiary_phone = Column(String(length=255))
    ref1_phone = Column(String(length=255))
    ref2_phone = Column(String(length=255))
    alternate_number = Column(String(length=255))
    add_line1 = Column(String(length=2055))
    add_line2 = Column(String(length=255))
    add_line3 = Column(String(length=255))
    add_line4 = Column(String(length=255))
    city = Column(String(length=30))
    state = Column(String(length=30))
    region = Column(String(length=30))
    pincode = Column(String(length=30))
    opportunity_name = Column(String(length=255))
    masked_opportunity_name = Column(String(length=15))
    loan_product = Column(String(length=64))
    booking_month = Column(String(length=15))
    next_emi_duedate = Column(Date())
    branch = Column(String(length=100))
    # TODO: CONVERT TO ENUM
    risk_bucket = Column(String(length=15))
    ots_waiver = Column(String(length=15))
    pos = Column(Integer())
    interest_on_dues = Column(Integer())
    bounce_charges = Column(Integer())
    penal_charges = Column(Integer())
    total_outstanding = Column(Integer())
    emi_amount = Column(Integer())
    disbursed_loan_amount = Column(Integer())
    sanctioned_loan_amount = Column(Integer())
    loan_tenor = Column(String(length=255))
    opp_id = Column(String(length=255))
    amount_already_paid_to_client = Column(String(length=255))
    lead_source = Column(String(length=120))
    Onus_Offus_Tag = Column(String(length=120))
    Product_name = Column(String(length=120))
    Product_model = Column(String(length=120))
    application_id = Column(String(length=255))
    close_date = Column(Date())
    writeoff_date = Column(Date())
    dealer_code = Column(String(length=120))
    dealer_name = Column(String(length=120))
    dealer_address = Column(String(length=2055))
    dealer_pincode = Column(String(length=120))
    dealer_mobile_number = Column(String(length=15))
    dealer_city = Column(String(length=120))
    dealer_contact_person_name = Column(String(length=120))
    # field_agency= Column(Integer(), ForeignKey(column="journey_fieldagency.id"), nullable=True)

    op0_1_paid = Column(Boolean,default=False) # UNUSED
    op1_1_paid = Column(Boolean,default=False) # UNUSED
    
    op2_1_paid = Column(Boolean,default=False) # UNUSED
    op2_2_paid = Column(Boolean,default=False) # UNUSED
    
    op3_1_paid = Column(Boolean,default=False) # UNUSED
    op3_2_paid = Column(Boolean,default=False) # UNUSED
    op3_3_paid = Column(Boolean,default=False) # UNUSED

    op0_1_payment_link = Column(String(length=255))
    op1_1_payment_link = Column(String(length=255))
    op2_1_payment_link = Column(String(length=255))
    op2_2_payment_link = Column(String(length=255))
    op3_1_payment_link = Column(String(length=255))
    op3_2_payment_link = Column(String(length=255))
    op3_3_payment_link = Column(String(length=255))

    outstanding_balance = Column(Integer())

    # applicable_offer1_id = Column (Integer() ,ForeignKey(column="journey_offer.id", ondelete="CASCADE"),autoincrement=True )
    # applicable_offer2_id = Column (Integer() ,ForeignKey(column="journey_offer.id", ondelete="CASCADE"),autoincrement=True )
    # applicable_offer3_id = Column (Integer() ,ForeignKey(column="journey_offer.id", ondelete="CASCADE"),autoincrement=True )

    op1_outstanding_balance = Column(Integer())
    op1_final_settlement_amount = Column(Integer())
    op1_no_of_installments = Column(Integer())
    op2_outstanding_balance = Column(Integer())
    op2_no_of_installments = Column(Integer())
    op2_final_settlement_amount = Column(Integer())
    op3_outstanding_balance = Column(Integer())
    op3_no_of_installments = Column(Integer())
    op3_final_settlement_amount = Column(Integer())
    op1_1_installment_amount = Column(Integer())
    op1_1_installment_date = Column(Date())
    op2_1_installment_amount = Column(Integer())
    op2_1_installment_date = Column(Date())
    op2_2_installment_amount = Column(Integer())
    op2_2_installment_date = Column(Date())
    op3_1_installment_amount = Column(Integer())
    op3_1_installment_date = Column(Date())
    op3_2_installment_amount = Column(Integer())
    op3_2_installment_date = Column(Date())
    op3_3_installment_amount = Column(Integer())
    op3_3_installment_date = Column(Date())
    cibilstatusop1 = Column(String(length=255))
    cibilstatusop2 = Column(String(length=255))
    cibilstatusop3 = Column(String(length=255))
    user_ip = Column(String(length=30))
    coupon_redem_date = Column(DateTime())

    tranch_id = Column(Integer(),ForeignKey(column="journey_tranch.id"))
    # cohort_id = Column (Integer() ,ForeignKey(column="journey_cohort.id", ondelete="CASCADE"),autoincrement=True )
    # campaign_id = Column (Integer() ,ForeignKey(column="journey_canpecampaign.id", ondelete="CASCADE"),autoincrement=True )
    client_id = Column(Integer(),ForeignKey(column="journey_client.id"))
    upload_id = Column(String(length=30))
    do_not_sms = Column(Boolean(), default=False)
    send_email = Column(Boolean(), default=True)
    do_not_call = Column(Boolean(), default=False)
    sms_short_link = Column(String(length=32),default=None)
    call_priority = Column(FLOAT, default=0.0)
    
    emi_short_link = Column(String(length=32),default=None)
    default_reason = Column(String(length=255),default=None)
   
    min_due_amount=Column(Integer())
    stab_amount=Column(Integer())
    rollback_by_three=Column(Integer())
    rollback_by_one=Column(Integer())
    rollback_by_two=Column(Integer())

    do_not_sms_secondary_phone = Column(Boolean(), default=False)
    do_not_sms_tertiary_phone = Column(Boolean(), default=False)

    total_outstanding_payment_link=Column(String(length=100))


    # applicable_offer1 = orm.relationship ("Offer" ,foreign_keys="[journey_borrower.c.applicable_offer1_id]" ,remote_side=None )
    # applicable_offer2 = orm.relationship ("Offer" ,foreign_keys="[journey_borrower.c.applicable_offer2_id]" ,remote_side=None )
    # applicable_offer3 = orm.relationship ("Offer" ,foreign_keys="[journey_borrower.c.applicable_offer3_id]" ,remote_side=None )

    tranch = relationship ("Tranch")
    # cohort = orm.relationship ("Cohort" ,foreign_keys="[journey_borrower.c.cohort_id]" ,remote_side=None )
    # campaign = orm.relationship ("CanpeCampaign" ,foreign_keys="[journey_borrower.c.campaign_id]" ,remote_side=None )
    # client = orm.relationship ("Client" ,foreign_keys="[journey_borrower.c.client_id]" ,remote_side=None )
    # coupon = orm.relationship ("Coupon" ,secondary="journey_borrower_coupon" ,foreign_keys="[journey_borrower_coupon.c.borrower_id, journey_borrower_coupon.c.coupon_id]" ,remote_side=None )
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}