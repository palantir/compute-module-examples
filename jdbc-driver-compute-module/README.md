# PostgreSQL Query Compute Module

A Foundry Compute Module that executes SQL queries against PostgreSQL databases and returns results directly as JSON.

## Overview

This module demonstrates how to:

- Connect to PostgreSQL using the official JDBC driver
- Load database credentials from Foundry Data Connection Sources
- Execute arbitrary SQL queries via a Compute Module endpoint
- Return query results as JSON

## Architecture

```
┌──────────────────┐     ┌─────────────────┐
│  Compute Module  │     │   PostgreSQL    │
│                  │     │                 │
│  1. Load creds   │     │                 │
│  2. Execute SQL  │────►│                 │
│  3. Return JSON  │◄────│                 │
└──────────────────┘     └─────────────────┘
```

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `POSTGRES_HOST` | PostgreSQL hostname |
| `POSTGRES_DATABASE` | Database name |
| `POSTGRES_USERNAME` | Database username |
| `SOURCE_CREDENTIALS` | Path to JSON file containing password (auto-mounted from Data Connection Source) |

## Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_SSL_MODE` | `verify-full` | SSL mode: `disable`, `allow`, `prefer`, `require`, `verify-ca`, `verify-full` |
| `SOURCE_API_NAME` | `postgres` | Key in credentials file for this source |
| `PASSWORD_SECRET_NAME` | `password` | Secret name in credentials |

## Endpoint: `executeQuery`

Executes a SQL query and returns results as JSON.

**Input:**
```json
{
  "query": "SELECT * FROM users LIMIT 10"
}
```

**Output:**
```json
{
  "status": "success",
  "rows": [
    {"id": "1", "name": "Alice"},
    {"id": "2", "name": "Bob"}
  ],
  "error": null
}
```

## Project Structure

```
deployed-apps-deployed-apps-definition-java/
├── build.gradle
├── libs/
│   └── postgresql-42.7.4.jar       # JDBC driver (place your driver here)
└── src/main/java/myproject/
    ├── DeployedApp.java            # Main entry point
    ├── config/
    │   └── PostgresConfig.java     # Connection configuration
    ├── connection/
    │   └── ConnectionManager.java  # JDBC connection handling
    ├── model/
    │   ├── QueryRequest.java       # Input model
    │   └── QueryResult.java        # Output model
    └── service/
        └── SqlService.java         # SQL execution
```

## Using a Different JDBC Driver

This example uses a local JAR file in `libs/` rather than Maven dependencies. This approach works for any JDBC driver, including proprietary drivers not available on public Maven repositories.

To use a different database:

1. Download your JDBC driver JAR and place it in `libs/`
2. Update `build.gradle` to reference the new JAR filename
3. Update `PostgresConfig.java` with the appropriate JDBC URL format
4. Update `ConnectionManager.java` with the correct driver class name
5. Update environment variable names as needed

## Deployment

1. Tag and publish from Code Repository
2. Create Compute Module with "Include runtime" turned **OFF**
3. Configure environment variables (`POSTGRES_HOST`, `POSTGRES_DATABASE`, `POSTGRES_USERNAME`)
4. Import a Data Connection Source to auto-mount `SOURCE_CREDENTIALS`
5. Start the Compute Module
