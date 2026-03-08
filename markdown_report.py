def generate_report(sector: str, analysis: str) -> str:
    """
    Generate a Markdown report for a sector based on AI analysis.
    """
    report = f"""
# Trade Opportunities Report

## Sector
{sector}

## AI Market Analysis
{analysis}

## Conclusion
The above insights highlight potential trade opportunities in the {sector} sector in India.
"""
    return report
