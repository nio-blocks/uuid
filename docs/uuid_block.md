UUID
=======
Generate Universally Unique ID codes according to RFC 4122.

Properties
----------
- **UUID Version**: (advanced) Select version of UUID to generate (use `v1` or `v4` for random IDs).
- **Name Options**: (advanced)
  - **Name**: Only used in versions 3 and 5.
  - **Namespace**: Only used in versions 3 and 5, if `custom` the value of **Custom Namespace** will be used.
  - **Custom Namespace**: A UUID object, or a byte sequence or hex string representing a UUID. Strings are case insensitive and optionally can include a `urn` prefix, curly braces, and/or hyphens. This value is ignored unless **Namespace** is `custom`.
- **Binary Ouptut** (advanced): Output byte sequence instead of canonical hex string.
- **Output Attribute** (advanced): Signal attribute to contain the new UUID, default `uuid`

Commands
--------
None
