text = """CALIFO RNIA
CALIFORNIA
RESIDENTIAL PURCHASE AGREEMENT
ASSOCIATION
OF REALTORS®
AND JOINT ESCROW INSTRUCTIONS
(C.A.R. Form RPA-CA, Revised 12/18)
Date Prepared: 09/01/2019
1. OFFER:
A. THIS IS AN OFFER FROM
B. THE REAL PROPERTY to be acquired is
Santosh Singh, Anupama Singh
2085 Parker Court, Simi Valley, CA 93065
93065 (Zip Code), Assessor's Parcel No.
("Buyer").
situated in
6410272495("Property").
Simi Valley
Ventura
C. THE PURCHASE PRICE offered is Five Hundred Sixty Thousand
(City),
(County), California,
D. CLOSE OF ESCROW shall occur on
E. Buyer and Seller are referred to herein as the "Parties." Brokers are not Parties to this Agreement.
Dollars $ 560,000.00
(date)(or X
40
Days After Acceptance).
2. AGENCY:
A. DISCLOSURE: The Parties each acknowledge receipt of a X "Disclosure Regarding Real Estate Agency Relationships" (C.A.R.
Form AD).
B. CONFIRMATION: The following agency relationships are confirmed for this transaction:
Seller's Brokerage Firm
Is the broker of (check one): X the seller; or both the buyer and seller. (dual agent)
Seller's Agent
Is (check one): X the Seller's Agent. (salesperson or broker associate)
Buyer's Brokerage Firm
Is the broker of (check one): X the buyer; or both the buyer and seller. (dual agent)
Buyer's Agent
Is (check one): X the Buyer's Agent. (salesperson or broker associate)
C. POTENTIALLY COMPETING BUYERS AND SELLERS: The Parties each acknowledge receipt of a
Representation of More than One Buyer or Seller - Disclosure and Consent" (C.A.R. Form PRBS).
Century 21 Hilltop
License Number
01518716
License Number
both the Buyer's and Seller's Agent. (dual agent)
Susie Hill
00526188
KW Encino-Sherman Oaks
License Number
Sunil Mehra
License Number
01474866
both the Buyer's and Seller's Agent. (dual agent)
X "Possible
3. FINANCE TERMS: Buyer represents that funds will be good when deposited with Escrow Holder.
A. INITIAL DEPOSIT: Deposit shall be in the amount of ...
(1) Buyer Direct Deposit: Buyer shall deliver deposit directly to Escrow Holder by electronic funds
transfer, cashier's check, personal check, other
after Acceptance (or
OR (2) Buyer Deposit with Agent: Buyer has given the deposit by personal check (or
to the agent submitting the offer (or to
16,800.00
within 3 business days
);
), made payable to
The deposit shall be held uncashed until Acceptance and then deposited
with Escrow Holder within 3 business days after Acceptance (or
Deposit checks given to agent shall be an original signed check and not a copy.
(Note: Initial and increased deposits checks received by agent shall be recorded in Broker's trust fund log.)
B. INCREASED DEPOSIT: Buyer shall deposit with Escrow Holder an increased deposit in the amount of.
within
Days After Acceptance (or
If the Parties agree to liquidated damages in this Agreement, they also agree to incorporate the increased
deposit into the liquidated damages amount in a separate liquidated damages clause (C.A.R. Form
RID) at the time the increased deposit is delivered to Escrow Holder.
c. O ALL CASH OFFER: No loan is needed to purchase the Property. This offer is NOT contingent on Buyer
obtaining a loan. Written verification of sufficient funds to close this transaction IS ATTACHED to this offer or
Buyer shall, within 3 (or
D. LOAN(S):
(1) FIRST LOAN: in the amount of.
This loan will be conventional financing OR
) Days After Acceptance, Deliver to Seller such verification.
448,000.00
Seller financing (C.A.R. Form SFA),
This loan shall be at a fixed
Other
assumed financing (C.A.R. Form AFA OOEHA, OVA,
% or, an adjustable rate loan with initial rate not to exceed
rate not to exceed
Regardless of the type of loan, Buyer shall pay points not to exceed
(2) ŠECOND LOAN in the amount of.
This loan will be conventional financing OR Seller financing (C.A.R. Form SFA), assumed
financing (C.A.R. Form AFA), Other
exceed
Regardless of the type of loan, Buyer shall pay points not to exceed
(3) FHAVA: For any FHA or VA loan specified in 3D(1), Buyer has 17 (or
to Deliver to Seller written notice (C.A.R. Form FVA) of any lender-required repairs or costs that
Buyer requests Seller to pay for or otherwise correct. Seller has no obligation to pay or satisfy lender
requirements unless agreed in writing. A FHAVA amendatory clause (C.A.R. Form FVAC) shall be a
part of this Agreement.
6.000
%.
% of the loan amount.
.....
This loan shall be at a fixed rate not to
% or,
an adjustable rate loan with initial rate not to exceed
%.
% of the loan amount.
) Days After Acceptance
E. ADDITIONAL FINANCING TERMS:
F. BALANCE OF DOWN PAYMENT OR PURCHASE PRICE in the amount of
to be deposited with Escrow Holder pursuant to Escrow Holder instructions.
G. PURCHASE PRICE (TOTAL): .
Buyer's Initials C
© 1991-2018, California Association of REALTORS®, Inc.
95,200.00
2$
560,000.00
Seller's Initials
%3D
RPA-CA REVISED 12/18 (PAGE 1 OF 10)
DQUAL MOUSNG
OPORTUNTY
CALIFORNIA RESIDENTIAL PURCHASE AGREEMENT (RPA-CA PAGE 1 OF 10)
Keller Williams Encino-Sherman Oaks, 16820 Ventura Blvd Encino CA 91436
Phone: 818.458.0346
Fax: 818.301.2166
2085 Parker Ct
Jennifer Santulan
Produced with zipForm® by zipLogix 18070 Fifteen Mile Road, Fraser, Michigan 48026 www.zipLogix.com
"""

text = text.lower()
text_split = text.splitlines()
text_join = '. '.join(text_split)
print(text_join)

entity = ['date prepared','purchase price',"seller's brokerage firm"]
text_join



res = [j for i in text_join for j in entity if j in i]

print(res)