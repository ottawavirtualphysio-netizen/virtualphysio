/* ============================================================
   Virtual Physio.ca — Premium JS Upgrade
   Scroll animations, navbar, 3D tilt, form UX, chat
   ============================================================ */

/* ── Navbar ──────────────────────────────────────────────── */
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");
const siteHeader = document.querySelector(".site-header");
const floatingAssistant = document.querySelector(".chatbot");

function trackConversion(eventName, eventParams = {}) {
  if (typeof window.gtag === "function") {
    window.gtag("event", eventName, eventParams);
  }
}

document.querySelectorAll("[data-track]").forEach((element) => {
  element.addEventListener("click", () => {
    trackConversion(element.dataset.track, {
      page_path: window.location.pathname,
      link_url: element.href || ""
    });
  });
});

function updateFloatingAssistantOffset() {
  if (!floatingAssistant) return;
  const footer = document.querySelector(".site-footer");
  const edgeOffset = window.innerWidth <= 640 ? 16 : 20;
  let bottomOffset = edgeOffset;

  if (footer) {
    const footerTop = footer.getBoundingClientRect().top;
    const viewportHeight = window.innerHeight;
    if (footerTop < viewportHeight - edgeOffset) {
      bottomOffset = Math.max(edgeOffset, viewportHeight - footerTop + edgeOffset);
    }
  }

  floatingAssistant.style.bottom = `${bottomOffset}px`;
}

if (floatingAssistant) {
  window.addEventListener("scroll", updateFloatingAssistantOffset, { passive: true });
  window.addEventListener("resize", updateFloatingAssistantOffset);
  updateFloatingAssistantOffset();
}

if (navToggle && navMenu) {
  const closeNavMenu = () => {
    navMenu.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", "Open navigation");
  };

  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("is-open");
    document.body.classList.toggle("nav-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
  });

  navMenu.addEventListener("click", (event) => {
    if (event.target.matches("a")) {
      closeNavMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navMenu.classList.contains("is-open")) {
      closeNavMenu();
      navToggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!navMenu.classList.contains("is-open")) return;
    const clickedInsideMenu = navMenu.contains(event.target);
    const clickedToggle = navToggle.contains(event.target);
    if (!clickedInsideMenu && !clickedToggle) {
      closeNavMenu();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920 && navMenu.classList.contains("is-open")) {
      closeNavMenu();
    }
  });
}

/* Navbar shrink on scroll */
if (siteHeader) {
  const handleNavScroll = () => {
    if (window.scrollY > 50) {
      siteHeader.classList.add("scrolled");
    } else {
      siteHeader.classList.remove("scrolled");
    }
  };
  window.addEventListener("scroll", handleNavScroll, { passive: true });
  handleNavScroll();
}

/* ── Scroll Reveal ───────────────────────────────────────── */
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
);

document.querySelectorAll(".reveal").forEach((el) => {
  revealObserver.observe(el);
});

/* ── Subtle 3D Tilt on Cards (desktop only) ──────────────── */
const isMobile = () => window.innerWidth < 768 || "ontouchstart" in window;

function applyCardTilt(cards) {
  cards.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      if (isMobile()) return;
      const rect = card.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / (rect.width / 2);
      const dy = (e.clientY - cy) / (rect.height / 2);
      const rotX = -dy * 4;
      const rotY = dx * 4;
      card.style.transform = `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-6px)`;
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "";
    });
  });
}

applyCardTilt(document.querySelectorAll(".service-card, .service-detail-card"));

/* ── Form UX ─────────────────────────────────────────────── */
const bookingForm = document.querySelector(".booking-form");

function showToast(message, tone = "success") {
  const existingToast = document.querySelector(".booking-toast");
  if (existingToast) existingToast.remove();

  const toast = document.createElement("div");
  toast.className = `booking-toast ${tone}`;
  toast.setAttribute("role", "status");
  toast.setAttribute("aria-live", "polite");
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add("is-visible");
  });

  window.setTimeout(() => {
    toast.classList.remove("is-visible");
    window.setTimeout(() => toast.remove(), 260);
  }, 2600);
}

/* Focus highlight label */
document.querySelectorAll("input, select, textarea").forEach((field) => {
  const label = field.closest(".form-row")?.querySelector("label");

  field.addEventListener("focus", () => {
    if (label) label.style.color = "var(--blue)";
  });
  field.addEventListener("blur", () => {
    if (label) label.style.color = "";
  });
});

if (bookingForm) {
  const submitButton = bookingForm.querySelector('button[type="submit"]');
  const defaultButtonText = submitButton ? submitButton.textContent : "";
  const googleSheetUrl = (bookingForm.dataset.googleSheetUrl || "").trim();
  const phoneInput = bookingForm.querySelector('input[name="phone"]');
  const emailInput = bookingForm.querySelector('input[name="email"]');
  const nameInput = bookingForm.querySelector('input[name="name"]');
  const serviceInput = bookingForm.querySelector('select[name="service"]');

  const encodeFormBody = (formData) =>
    new URLSearchParams(Array.from(formData.entries()).map(([key, value]) => [key, String(value)])).toString();

  const normalizePhone = (value) => {
    const raw = String(value || "").trim();
    const hasPlus = raw.startsWith("+");
    const digits = raw.replace(/\D/g, "").slice(0, 15);
    return `${hasPlus ? "+" : ""}${digits}`;
  };

  const formatPhoneForDisplay = (value) => {
    const normalized = normalizePhone(value);
    const digits = normalized.replace(/\D/g, "");
    if (!digits) return "";
    const country = digits.slice(0, 3);
    const remaining = digits.slice(3);
    const p1 = remaining.slice(0, 3);
    const p2 = remaining.slice(3, 6);
    const p3 = remaining.slice(6, 10);
    return `+${country}${p1 ? ` ${p1}` : ""}${p2 ? ` ${p2}` : ""}${p3 ? ` ${p3}` : ""}`;
  };

  const isValidPhone = (value) => /^\+\d{8,15}$/.test(normalizePhone(value));
  const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || "").trim());

  const setFieldError = (field, message) => {
    const row = field?.closest(".form-row");
    const errorEl = row?.querySelector(".field-error");
    if (errorEl) errorEl.textContent = message || "";
    if (message) {
      field?.setAttribute("aria-invalid", "true");
    } else {
      field?.removeAttribute("aria-invalid");
    }
  };

  const clearAllErrors = () => {
    bookingForm.querySelectorAll(".field-error").forEach((el) => {
      el.textContent = "";
    });
    bookingForm.querySelectorAll("[aria-invalid='true']").forEach((el) => {
      el.removeAttribute("aria-invalid");
    });
  };

  if (phoneInput) {
    phoneInput.addEventListener("input", () => {
      phoneInput.value = formatPhoneForDisplay(phoneInput.value);
      setFieldError(phoneInput, "");
    });
  }

  [nameInput, emailInput, serviceInput].forEach((field) => {
    field?.addEventListener("input", () => setFieldError(field, ""));
    field?.addEventListener("change", () => setFieldError(field, ""));
  });

  bookingForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(bookingForm);
    const status = bookingForm.querySelector(".form-status");
    const name = data.get("name") || "Patient";
    const service = data.get("service") || "Physiotherapy";
    const date = data.get("date") || "next available date";
    const time = data.get("time") || "next available time";
    if (submitButton) {
      submitButton.classList.remove("is-success");
      submitButton.disabled = true;
      submitButton.classList.add("is-loading");
      submitButton.textContent = "Sending...";
    }

    try {
      clearAllErrors();
      let firstInvalidField = null;

      if (!String(nameInput?.value || "").trim()) {
        setFieldError(nameInput, "Please enter your full name.");
        firstInvalidField = firstInvalidField || nameInput;
      }

      if (!isValidPhone(phoneInput?.value || "")) {
        setFieldError(phoneInput, "Please enter a valid phone number with country code.");
        firstInvalidField = firstInvalidField || phoneInput;
      } else if (phoneInput) {
        phoneInput.value = normalizePhone(phoneInput.value);
      }

      const emailValue = String(emailInput?.value || "").trim();
      if (emailValue && !isValidEmail(emailValue)) {
        setFieldError(emailInput, "Please enter a valid email address.");
        firstInvalidField = firstInvalidField || emailInput;
      }

      if (!String(serviceInput?.value || "").trim()) {
        setFieldError(serviceInput, "Please select a service.");
        firstInvalidField = firstInvalidField || serviceInput;
      }

      if (firstInvalidField) {
        if (status) status.textContent = "Please fix the highlighted fields and try again.";
        firstInvalidField.focus();
        throw new Error("Validation failed");
      }

      const submitData = new FormData(bookingForm);
      const payload = {
        name: String(submitData.get("name") || ""),
        phone: String(submitData.get("phone") || ""),
        email: String(submitData.get("email") || ""),
        service: String(submitData.get("service") || ""),
        date: String(submitData.get("date") || ""),
        time: String(submitData.get("time") || ""),
        problemArea: submitData.getAll("problemArea").join(", "),
        message: String(submitData.get("message") || ""),
        source: window.location.pathname,
        submittedAt: new Date().toISOString()
      };

      const hasGoogleSheetEndpoint =
        googleSheetUrl && !googleSheetUrl.includes("YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL");

      const response = hasGoogleSheetEndpoint
        ? await fetch(googleSheetUrl, {
            method: "POST",
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: JSON.stringify(payload)
          })
        : await fetch("/", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: encodeFormBody(submitData)
          });

      if (!response.ok) {
        throw new Error("Form submit failed");
      }

      if (status) {
        status.textContent = `Thanks, ${name}. Your appointment request was submitted successfully. Thanks for choosing us.`;
      }
      trackConversion("generate_lead", {
        page_path: window.location.pathname,
        service: payload.service
      });
      showToast("Appointment request submitted successfully.");

      if (submitButton) {
        submitButton.classList.remove("is-loading");
        submitButton.classList.add("is-success");
        submitButton.disabled = false;
        submitButton.textContent = "✓ Request Sent Successfully";
      }

      if (chatPanel && chatToggle) {
        chatPanel.removeAttribute("hidden");
        chatToggle.setAttribute("aria-expanded", "true");
      }

      addChatMessage("Appointment request submitted.", "user");
      addChatMessage(
        [
          "Your request details:",
          `Name: ${payload.name}`,
          `Phone: ${payload.phone}`,
          `Email: ${payload.email}`,
          `Service: ${payload.service}`,
          `Date: ${payload.date}`,
          `Time: ${payload.time}`,
          `Problem Area: ${payload.problemArea || "Not specified"}`,
          `Message: ${payload.message}`
        ].join("\n")
      );

      bookingForm.reset();

      /* Reset label colors */
      document.querySelectorAll(".booking-form label").forEach((l) => {
        l.style.color = "";
      });
    } catch (error) {
      if (error instanceof Error && error.message === "Validation failed") {
        if (submitButton) {
          submitButton.classList.remove("is-loading");
          submitButton.classList.remove("is-success");
          submitButton.disabled = false;
          submitButton.textContent = defaultButtonText;
        }
        return;
      }

      if (status) {
        status.textContent = "Unable to submit right now. Please try again.";
      }
      showToast("Submission failed. Please try again.", "error");

      if (submitButton) {
        submitButton.classList.remove("is-loading");
        submitButton.classList.remove("is-success");
        submitButton.disabled = false;
        submitButton.textContent = defaultButtonText;
      }
    }
  });
}

/* ── Smooth anchor scroll ────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (e) => {
    const id = anchor.getAttribute("href").slice(1);
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      const offset = 90;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
    }
  });
});

/* ── Chatbot ─────────────────────────────────────────────── */
const chatToggle = document.querySelector(".chat-toggle");
const chatPanel = document.querySelector(".chat-panel");
const chatClose = document.querySelector(".chat-close");
const chatForm = document.querySelector(".chat-form");
const chatLog = document.querySelector(".chat-log");
const chatInput = document.querySelector("#chat-input");

const replies = [
  {
    keys: ["book", "appointment", "schedule", "visit"],
    text: "You can book from the Contact page appointment form. Share your service, preferred date and phone number, and Virtual Physio.ca will confirm by WhatsApp. In-home treatment in Ottawa, home clinic room care and person-to-person appointments are available by request."
  },
  {
    keys: ["pain", "back", "neck", "shoulder", "knee"],
    text: "For pain, a physiotherapist starts with assessment, movement testing and a plan that may include manual therapy, exercise and posture guidance. Seek urgent care for severe trauma, numbness, chest pain or sudden weakness."
  },
  {
    keys: ["service", "physio", "pelvic", "exercise", "rehab", "home"],
    text: "Virtual Physio.ca offers physiotherapy assessment, follow-up treatment, extended treatment, in-home treatment in Ottawa, home clinic room care, person-to-person physiotherapy, pelvic floor physiotherapy, post-surgery rehab, pain management and sports injury care."
  },
  {
    keys: ["cost", "price", "fee"],
    text: "Fees depend on the service and session length. Send Virtual Physio.ca your preferred service and they can confirm availability and pricing."
  },
  {
    keys: ["hours", "open", "time"],
    text: "Virtual appointments are available Monday to Saturday, 9:00 AM to 7:00 PM."
  },
  {
    keys: ["location", "online", "virtual", "address"],
    text: "Virtual appointments are available across Ottawa, and in-home treatment in Ottawa is available by request. The Contact page has direct phone, WhatsApp and email links."
  }
];

function addChatMessage(text, type = "assistant") {
  if (!chatLog) return;
  const message = document.createElement("div");
  message.className = `chat-message ${type}`;
  message.textContent = text;
  chatLog.appendChild(message);
  requestAnimationFrame(() => {
    chatLog.scrollTop = chatLog.scrollHeight;
  });
}

function getAssistantReply(input) {
  const normalized = input.toLowerCase();
  const match = replies.find((item) =>
    item.keys.some((key) => normalized.includes(key))
  );
  return match
    ? match.text
    : "I can help with services, pain questions, virtual care hours and booking. For a personal diagnosis, please book an assessment with a licensed physiotherapist.";
}

/* Typing indicator */
function showTypingIndicator() {
  if (!chatLog) return null;
  const el = document.createElement("div");
  el.className = "chat-message assistant typing-indicator";
  el.textContent = "Typing…";
  el.style.opacity = "0.6";
  el.style.fontStyle = "italic";
  chatLog.appendChild(el);
  chatLog.scrollTop = chatLog.scrollHeight;
  return el;
}

if (chatToggle && chatPanel) {
  chatToggle.addEventListener("click", () => {
    const willOpen = chatPanel.hasAttribute("hidden");
    if (willOpen) {
      chatPanel.removeAttribute("hidden");
      chatToggle.setAttribute("aria-expanded", "true");
      if (chatLog && !chatLog.children.length) {
        addChatMessage(
          "Hello. I can answer common physiotherapy questions and guide you to booking."
        );
      }
      setTimeout(() => chatInput?.focus(), 80);
    } else {
      chatPanel.setAttribute("hidden", "");
      chatToggle.setAttribute("aria-expanded", "false");
    }
  });
}

if (chatClose && chatPanel && chatToggle) {
  chatClose.addEventListener("click", () => {
    chatPanel.setAttribute("hidden", "");
    chatToggle.setAttribute("aria-expanded", "false");
    chatToggle.focus();
  });
}

if (chatForm) {
  chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const value = chatInput.value.trim();
    if (!value) return;
    addChatMessage(value, "user");
    chatInput.value = "";

    const indicator = showTypingIndicator();
    setTimeout(() => {
      indicator?.remove();
      addChatMessage(getAssistantReply(value));
    }, 520 + Math.random() * 280);
  });
}

/* ── Hero image parallax (subtle) ───────────────────────── */
const heroVisual = document.querySelector(".hero-visual");
if (heroVisual && !isMobile()) {
  window.addEventListener(
    "scroll",
    () => {
      const scrolled = window.scrollY;
      if (scrolled < window.innerHeight) {
        heroVisual.style.transform = `translateY(${scrolled * 0.06}px)`;
      }
    },
    { passive: true }
  );
}
