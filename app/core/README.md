# PlainClause: AI for Legal Assistance & Access

PlainClause is a GenAI-powered solution that makes legal information and basic legal assistance more accessible by helping users understand, compare, and navigate legal documents and information.

## Overview

Legal information can often be complex, difficult to understand, and challenging to navigate without professional assistance. PlainClause provides:

- **Simplifying complex legal documents** - Break down complex clauses into understandable language
- **Comparing contracts, agreements, or policies** - Identify similarities and differences between documents
- **Highlighting important clauses, obligations, risks, or inconsistencies** - Focus on what matters most for your situation
- **Answering questions based on provided legal documents** - Get context-specific insights
- **Helping users understand their options and potential next steps** - Provide actionable guidance
- **Generating summaries, checklists, or other actionable outputs** - Create practical documents for review
- **Helping users prepare information or questions for a legal professional** - Organize thoughts for legal consultation

## Key Features

### Persona-Based Analysis
The application uses different personas to tailor analysis based on the user's role:

- **Tenant** - For rental agreements and leases
- **Employee** - For employment contracts and workplace agreements
- **Freelancer** - For client contracts and service agreements
- **Consumer** - For terms of service, subscriptions, and privacy policies
- **Founder** - For partnership, shareholder, and investment documents
- **Buyer** - For purchase agreements, loans, and credit documents
- **Other** - General analysis for any document type

### Clause Detection
PlainClause can detect and analyze over 50 different types of legal clauses, including:

- **Control and Change** - Unilateral changes, assignment rights, exclusivity
- **Money and Exit** - Liability caps, payment terms, termination provisions
- **Rights and Restrictions** - Non-compete, IP ownership, indemnification
- **Housing and Work** - Employment terms, overtime, probation
- **Disputes and Warranties** - Arbitration, governing law, warranties

### Risk Assessment
Each clause is scored for severity (0-10) and categorized into:

- **High Risk** (≥7) - Requires immediate attention
- **Moderate Risk** (4-6) - Should be reviewed carefully
- **Low Risk** (<4) - Generally acceptable

## How It Works

1. **Document Input** - Upload or paste your legal document
2. **Persona Selection** - Choose the relevant persona for analysis
3. **AI Analysis** - The system scans for legal clauses and assesses risk
4. **Results Presentation** - Get a summary with key findings and recommendations
5. **Action Items** - Receive questions to consider and documents to gather

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git (for version control)

### Installation

```bash
# Clone this repository
git clone <repository-url>
cd plainclause

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Command Line Interface

```bash
# Analyze a document with default persona
python main.py --document lease.txt

# Analyze with specific persona
python main.py --document contract.txt --persona tenant

# Show detailed output
python main.py --document document.txt --verbose

# Output in JSON format
python main.py --document document.txt --output json
```

#### Example Analysis

```bash
python main.py --document sample_lease.txt --persona tenant
```

### Sample Documents

The repository includes sample documents for different scenarios:

- `sample_lease.txt` - Residential lease agreement
- `sample_contract.txt` - Generic service contract
- `sample_offer_letter.txt` - Employment offer letter

### Testing

```bash
# Run basic tests
python -m pytest tests/ -v

# Run demo script
python demo.py
```

## Project Structure

```
plainclause/
├── app/                    # Core application code
│   ├── __init__.py        # Core exports
│   └── core/              # Core modules
│       ├── __init__.py    # Core package
│       ├── clause_defs.py # Clause type definitions
│       ├── clauses.py     # Clause catalog and utilities
│       └── personas.py    # User persona definitions
├── main.py                # Main application entry point
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── sample_lease.txt       # Sample lease agreement
├── demo.py               # Demo script
└── tests/                # Test suite
    ├── test_core.py       # Core functionality tests
    └── test_cli.py        # CLI interface tests
```

## Example Output

When analyzing a lease agreement as a tenant, PlainClause might output:

```
PLAINCLAUSE: LEGAL DOCUMENT ANALYSIS

Document Analysis Results
Persona: Tenant or flatmate
Risk Level: Moderate
Clauses Found: 6
Average Severity: 4.2/10

Analysis for Tenant or flatmate:
- Found 6 relevant clause(s)
- 1 high-risk items (≥7 severity)
- 4 medium-risk items (4-6 severity)
- 1 low-risk items (<4 severity)

High-risk items requiring attention:
• Entry rights (line 6)
  Severity: 7/10 (base: 6)
  Group: People
  Summary: When the owner may come into your home, and on what notice.

KEY QUESTIONS TO CONSIDER:
1. Who holds my deposit, and what must happen for it to be returned in full?
2. How much notice must the landlord give before entering, and for what reasons?
3. What repairs are my responsibility and which are the landlord's?
4. Can the rent be increased during the fixed term, and by how much?
5. What exactly must I do at the end of the tenancy to avoid a deduction?

RECOMMENDED DOCUMENTS TO GATHER:
1. The signed tenancy agreement and any addendum
2. The inventory or condition report from move-in day
3. Dated photos of the property at move-in and move-out
4. Receipts for any repairs or works you paid for
5. Proof of every rent payment made
```

## Technology Stack

- **Python** - Core programming language
- **Dataclasses** - For structured data handling
- **Regular Expressions** - For clause pattern matching
- **argparse** - For command-line interface
- **JSON** - For data serialization

## Limitations and Disclaimers

PlainClause provides information and assistance, rather than replacing professional legal advice. The analysis is based on pattern matching and general legal knowledge, and should not be considered as legal advice.

**Important:**
- Always consult a qualified attorney for specific legal matters
- This tool is designed to help you prepare for legal consultation, not replace it
- The accuracy of analysis depends on the quality and completeness of the input document
- Legal requirements vary by jurisdiction

## Future Enhancements

Potential future improvements include:

- **Natural Language Processing** - More sophisticated document understanding
- **Document Comparison** - Side-by-side analysis of multiple documents
- **Legal Research Integration** - Access to current case law and statutes
- **Chat Interface** - Interactive Q&A about legal documents
- **Mobile App** - Access on smartphones and tablets
- **API Integration** - Integration with other legal tech tools

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please refer to the project documentation or contact the development team.