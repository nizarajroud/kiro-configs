---
name: aws-pricing
description: AWS Pricing MCP Server (official awslabs) — real-time pricing data, cost report generation (PDF/Markdown/HTML), CDK/Terraform cost analysis.
---
# AWS Pricing MCP Server

- **Status**: installed
- **JSON key**: `aws-pricing`
- **Wrapper**: none (uses standard AWS credentials ~/.aws/credentials)
- **Command**: `uvx awslabs.aws-pricing-mcp-server@latest`
- **Source**: https://github.com/awslabs/mcp (official AWS)
- **Blog**: https://aws.amazon.com/blogs/machine-learning/aws-costs-estimation-using-amazon-q-cli-and-aws-pricing-mcp-server/
- **Verdict**: adopted — official awslabs, uses real-time AWS pricing data

## Tools

| Tool | Description |
|------|-------------|
| `get_pricing` | Retrieve pricing info for any AWS service in any region |
| `generate_cost_report` | Generate detailed cost analysis report (PDF, Markdown, HTML, DOCX) |
| `analyze_cdk_project` | Analyze CDK project to identify services and estimate costs |
| `analyze_terraform_project` | Analyze Terraform project for cost estimation |
| `get_bedrock_patterns` | Get Bedrock architecture patterns with cost considerations |

## Usage

Provide a natural language description of the infrastructure, the server will:
1. Retrieve real-time pricing from AWS
2. Calculate costs based on usage assumptions
3. Generate a formatted report with breakdowns and optimization recommendations

## Prerequisites

- Python 3.10+
- `uv` installed (`pip install uv`)
- AWS credentials configured (for pricing API access)
- Optional: `pandoc` for PDF output (`pip install pandoc`)

## Example prompt

```
Create a cost analysis for 4 EC2 r6i.xlarge instances (192GB RAM each),
4 EBS io2 volumes (1.2TB, 2000 IOPS), Amazon EFS 5TB,
ALB, Site-to-Site VPN, CloudWatch, AWS Backup in ca-central-1.
Generate as PDF.
```

## Limitations

- Pricing data is real-time but on-demand only (Reserved/Savings Plans need manual adjustment)
- PDF generation requires pandoc
- Does not create a shareable calculator.aws link (use aws-calculator-mcp for that)
