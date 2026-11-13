# Publication safety gate

1. Public output may include OS name, package names and versions, installed command names, public Skill URI metadata, general capability counts and non-sensitive test outcomes.
2. Do not upload secrets, environment variable values, tokens, authentication cookies, SSH keys, credentials, private filenames, private repository lists, account financial information, browser profiles, contact or email bodies.
3. Do not mirror original platform-provided Skills into a public repository without an appropriate license or explicit redistribution permission; publish metadata and original adaptations instead.
4. Review absolute paths for usernames, home directories, mounts and runtime-internal details; redact or generalize before publishing.
5. Run `git diff --cached` / secret scanning locally before publishing. Files in private ZIPs remain subject to local privacy review.
6. Never claim external connectors have been audited without actual permission-specific test evidence.
