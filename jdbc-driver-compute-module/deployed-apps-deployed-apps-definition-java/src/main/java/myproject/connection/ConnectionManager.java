package myproject.connection;

import myproject.config.PostgresConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Manages database connections to PostgreSQL using plain JDBC.
 * Creates a new connection for each request (suitable for compute modules
 * that process queries serially).
 */
public class ConnectionManager {
    private static final Logger log = LoggerFactory.getLogger(ConnectionManager.class);
    private final PostgresConfig config;

    public ConnectionManager(PostgresConfig config) {
        this.config = config;
        // Load the PostgreSQL JDBC driver
        try {
            Class.forName("org.postgresql.Driver");
            log.info("Loaded PostgreSQL JDBC driver");
        } catch (ClassNotFoundException e) {
            throw new IllegalStateException("PostgreSQL JDBC driver not found", e);
        }
    }

    /**
     * Creates a new connection to PostgreSQL.
     * The caller is responsible for closing the connection.
     */
    public Connection getConnection() throws SQLException {
        log.debug("Creating new PostgreSQL connection to {}", config.getHost());
        return DriverManager.getConnection(
                config.buildJdbcUrl(),
                config.getUsername(),
                config.getPassword()
        );
    }

    public void close() {
        // No resources to clean up with plain JDBC
        log.info("ConnectionManager closed");
    }
}
