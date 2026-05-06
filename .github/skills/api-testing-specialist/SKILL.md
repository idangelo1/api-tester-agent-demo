---
name: api-testing-specialist
description: 'Structured API testing workflow. Use for API test strategy, contract validation, security review, k6 load testing, performance baselines, Postman tests, or Scala microservice API tests.'
argument-hint: 'Describe the API, contract, authentication, risks, and expected behavior.'
user-invocable: true
---

# API Testing Specialist

## When to Use

- Design API test plans before implementation or release.
- Review REST, GraphQL, and webhook contracts.
- Create or improve Postman test coverage.
- Validate authentication, authorization, and input handling.
- Define performance baselines and resilience checks with k6 when load testing is required.
- Generate ScalaTest + sttp coverage for Scala microservices.

## Workflow

### 1. Functional Testing

- Validate endpoints against specifications.
- Test request and response formats and data types.
- Verify business logic and validations.
- Test error handling and edge cases.
- Ensure proper status codes and headers.

### 2. Contract Testing

- Validate API contracts against OpenAPI or JSON Schema.
- Test backward compatibility for changes.
- Verify request and response validation.
- Ensure documentation matches runtime behavior.
- Catch breaking changes before deployment.

### 3. Security Testing

- Test authentication and authorization.
- Check for common vulnerabilities such as injection and IDOR.
- Validate input sanitization.
- Test rate limiting and abuse prevention.
- Verify sensitive data handling.

### 4. Performance Testing

- Measure response time baselines.
- Identify slow endpoints.
- Test under simulated load with k6 scripts and explicit scenarios.
- Find concurrency issues.
- Validate timeout handling.
- Define and validate thresholds (for example p95 latency and error rate).
- Export execution artifacts on every run: JSON summary (`--summary-export`) and HTML report (`K6_WEB_DASHBOARD=true` + `K6_WEB_DASHBOARD_EXPORT`).

### 5. Integration Testing

- Test API integration with clients.
- Validate end-to-end flows.
- Test handling of external dependencies.
- Verify data consistency across services.
- Check webhook and callback functionality.

## Decision Points

- Severity categorization: prioritize issues based on impact.
- Testing depth: balance exhaustive testing with practical constraints.
- Tool selection: choose tools based on API complexity and requirements.
- Scala microservices: use ScalaTest + sttp + play-json and run `sbt test` when execution is required.

## Quality Criteria

- All relevant endpoints validated against specifications.
- No critical security vulnerabilities left unreported.
- Performance metrics compared against explicit baselines.
- Integration flows checked for expected behavior and failure handling.
- k6 executions generate traceable artifacts per run (timestamped JSON summary and HTML report).

## Example Prompts

- Design a test strategy for this new REST API.
- Create Postman tests for these authentication endpoints.
- Are there security vulnerabilities in this API design?
- Test this API for backward compatibility with v1.
- Help me set up automated API tests in our CI pipeline.
- Generate a k6 script for this endpoint with ramp-up, duration, and thresholds.
- Review and improve this k6 script for production-like load.
- Generate ScalaTest + sttp tests for this microservice API.