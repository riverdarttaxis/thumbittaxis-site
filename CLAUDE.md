# CLAUDE.md

## House rules (ThumbiT, owner: Shabba)

These apply to every session in this folder. They protect a live taxi business with real bookings, drivers and money.

### How to talk to the owner
- He is not a developer. Explain in plain, short, numbered steps. One step at a time when he has to do something.
- Say what a change does for drivers, passengers or the office, not how the code works, unless he asks.

### Never
- Never lose a booking. Database changes only ever add (new tables, new columns, new functions). Never drop, rename or empty a table or column.
- Never rename or remove anything the published apps rely on (API actions, columns, routes, screens). Add alongside instead.
- Never read, print, edit or commit `.env` files, keys, passwords or tokens, and never ask for them in chat. He types secrets himself.
- Never delete user accounts.
- Never mention "thumbit test" anywhere. Any test booking is labelled "test".
- Never run Prettier on existing files (only on brand-new files).
- Never give legal advice: legal questions go to the solicitor.

### Always ask him first, and wait for a clear yes, before
- `git push`, merging into `main`, or opening a pull request
- `eas update`, `eas build` or `eas submit` (sends to real phones / app stores)
- any Supabase deploy, migration or command that touches the live database
- sending any real SMS, email, WhatsApp or push message
- deleting any file or folder

### How a change is made
1. Work on a new branch, never straight on `main`.
2. Make the smallest change that does the job, following the existing structure (no mish-mash).
3. Run this folder's checks (below) and fix anything that fails.
4. Test on staging when staging exists; give him a short checklist to try.
5. Only then, with his yes, it goes live.

### Costs
- Prefer email or app push over SMS: texts cost the firm money.

### This folder's checks
- Open the changed pages in a browser and check they look right on a phone-sized screen.

### Going live
- This is the public site on GitHub Pages: pushing to `main` publishes it. Ask first.
