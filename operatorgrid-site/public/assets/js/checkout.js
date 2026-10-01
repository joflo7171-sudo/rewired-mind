/*
 * OperatorGrid checkout wiring: the ONLY place the purchase link is configured.
 *
 * PREVIEW STATE: CHECKOUT_URL is empty, so every [data-checkout] button stays inactive.
 * At launch (owner approval required), paste the Stripe-hosted checkout or payment link URL
 * for the $149 one-time product below. No other file needs to change.
 */
(function () {
  var CHECKOUT_URL = ""; // e.g. "https://buy.stripe.com/XXXXXXXX" (do not fill in until launch is approved)

  var buttons = document.querySelectorAll("[data-checkout]");
  var notes = document.querySelectorAll("[data-checkout-note]");

  if (CHECKOUT_URL) {
    buttons.forEach(function (b) {
      b.setAttribute("href", CHECKOUT_URL);
      b.removeAttribute("aria-disabled");
      b.removeAttribute("role");
    });
    notes.forEach(function (n) { n.textContent = "Secure checkout. Instant download after purchase."; });
    return;
  }

  // Not connected: buttons that point at #pricing just scroll there; the pricing button does nothing.
  buttons.forEach(function (b) {
    var target = b.getAttribute("data-preview-target");
    if (target) { b.setAttribute("href", target); return; }
    b.setAttribute("aria-disabled", "true");
    b.addEventListener("click", function (e) { e.preventDefault(); });
  });
})();
