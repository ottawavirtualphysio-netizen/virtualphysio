/* ============================================================
   Virtual Physio — site script
   Navigation, analytics events, booking form (Netlify Forms + WhatsApp)
   ============================================================ */
(function () {
  "use strict";

  var WHATSAPP_NUMBER = "13432024226";
  var PHONE_DISPLAY = "+1 (343) 202-4226";

  /* ── Analytics (only if Google Analytics is installed) ───── */
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-track]");
    if (el) track(el.dataset.track, { page_path: location.pathname, link_url: el.href || "" });
  });

  /* ── Mobile navigation ───────────────────────────────────── */
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.querySelector(".nav-menu");
  if (toggle && menu) {
    var setOpen = function (open) {
      menu.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
    };
    toggle.addEventListener("click", function () { setOpen(!menu.classList.contains("is-open")); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (menu.classList.contains("is-open") && !menu.contains(e.target) && !toggle.contains(e.target)) setOpen(false);
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 920) setOpen(false); });
  }

  /* ── Header shadow on scroll ─────────────────────────────── */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 30); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ── Blog topic filter ───────────────────────────────────── */
  var filterButtons = document.querySelectorAll(".filter-row button");
  filterButtons.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.filter;
      filterButtons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      document.querySelectorAll("#post-grid .post-card").forEach(function (c) {
        c.hidden = !(f === "all" || c.dataset.category === f);
      });
    });
  });

  /* ── Booking form ────────────────────────────────────────── */
  var form = document.getElementById("appointment-form");
  if (!form) return;

  var status = form.querySelector(".form-status");
  var submitBtn = form.querySelector('button[type="submit"]');
  var submitLabel = submitBtn ? submitBtn.textContent : "Send request";

  // Old link names still used around the web -> current form values
  var SERVICE_ALIASES = {
    "Physiotherapy": "Initial Assessment",
    "Physiotherapy Subsequent Treatment": "Follow-up Treatment",
    "Physiotherapy Extended Treatment": "Initial Assessment",
    "In-Home Treatment": "Initial Assessment",
    "Pelvic Floor Treatment": "Pelvic Floor Physiotherapy",
    "Motor Vehicle Accident Rehab": "Car Accident (MVA) Rehab"
  };

  // Phone: 10 digits -> +1XXXXXXXXXX; 11 digits starting with 1 -> +1...; others need +country code
  function normalizePhone(value) {
    var raw = String(value || "").trim();
    var d = raw.replace(/\D/g, "").slice(0, 15);
    if (d.length === 10 && /^[2-9]/.test(d)) return "+1" + d;
    if (d.length === 11 && d.charAt(0) === "1") return "+" + d;
    return raw.charAt(0) === "+" ? "+" + d : d;
  }
  function prettyPhone(value) {
    var n = normalizePhone(value);
    var m = /^\+1(\d{3})(\d{3})(\d{4})$/.exec(n);
    return m ? "+1 (" + m[1] + ") " + m[2] + "-" + m[3] : String(value || "").trim();
  }
  function validPhone(value) { return /^\+\d{10,15}$/.test(normalizePhone(value)); }
  function validEmail(value) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value); }

  function errorEl(field) {
    var box = field.closest(".form-row") || field.closest("fieldset") || field.closest(".consent");
    return box ? box.querySelector(".field-error") : null;
  }
  function setError(field, msg) {
    var el = errorEl(field);
    if (el) el.textContent = msg || "";
    var target = field.matches("input[type=radio]") ? field.closest(".choices") : field;
    if (msg) target.setAttribute("aria-invalid", "true"); else target.removeAttribute("aria-invalid");
  }
  function clearErrors() {
    form.querySelectorAll(".field-error").forEach(function (e) { e.textContent = ""; });
    form.querySelectorAll("[aria-invalid]").forEach(function (e) { e.removeAttribute("aria-invalid"); });
  }

  // Conditional fields (e.g. area for in-home visits)
  function updateConditional() {
    var visit = (form.querySelector('input[name="visitType"]:checked') || {}).value || "";
    form.querySelectorAll("[data-show-when]").forEach(function (row) {
      row.hidden = row.dataset.showWhen !== visit;
    });
    var age = form.querySelector('select[name="ageGroup"]');
    var note = form.querySelector(".age-note");
    if (age && note) note.hidden = age.value !== "Under 18";
  }

  // Pre-select from the URL: /booking?service=...&visit=...
  var params = new URLSearchParams(location.search);
  var wantService = params.get("service");
  var wantVisit = params.get("visit");
  if (wantService === "In-Home Treatment" && !wantVisit) wantVisit = "In my home";
  if (wantService) wantService = SERVICE_ALIASES[wantService] || wantService;
  [["service", wantService], ["visitType", wantVisit]].forEach(function (pair) {
    if (!pair[1]) return;
    form.querySelectorAll('input[name="' + pair[0] + '"]').forEach(function (r) {
      if (r.value === pair[1]) r.checked = true;
    });
  });

  form.addEventListener("change", function (e) {
    if (e.target.name) setError(e.target, "");
    updateConditional();
  });
  form.addEventListener("input", function (e) { if (e.target.name) setError(e.target, ""); });
  var phoneInput = form.querySelector('input[name="phone"]');
  // Format Canadian/US numbers as the user types: (343) 202-4226. International (+...) numbers are left as typed.
  function liveFormat(v) {
    if (/^\s*\+/.test(v) && !/^\s*\+1/.test(v)) return v;
    var d = v.replace(/\D/g, "");
    if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
    if (d.length > 10) return v;
    if (d.length < 4) return d;
    if (d.length < 7) return "(" + d.slice(0, 3) + ") " + d.slice(3);
    return "(" + d.slice(0, 3) + ") " + d.slice(3, 6) + "-" + d.slice(6);
  }
  if (phoneInput) {
    phoneInput.addEventListener("input", function (e) {
      if (e.inputType && e.inputType.indexOf("delete") === 0) return; // don't fight backspace
      var atEnd = phoneInput.selectionStart === phoneInput.value.length;
      if (atEnd) phoneInput.value = liveFormat(phoneInput.value);
    });
    phoneInput.addEventListener("blur", function () {
      var v = phoneInput.value;
      phoneInput.value = /^\s*\+(?!1)/.test(v) ? v.trim() : liveFormat(v);
    });
  }
  updateConditional();

  function validate() {
    clearErrors();
    var first = null;
    function fail(field, msg) { setError(field, msg); if (!first) first = field; }
    var get = function (n) { return form.querySelector('[name="' + n + '"]'); };

    if (!form.querySelector('input[name="service"]:checked')) fail(get("service"), "Please choose what you need help with.");
    var visit = form.querySelector('input[name="visitType"]:checked');
    if (!visit) fail(get("visitType"), "Please choose how you'd like to be seen.");
    else if (visit.value === "In my home" && !get("area").value.trim()) fail(get("area"), "Please tell us your area so we can plan the visit.");
    if (!get("name").value.trim()) fail(get("name"), "Please enter your name.");
    if (!validPhone(get("phone").value)) fail(get("phone"), "Please enter a valid phone number, e.g. 343 202 4226.");
    var email = get("email").value.trim();
    if (email && !validEmail(email)) fail(get("email"), "Please check your email address.");
    if (!get("ageGroup").value) fail(get("ageGroup"), "Please select the patient's age group.");
    if (!get("consent").checked) fail(get("consent"), "Please confirm so we can contact you.");

    if (first) {
      var focusTarget = first.matches("input[type=radio]") ? first.closest("fieldset") : first;
      focusTarget.scrollIntoView({ behavior: "smooth", block: "center" });
      if (first.focus) first.focus({ preventScroll: true });
      if (status) status.textContent = "Please check the highlighted fields.";
    }
    return !first;
  }

  function whatsappLink(d) {
    var lines = [
      "Hi Virtual Physio, I just sent an appointment request on your website:",
      "Name: " + d.name,
      "Phone: " + prettyPhone(d.phone),
      "Age group: " + d.ageGroup,
      "Service: " + d.service,
      "Visit: " + d.visitType + (d.area ? " (" + d.area + ")" : ""),
      d.date || d.timeOfDay ? "Preferred: " + [d.date, d.timeOfDay].filter(Boolean).join(", ") : ""
    ].filter(Boolean);
    return "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (status) { status.className = "form-status"; status.textContent = ""; }
    var phone = form.querySelector('[name="phone"]');
    if (!validate()) return;

    phone.value = normalizePhone(phone.value);
    var fd = new FormData(form);
    phone.value = prettyPhone(phone.value);
    var d = {};
    fd.forEach(function (v, k) { d[k] = String(v); });

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    fetch(form.getAttribute("action") || "/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(fd).toString()
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      track("generate_lead", { service: d.service, visit_type: d.visitType });
      var wa = whatsappLink(d);
      form.querySelectorAll(".form-step, .consent, button[type=submit]").forEach(function (el) { el.hidden = true; });
      status.className = "form-status is-success";
      status.innerHTML = "";
      var h = document.createElement("h2");
      h.textContent = "Thanks, " + d.name.split(" ")[0] + "! Your request was sent.";
      var p = document.createElement("p");
      p.textContent = "We'll contact you to confirm your appointment, usually the same day. For the fastest reply, also send your request to us on WhatsApp:";
      var a = document.createElement("a");
      a.className = "btn btn-whatsapp";
      a.href = wa; a.target = "_blank"; a.rel = "noopener";
      a.textContent = "Send on WhatsApp";
      a.setAttribute("data-track", "whatsapp_after_submit");
      status.append(h, p, a);
      status.scrollIntoView({ behavior: "smooth", block: "center" });
      // Phones: open WhatsApp automatically; the button stays as a fallback.
      if (window.matchMedia("(max-width: 900px)").matches) {
        setTimeout(function () { window.location.href = wa; }, 1500);
      }
    }).catch(function () {
      status.className = "form-status is-error";
      status.textContent = "Sorry, your request couldn't be sent. Please call " + PHONE_DISPLAY + " or message us on WhatsApp.";
      submitBtn.disabled = false;
      submitBtn.textContent = submitLabel;
    });
  });
})();
