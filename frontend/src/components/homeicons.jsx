import React from "react";

/* ---------- ICONS (inline SVG, no packages) ---------- */
const Svg = ({ children, size = 20, fill = "none", sw = 1.6 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill={fill}
    stroke="currentColor"
    strokeWidth={sw}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    {children}
  </svg>
);

export const Icon = {
  search: (s) => (<Svg size={s}><circle cx="11" cy="11" r="7" /><path d="M21 21l-4.3-4.3" /></Svg>),
  globe: (s) => (<Svg size={s}><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18" /></Svg>),
  chevron: (s) => (<Svg size={s} sw={2.2}><path d="M6 9l6 6 6-6" /></Svg>),
  arrow: (s) => (<Svg size={s} sw={2}><path d="M5 12h14M13 6l6 6-6 6" /></Svg>),
  sparkle: (s) => (<Svg size={s} fill="currentColor" sw={0}><path d="M12 2l2.2 6.3L21 10.5l-6.8 2.2L12 20l-2.2-7.3L3 10.5l6.8-2.2z" /></Svg>),
  trident: (s) => (<Svg size={s} sw={1.8}><path d="M12 21V6M5 4v5a7 7 0 0 0 14 0V4M9 21h6" /><path d="M12 6l-1.5-3M12 6l1.5-3" /></Svg>),
  kebab: (s) => (<Svg size={s} fill="currentColor" sw={0}><circle cx="12" cy="5" r="1.8" /><circle cx="12" cy="12" r="1.8" /><circle cx="12" cy="19" r="1.8" /></Svg>),
  user: (s) => (<Svg size={s}><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4 4-6 8-6s8 2 8 6" /></Svg>),
  image: (s) => (<Svg size={s}><rect x="3" y="3" width="18" height="18" rx="3" /><circle cx="8.5" cy="8.5" r="1.5" /><path d="M21 15l-5-5L5 21" /></Svg>),
  mic: (s) => (<Svg size={s}><rect x="9" y="2" width="6" height="12" rx="3" /><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3" /></Svg>),
  send: (s) => (<Svg size={s} fill="currentColor" sw={0}><path d="M3.4 20.4l17.4-7.5a1 1 0 0 0 0-1.8L3.4 3.6a1 1 0 0 0-1.4 1.2L4 11l9 1-9 1-2 6.2a1 1 0 0 0 1.4 1.2z" /></Svg>),
  temple: (s) => (<Svg size={s}><path d="M12 2l2 3.5h-4zM8 9l4-4 4 4M5 13l7-4 7 4M4 21V13h16v8M10 21v-5h4v5" /></Svg>),
  route: (s) => (<Svg size={s}><circle cx="6" cy="19" r="2" /><circle cx="18" cy="5" r="2" /><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7" /></Svg>),
  lotus: (s) => (<Svg size={s}><path d="M12 20c-2.5-2-4-4.5-4-8 2 1 3.5 2 4 4 .5-2 2-3 4-4 0 3.5-1.5 6-4 8z" /><path d="M12 16c-1.5-2-1.5-6 0-10 1.5 4 1.5 8 0 10zM3 11c0 5 4 8.5 9 9M21 11c0 5-4 8.5-9 9" /></Svg>),
  map: (s) => (<Svg size={s}><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14" /></Svg>),
  cloudsun: (s) => (<Svg size={s}><path d="M7 20a4 4 0 1 1 .8-7.9A5.5 5.5 0 0 1 18 13a3.5 3.5 0 0 1 0 7z" /><path d="M16 3v1.5M21 8h-1.5M11 8h1.5M19.5 4.5l-1 1M12.5 4.5l1 1" /></Svg>),
  book: (s) => (<Svg size={s}><path d="M2 5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v15a2 2 0 0 0-2-2H2zM22 5a2 2 0 0 0-2-2h-6a2 2 0 0 0-2 2v15a2 2 0 0 1 2-2h8z" /></Svg>),
  compass: (s) => (<Svg size={s}><circle cx="12" cy="12" r="9" /><path d="M15.5 8.5l-2 5-5 2 2-5z" /></Svg>),
  chat: (s) => (<Svg size={s}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" /></Svg>),
  calendar: (s) => (<Svg size={s}><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M3 10h18M8 3v4M16 3v4M8 14h2M12 14h2M8 17.5h2M12 17.5h2" /></Svg>),
  pin: (s) => (<Svg size={s}><path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z" /><circle cx="12" cy="10" r="2.5" /></Svg>),
  doc: (s) => (<Svg size={s}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M9 13h6M9 17h6" /></Svg>),
  mountain: (s) => (<Svg size={s}><path d="M3 20l6-11 4 6 3-4 5 9z" /></Svg>),
  building: (s) => (<Svg size={s}><path d="M4 21V8l8-5 8 5v13M9 21v-6h6v6" /></Svg>),
  city: (s) => (<Svg size={s}><path d="M4 21V9h6v12M14 21V4h6v17M7 13h1M7 17h1M17 8h1M17 12h1M17 16h1" /></Svg>),
  clock: (s) => (<Svg size={s}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></Svg>),
  menu: (s) => (<Svg size={s} sw={2}><path d="M4 7h16M4 12h16M4 17h16" /></Svg>),
  close: (s) => (<Svg size={s} sw={2}><path d="M18 6L6 18M6 6l12 12" /></Svg>),
  mail: (s) => (<Svg size={s}><rect x="3" y="5" width="18" height="14" rx="3" /><path d="M3 8l9 6 9-6" /></Svg>),
  lock: (s) => (<Svg size={s}><rect x="4" y="11" width="16" height="10" rx="3" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></Svg>),
  eye: (s) => (<Svg size={s}><path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z" /><circle cx="12" cy="12" r="3" /></Svg>),
  eyeoff: (s) => (<Svg size={s}><path d="M3 3l18 18M10.6 5.1A10 10 0 0 1 12 5c6.5 0 10.5 7 10.5 7a17 17 0 0 1-3.2 3.9M6.6 6.6A17 17 0 0 0 1.5 12S5.5 19 12 19a10 10 0 0 0 4.4-1M9.9 9.9a3 3 0 0 0 4.2 4.2" /></Svg>),
  speaker: (s) => (<Svg size={s}><path d="M11 5L6 9H2v6h4l5 4V5z" /><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13" /></Svg>),
  stop: (s) => (<Svg size={s} fill="currentColor" sw={0}><rect x="6" y="6" width="12" height="12" rx="2.5" /></Svg>),
  check: (s) => (<Svg size={s} sw={2.2}><path d="M20 6L9 17l-5-5" /></Svg>),
  trash: (s) => (<Svg size={s}><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14M10 11v5M14 11v5" /></Svg>),
  camera: (s) => (<Svg size={s}><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" /><circle cx="12" cy="13" r="4" /></Svg>),
};

/* Brand mark: mountains + temple */
export const Logo = () => (
  <svg width="46" height="40" viewBox="0 0 46 40" fill="none" aria-hidden="true">
    <path d="M2 35L15 16l6 8 6-10 17 21z" fill="#f4b95f" opacity="0.28" />
    <path d="M2 35L15 16l6 8M27 14l17 21" stroke="#f4b95f" strokeWidth="1.6" strokeLinejoin="round" />
    <path d="M23 6l3 4h-6zM18 14l5-4 5 4M16 18l7-4 7 4M14 35V22h18v13" stroke="#f4b95f" strokeWidth="1.6" strokeLinejoin="round" strokeLinecap="round" />
    <path d="M23 2v4" stroke="#f4b95f" strokeWidth="1.6" strokeLinecap="round" />
    <path d="M3 37h40" stroke="#f4b95f" strokeWidth="1.6" strokeLinecap="round" />
  </svg>
);