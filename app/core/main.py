"""PlainClause: AI for Legal Assistance & Access
Main application entry point
"""

import sys
import argparse
from typing import Optional
from app.core.clauses import get_clause_type, compiled_patterns
from app.core.personas import get_persona, PERSONA_IDS
import re


class PlainClauseAnalyzer:
    """Main analyzer for legal documents."""
    
    def __init__(self):
        self.patterns = compiled_patterns()
    
    def analyze_document(self, text: str, persona_id: str = "other") -> dict:
        """
        Analyze a legal document for clause detection and risk assessment.
        
        Args:
            text: The legal document text to analyze
            persona_id: The persona to use for analysis (tenant, employee, etc.)
            
        Returns:
            Dictionary containing analysis results
        """
        persona = get_persona(persona_id)
        lines = text.split('\n')
        
        detected_clauses = []
        total_severity = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # Check each clause pattern
            for clause_id, pattern_group in self.patterns:
                for pattern in pattern_group:
                    if pattern.search(line):
                        clause_type = get_clause_type(clause_id)
                        
                        # Apply persona weighting
                        weighted_severity = clause_type.base_severity + \
                                          persona.severity_weights.get(clause_id, 0)
                        weighted_severity = max(0, min(10, weighted_severity))
                        
                        detected_clauses.append({
                            'line_number': i,
                            'line_text': line,
                            'clause_id': clause_id,
                            'clause_label': clause_type.label,
                            'group': clause_type.group,
                            'base_severity': clause_type.base_severity,
                            'weighted_severity': weighted_severity,
                            'summary': clause_type.summary,
                            'why_it_matters': clause_type.why_it_matters,
                            'watch_for': clause_type.watch_for,
                            'negotiation_tip': clause_type.negotiation_tip,
                            'matched_pattern': pattern.pattern
                        })
                        
                        total_severity += weighted_severity
                        break  # Avoid double counting same line
        
        # Calculate risk level
        avg_severity = total_severity / len(detected_clauses) if detected_clauses else 0
        risk_level = self._get_risk_level(avg_severity)
        
        return {
            'persona': persona.label,
            'total_clauses_found': len(detected_clauses),
            'average_severity': round(avg_severity, 2),
            'risk_level': risk_level,
            'clauses': detected_clauses,
            'summary': self._generate_summary(detected_clauses, persona),
            'questions_to_ask': persona.questions,
            'documents_to_gather': persona.documents_to_gather
        }
    
    def _get_risk_level(self, avg_severity: float) -> str:
        """Convert average severity to risk level."""
        if avg_severity >= 7:
            return "High"
        elif avg_severity >= 4:
            return "Moderate"
        else:
            return "Low"
    
    def _generate_summary(self, clauses: list, persona) -> str:
        """Generate a human-readable summary."""
        if not clauses:
            return f"No significant clauses detected for {persona.label} review."
        
        high_risk = [c for c in clauses if c['weighted_severity'] >= 7]
        medium_risk = [c for c in clauses if 4 <= c['weighted_severity'] < 7]
        low_risk = [c for c in clauses if c['weighted_severity'] < 4]
        
        summary_parts = [
            f"Analysis for {persona.label}:",
            f"- Found {len(clauses)} relevant clause(s)",
            f"- {len(high_risk)} high-risk items (≥7 severity)",
            f"- {len(medium_risk)} medium-risk items (4-6 severity)", 
            f"- {len(low_risk)} low-risk items (<4 severity)"
        ]
        
        if high_risk:
            summary_parts.append("\nHigh-risk items requiring attention:")
            for clause in high_risk[:3]:  # Show top 3
                summary_parts.append(f"  • {clause['clause_label']} (line {clause['line_number']})")
        
        return '\n'.join(summary_parts)


def main():
    """Main entry point for the PlainClause application."""
    parser = argparse.ArgumentParser(
        description="PlainClause: AI for Legal Assistance & Access",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --document lease.txt --persona tenant
  python main.py --document contract.txt --persona employee --verbose
        """
    )
    
    parser.add_argument(
        '--document', '-d',
        type=str,
        required=True,
        help='Path to the legal document to analyze'
    )
    
    parser.add_argument(
        '--persona', '-p',
        type=str,
        choices=PERSONA_IDS,
        default='other',
        help='Persona to use for analysis (default: other)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed clause information'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    try:
        # Read the document
        with open(args.document, 'r', encoding='utf-8') as f:
            document_text = f.read()
        
        # Analyze
        analyzer = PlainClauseAnalyzer()
        results = analyzer.analyze_document(document_text, args.persona)
        
        # Output results
        if args.output == 'json':
            import json
            print(json.dumps(results, indent=2))
        else:
            print_analysis_results(results, args.verbose)
            
    except FileNotFoundError:
        print(f"Error: Document '{args.document}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_analysis_results(results: dict, verbose: bool = False):
    """Print analysis results in human-readable format."""
    print("=" * 60)
    print("PLAINCLAUSE: LEGAL DOCUMENT ANALYSIS")
    print("=" * 60)
    print()
    
    print(f"Document Analysis Results")
    print(f"Persona: {results['persona']}")
    print(f"Risk Level: {results['risk_level']}")
    print(f"Clauses Found: {results['total_clauses_found']}")
    print(f"Average Severity: {results['average_severity']}/10")
    print()
    
    print(results['summary'])
    print()
    
    if verbose and results['clauses']:
        print("DETAILED CLAUSE FINDINGS:")
        print("-" * 40)
        for clause in results['clauses']:
            print(f"Line {clause['line_number']}: {clause['clause_label']}")
            print(f"  Severity: {clause['weighted_severity']}/10 "
                  f"(base: {clause['base_severity']})")
            print(f"  Group: {clause['group']}")
            print(f"  Summary: {clause['summary']}")
            if verbose:
                print(f"  Why it matters: {clause['why_it_matters']}")
                print(f"  Watch for: {', '.join(clause['watch_for'])}")
                print(f"  Negotiation tip: {clause['negotiation_tip']}")
            print()
    
    print("KEY QUESTIONS TO CONSIDER:")
    print("-" * 40)
    for i, question in enumerate(results['questions_to_ask'], 1):
        print(f"{i}. {question}")
    print()
    
    print("RECOMMENDED DOCUMENTS TO GATHER:")
    print("-" * 40)
    for i, doc in enumerate(results['documents_to_gather'], 1):
        print(f"{i}. {doc}")
    print()
    
    print("=" * 60)
    print("Disclaimer: This tool provides information and assistance,")
    print("not professional legal advice. Consult a qualified attorney")
    print("for specific legal matters.")
    print("=" * 60)


if __name__ == "__main__":
    main()