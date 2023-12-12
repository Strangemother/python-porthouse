# Secure WebSocket Connection Strategy

## Overview

This document outlines the recommended practices for establishing secure WebSocket connections for both browser-based clients and non-browser clients, such as IoT devices. Ensuring the security of our WebSocket connections is critical to protect sensitive data and maintain the integrity of our communication channels.

## Security Practices

### Browser-Based Clients

For clients operating within a browser environment, security is centered around standard web security protocols:

- **HTTPS**: All communications must be over HTTPS to prevent man-in-the-middle (MITM) attacks.
- **CSRF Tokens**: Cross-Site Request Forgery (CSRF) tokens must be used in all forms to protect against CSRF attacks.
- **Cookies**: Authentication tokens are stored in secure, HttpOnly cookies. These cookies are automatically included in the WebSocket handshake by the browser and are not accessible via JavaScript.

### IoT and Non-Browser Clients

For non-browser clients, such as IoT devices:

- **Client ID**: The Client ID should be passed in the header of the WebSocket handshake request to identify the device.
- **Auth Tokens**: Authentication tokens should also be passed in the header (not the URL) to prevent exposure.
- **Secure Channels**: Use `wss://` for all WebSocket communications to ensure encryption.

## Expected Connection Flow

### Browser-Based Clients

```plaintext
  Browser Client                 Web Server
       |                              |
       |----[HTTPS] Request Auth----->|
       |<---[Set-Cookie] Auth Token---|
       |                              |
       |----[wss:// + Cookie] WebSocket Connection Request----->|
       |<----- Validate CSRF Token, Cookie, Upgrade Connection--|
       |                              |
       |------- Secure WebSocket Communication ---------------->|
       |<-------------------------------------------------------|
```

```plaintext
 IoT Device                      Auth Server                    Web Server
      |                              |                              |
      |---[HTTPS] Request Auth------>|                              |
      |<-----[HTTPS] Auth Token------|                              |
      |                              |                              |
      |-----[wss:// + Headers] WebSocket Connection Request-------->|
      |<------ Validate Headers, Upgrade Connection-----------------|
      |                              |                              |
      |-------- Secure WebSocket Communication -------------------->|
      |<------------------------------------------------------------|
```


Implementation Notes

- Token Generation: Tokens must be generated securely and should have an expiration time. JSON Web Tokens (JWTs) are recommended for their self-contained nature.
- Token Validation: Upon each WebSocket connection request, the server must validate the provided token before allowing the communication to proceed.
- Refresh Tokens: For non-browser clients, implement a secure HTTPS token refresh mechanism.
- Origin Checks: For browser clients, validate the Origin header during the WebSocket handshake to prevent unauthorized WebSocket connections.
- Documentation: All developers should document their code changes related to WebSocket connection handling.


### Conclusion
Adhering to these security practices will help safeguard our WebSocket connections against common vulnerabilities. It is the responsibility of each developer to understand and implement these measures in their respective areas of work.