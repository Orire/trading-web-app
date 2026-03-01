"""
Architect Agent Runner
Executes the architect agent and generates reports
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from architect.agent import ArchitectAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run architect agent analysis"""
    # Get project root (parent of architect directory)
    project_root = Path(__file__).parent.parent
    
    logger.info(f"Initializing Architect Agent for project: {project_root}")
    
    # Create agent
    agent = ArchitectAgent(str(project_root))
    
    # Run analysis
    logger.info("Running project analysis...")
    analysis = agent.analyze_project()
    
    # Generate report
    report_path = project_root / "architect" / "reports" / f"improvement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Generating report: {report_path}")
    report = agent.generate_report(str(report_path))
    
    print("\n" + "="*80)
    print("ARCHITECT AGENT ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nTotal Issues Found: {analysis['total_issues']}")
    print(f"\nBy Category:")
    for cat, count in analysis['by_category'].items():
        print(f"  - {cat}: {count}")
    print(f"\nBy Severity:")
    for sev, count in analysis['by_severity'].items():
        print(f"  - {sev}: {count}")
    print(f"\nRecommendations:")
    for rec in analysis['recommendations']:
        print(f"  {rec}")
    print(f"\n📄 Full report saved to: {report_path}")
    print("="*80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
