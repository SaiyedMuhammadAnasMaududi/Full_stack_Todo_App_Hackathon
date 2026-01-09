# ADR 001: Backend Architecture for Secure Multi-User Todo API

## Status
Accepted

## Date
2026-01-08

## Context
We need to implement a secure, multi-user todo application backend that enforces strict user isolation for all operations. The system must use JWT-based authentication and Neon Serverless PostgreSQL for data persistence while maintaining high security standards and performance.

## Decision

We have made the following architectural decisions:

### 1. JWT Verification Strategy
- Use server-side JWT verification in FastAPI using python-jose library
- Extract and validate tokens from Authorization headers using HTTPBearer scheme
- Verify tokens using shared secret (BETTER_AUTH_SECRET) from environment variables
- Extract user identity (user_id, email) from JWT claims
- Implement FastAPI dependency injection for consistent authentication across endpoints

**Rationale**: This approach prevents spoofing and privilege escalation by validating tokens on every request rather than trusting frontend-provided user data.

### 2. SQLModel Relationship Architecture
- Implement User and Task models with proper foreign key relationships
- Use UUID primary keys for both User and Task entities
- Create bidirectional relationships using SQLModel's Relationship attributes
- Enforce ownership through database-level foreign key constraints and application-level filtering
- Index user_id field for optimized querying

**Rationale**: Proper ORM relationships ensure data integrity and enforce user isolation at both database and application levels.

### 3. Neon PostgreSQL Connection Management
- Use environment variable (DATABASE_URL) for connection string configuration
- Configure connection pooling with pool_pre_ping enabled for Neon's serverless nature
- Set appropriate pool sizes and recycle intervals to handle connection drops
- Implement proper session management with FastAPI dependency injection

**Rationale**: Neon's serverless architecture requires specific connection handling to maintain performance and reliability.

### 4. Multi-User Data Isolation Strategy
- Validate that user_id in URL path matches the user_id in JWT token
- Filter all database queries by user_id to enforce ownership
- Return appropriate HTTP status codes (401, 403) for unauthorized access
- Implement ownership validation in each endpoint before performing operations

**Rationale**: Strict enforcement of user isolation is critical for security and privacy compliance.

### 5. FastAPI Dependency Injection Pattern
- Create JWT verification dependency using FastAPI's Depends()
- Centralize authentication logic to reduce code duplication
- Pass authenticated user object to endpoints automatically
- Implement automatic error handling for invalid tokens

**Rationale**: Centralized authentication logic ensures consistent security enforcement across all endpoints.

## Consequences

### Positive
- Strong security posture with server-side token validation
- Data integrity through proper foreign key constraints
- Good performance with optimized connection pooling for Neon
- Consistent authentication implementation across all endpoints
- Clear separation of concerns between authentication and business logic

### Negative
- Slight increase in complexity compared to client-trusted approaches
- Need for proper secret management for JWT verification
- Additional network calls to verify tokens on each request
- Requirement for proper connection handling with Neon's serverless model

## Alternatives Considered

### JWT Verification
- Trusting frontend user_id: Rejected due to security concerns
- Session-based authentication: Rejected as it contradicts stateless backend requirement

### Data Modeling
- Direct SQL queries: Rejected due to increased risk of injection attacks
- No foreign key constraints: Rejected as it would allow data corruption

### Connection Management
- Standard PostgreSQL configuration: Rejected as it would cause connection issues with Neon's serverless model
- No connection pooling: Rejected due to performance concerns