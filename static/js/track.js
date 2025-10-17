// Day 1: lightweight visitor capture helper (sends screen/device info via fetch later)
(function () {
  try {
    window._cs = window._cs || {};
    _cs.screen = {
      w: screen.width,
      h: screen.height,
      availW: screen.availWidth,
      availH: screen.availHeight,
    };
    _cs.userAgent = navigator.userAgent;
    _cs.lang = navigator.language || navigator.userLanguage;
    // We'll POST this data after user logs in or on page load in later days
    // Example: fetch('/api/track', {method:'POST', body: JSON.stringify(_cs)})
  } catch (e) {
    console.warn(e);
  }
})();
