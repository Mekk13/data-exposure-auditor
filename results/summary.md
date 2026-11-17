# Results summary

Synthetic data only. These numbers show the method, not real findings.

## Detector metrics

| category | tp | fp | fn | precision | recall | f1 |
|---|---|---|---|---|---|---|
| cnp | 57 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| health | 54 | 35 | 12 | 0.607 | 0.818 | 0.697 |
| names | 126 | 5 | 32 | 0.962 | 0.797 | 0.872 |
| email | 29 | 28 | 0 | 0.509 | 1.000 | 0.674 |
| phone | 44 | 62 | 0 | 0.415 | 1.000 | 0.587 |
| birthdate | 63 | 0 | 15 | 1.000 | 0.808 | 0.894 |
| sensitive | 91 | 28 | 7 | 0.765 | 0.929 | 0.839 |

## Hypothesis

Among exposed pre-GDPR documents that contain personal data, the share labelled sensitive:

| group | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| all | 62 | 108 | 57.4% | 48.0% - 66.3% |

## By institution type (pre-GDPR)

| institution_type | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| hospital | 20 | 22 | 90.9% | 72.2% - 97.5% |
| results_portal | 17 | 27 | 63.0% | 44.2% - 78.5% |
| school | 14 | 30 | 46.7% | 30.2% - 63.9% |
| town_hall | 11 | 29 | 37.9% | 22.7% - 56.0% |

## By city size (pre-GDPR)

| city_size | sensitive | with personal data | share | 95% CI |
|---|---|---|---|---|
| large | 27 | 45 | 60.0% | 45.5% - 73.0% |
| medium | 21 | 36 | 58.3% | 42.2% - 72.9% |
| small | 14 | 27 | 51.9% | 34.0% - 69.3% |
