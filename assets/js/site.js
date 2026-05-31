const body = document.body;
const navToggle = document.querySelector("[data-nav-toggle]");
const navLinks = document.querySelector("[data-nav-links]");

const trackEvent = (eventName, parameters = {}) => {
  if (typeof window.gtag !== "function") {
    return;
  }

  window.gtag("event", eventName, {
    page_location: window.location.href,
    page_path: window.location.pathname,
    page_title: document.title,
    ...parameters,
  });
};

const analyticsFormSource = (form) =>
  form.dataset.analyticsSource ||
  form.querySelector('[name="metadata__source"], [name="source"]')?.value ||
  form.getAttribute("name") ||
  "unknown";

const formValue = (form, name) => {
  const field = form.querySelector(`[name="${name}"]`);
  return field?.value?.trim() || "";
};

const openMailtoFallback = (form) => {
  const recipient = form.dataset.mailtoFallback;
  if (!recipient) {
    return false;
  }

  const subject =
    formValue(form, "_subject") ||
    (form.getAttribute("name") === "private-note" ? "Private note from munyachipunza.com" : "Message from munyachipunza.com");
  const name = formValue(form, "name") || "Not provided";
  const senderEmail = formValue(form, "email") || "Not provided";
  const message = formValue(form, "message") || "No message entered";
  const articleTitle = formValue(form, "article_title");
  const articleUrl = formValue(form, "article_url") || window.location.href;
  const source = analyticsFormSource(form);
  const bodyLines = [
    message,
    "",
    "---",
    `Name: ${name}`,
    `Email: ${senderEmail}`,
    articleTitle ? `Reflection: ${articleTitle}` : "",
    `Page: ${articleUrl}`,
    `Source: ${source}`,
  ].filter(Boolean);

  window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(bodyLines.join("\n"))}`;
  return true;
};

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    body.classList.toggle("nav-open", !expanded);
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.setAttribute("aria-expanded", "false");
      body.classList.remove("nav-open");
    });
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll(".will-reveal").forEach((element) => {
  revealObserver.observe(element);
});

document.querySelectorAll("[data-copy-link]").forEach((button) => {
  button.addEventListener("click", async () => {
    const label = button.querySelector("[data-copy-text]");
    const originalLabel = label?.textContent || button.getAttribute("aria-label") || button.textContent;
    const setStatus = (message, state) => {
      if (label) {
        label.textContent = message;
      } else {
        button.textContent = message;
      }
      button.setAttribute("aria-label", message);
      button.setAttribute("title", message);
      button.classList.remove("is-copied", "is-error");
      if (state) {
        button.classList.add(state);
      }
    };

    try {
      await navigator.clipboard.writeText(button.dataset.copyLink);
      trackEvent("share_click", {
        share_platform: button.dataset.sharePlatform || "copy_link",
        link_url: button.dataset.copyLink,
      });
      setStatus("Link copied", "is-copied");
      window.setTimeout(() => {
        setStatus(originalLabel, "");
      }, 1600);
    } catch (error) {
      setStatus("Copy failed", "is-error");
      window.setTimeout(() => {
        setStatus(originalLabel, "");
      }, 1600);
    }
  });
});

document.querySelectorAll("a[data-share-platform]").forEach((link) => {
  link.addEventListener("click", () => {
    trackEvent("share_click", {
      share_platform: link.dataset.sharePlatform,
      link_url: link.href,
    });
  });
});

document.querySelectorAll("[data-native-share]").forEach((button) => {
  if (!navigator.share) {
    return;
  }

  button.hidden = false;
  button.addEventListener("click", async () => {
    const shareUrl = button.dataset.shareUrl || window.location.href;
    const shareTitle = button.dataset.shareTitle || document.title;

    try {
      await navigator.share({
        title: shareTitle,
        url: shareUrl,
      });
      trackEvent("share_click", {
        share_platform: button.dataset.sharePlatform || "native",
        link_url: shareUrl,
      });
    } catch (error) {
      if (error?.name !== "AbortError") {
        trackEvent("share_error", {
          share_platform: button.dataset.sharePlatform || "native",
          link_url: shareUrl,
        });
      }
    }
  });
});

document.querySelectorAll("[data-contact-form], [data-subscribe-form]").forEach((form) => {
  const button = form.querySelector('button[type="submit"]');
  const note = form.parentElement?.querySelector("[data-form-status]");
  const isSubscribe = form.hasAttribute("data-subscribe-form");
  const isButtondownSubscribe = isSubscribe && form.action.includes("buttondown.com/api/emails/embed-subscribe/");
  const ajaxAction = form.dataset.ajaxAction;
  const mailtoFallback = form.dataset.mailtoFallback;
  const useMailtoSubmit = mailtoFallback && form.dataset.submitMode === "mailto";
  const pendingMessage =
    form.dataset.pendingMessage || (isSubscribe ? "Saving your subscription..." : "Sending your note...");
  const successMessage =
    form.dataset.successMessage ||
    (isSubscribe ? "Thank you. Please check your inbox to confirm your subscription." : "Thank you. Your message is on its way.");
  const errorMessage =
    form.dataset.errorMessage ||
    (isSubscribe ? "Subscription did not go through. Please try again in a moment." : "The message did not send. Please try again in a moment.");
  const successButtonLabel = form.dataset.successButtonLabel || (isSubscribe ? "Check your inbox" : "Message sent");
  const errorButtonLabel = form.dataset.errorButtonLabel || "Try again";

  if (isButtondownSubscribe) {
    // Let Buttondown's official embedded form handle validation, subscription,
    // confirmation, and any visible error state. A no-cors fetch hides failures.
    form.addEventListener("submit", () => {
      if (form.reportValidity()) {
        trackEvent("newsletter_subscribe_submit", {
          form_provider: "buttondown",
          form_source: analyticsFormSource(form),
        });
      }
    });
    return;
  }

  if (useMailtoSubmit) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();

      if (!form.reportValidity()) {
        return;
      }

      const eventPrefix = isSubscribe ? "newsletter_subscribe" : "contact_form";
      trackEvent(`${eventPrefix}_submit`, {
        form_provider: "mailto",
        form_source: analyticsFormSource(form),
      });

      const originalLabel = button?.textContent ?? "";
      if (button) {
        button.disabled = true;
        button.textContent = pendingMessage;
      }

      try {
        openMailtoFallback(form);
        trackEvent(`${eventPrefix}_success`, {
          form_provider: "mailto",
          form_source: analyticsFormSource(form),
        });
        if (note) {
          note.dataset.state = "success";
          note.textContent = successMessage;
        }
        if (button) {
          button.textContent = successButtonLabel;
        }
      } catch (error) {
        trackEvent(`${eventPrefix}_error`, {
          form_provider: "mailto",
          form_source: analyticsFormSource(form),
        });
        if (note) {
          note.dataset.state = "error";
          note.textContent = errorMessage;
        }
        if (button) {
          button.textContent = errorButtonLabel;
        }
      } finally {
        window.setTimeout(() => {
          if (button) {
            button.disabled = false;
            button.textContent = originalLabel;
          }
        }, 2200);
      }
    });
    return;
  }

  if (!ajaxAction) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!form.reportValidity() || !ajaxAction) {
      return;
    }

    const eventPrefix = isSubscribe ? "newsletter_subscribe" : "contact_form";
    trackEvent(`${eventPrefix}_submit`, {
      form_provider: "formsubmit",
      form_source: analyticsFormSource(form),
    });

    const originalLabel = button?.textContent ?? "";
    if (button) {
      button.disabled = true;
      button.textContent = "Sending...";
    }

    if (note) {
      note.dataset.state = "";
      note.textContent = pendingMessage;
    }

    try {
      const response = await fetch(ajaxAction, {
        method: "POST",
        body: new FormData(form),
        headers: {
          Accept: "application/json",
        },
      });

      const payload = await response.json().catch(() => ({}));
      if (!response.ok || !["true", true].includes(payload.success)) {
        throw new Error("Submission failed");
      }

      form.reset();
      trackEvent(`${eventPrefix}_success`, {
        form_provider: "formsubmit",
        form_source: analyticsFormSource(form),
      });
      if (note) {
        note.dataset.state = "success";
        note.textContent = successMessage;
      }
      if (button) {
        button.textContent = successButtonLabel;
      }
    } catch (error) {
      trackEvent(`${eventPrefix}_error`, {
        form_provider: "formsubmit",
        form_source: analyticsFormSource(form),
      });
      if (mailtoFallback && openMailtoFallback(form)) {
        trackEvent(`${eventPrefix}_success`, {
          form_provider: "mailto_fallback",
          form_source: analyticsFormSource(form),
        });
        if (note) {
          note.dataset.state = "success";
          note.textContent = successMessage;
        }
        if (button) {
          button.textContent = successButtonLabel;
        }
        return;
      }
      if (note) {
        note.dataset.state = "error";
        note.textContent = errorMessage;
      }
      if (button) {
        button.textContent = errorButtonLabel;
      }
    } finally {
      window.setTimeout(() => {
        if (button) {
          button.disabled = false;
          button.textContent = originalLabel;
        }
      }, 1800);
    }
  });
});

const articleBody = document.querySelector(".article-body");
if (articleBody) {
  const sentDepths = new Set();
  const thresholds = [50, 90];
  let isQueued = false;

  const articleTitle = document.querySelector(".article-hero h1")?.textContent?.trim() || document.title;

  const checkReadDepth = () => {
    isQueued = false;

    const articleTop = articleBody.getBoundingClientRect().top + window.scrollY;
    const articleHeight = articleBody.offsetHeight;
    if (!articleHeight) {
      return;
    }

    const progress = Math.max(
      0,
      Math.min(100, ((window.scrollY + window.innerHeight - articleTop) / articleHeight) * 100)
    );

    thresholds.forEach((threshold) => {
      if (progress >= threshold && !sentDepths.has(threshold)) {
        sentDepths.add(threshold);
        trackEvent(`article_read_${threshold}`, {
          article_title: articleTitle,
          article_path: window.location.pathname,
          percent_scrolled: threshold,
        });
      }
    });

    if (sentDepths.size === thresholds.length) {
      window.removeEventListener("scroll", queueReadDepthCheck);
      window.removeEventListener("resize", queueReadDepthCheck);
    }
  };

  function queueReadDepthCheck() {
    if (isQueued) {
      return;
    }

    isQueued = true;
    window.requestAnimationFrame(checkReadDepth);
  }

  window.addEventListener("scroll", queueReadDepthCheck, { passive: true });
  window.addEventListener("resize", queueReadDepthCheck);
  queueReadDepthCheck();
}

document.querySelectorAll("[data-audio-player]").forEach((player) => {
  const toggle = player.querySelector("[data-audio-toggle]");
  const label = player.querySelector("[data-audio-label]");
  const iconPath = player.querySelector("[data-audio-toggle] svg path");
  const audio = player.querySelector("audio");

  if (!toggle || !audio) {
    return;
  }

  const route = player.dataset.audioRoute || window.location.pathname;
  const setPlayingState = (isPlaying) => {
    toggle.classList.toggle("is-playing", isPlaying);
    toggle.setAttribute("aria-pressed", isPlaying ? "true" : "false");
    if (label) {
      label.textContent = isPlaying ? "Pause audio" : "Listen to this reflection";
    }
    if (iconPath) {
      iconPath.setAttribute("d", isPlaying ? "M7 5h3v14H7V5Zm7 0h3v14h-3V5Z" : "M8 5v14l11-7L8 5Z");
    }
  };

  toggle.addEventListener("click", async () => {
    if (audio.paused) {
      try {
        await audio.play();
        trackEvent("audio_play", {
          article_path: window.location.pathname,
          article_route: route,
        });
      } catch (error) {
        trackEvent("audio_error", {
          article_path: window.location.pathname,
          article_route: route,
        });
      }
    } else {
      audio.pause();
      trackEvent("audio_pause", {
        article_path: window.location.pathname,
        article_route: route,
      });
    }
  });

  audio.addEventListener("play", () => setPlayingState(true));
  audio.addEventListener("pause", () => setPlayingState(false));
  audio.addEventListener("ended", () => setPlayingState(false));
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});
