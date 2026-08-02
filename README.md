<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# rvnd-plugins

The RVND plugin marketplace. Distribution metadata only: each plugin's
content lives in its home repository and is referenced here as an
installable source. The rvnd-governance plugin lives in the rvnd
repository at plugin/rvnd-governance beside the server surface it
versions with.

The canonical Claude marketplace now lives in RVND itself, beside the plugin:

```text
/plugin marketplace add flxk1/RVND
/plugin install rvnd-governance@rvnd
```

This catalog remains a compatibility entry point. It resolves the same
repository-root plugin manifest and never carries a second copy of the skills.
Access follows the RVND source repository's visibility.

## License

GNU Affero General Public License v3.0 only. See
`LICENSES/AGPL-3.0-only.txt` and `NOTICE`.
