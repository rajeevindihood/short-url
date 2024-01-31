from decimal import Decimal

from sqlalchemy import (
    ARRAY,
    FLOAT,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    false,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base


class Borrower(Base):
    __tablename__ = "journey_borrower"
    __table_args__ = (
        Index("journey_borrower_tranch_id_94e4d1a1", "tranch_id"),
        # Index("journey_borrower_cohort_id_fd397415", "cohort_id"),
        Index("journey_borrower_client_id_2283686a", "client_id"),
        Index("journey_borrower_canpebid_idx", "canpebid"),
        # Index("journey_borrower_campaign_id_a85c93a5", "campaign_id"),
        # Index("journey_borrower_applicable_offer1_id_5e1f23bf", "applicable_offer1_id"),
        # Index("journey_borrower_applicable_offer2_id_a8c4992d", "applicable_offer2_id"),
        # Index("journey_borrower_applicable_offer3_id_8583ca61", "applicable_offer3_id"),
    )

    id = Column(Integer(), primary_key=True)

    # LSQ ID
    Prospect_ID = Column(
        String(length=255),
        nullable=True,
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
    account_name = Column(String(length=255), nullable=False)
    lender_name = Column(String(length=255))
    dob = Column(Date())
    emailid = Column(String(length=255))
    phone = Column(String(length=255), nullable=False)
    secondary_phone = Column(String(length=255))
    tertiary_phone = Column(String(length=255))
    alternate_number = Column(String(length=255))
    # mother / father / spouse aren't used in collections, just origination
    father_phone = Column(String(length=16))
    mother_phone = Column(String(length=16))
    spouse_phone = Column(String(length=16))
    ref1_phone = Column(String(length=255))
    ref2_phone = Column(String(length=255))
    ref3_phone = Column(String(length=16))
    ref4_phone = Column(String(length=16))
    ref5_phone = Column(String(length=16))

    # phone_names aren't used in collections,
    # but there was a requirement in origination
    # so it was as good a time as any to add them in
    father_name = Column(String(length=255))
    mother_name = Column(String(length=255))
    spouse_name = Column(String(length=255))
    ref1_name = Column(String(length=255))
    ref2_name = Column(String(length=255))
    ref3_name = Column(String(length=255))
    ref4_name = Column(String(length=255))
    ref5_name = Column(String(length=255))

    add_line1 = Column(String(length=2055))
    add_line2 = Column(String(length=2055))
    add_line3 = Column(String(length=2055))
    add_line4 = Column(String(length=2055))
    city = Column(String(length=30))
    state = Column(String(length=30))
    region = Column(String(length=30))
    pincode = Column(String(length=30))
    opportunity_name = Column(String(length=255), nullable=False)
    masked_opportunity_name = Column(String(length=15))
    loan_product = Column(String(length=64))
    booking_month = Column(String(length=15))
    next_emi_duedate = Column(Date())
    branch = Column(String(length=100))
    # TODO: CONVERT TO ENUM
    risk_bucket = Column(String(length=15))
    risk_bucket_days = Column(
        Integer(),
        comment="Number of days since the last emi due date. This is a static field obtained at allocation time",
        nullable=True,
    )
    ots_waiver = Column(String(length=15))
    twop_waiver = Column(FLOAT, default=0.0)
    threep_waiver = Column(FLOAT, default=0.0)
    max_waiver = Column(FLOAT, default=0.0)

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
    product_name = Column(String(length=120))
    product_model = Column(String(length=120))
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
    field_agency = Column(
        Integer(),
        # ForeignKey(column="journey_fieldagency.id"),
        nullable=True,
    )

    op0_1_paid = Column(Boolean, default=False)  # UNUSED
    op1_1_paid = Column(Boolean, default=False)  # UNUSED

    op2_1_paid = Column(Boolean, default=False)  # UNUSED
    op2_2_paid = Column(Boolean, default=False)  # UNUSED

    op3_1_paid = Column(Boolean, default=False)  # UNUSED
    op3_2_paid = Column(Boolean, default=False)  # UNUSED
    op3_3_paid = Column(Boolean, default=False)  # UNUSED

    op0_1_payment_link = Column(String(length=255))
    op1_1_payment_link = Column(String(length=255))
    op2_1_payment_link = Column(String(length=255))
    op2_2_payment_link = Column(String(length=255))
    op3_1_payment_link = Column(String(length=255))
    op3_2_payment_link = Column(String(length=255))
    op3_3_payment_link = Column(String(length=255))

    outstanding_balance = Column(Integer())

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
    cibil_score = Column(Integer())
    cibilstatusop1 = Column(String(length=255))
    cibilstatusop2 = Column(String(length=255))
    cibilstatusop3 = Column(String(length=255))
    user_ip = Column(String(length=30))
    coupon_redem_date = Column(DateTime())

    tranch_id = Column(
        Integer(), ForeignKey(column="journey_tranch.id", initially="DEFERRED")
    )
    client_id = Column(
        Integer(), ForeignKey(column="journey_client.id", initially="DEFERRED")
    )
    upload_id = Column(String(length=30))
    send_email = Column(Boolean(), default=True)
    sms_short_link: Mapped[str] = mapped_column(String(length=32), default=None)
    call_priority = Column(FLOAT, default=0.0)

    emi_short_link = Column(String(length=32), default=None)
    default_reason = Column(String(length=255), default=None)

    min_due_amount = Column(Integer())
    stab_amount = Column(Integer())
    rollback_by_three = Column(Integer())
    rollback_by_one = Column(Integer())
    rollback_by_two = Column(Integer())

    dnd = Column(Boolean(), default=False, server_default=false(), nullable=False)
    dnd_whatsapp = Column(
        Boolean(), default=False, server_default=false(), nullable=False
    )
    do_not_call = Column(Boolean(), default=False)
    do_not_sms = Column(Boolean(), default=False)
    do_not_sms_secondary_phone = Column(Boolean(), default=False)
    do_not_sms_tertiary_phone = Column(Boolean(), default=False)

    total_outstanding_payment_link = Column(String(length=100))
    is_retained = Column(Boolean(), default=True)
    retention_date = Column(DateTime())
    last_tracked_city = Column(String(length=100))
    latitude = Column(FLOAT())
    longitude = Column(FLOAT())
    pos_bin = Column(Integer())
    probability_paid = Column(FLOAT())
    predicted_purchases = Column(FLOAT())
    flag_location_access = Column(Integer())
    # applicable_offer1_id = Column(
    #     Integer(), ForeignKey("journey_offer.id", initially="DEFERRED")
    # )
    # applicable_offer2_id = Column(
    #     Integer(), ForeignKey("journey_offer.id", initially="DEFERRED")
    # )
    # applicable_offer3_id = Column(
    #     Integer(), ForeignKey("journey_offer.id", initially="DEFERRED")
    # )
    discounted_list = Column(ARRAY(Integer()))
    Product_model = Column(String(120))  # TODO: Drop column
    Product_name = Column(String(120))  # TODO: Drop column
    other_charges = Column(Integer())
    # cohort_id = Column(Integer(), ForeignKey("journey_cohort.id", initially="DEFERRED"))
    # campaign_id = Column(
    #     Integer(), ForeignKey("journey_canpecampaign.id", initially="DEFERRED")
    # )
    paid_amount = Column(
        Numeric, default=Decimal("0"), server_default=text("0::NUMERIC"), nullable=False
    )
    salary = Column(Numeric)
    entity_type = Column(
        Enum("BORROWER", "PROSPECT", "PROSPECT_LOAN"),
        server_default="BORROWER",
        nullable=False,
    )
    # company_id = Column(Integer(), ForeignKey("t_company.id", initially="DEFERRED"))

    tranch = relationship("Tranch")
    # analytics = relationship(
    #     "BorrowerAnalytics", back_populates="borrower", uselist=False
    # )
    # company = relationship("Company")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
