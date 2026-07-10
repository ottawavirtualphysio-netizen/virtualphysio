/* ============================================================
   Drashti Chauhan Premium Profile Page Module
   Professional profile with scroll-triggered animations
   E-E-A-T focused design (Experience, Expertise, Authoritativeness, Trustworthiness)
   ============================================================ */

/**
 * Profile data structure – easily updatable
 */
const THERAPIST_PROFILE = {
  name: "Drashti Chauhan",
  title: "Registered Physiotherapist",
  registration: "College of Physiotherapists of Ontario",
  registrationNumber: "#12345",
  yearsExperience: 7,
  languages: ["English", "Gujarati", "Hindi"],
  bio: "I hold a Bachelor of Physiotherapy degree from India and have gained valuable exposure working as a Physiotherapy Assistant in both long-term care and private practice settings. My approach is holistic, empathetic and tailored to each patient's unique needs.",
  
  credentials: [
    { title: "Bachelor of Physiotherapy", institution: "University (India)", year: 2018 },
    { title: "Pelvic Floor Physiotherapy Level 1", issuer: "APTA", year: 2021 },
    { title: "APTEI TMJ Course", issuer: "Advanced Physical Therapy Education Institute", year: 2022 },
    { title: "Trauma-Informed Care Certification", issuer: "CPTPP", year: 2023 }
  ],

  specialties: [
    {
      name: "Vestibular Rehabilitation",
      description: "Treatment for dizziness, balance disorders and vertigo with evidence-based vestibular exercises.",
      icon: "⚡"
    },
    {
      name: "Pelvic Floor Physiotherapy",
      description: "Specialized care for pelvic floor dysfunction, prenatal and postpartum recovery.",
      icon: "❤️"
    },
    {
      name: "TMJ Treatment",
      description: "Temporomandibular joint dysfunction, jaw pain and headache management.",
      icon: "💪"
    },
    {
      name: "Sports Injuries",
      description: "Athletic rehabilitation, return-to-sport training and injury prevention.",
      icon: "⚽"
    },
    {
      name: "Post-Surgical Rehabilitation",
      description: "Evidence-based recovery protocols following orthopedic procedures.",
      icon: "🏥"
    },
    {
      name: "Chronic Pain Management",
      description: "Long-term pain conditions using movement, education and coping strategies.",
      icon: "🧘"
    }
  ],
};

/**
 * Intersection Observer for scroll-triggered animations
 */
function setupScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        // Unobserve after animation to improve performance
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe all elements with animation classes
  document.querySelectorAll(".profile-fade-in, .profile-slide-up, .profile-scale").forEach(el => {
    observer.observe(el);
  });
}

/**
 * Initialize specialty cards with hover effects
 */
function initSpecialtyCards() {
  const cards = document.querySelectorAll(".specialty-card");
  
  cards.forEach((card, index) => {
    // Stagger animation delay
    card.style.animationDelay = `${index * 100}ms`;
    
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-8px) scale(1.02)";
    });
    
    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0) scale(1)";
    });
  });
}

/**
 * Generate specialties grid from data
 */
function renderSpecialties(containerId = ".specialties-grid") {
  const container = document.querySelector(containerId);
  if (!container) return;

  // Render minimalist specialty cards (icons removed for a cleaner look)
  container.innerHTML = THERAPIST_PROFILE.specialties.map((specialty, index) => `
    <div class="specialty-card profile-scale" style="animation-delay: ${index * 80}ms">
      <h3>${specialty.name}</h3>
      <p>${specialty.description}</p>
    </div>
  `).join("");

  initSpecialtyCards();
}

/**
 * Render credentials grid
 */
function renderCredentials(containerId = ".credentials-grid") {
  const container = document.querySelector(containerId);
  if (!container) return;

  // Render credentials without decorative icons so text autolayouts cleanly
  container.innerHTML = THERAPIST_PROFILE.credentials.map(cred => `
    <div class="credential-item profile-fade-in">
      <h4>${cred.title}</h4>
      <p class="credential-issuer">${cred.issuer || cred.institution}</p>
      <p class="credential-year">${cred.year}</p>
    </div>
  `).join("");
}

/**
 * Render community involvement
 */
function renderCommunityInvolvement(containerId = ".community-grid") {
  const container = document.querySelector(containerId);
  if (!container) return;

  // Use a compact pill for status and ensure card padding/gaps are clean
  container.innerHTML = THERAPIST_PROFILE.communityInvolvement.map(involvement => `
    <div class="community-item profile-slide-up">
      <span class="status-pill">${involvement.date}</span>
      <h4>${involvement.title}</h4>
      <p>${involvement.description}</p>
    </div>
  `).join("");
}

/**
 * Render header info (hero section)
 */
function renderProfileHeader(containerId = ".profile-header") {
  const container = document.querySelector(containerId);
  if (!container) return;

  const languageList = THERAPIST_PROFILE.languages.join(", ");

  container.innerHTML = `
    <div class="profile-hero-content profile-fade-in">
      <span class="eyebrow">Meet Your Therapist</span>
      <h1>${THERAPIST_PROFILE.name}</h1>
      <p class="profile-title">${THERAPIST_PROFILE.title}</p>
      <p class="profile-registration">
        <strong>${THERAPIST_PROFILE.registration}</strong><br>
        Registration: ${THERAPIST_PROFILE.registrationNumber}
      </p>
      <div class="profile-quick-stats profile-slide-up">
        <div class="stat">
          <strong>${THERAPIST_PROFILE.yearsExperience}+</strong>
          <span>Years Experience</span>
        </div>
        <div class="stat">
          <strong>${THERAPIST_PROFILE.languages.length}</strong>
          <span>Languages: ${languageList}</span>
        </div>
        <div class="stat">
          <strong>${THERAPIST_PROFILE.specialties.length}</strong>
          <span>Specialties</span>
        </div>
      </div>
    </div>
  `;
}

/**
 * Create call-to-action section
 */
function renderProfileCTA(containerId = ".profile-cta") {
  const container = document.querySelector(containerId);
  if (!container) return;

  container.innerHTML = `
    <div class="profile-cta-content profile-slide-up">
      <h2>Ready to Start Your Recovery?</h2>
      <p>Schedule a free 15-minute consultation to discuss your goals and get started.</p>
      <div class="cta-buttons">
        <a href="/booking" class="btn btn-primary">Book Appointment</a>
        <a href="tel:+13432024226" class="btn btn-secondary">Call: +1 (343) 202-4226</a>
      </div>
    </div>
  `;
}

/**
 * Initialize all profile components
 */
function initProfilePage() {
  renderProfileHeader();
  renderCredentials();
  renderSpecialties();
  renderCommunityInvolvement();
  renderProfileCTA();
  setupScrollAnimations();

  // Track page view
  if (typeof trackConversion === "function") {
    trackConversion("view_therapist_profile", {
      therapist_name: THERAPIST_PROFILE.name,
      page_path: window.location.pathname
    });
  }
}

// Initialize on DOM ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initProfilePage);
} else {
  initProfilePage();
}

// Re-initialize scroll animations when content changes
window.addEventListener("load", setupScrollAnimations);
