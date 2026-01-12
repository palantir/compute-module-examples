package myproject;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.palantir.interactive.module.tasks.deployedapps.DeployedAppRuntime;
import myproject.config.PostgresConfig;
import myproject.connection.ConnectionManager;
import myproject.model.QueryRequest;
import myproject.model.QueryResult;
import myproject.service.SqlService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.File;
import java.util.Map;

/**
 * PostgreSQL Compute Module - executes SQL queries against a PostgreSQL database.
 *
 * Required environment variables:
 *   POSTGRES_HOST      - PostgreSQL hostname
 *   POSTGRES_DATABASE  - Database name
 *   POSTGRES_USERNAME  - Username
 *
 * Required files:
 *   SOURCE_CREDENTIALS - Path to JSON file containing password
 *
 * Optional environment variables:
 *   POSTGRES_PORT      - Port (default: 5432)
 *   POSTGRES_SSL_MODE  - SSL mode: disable, allow, prefer, require, verify-ca, verify-full (default: verify-full)
 *   SOURCE_API_NAME    - Key in credentials file (default: "postgres")
 *   PASSWORD_SECRET_NAME - Secret name in credentials (default: "password")
 */
final class DeployedApp {
    private static final Logger log = LoggerFactory.getLogger(DeployedApp.class);
    private static SqlService sqlService;

    public static void main(String[] _args) {
        log.info("Starting PostgreSQL Compute Module");

        PostgresConfig config = loadConfiguration();
        log.info("Configured connection to {}:{}/{}",
                config.getHost(), config.getPort(),
                config.getDatabase() != null ? config.getDatabase() : "(default)");

        ConnectionManager connectionManager = new ConnectionManager(config);
        sqlService = new SqlService(connectionManager);

        DeployedAppRuntime.builder()
                .addQueryRunner(DeployedApp::executeQuery, QueryRequest.class, QueryResult.class, "executeQuery")
                .buildAndStart();
    }

    /**
     * Executes a SQL query against PostgreSQL.
     */
    static QueryResult executeQuery(QueryRequest request) {
        return sqlService.executeQuery(request);
    }

    private static PostgresConfig loadConfiguration() {
        PostgresConfig config = new PostgresConfig();

        config.setHost(requireEnv("POSTGRES_HOST"));
        config.setDatabase(requireEnv("POSTGRES_DATABASE"));
        config.setUsername(requireEnv("POSTGRES_USERNAME"));
        config.setPassword(loadPasswordFromCredentials());

        String port = System.getenv("POSTGRES_PORT");
        if (port != null) {
            config.setPort(Integer.parseInt(port));
        }

        String sslMode = System.getenv("POSTGRES_SSL_MODE");
        if (sslMode != null) {
            config.setSslMode(sslMode);
        }

        return config;
    }

    /**
     * Loads the password from the SOURCE_CREDENTIALS file.
     * The file format is: {"<sourceApiName>": {"<secretName>": "value"}}
     */
    private static String loadPasswordFromCredentials() {
        String credentialsPath = System.getenv("SOURCE_CREDENTIALS");
        if (credentialsPath == null || credentialsPath.isEmpty()) {
            throw new IllegalStateException("SOURCE_CREDENTIALS environment variable not set");
        }

        String sourceApiName = System.getenv("SOURCE_API_NAME");
        if (sourceApiName == null) {
            sourceApiName = "postgres";
        }

        String secretName = System.getenv("PASSWORD_SECRET_NAME");
        if (secretName == null) {
            secretName = "password";
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            @SuppressWarnings("unchecked")
            Map<String, Map<String, String>> credentials = mapper.readValue(
                    new File(credentialsPath), Map.class);

            if (!credentials.containsKey(sourceApiName)) {
                throw new IllegalStateException("Source '" + sourceApiName + "' not found in credentials file");
            }

            Map<String, String> sourceSecrets = credentials.get(sourceApiName);
            if (!sourceSecrets.containsKey(secretName)) {
                throw new IllegalStateException("Secret '" + secretName + "' not found for source '" + sourceApiName + "'");
            }

            log.info("Loaded password from SOURCE_CREDENTIALS");
            return sourceSecrets.get(secretName);
        } catch (Exception e) {
            throw new IllegalStateException("Failed to read password from SOURCE_CREDENTIALS: " + e.getMessage(), e);
        }
    }

    private static String requireEnv(String name) {
        String value = System.getenv(name);
        if (value == null || value.isEmpty()) {
            throw new IllegalStateException("Required environment variable not set: " + name);
        }
        return value;
    }

    private DeployedApp() {}
}
