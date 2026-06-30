# Email Signature — React Model

Composant React pour la signature email "marin", utilisé dans les campagnes Resend et loop.so.

## Palette

- Accent light: `#49C5B6`
- Accent dark: `#015048`
- Background: `#FAFAFA`
- Text: `#000000`
- Police: Inter, system-ui, sans-serif

## Composant

```tsx
import React from "react";

const STYLES = {
  container: {
    fontFamily: "'Inter', system-ui, sans-serif",
    color: "#000000",
    fontSize: "14px",
    lineHeight: "1.5",
    paddingTop: "16px",
    borderTop: "1px solid #e0e0e0",
    marginTop: "16px",
  },
  name: {
    fontSize: "16px",
    fontWeight: "700",
    color: "#015048",
    margin: "0 0 2px 0",
  },
  title: {
    fontSize: "13px",
    color: "#49C5B6",
    margin: "0 0 8px 0",
    fontWeight: "500",
  },
  link: {
    color: "#015048",
    textDecoration: "none",
    fontSize: "13px",
  },
  separator: {
    color: "#c0c0c0",
    margin: "0 8px",
    fontSize: "12px",
  },
};

export function EmailSignature() {
  return (
    <div style={STYLES.container}>
      <p style={STYLES.name}>Evan Nanguy</p>
      <p style={STYLES.title}>Marin Agency</p>
      <div>
        <span style={STYLES.link}>evan@marinlite.agency</span>
        <span style={STYLES.separator}>|</span>
        <span style={STYLES.link}>marinlite.agency</span>
      </div>
    </div>
  );
}
```

## HTML Output

```html
<table cellpadding="0" cellspacing="0" style="font-family:'Inter',system-ui,sans-serif;color:#000000;font-size:14px;line-height:1.5;padding-top:16px;border-top:1px solid #e0e0e0;margin-top:16px;">
  <tr>
    <td>
      <p style="font-size:16px;font-weight:700;color:#015048;margin:0 0 2px 0;">Evan Nanguy</p>
      <p style="font-size:13px;color:#49C5B6;margin:0 0 8px 0;font-weight:500;">Marin Agency</p>
      <p style="margin:0;">
        <a href="mailto:evan@marinlite.agency" style="color:#015048;text-decoration:none;font-size:13px;">evan@marinlite.agency</a>
        <span style="color:#c0c0c0;margin:0 8px;font-size:12px;">|</span>
        <a href="https://marinlite.agency" style="color:#015048;text-decoration:none;font-size:13px;">marinlite.agency</a>
      </p>
    </td>
  </tr>
</table>
```
