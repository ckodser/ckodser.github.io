// Adds a small "expand" icon button to content images
// and opens them with Medium Zoom when clicked.
// Also applies an adaptive max-width based on aspect ratio.

function summaryMaxWidthForAspectRatio(aspectRatio) {
  // aspectRatio = width / height
  // Keep square-ish images smaller; allow wide, short images to be larger.
  // Tuned for aesthetics: wide diagrams should be readable without looking cramped.
  if (!Number.isFinite(aspectRatio) || aspectRatio <= 0) return "50%";

  // Square / portrait
  if (aspectRatio <= 1.2) return "50%";

  // Mildly wide: 50% -> 65%
  if (aspectRatio <= 1.7) {
    const t = (aspectRatio - 1.2) / (1.7 - 1.2);
    return `${Math.round(50 + t * 15)}%`;
  }

  // Wide: 65% -> 85%
  if (aspectRatio <= 2.6) {
    const t = (aspectRatio - 1.7) / (2.6 - 1.7);
    return `${Math.round(65 + t * 20)}%`;
  }

  // Very wide panoramas / plots
  return "92%";
}

function applySummarySizingFromImage(wrap, img) {
  const apply = () => {
    const w = img.naturalWidth;
    const h = img.naturalHeight;
    if (!w || !h) return;
    const ar = w / h;
    wrap.style.setProperty("--summary-img-max-width", summaryMaxWidthForAspectRatio(ar));
  };

  if (img.complete) {
    apply();
  } else {
    img.addEventListener("load", apply, { once: true });
  }
}

function initSummaryImageExpandButtons() {
  if (!document.body) return;
  const isTargetCollection =
    document.body.classList.contains("collection-summaries") || document.body.classList.contains("collection-projects");
  if (!isTargetCollection) return;

  const figures = document.querySelectorAll(".post article figure, .post.distill d-article figure");
  if (!figures.length) return;

  figures.forEach((figure) => {
    // Avoid double-injecting.
    if (figure.querySelector(":scope > .summary-img-wrap")) return;

    const picture = figure.querySelector("picture");
    const img = figure.querySelector("img");
    if (!picture || !img) return;

    // Wrap the picture so we can absolutely position the button.
    const wrap = document.createElement("span");
    wrap.className = "summary-img-wrap";
    picture.parentNode.insertBefore(wrap, picture);
    wrap.appendChild(picture);

    // Adaptive sizing: wide images get more horizontal room.
    applySummarySizingFromImage(wrap, img);

    // Ensure Medium Zoom sees this image.
    img.setAttribute("data-zoomable", "");

    // Create the expand button.
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "summary-img-expand";
    btn.setAttribute("aria-label", "Expand image");
    btn.title = "Expand";
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      // Simple "expand" icon (two arrows)
      '<path d="M4 10V4h6v2H6v4H4zm14 0V6h-4V4h6v6h-2zM10 20H4v-6h2v4h4v2zm10 0h-6v-2h4v-4h2v6z"/>' +
      "</svg>";

    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      // Medium Zoom instance is created in `assets/js/zoom.js`.
      const mz = window.medium_zoom;
      if (mz && typeof mz.open === "function") {
        // Make sure it's attached even though we added the attribute dynamically.
        if (typeof mz.attach === "function") mz.attach(img);
        mz.open({ target: img });
        return;
      }

      // Fallback: open image in a new tab.
      const src = img.currentSrc || img.src;
      if (src) window.open(src, "_blank", "noopener,noreferrer");
    });

    wrap.appendChild(btn);
  });
}

// Run after deferred scripts (including medium-zoom + zoom.js) have executed.
document.addEventListener("DOMContentLoaded", initSummaryImageExpandButtons);
