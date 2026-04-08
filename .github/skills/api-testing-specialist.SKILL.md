---
name: API Testing Specialist
category: testing
---

# API Testing Specialist Skill

## Purpose

This skill provides a structured approach to API testing, ensuring APIs are functional, reliable, secure, and performant. It emphasizes thoroughness while balancing practical testing efficiency.

## Workflow

### 1. Functional Testing

- Validate endpoints against specifications.
- Test request/response formats and data types.
- Verify business logic and validations.
- Test error handling and edge cases.
- Ensure proper status codes and headers.

### 2. Contract Testing

- Validate API contracts (OpenAPI, JSON Schema).
- Test backward compatibility for changes.
- Verify request/response validation.
- Ensure documentation matches reality.
- Catch breaking changes before deployment.

### 3. Security Testing

- Test authentication and authorization.
- Check for common vulnerabilities (e.g., injection, IDOR).
- Validate input sanitization.
- Test rate limiting and abuse prevention.
- Verify sensitive data handling.

### 4. Performance Testing

- Measure response time baselines.
- Identify slow endpoints.
- Test under simulated load.
- Find concurrency issues.
- Validate timeout handling.

### 5. Integration Testing

- Test API integration with clients.
- Validate end-to-end flows.
- Test external dependencies handling.
- Verify data consistency across services.
- Check webhook and callback functionality.

## Decision Points

- **Severity Categorization:** Prioritize issues based on impact.
- **Testing Depth:** Balance between exhaustive testing and practical constraints.
- **Tool Selection:** Choose tools based on the API's complexity and requirements.
  - **Scala microservices:** Use ScalaTest + sttp (sync) + play-json. Run with `sbt test`.

## Quality Criteria

- All endpoints validated against specifications.
- No critical security vulnerabilities.
- Performance metrics meet defined baselines.
- Integration flows function as expected.

## Example Prompts

- "Design a test strategy for this new REST API."
- "Create Postman tests for these authentication endpoints."
- "Are there security vulnerabilities in this API design?"
- "Test this API for backward compatibility with v1."
- "Help me set up automated API tests in our CI pipeline."
- "Generate ScalaTest + sttp tests for this microservice API."

## Related Skills

- **Backend Architect** — For API design review.
- **Performance Benchmarker** — For load testing.
- **DevOps Automator** — For CI integration.
- **Infrastructure Maintainer** — For health checks.
