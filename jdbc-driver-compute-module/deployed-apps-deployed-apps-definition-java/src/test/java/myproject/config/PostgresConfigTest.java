package myproject.config;

import static org.assertj.core.api.Assertions.assertThat;
import org.junit.jupiter.api.Test;

public final class PostgresConfigTest {

    @Test
    public void testDefaultValues() {
        PostgresConfig config = new PostgresConfig();

        assertThat(config.getPort()).isEqualTo(5432);
        assertThat(config.getSslMode()).isEqualTo("verify-full");
    }

    @Test
    public void testBuildJdbcUrlBasic() {
        PostgresConfig config = new PostgresConfig();
        config.setHost("postgres.example.com");
        config.setPort(5432);
        config.setDatabase("mydb");

        String url = config.buildJdbcUrl();

        assertThat(url).isEqualTo("jdbc:postgresql://postgres.example.com:5432/mydb?sslmode=verify-full");
    }

    @Test
    public void testBuildJdbcUrlWithoutDatabase() {
        PostgresConfig config = new PostgresConfig();
        config.setHost("postgres.example.com");
        config.setPort(5432);

        String url = config.buildJdbcUrl();

        assertThat(url).isEqualTo("jdbc:postgresql://postgres.example.com:5432/?sslmode=verify-full");
    }

    @Test
    public void testBuildJdbcUrlWithDifferentSslMode() {
        PostgresConfig config = new PostgresConfig();
        config.setHost("postgres.example.com");
        config.setPort(5432);
        config.setDatabase("mydb");
        config.setSslMode("require");

        String url = config.buildJdbcUrl();

        assertThat(url).isEqualTo("jdbc:postgresql://postgres.example.com:5432/mydb?sslmode=require");
    }

    @Test
    public void testBuildJdbcUrlWithSslDisabled() {
        PostgresConfig config = new PostgresConfig();
        config.setHost("postgres.example.com");
        config.setPort(5432);
        config.setDatabase("mydb");
        config.setSslMode("disable");

        String url = config.buildJdbcUrl();

        assertThat(url).isEqualTo("jdbc:postgresql://postgres.example.com:5432/mydb");
    }

    @Test
    public void testBuildJdbcUrlWithCustomPort() {
        PostgresConfig config = new PostgresConfig();
        config.setHost("postgres.example.com");
        config.setPort(15432);
        config.setDatabase("mydb");

        String url = config.buildJdbcUrl();

        assertThat(url).startsWith("jdbc:postgresql://postgres.example.com:15432/mydb");
    }

    @Test
    public void testSettersAndGetters() {
        PostgresConfig config = new PostgresConfig();

        config.setHost("test-host");
        config.setPort(12345);
        config.setDatabase("testdb");
        config.setUsername("user1");
        config.setPassword("secret");
        config.setSslMode("require");

        assertThat(config.getHost()).isEqualTo("test-host");
        assertThat(config.getPort()).isEqualTo(12345);
        assertThat(config.getDatabase()).isEqualTo("testdb");
        assertThat(config.getUsername()).isEqualTo("user1");
        assertThat(config.getPassword()).isEqualTo("secret");
        assertThat(config.getSslMode()).isEqualTo("require");
    }
}
