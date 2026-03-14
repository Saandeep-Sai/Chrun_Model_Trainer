# Monitoring Strategy for Customer Churn Prediction System

## Overview

This document outlines the comprehensive monitoring strategy for the customer churn prediction system to ensure reliability, performance, and business value in production.

---

## 1. Logging Architecture

### Log Levels

**INFO**: Normal operations
- Model loaded successfully
- Prediction requests received
- Batch scoring completed
- API startup/shutdown

**WARNING**: Potential issues
- High response times
- Unusual prediction distributions
- Missing optional features
- Deprecated feature usage

**ERROR**: Failures requiring attention
- Model loading failures
- Prediction errors
- API timeouts
- Data validation failures

**CRITICAL**: System-level failures
- API crashes
- Database connection loss
- Out of memory errors
- Security breaches

### Log Files

#### monitoring.log
**Purpose**: API activity and predictions  
**Rotation**: Daily, keep 30 days  
**Location**: Project root  

**Contents**:
```
Timestamp | Level | Message | Context
```

**Example**:
```
2024-01-15 10:30:45,123 - INFO - Prediction successful - Churn: No Churn, Probability: 0.2345
2024-01-15 10:31:12,456 - ERROR - Prediction failed: Missing feature 'tenure'
2024-01-15 10:32:03,789 - WARNING - High response time: 1.2s
```

#### batch_scoring.log
**Purpose**: Batch job execution  
**Rotation**: Weekly, keep 12 weeks  
**Location**: Project root  

**Contents**:
- Job start/end times
- Records processed
- Success/failure counts
- Error details

---

## 2. Metrics to Track

### System Metrics

#### API Performance
- **Request Rate**: Requests per minute/hour
  - Target: Stable, no sudden spikes
  - Alert: >200% increase in 5 minutes

- **Response Time**: Time to return prediction
  - Target: <500ms (p95)
  - Warning: >500ms
  - Critical: >2000ms

- **Error Rate**: Failed requests / total requests
  - Target: <1%
  - Warning: >1%
  - Critical: >5%

- **Uptime**: Percentage of time API is available
  - Target: >99.5%
  - Alert: <99%

#### Resource Utilization
- **CPU Usage**: Percentage of CPU used
  - Target: <70%
  - Warning: >80%
  - Critical: >95%

- **Memory Usage**: RAM consumption
  - Target: <4GB
  - Warning: >6GB
  - Critical: >8GB

- **Disk Space**: Available storage
  - Target: >50% free
  - Warning: <20% free
  - Critical: <10% free

### Model Performance Metrics

#### Prediction Quality
- **Prediction Distribution**: Churn vs No Churn ratio
  - Expected: ~20-30% churn rate
  - Alert: >50% deviation from baseline

- **Confidence Distribution**: Average prediction probability
  - Monitor: Mean, median, std dev
  - Alert: Significant shifts in distribution

- **Feature Statistics**: Input data characteristics
  - Track: Mean, std dev for numeric features
  - Track: Category frequencies for categorical
  - Alert: >20% drift from training data

#### Business Metrics
- **Actual Churn Rate**: Real customer churn (when available)
  - Compare: Predicted vs actual
  - Target: <10% difference

- **Prediction Accuracy**: Correct predictions / total
  - Target: >80%
  - Warning: <75%
  - Critical: <70%

- **Precision**: True positives / (True positives + False positives)
  - Target: >75%
  - Monitor: Weekly

- **Recall**: True positives / (True positives + False negatives)
  - Target: >70%
  - Monitor: Weekly

---

## 3. Monitoring Implementation

### Real-Time Monitoring

#### Log Parsing Script
```python
# monitor_logs.py
import re
from collections import Counter
from datetime import datetime, timedelta

def analyze_logs(log_file, hours=1):
    """Analyze recent log entries"""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    metrics = {
        'total_requests': 0,
        'errors': 0,
        'warnings': 0,
        'predictions': Counter()
    }
    
    with open(log_file, 'r') as f:
        for line in f:
            # Parse timestamp and level
            # Count metrics
            # Detect anomalies
            pass
    
    return metrics
```

#### Health Check Endpoint
Already implemented in `app/main.py`:
```python
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })
```

**Monitoring Frequency**: Every 30 seconds

### Batch Monitoring

#### Daily Reports
Generate daily summary:
- Total predictions made
- Error count and types
- Average response time
- Prediction distribution
- Top error messages

#### Weekly Analysis
- Model performance trends
- Feature drift detection
- Business metric correlation
- Capacity planning

#### Monthly Reviews
- Comprehensive performance report
- Model accuracy assessment
- Infrastructure optimization
- Cost analysis

---

## 4. Alerting Rules

### Critical Alerts (Immediate Response)

**API Down**
- Condition: Health check fails 3 consecutive times
- Response Time: 5 minutes
- Action: Restart API, check logs, escalate if needed

**High Error Rate**
- Condition: Error rate >5% for 5 minutes
- Response Time: 15 minutes
- Action: Investigate logs, check data quality

**Model Loading Failure**
- Condition: Model fails to load on startup
- Response Time: Immediate
- Action: Check model file, restore from backup

**Resource Exhaustion**
- Condition: Memory >95% or Disk <5%
- Response Time: 10 minutes
- Action: Clear logs, restart services, scale resources

### Warning Alerts (Monitor Closely)

**Slow Response Time**
- Condition: p95 response time >500ms for 10 minutes
- Response Time: 1 hour
- Action: Check system load, optimize if needed

**Elevated Error Rate**
- Condition: Error rate >1% for 15 minutes
- Response Time: 2 hours
- Action: Review error patterns, fix common issues

**Prediction Drift**
- Condition: Churn rate prediction >40% deviation
- Response Time: 4 hours
- Action: Investigate data quality, check for drift

**Resource Warning**
- Condition: CPU >80% or Memory >6GB
- Response Time: 4 hours
- Action: Monitor trends, plan scaling

### Info Alerts (Track Trends)

**Usage Spike**
- Condition: Request rate >150% of average
- Response Time: Next business day
- Action: Document, plan capacity

**Feature Drift**
- Condition: >10% of features show statistical drift
- Response Time: Weekly review
- Action: Assess need for retraining

---

## 5. Dashboards

### Real-Time Dashboard

**Key Metrics Display**:
- Current API status (UP/DOWN)
- Requests in last hour
- Current error rate
- Average response time
- Active predictions

**Visualization**:
- Line chart: Requests over time
- Gauge: Error rate
- Bar chart: Prediction distribution
- Heatmap: Response times

### Performance Dashboard

**Model Metrics**:
- Accuracy trend (last 30 days)
- Precision/Recall curves
- Confusion matrix
- Feature importance

**System Metrics**:
- CPU/Memory usage over time
- Disk space trend
- API uptime percentage
- Error breakdown by type

### Business Dashboard

**Impact Metrics**:
- High-risk customers identified
- Retention campaign effectiveness
- Cost savings from predictions
- ROI calculation

**Trends**:
- Churn rate over time
- Customer segments at risk
- Prediction accuracy by segment
- Business value delivered

---

## 6. Failure Handling Procedures

### Automated Recovery

**API Restart**:
```bash
# Systemd service auto-restart
[Service]
Restart=always
RestartSec=10
```

**Log Rotation**:
```bash
# Logrotate configuration
/path/to/monitoring.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

**Disk Space Management**:
```bash
# Cron job to clean old files
0 2 * * * find /path/to/logs -mtime +30 -delete
```

### Manual Intervention

**Escalation Path**:
1. **Level 1**: Automated alerts → On-call engineer
2. **Level 2**: Persistent issues → Team lead
3. **Level 3**: System outage → Engineering manager

**Response Procedures**:
- Document incident in log
- Follow troubleshooting guide
- Implement fix
- Verify resolution
- Post-mortem analysis

---

## 7. Data Quality Monitoring

### Input Validation

**Check for**:
- Missing required features
- Out-of-range values
- Invalid data types
- Unexpected categories
- Null/NaN values

**Implementation**:
```python
def validate_input(data):
    """Validate customer data before prediction"""
    required_features = [...]
    numeric_ranges = {...}
    valid_categories = {...}
    
    # Validation logic
    # Return errors if any
```

### Output Validation

**Check for**:
- Prediction probabilities in [0, 1]
- Consistent prediction labels
- Reasonable confidence levels
- No null predictions

---

## 8. Monitoring Tools

### Recommended Stack

**Logging**: Python logging module (current)  
**Metrics**: Prometheus (future)  
**Visualization**: Grafana (future)  
**Alerting**: PagerDuty or Slack (future)  
**APM**: New Relic or DataDog (future)  

### Current Implementation

**Built-in Logging**:
- Python logging module
- File-based logs
- Manual log analysis

**Future Enhancements**:
- Centralized log aggregation (ELK stack)
- Real-time dashboards (Grafana)
- Automated alerting (PagerDuty)
- Distributed tracing (Jaeger)

---

## 9. Reporting

### Daily Report Template

```
DAILY CHURN PREDICTION REPORT
Date: YYYY-MM-DD

API PERFORMANCE
- Total Requests: X
- Error Rate: X%
- Avg Response Time: Xms
- Uptime: X%

PREDICTIONS
- Total Predictions: X
- Churn Predicted: X (X%)
- No Churn Predicted: X (X%)
- High Risk Customers: X

ISSUES
- Errors: X
- Warnings: X
- Critical Alerts: X

ACTION ITEMS
- [ ] Item 1
- [ ] Item 2
```

### Weekly Report Template

```
WEEKLY CHURN PREDICTION REPORT
Week: YYYY-WW

SUMMARY
- Total Predictions: X
- Model Accuracy: X%
- System Uptime: X%

TRENDS
- Prediction distribution trend
- Error rate trend
- Performance trend

MODEL HEALTH
- Feature drift: [Status]
- Concept drift: [Status]
- Retraining needed: [Yes/No]

RECOMMENDATIONS
- Action item 1
- Action item 2
```

---

## 10. Continuous Improvement

### Monitoring Evolution

**Phase 1 (Current)**: Basic logging and manual monitoring  
**Phase 2 (3 months)**: Automated alerting and dashboards  
**Phase 3 (6 months)**: Advanced analytics and ML monitoring  
**Phase 4 (12 months)**: Full observability stack  

### Feedback Loop

1. **Collect**: Gather metrics and logs
2. **Analyze**: Identify patterns and issues
3. **Act**: Implement improvements
4. **Measure**: Verify impact
5. **Iterate**: Continuous refinement

---

## Appendix: Monitoring Checklist

### Daily
- [ ] Check API status
- [ ] Review error logs
- [ ] Verify batch job completion
- [ ] Monitor disk space

### Weekly
- [ ] Analyze performance trends
- [ ] Review prediction accuracy
- [ ] Check for feature drift
- [ ] Update dashboards

### Monthly
- [ ] Generate comprehensive report
- [ ] Assess model performance
- [ ] Plan infrastructure changes
- [ ] Review and update alerts

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-15  
**Next Review**: 2024-02-15
