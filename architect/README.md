# Architect Agent System

An intelligent agent that continuously analyzes and improves the trading web application codebase.

## Features

- 🔍 **Automated Code Analysis**: Scans backend and frontend for issues
- 🎯 **Categorized Improvements**: Security, performance, architecture, best practices
- 📊 **Priority Scoring**: Issues ranked by severity and impact
- 🔄 **Continuous Monitoring**: Runs periodic analysis and tracks trends
- 📝 **Detailed Reports**: Generates markdown reports with actionable suggestions

## Usage

### One-time Analysis

```bash
cd /Users/orire/trading-web-app
python -m architect.runner
```

This will:
1. Analyze the entire codebase
2. Generate a detailed improvement report
3. Save report to `architect/reports/improvement_report_YYYYMMDD_HHMMSS.md`

### Continuous Monitoring

```python
from architect.continuous_improvement import ContinuousImprovementAgent

agent = ContinuousImprovementAgent(
    project_root="/Users/orire/trading-web-app",
    check_interval=3600  # Check every hour
)

# Register callbacks (e.g., create GitHub issues)
agent.register_callback(create_github_issue_callback(token, "orire-dev/trading-web-app"))

# Start monitoring
agent.start_monitoring()
```

## Analysis Categories

### Security
- Authentication/authorization
- Input validation
- CORS configuration
- Secrets management

### Performance
- Database query optimization
- Caching strategies
- Code splitting
- Async operations

### Architecture
- API versioning
- Database connection management
- Configuration management
- Monitoring/observability

### Best Practices
- Error handling
- Logging
- Type hints
- Code organization

## Improvement Severity Levels

- **Critical**: Security vulnerabilities, must fix immediately
- **High**: Important issues affecting functionality or security
- **Medium**: Should be addressed soon
- **Low**: Nice to have improvements

## Reports

Reports are saved in `architect/reports/` with timestamps. Each report includes:

- Summary statistics
- Categorized improvements
- Detailed suggestions with file paths
- Priority rankings
- Impact analysis

## Integration

The agent can be integrated into:

- **CI/CD Pipelines**: Run analysis on every commit
- **GitHub Actions**: Create issues automatically
- **Scheduled Jobs**: Periodic analysis and reporting
- **Development Workflow**: Pre-commit hooks

## Example Output

```
ARCHITECT AGENT ANALYSIS COMPLETE
================================================================================

Total Issues Found: 15

By Category:
  - security: 4
  - performance: 3
  - architecture: 5
  - best_practices: 3

By Severity:
  - critical: 1
  - high: 4
  - medium: 7
  - low: 3

Recommendations:
  🚨 1 critical security issues found - address immediately
  ⚠️ 5 high-priority improvements identified
  🔒 4 security improvements recommended
  ⚡ 3 performance optimizations available

📄 Full report saved to: architect/reports/improvement_report_20260301_120000.md
```
