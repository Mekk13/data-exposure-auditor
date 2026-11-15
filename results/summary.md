# Results summary

Synthetic data only. These numbers show the method, not real findings.

## Detector metrics

| category | tp | fp | fn | precision | recall | f1 |
|---|---|---|---|---|---|---|
| cnp | 66 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| health | 63 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| names | 172 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| email | 37 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| phone | 53 | 65 | 0 | 0.449 | 1.000 | 0.620 |
| birthdate | 80 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| sensitive | 101 | 0 | 0 | 1.000 | 1.000 | 1.000 |

## Hypothesis

Among exposed pre-GDPR documents that contain personal data, the share labelled sensitive:

| group | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| all | 56 | 116 | 48.3% | 39.4% - 57.3% |

## By institution type (pre-GDPR)

| institution_type | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| hospital | 21 | 25 | 84.0% | 65.3% - 93.6% |
| results_portal | 7 | 30 | 23.3% | 11.8% - 40.9% |
| school | 14 | 31 | 45.2% | 29.2% - 62.2% |
| town_hall | 14 | 30 | 46.7% | 30.2% - 63.9% |

## By city size (pre-GDPR)

| city_size | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| large | 20 | 39 | 51.3% | 36.2% - 66.1% |
| medium | 20 | 44 | 45.5% | 31.7% - 59.9% |
| small | 16 | 33 | 48.5% | 32.5% - 64.8% |
