-- Cleaned Merchant Daily Stats Query
-- Simplified from Looker-generated query to focus on daily aggregation

WITH merchant_daily_aggregation AS (
  SELECT
    merchant_ari,
    date_key,
    SUM(mdaily_authed_amount) AS total_authed_amount,
    MIN(days_since_last_authed_checkout) AS min_days_since_last_loan,
    MAX(days_since_last_authed_checkout) AS max_days_since_last_loan,
    MAX(CASE WHEN days_since_last_authed_checkout = 365 THEN 1 ELSE 0 END) AS max_is_churned_365,
    MAX(CASE WHEN days_since_last_authed_checkout = 182 THEN 1 ELSE 0 END) AS max_is_churned_182,
    MAX(CASE WHEN days_since_last_authed_checkout = 91 THEN 1 ELSE 0 END) AS max_is_churned_91,
    MAX(CASE WHEN days_since_first_authed_checkout = 0 THEN 1 ELSE 0 END) AS merchant_activation_flag
  FROM dbt_analytics.merchant_daily_stats_mart
  GROUP BY merchant_ari, date_key
)

SELECT
  mds.date_key,
  
  -- Merchant Counts by Status
  COUNT(DISTINCT CASE 
    WHEN agg.merchant_activation_flag = 1 
    THEN mds.merchant_ari 
  END) AS activated_merchant_count,
  
  COUNT(DISTINCT CASE 
    WHEN agg.merchant_activation_flag = 0 
      AND mds.days_since_last_authed_checkout < 365 
      AND agg.max_is_churned_365 = 0 
    THEN mds.merchant_ari 
  END) AS active_merchant_count_non_activated,
  
  COUNT(DISTINCT CASE 
    WHEN agg.min_days_since_last_loan > 0 
      AND agg.max_is_churned_365 = 1 
    THEN mds.merchant_ari 
  END) AS churned_merchant_count_365,
  
  COUNT(DISTINCT CASE 
    WHEN agg.min_days_since_last_loan = 0 
      AND agg.max_days_since_last_loan >= 365 
    THEN mds.merchant_ari 
  END) AS reactivated_merchant_count_365,
  
  COUNT(DISTINCT CASE 
    WHEN mds.has_authed_charge_last_182d = 1 
    THEN mds.merchant_ari 
  END) AS active_merchants_past_182_days

FROM dbt_analytics.merchant_daily_stats_mart mds

-- Join dimension and stats tables
LEFT JOIN dbt_analytics.merchant_dim md 
  ON mds.merchant_ari = md.merchant_ari
  
LEFT JOIN dbt_analytics.merchant_stats_mart msm 
  ON mds.merchant_ari = msm.merchant_ari

-- Join aggregated metrics
INNER JOIN merchant_daily_aggregation agg 
  ON mds.merchant_ari = agg.merchant_ari 
  AND mds.date_key = agg.date_key

WHERE 
  -- Date range: Last 365 days
  mds.date_key >= DATEADD('day', -364, CURRENT_DATE())
  AND mds.date_key < DATEADD('day', 1, CURRENT_DATE())
  
  -- Filter to Shopify Whitelabel Installments
  AND UPPER(md.merchant_platform) = 'SHOPIFY WHITELABEL INSTALLMENTS'
  
  -- Only merchants with first non-employee checkout
  AND msm.merchant_first_non_employee_authed_checkout_created_dt IS NOT NULL

GROUP BY mds.date_key
ORDER BY mds.date_key DESC
LIMIT 500;
