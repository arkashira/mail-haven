# 📨 mail-haven – STORIES.md  

## Table of Contents
1. [Epics Overview](#epics-overview)  
2. [MVP Backlog (Ordered)](#mvp-backlog-ordered)  
3. [Future Enhancements](#future-enhancements)  

---  

## Epics Overview  

| Epic ID | Title | Description | Target Release |
|---------|-------|-------------|----------------|
| **E1** | **Secure Foundations** | Core security primitives – user authentication, end‑to‑end encryption, and secure transport. | MVP |
| **E2** | **Core Mail Flow** | Sending, receiving, and storing encrypted messages with basic UI. | MVP |
| **E3** | **Domain & Identity** | Custom domain onboarding and DKIM/SPF/DMARC configuration. | MVP + |
| **E4** | **User Experience** | Dashboard, inbox/outbox views, and responsive UI. | MVP |
| **E5** | **Contact & Calendar** | Manage contacts and integrate with external calendar services. | Post‑MVP |
| **E6** | **File Sharing** | Secure attachment handling with granular access controls. | Post‑MVP |
| **E7** | **Compliance & Auditing** | Logging, export, and GDPR/CCPA compliance features. | Post‑MVP |
| **E8** | **Scalability & Ops** | Multi‑tenant deployment, health checks, and CI/CD pipelines. | Ongoing |

---  

## MVP Backlog (Ordered)

> **Priority**: Stories are ordered from highest to lowest importance for the Minimum Viable Product (MVP). All acceptance criteria must be met before a story is considered **Done**.

### Epic **E1 – Secure Foundations**

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| **E1‑01** | **As a new user, I want to register with my email address and a strong password, so that I can create a secure account.** | - Registration form validates email format and password strength (≥12 chars, mix of upper/lower, numbers, symbols). <br> - Password is hashed with Argon2 before storage. <br> - A verification email containing a time‑limited token is sent. <br> - Account remains inactive until verification link is clicked. |
| **E1‑02** | **As a registered user, I want to log in using OAuth 2.0 (Google/Microsoft), so that I can avoid managing another password.** | - OAuth flow follows RFC 6749. <br> - On first login, a user profile is created and linked to the provider’s sub ID. <br> - JWT access token (signed with RS256) is issued with 15 min expiry and refresh token stored httpOnly. |
| **E1‑03** | **As a logged‑in user, I want all API traffic to be encrypted with TLS 1.3, so that my data is protected in transit.** | - Server enforces HTTPS on all endpoints. <br> - Invalid or weak cipher suites are rejected (tested via SSL Labs “A” rating). |
| **E1‑04** | **As a user, I want my emails to be end‑to‑end encrypted, so that only the intended recipient can read them.** | - Client generates a fresh X25519 key pair per user. <br> - Public keys are exchanged via a signed key‑directory endpoint. <br> - Message payload is encrypted with NaCl `crypto_box` (or libsodium) before being persisted. <br> - Decryption succeeds only with the recipient’s private key. |
| **E1‑05** | **As a security auditor, I need audit logs for authentication events, so that I can detect suspicious activity.** | - Every login, logout, failed login, and password reset writes an immutable log entry to MongoDB `audit_events` collection. <br> - Logs include timestamp, user‑id, IP, user‑agent, and event type. <br> - Logs are write‑once (no updates or deletes). |

### Epic **E2 – Core Mail Flow**

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| **E2‑01** | **As a user, I want to compose a new email, add recipients, and send it, so that I can communicate securely.** | - Composer UI includes To, Cc, Bcc, Subject, Body (rich‑text). <br> - Recipients are validated against existing user accounts or external public keys. <br> - On send, the client encrypts the body and attachments with the recipients’ public keys and stores the ciphertext via `/api/messages`. <br> - Sender receives a “sent” confirmation within 2 s. |
| **E2‑02** | **As a recipient, I want to see incoming encrypted emails in my inbox, so that I can read them.** | - Inbox view lists messages with sender, subject, and received timestamp. <br> - Clicking a message triggers client‑side decryption; if decryption fails, an error “Unable to decrypt – missing key” is shown. |
| **E2‑03** | **As a user, I want deleted emails to be moved to a Trash folder for 30 days, so that I can recover accidental deletions.** | - Delete action moves message metadata to `trash` collection. <br> - Trash UI shows messages with original timestamps. <br> - Automatic purge job runs nightly, permanently removing items older than 30 days. |
| **E2‑04** | **As a user, I want to search my mailbox by sender or subject, so that I can locate messages quickly.** | - Search endpoint supports case‑insensitive partial matches on `sender` and `subject`. <br> - Results are returned within 500 ms for a mailbox of up to 10 k messages. |
| **E2‑05** | **As a system, I need rate‑limiting on send/receive APIs, so that abuse is prevented.** | - 100 requests/min per user IP; exceeding returns HTTP 429 with retry‑after header. <br> - Rate limits are configurable via environment variables. |

### Epic **E3 – Domain & Identity**

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| **E3‑01** | **As an organization admin, I want to add a custom domain (e.g., mail.mycompany.com), so that my team can use branded email addresses.** | - Admin can enter a domain name and upload DKIM private key. <br> - System validates DNS TXT records for DKIM, SPF, and DMARC. <br> - Upon successful verification, the domain is listed as “Active”. |
| **E3‑02** | **As a user with a custom domain address, I want to receive emails sent to that address, so that I can use my corporate identity.** | - MX records pointing to `mail-haven.axentx.com` route inbound mail to the platform. <br> - Incoming mail is processed, encrypted with the recipient’s public key, and appears in the user’s inbox. |
| **E3‑03** | **As an admin, I want to enforce password policies for all users on my domain, so that security standards are met.** | - Admin can toggle “Strong Password Required”. <br> - When enabled, registration and password‑change flows enforce the policy defined in **E1‑01**. |

### Epic **E4 – User Experience**

| # | User Story | Acceptance Criteria |
|---|------------|---------------------|
| **E4‑01** | **As a user, I want a responsive dashboard that works on desktop and mobile, so that I can manage mail anywhere.** | - UI built with React + Tailwind, passes Lighthouse ≥90 on mobile & desktop. <br> - Navigation drawer collapses on < 768 px width. |
| **E4‑02** | **As a user, I want real‑time notification of new mail, so that I never miss important messages.** | - WebSocket (or Server‑Sent Events) pushes a “new‑mail” event. <br> - Browser shows a toast and updates the inbox badge instantly. |
| **E4‑03** | **As a user, I want to toggle a “dark mode”, so that I can reduce eye strain.** | - Theme preference stored in user profile; UI switches without page reload. |
| **E4‑04** | **As a user, I want to set a signature that is automatically appended to outgoing messages, so that I can include my contact info.** | - Signature editor supports plain‑text and limited HTML. <br> - Signature is stored encrypted and appended client‑side before encryption of the message body. |

---  

## Future Enhancements (Post‑MVP)

| Epic | Story ID | Title |
|------|----------|-------|
| **E5** | **E5‑01** | Contact import from Google Contacts / CSV |
| **E5** | **E5‑02** | Two‑way calendar sync with Google Calendar & Outlook |
| **E6** | **E6‑01** | Secure file upload with per‑file encryption keys |
| **E6** | **E6‑02** | Shareable, expiring download links with revocation |
| **E7** | **E7‑01** | GDPR data‑export tool (JSON/EML) |
| **E7** | **E7‑02** | Automated retention policies per organization |
| **E8** | **E8‑01** | Kubernetes Helm chart for multi‑region deployment |
| **E8** | **E8‑02** | Blue‑green CI/CD pipeline with automated rollback |

---  

*Prepared by the product/engineering lead, mail‑haven repository (axentx/mail-haven). All stories are scoped to be implementable with the proposed tech stack (React, Node/Express, MongoDB, OAuth 2.0) and aligned with the company’s security‑first mandate.*
