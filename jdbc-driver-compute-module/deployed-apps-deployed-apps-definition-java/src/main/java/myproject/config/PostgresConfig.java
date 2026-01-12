package myproject.config;

/**
 * Configuration for PostgreSQL database connection.
 */
public class PostgresConfig {
    private String host;
    private int port = 5432;  // Default PostgreSQL port
    private String database;
    private String username;
    private String password;
    private String sslMode = "verify-full";  // Secure default: verify-full

    public PostgresConfig() {
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public String getDatabase() {
        return database;
    }

    public void setDatabase(String database) {
        this.database = database;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getSslMode() {
        return sslMode;
    }

    public void setSslMode(String sslMode) {
        this.sslMode = sslMode;
    }

    /**
     * Builds JDBC connection URL for PostgreSQL.
     * Format: jdbc:postgresql://hostname:port/database?sslmode=verify-full
     */
    public String buildJdbcUrl() {
        StringBuilder url = new StringBuilder();
        url.append("jdbc:postgresql://")
                .append(host)
                .append(":")
                .append(port)
                .append("/");

        if (database != null && !database.isEmpty()) {
            url.append(database);
        }

        // Add sslmode parameter (controls both SSL usage and verification level)
        if (sslMode != null && !sslMode.equals("disable")) {
            url.append("?sslmode=").append(sslMode);
        }

        return url.toString();
    }
}
