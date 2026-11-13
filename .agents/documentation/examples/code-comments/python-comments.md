# Python Comment Examples

Use docstrings for modules, public classes, public functions, and public
methods. Use `#` comments for local implementation notes that are not API
contracts.

## Package Level

```python
"""Customer export package.

The package builds warehouse-ready export files from tenant-scoped customer
records. Authorization and tenant filtering must happen before callers pass
records into this package.
"""
```

## Module Level

```python
"""Builds customer export files for downstream warehouse ingestion.

The module owns CSV shape and field ordering. Callers provide already-filtered
records; authorization and tenant scoping must happen before data reaches this
boundary.
"""
```

## Class Level

```python
class ExportWriter:
    """Streams one customer export to a file-like object.

    The writer does not close the stream it receives. Callers own stream
    lifetime so the same object can be used with local files, cloud upload
    buffers, and test doubles.
    """
```

## Function Level: Google Style

```python
def write_rows(rows: Iterable[CustomerRow], stream: TextIO) -> int:
    """Write rows to ``stream``.

    Args:
        rows: Customer rows already sorted by stable customer ID.
        stream: Text stream opened by the caller.

    Returns:
        Number of records emitted, excluding the header row.

    Raises:
        ValueError: If a row contains a field that cannot be represented in the
            configured CSV dialect.
    """
```

## Function Level: Sphinx Style

```python
def write_rows(rows: Iterable[CustomerRow], stream: TextIO) -> int:
    """Write rows to ``stream``.

    :param rows: Customer rows already sorted by stable customer ID.
    :type rows: Iterable[CustomerRow]
    :param stream: Text stream opened by the caller.
    :type stream: TextIO
    :return: Number of records emitted, excluding the header row.
    :rtype: int
    :raises ValueError: If a row contains a field that cannot be represented in
        the configured CSV dialect.
    """
```

## Method Level

```python
class ExportWriter:
    def flush(self) -> None:
        """Flush buffered rows without closing the underlying stream.

        Use this before handing the stream to an upload client that reads from
        the current file position.
        """
```

## Implementation Note

```python
# Keep the header order stable. The warehouse maps columns by position during
# backfill imports, even though normal daily imports use the names.
writer.writerow(EXPORT_COLUMNS)
```

## Freshness Check

```python
# Bad: stale after uploads became caller-owned.
stream.close()  # Close the export stream.

# Better: no comment here. Ownership is documented on ExportWriter.
```
