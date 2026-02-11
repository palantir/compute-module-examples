package myproject.service;

import myproject.connection.ConnectionManager;
import myproject.model.QueryRequest;
import myproject.model.QueryResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Service to execute SQL queries against SAP HANA.
 */
public class SqlService {
    private static final Logger log = LoggerFactory.getLogger(SqlService.class);
    private final ConnectionManager connectionManager;

    public SqlService(ConnectionManager connectionManager) {
        this.connectionManager = connectionManager;
    }

    /**
     * Executes a SQL query and returns the result.
     */
    public QueryResult executeQuery(QueryRequest request) {
        log.info("Executing query");

        try (Connection connection = connectionManager.getConnection();
             PreparedStatement stmt = connection.prepareStatement(request.query());
             ResultSet rs = stmt.executeQuery()) {

            List<Map<String, String>> rows = resultSetToList(rs);
            log.info("Query returned {} rows", rows.size());
            return new QueryResult("success", rows, null);

        } catch (SQLException e) {
            log.error("Query failed: {}", e.getMessage());
            return new QueryResult("error", null, e.getMessage());
        }
    }

    private List<Map<String, String>> resultSetToList(ResultSet rs) throws SQLException {
        List<Map<String, String>> rows = new ArrayList<>();
        ResultSetMetaData metadata = rs.getMetaData();
        int columnCount = metadata.getColumnCount();

        while (rs.next()) {
            Map<String, String> row = new LinkedHashMap<>();  // Preserve column order
            for (int i = 1; i <= columnCount; i++) {
                String columnName = metadata.getColumnName(i);
                Object value = rs.getObject(i);
                row.put(columnName, value == null ? null : value.toString());
            }
            rows.add(row);
        }

        return rows;
    }
}
