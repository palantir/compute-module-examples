package myproject.model;

import java.util.List;
import java.util.Map;

/**
 * Result object for SQL query execution.
 */
public record QueryResult(
    String status,
    List<Map<String, String>> rows,
    String error
) {}
