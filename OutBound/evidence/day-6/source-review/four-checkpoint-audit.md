# Four-checkpoint audit: November 6 rerun

Nine flags, four sequential batch executions, 36 per-flag results. [Frozen collector packet](source-review-request.json). [Original shared-session verdicts](desktop-verdicts.json). These new checkpoints audited the retained evidence and disposition; their timestamps belong to this rerun. The original review remains historical. Code verifies the complete chain and verdict digest before applying a decision. Roles shared assistant context. Pass denotes completion of the specified check; commercial disposition is separate.

| Account / category | Collection/QC | Researcher | Skeptic | Fact-checker |
|---|---|---|---|---|
| SURREY FOOD BANK SOCIETY / operational_strain (`signal-05cb7c7fb182aa89f8d18520`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| Seattle Good Business Network / financial_pressure (`signal-fd575c91233a256a8e898589`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Hold](checkpoints/fact_checker.json) |
| CLARK COUNTY FOOD BANK / operational_strain (`signal-5eff20a2203c656f9bb5c616`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| CLARK COUNTY FOOD BANK / financial_pressure (`signal-bc6d441f41e791b2b95e57c2`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| SURREY FOOD BANK SOCIETY / fundraising_pressure (`signal-82ce9ff52cb9b7c94898de91`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| CLARK COUNTY FOOD BANK / operational_strain (`signal-6e9ef48a6633133f4c83bdca`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| Food Lifeline / campaign_performance (`signal-e30d24146a3d0e4d851f7181`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| Food Lifeline / fundraising_pressure (`signal-e9eb4b0e748f8cc244e0a9a8`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Pass](checkpoints/fact_checker.json) |
| FamilyWorks / campaign_performance (`signal-606f8881901d692f838825a8`) | [Pass](checkpoints/qc.json) | [Pass](checkpoints/researcher.json) | [Pass](checkpoints/skeptic.json) | [Hold](checkpoints/fact_checker.json) |

Each linked execution contains the per-flag reasons, document and candidate versions, source URL, actor, execution time and predecessor. [Submitted inputs](audit-inputs). The two holds are FamilyWorks (campaign outcome/period) and Good Business Network (funding-cut timing and remaining effect). Neither reaches the owner queue. The other seven flags supply historical/positive context or rejected interpretations.
