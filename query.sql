SELECT
-- need to have these dates based on the input from the questionnaire -- 

CASE 
    WHEN to_date(cfv5.checkout_created_dt) BETWEEN '{pre_start_date}' AND '{pre_end_date}' THEN 'Pre'
    WHEN to_date(cfv5.checkout_created_dt) BETWEEN '{post_start_date}' AND '{post_end_date}' THEN 'Post'
    ELSE 'Other'
END AS analysis_period


, CASE WHEN cfv5.user_ari IS NULL THEN 'UNKNOWN'
    WHEN to_date(cfv5.checkout_created_dt) <= coalesce(to_date(person_first_authed_charge_created_dt),current_date+1) THEN 'NEW'
    WHEN to_date(cfv5.checkout_created_dt) > coalesce(to_date(person_first_authed_charge_created_dt),current_date+1) THEN 'REPEAT'
    ELSE 'OTHER' END AS new_vs_repeat_person
    
, CASE 
  WHEN cfv5.total_amount < 100 THEN '1|<$100'
  WHEN cfv5.total_amount >= 100 AND cfv5.total_amount < 250 THEN '2|$100-250'
  WHEN cfv5.total_amount >= 250 AND cfv5.total_amount < 500 THEN '3|$250-500'
  WHEN cfv5.total_amount >= 500 AND cfv5.total_amount < 1000 THEN '4|$500-1000'
  WHEN cfv5.total_amount >= 1000 THEN '5|$1000+'
  ELSE '6|Other'
END AS AOV_bucket

, CASE
        WHEN fico_score >= 729 THEN '1: Super Prime (729+)'
        WHEN fico_score >= 660 THEN '2: Prime (660-729)'
        WHEN fico_score >= 620 THEN '3: Near Prime (620-659)'
        WHEN fico_score >= 580 THEN '4: Subprime (580-619)'
        WHEN fico_score >= 550 THEN '5: Deep Subprime (550-579)'
        WHEN fico_score >= 250 THEN '6: Deep Subprime (<550)'
        ELSE '7: Missing FICO'
    END AS fico_bucket

, CASE
        WHEN itacs_v1 >= 98 then '1: 98+'
        WHEN itacs_v1 >= 96 then '2: 96+'
        WHEN itacs_v1 >= 95 then '3: 95-96'
        WHEN itacs_v1 >= 94 then '4: 94-95'
        WHEN itacs_v1 IS NOT NULL AND itacs < 94 THEN '5: < 94'
        ELSE 'Unknown'
    END as itacs_bucket


, CASE when cfv5.loan_type = 'affirm_go_v3' then 'PI4' 
         when cfv5.loan_type = 'classic' and cf.apr > 0 then 'IB'
         when cfv5.loan_type = 'classic' and cf.apr = 0 then '0pct' end as loan_type_checkout, 
 
, count(distinct cfv5.checkout_ari) as checkouts
, count(distinct case when cfv5.is_login_authenticated = 1 then cfv5.checkout_ari end) as authenticated
, count(distinct case when is_identity_approved = 1 then checkout_ari end) as identity_approved 
, count(distinct case when is_fraud_approved = 1 then checkout_ari end) as fraud_approved 
, count(distinct case when cfv5.is_checkout_applied = 1 then cfv5.checkout_ari end) as applied
, count(distinct case when cfv5.is_approved = 1 then cfv5.checkout_ari end) as approved_checkouts 
, count(distinct case when cfv5.is_confirmed = 1 then cfv5.checkout_ari end) as confirmed_checkouts
, count(distinct case when cfv5.is_authed = 1 then cfv5.checkout_ari end) as authed_checkouts
, sum(case when cfv5.is_authed = 1 then cfv5.total_amount end) as GMV
, COALESCE(authenticated,0) / NULLIF(checkouts,0) as authentication_rate
, COALESCE(identity_approved,0) / NULLIF(authenticated,0) as identity_approval_rate
, COALESCE(fraud_approved,0) / NULLIF(authenticated,0) as fraud_approval_rate
, COALESCE(applied,0) / NULLIF(checkouts,0) as application_rate
, COALESCE(approved_checkouts,0) / NULLIF(applied,0) as credit_approval_rate
, COALESCE(confirmed_checkouts,0) / NULLIF(approved_checkouts,0) as confirmation_rate
, COALESCE(authed_checkouts,0) / NULLIF(confirmed_checkouts,0) as authorization_rate
, COALESCE(authed_checkouts,0) / NULLIF(checkouts,0) as E2E
, COALESCE(SUM(CASE WHEN cfv5.is_authed = 1 THEN cfv5.total_amount END),0)/ NULLIF(authed_checkouts,0) as AOV


from prod__us.dbt_analytics.checkout_funnel_v5 cfv5
left join prod__us.dbt_analytics.merchant_dim md on md.merchant_ari = cfv5.merchant_ari
left join prod__us.dbt_analytics.user_dim on cfv5.user_ari = user_dim.user_ari
left join prod__us.dbt_analytics.person_stats_mart on user_dim.person_uuid = person_stats_mart.person_uuid

-- need to have this based on the input from the questionnaire -- 
WHERE md.merchant_ari IN ({merchant_ari_list}) OR md.merchant_partner_ari IN ({merchant_ari_list})

group by all 
