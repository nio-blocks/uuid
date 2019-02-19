UUID
=======
Generate Universally Unique ID codes according to RFC 4122.

Properties
----------
- **UUID Version**: (advanced) Select version of UUID to generate (use version `one` or `four` for random IDs).
- **Name Options: (advanced)
  - **Name**: (advanced) Only used in versions 3 and 5.
  - **Namespace**: (advanced) Only used in versions 3 and 5.
  - **Custom Namespace**: (advanced) If not `None` this UUID will be used instead of the **Namespace** selection. The value must be a UUID object, or a byte sequence or hex string representing a UUID. Strings are case insensitive and optionally can include a `URN` prefix, curly braces, and/or hyphens.
- **Binary Ouptut** (advanced): Output byte sequence instead of canonical hex string.
- **Output Attribute** (advanced): Signal attribute to contain the new UUID, default `uuid`

Commands
--------
None
