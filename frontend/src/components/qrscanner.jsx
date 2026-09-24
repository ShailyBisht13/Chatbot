import React, { useEffect, useRef } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";
import "./qrscanner.css";

export default function QRScanner({ onScan, onClose }) {
  // Keep the latest callbacks in refs so the camera is set up only once,
  // even when the parent re-renders with new inline functions.
  const onScanRef = useRef(onScan);
  const onCloseRef = useRef(onClose);
  onScanRef.current = onScan;
  onCloseRef.current = onClose;

  useEffect(() => {
    const scanner = new Html5QrcodeScanner(
      "qr-reader",
      { fps: 10, qrbox: 250 },
      false
    );

    scanner.render(
      (decodedText) => {
        onScanRef.current(decodedText);
        scanner.clear();
        onCloseRef.current();
      },
      (error) => {}
    );

    return () => {
      scanner.clear().catch(() => {});
    };
  }, []);

  return (
    <div className="qr-overlay" onClick={onClose}>
      <div
        className="qr-box"
        role="dialog"
        aria-modal="true"
        aria-label="Scan QR Code"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="qr-head">
          <h3>Scan QR Code</h3>
          <p>Point your camera at the code</p>
        </div>

        <div className="qr-frame">
          <div id="qr-reader" />
        </div>

        <button className="close-btn" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}