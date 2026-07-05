/* ============================================================
   Content Architecture & Routing System
   Structural framework for multi-page expansion
   ============================================================ */

/**
 * Service pages routing array
 * Prepare clean URL paths for location-based and specialized service pages
 */
const SERVICE_ROUTES = [
  // Location-based services (Ottawa neighborhoods)
  {
    path: "/services/in-home-ottawa",
    title: "In-Home Physiotherapy in Ottawa",
    description: "Virtual Physio brings physiotherapy directly to your home across Ottawa",
    category: "location",
    featured: true
  },
  {
    path: "/services/kanata",
    title: "Physiotherapy in Kanata",
    description: "In-home and virtual care serving Kanata residents",
    category: "location"
  },
  {
    path: "/services/barrhaven",
    title: "Physiotherapy in Barrhaven",
    description: "Local physiotherapy support for Barrhaven and surrounding areas",
    category: "location"
  },
  {
    path: "/services/orleans",
    title: "Physiotherapy in Orleans",
    description: "Accessible in-home and virtual physiotherapy in Orleans",
    category: "location"
  },
  {
    path: "/services/nepean",
    title: "Physiotherapy in Nepean",
    description: "In-home treatment and virtual care in Nepean",
    category: "location"
  },
  {
    path: "/services/stittsville",
    title: "Physiotherapy in Stittsville",
    description: "Professional physiotherapy services for Stittsville",
    category: "location"
  },
  {
    path: "/services/mobile-ottawa",
    title: "Mobile Physiotherapy Service in Ottawa",
    description: "On-demand in-home physiotherapy appointments across Ottawa",
    category: "location",
    featured: true
  },

  // Specialized condition services
  {
    path: "/services/vestibular",
    title: "Vestibular Rehabilitation Ottawa",
    description: "Expert treatment for dizziness, vertigo and balance disorders",
    category: "specialty",
    featured: true
  },
  {
    path: "/services/pelvic-floor",
    title: "Pelvic Floor Physiotherapy",
    description: "Specialized care for pelvic floor dysfunction and women's health",
    category: "specialty",
    featured: true
  },
  {
    path: "/services/tmj",
    title: "TMJ Physiotherapy & Jaw Pain Treatment",
    description: "Effective treatment for temporomandibular joint disorders",
    category: "specialty"
  },
  {
    path: "/services/post-surgical",
    title: "Post-Surgical Rehabilitation",
    description: "Evidence-based recovery after orthopedic procedures",
    category: "specialty"
  },
  {
    path: "/services/sports-injury",
    title: "Sports Injury Physiotherapy",
    description: "Return-to-sport rehabilitation and athletic performance optimization",
    category: "specialty"
  },
  {
    path: "/services/virtual-physiotherapy",
    title: "Virtual Physiotherapy",
    description: "Online physiotherapy appointments from home",
    category: "specialty"
  }
];

/**
 * Success stories / Case studies template structure
 * Initialize with example – easily expandable
 */
const CASE_STUDIES = [
  {
    id: 1,
    slug: "ottawa-senior-balance-recovery",
    title: "How an Ottawa Senior Improved Balance and Reduced Falls",
    problem: "76-year-old Margaret was experiencing frequent dizziness and near-falls, limiting her independence and causing anxiety about daily activities.",
    approach: [
      "Comprehensive vestibular assessment in home environment",
      "Customized balance training protocol with Cawthorne-Cooksey exercises",
      "Fall risk assessment and home safety modifications",
      "Progressive strengthening focused on leg stability"
    ],
    outcome: {
      improvement: "Zero falls over 3 months",
      confidence: "Returned to independent grocery shopping and social activities",
      timeline: "12 weeks of bi-weekly in-home sessions"
    },
    testimonial: "I feel confident walking again. Virtual Physio gave me my independence back.",
    patientName: "Margaret, 76"
  },
  {
    id: 2,
    slug: "postpartum-core-recovery",
    title: "Postpartum Core Recovery: From Diastasis Recti to Strength",
    problem: "New mother struggled with core weakness, pelvic floor dysfunction and 3-finger diastasis recti separation.",
    approach: [
      "Pelvic floor assessment and targeted pelvic floor rehabilitation",
      "Progressive core activation sequence avoiding traditional sit-ups",
      "Functional movement integration for daily demands",
      "Education on breathing and load management"
    ],
    outcome: {
      improvement: "2-finger diastasis recti closure, return to exercise",
      confidence: "Able to lift toddler and manage daily activities pain-free",
      timeline: "16 weeks of virtual and in-home sessions"
    },
    testimonial: "I didn't think I'd feel strong again. This program was exactly what I needed.",
    patientName: "Sarah, 32"
  }
];

/**
 * Resource Hub – Pain point topics and content paths
 * Maps patient search intents to content for organic discovery
 */
const RESOURCE_HUB_TOPICS = [
  {
    category: "Pain Management",
    subtopics: [
      { topic: "Back pain", path: "/resources/back-pain", priority: "high" },
      { topic: "Neck pain", path: "/resources/neck-pain", priority: "high" },
      { topic: "Sciatica", path: "/resources/sciatica", priority: "high" },
      { topic: "Chronic pain", path: "/resources/chronic-pain", priority: "medium" }
    ]
  },
  {
    category: "Specialized Conditions",
    subtopics: [
      { topic: "Vertigo", path: "/resources/vertigo", priority: "high" },
      { topic: "Sports injuries", path: "/resources/sports-injuries", priority: "high" },
      { topic: "Pelvic health", path: "/resources/pelvic-health", priority: "high" },
      { topic: "TMJ disorders", path: "/resources/tmj-disorders", priority: "medium" }
    ]
  },
  {
    category: "Recovery & Rehabilitation",
    subtopics: [
      { topic: "Post-surgical rehabilitation", path: "/resources/post-surgical", priority: "high" },
      { topic: "Home physiotherapy", path: "/resources/home-physiotherapy", priority: "high" },
      { topic: "Virtual physiotherapy", path: "/resources/virtual-physiotherapy", priority: "medium" },
      { topic: "Exercise recovery", path: "/resources/exercise-recovery", priority: "medium" }
    ]
  }
];

/**
 * Navigation helper: Get featured services
 */
function getFeaturedServices() {
  return SERVICE_ROUTES.filter(route => route.featured);
}

/**
 * Navigation helper: Get services by category
 */
function getServicesByCategory(category) {
  return SERVICE_ROUTES.filter(route => route.category === category);
}

/**
 * Render resource hub filter tabs
 * Creates interactive content discovery interface
 */
function renderResourceHubTabs(containerId = ".resource-hub-container") {
  const container = document.querySelector(containerId);
  if (!container) return;

  const tabHTML = `
    <div class="resource-hub">
      <div class="resource-tabs">
        ${RESOURCE_HUB_TOPICS.map((cat, idx) => `
          <button class="resource-tab ${idx === 0 ? "active" : ""}" data-category="${cat.category}">
            ${cat.category}
          </button>
        `).join("")}
      </div>
      <div class="resource-content">
        ${RESOURCE_HUB_TOPICS.map((cat, idx) => `
          <div class="resource-category ${idx === 0 ? "active" : ""}" data-category="${cat.category}">
            <ul class="resource-list">
              ${cat.subtopics.map(sub => `
                <li class="resource-item priority-${sub.priority}">
                  <a href="${sub.path}">${sub.topic}</a>
                  <span class="priority-badge">${sub.priority}</span>
                </li>
              `).join("")}
            </ul>
          </div>
        `).join("")}
      </div>
    </div>
  `;

  container.innerHTML = tabHTML;

  // Attach event listeners
  document.querySelectorAll(".resource-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      const category = tab.dataset.category;
      
      // Update active tab
      document.querySelectorAll(".resource-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      
      // Update active content
      document.querySelectorAll(".resource-category").forEach(cat => cat.classList.remove("active"));
      document.querySelector(`[data-category="${category}"]`).classList.add("active");
    });
  });
}

/**
 * Generate case study card grid
 */
function renderCaseStudies(containerId = ".case-studies-grid") {
  const container = document.querySelector(containerId);
  if (!container) return;

  container.innerHTML = CASE_STUDIES.map(study => `
    <article class="case-study-card" data-study-slug="${study.slug}">
      <h3>${study.title}</h3>
      <div class="case-study-flow">
        <div class="flow-step">
          <strong>Problem</strong>
          <p>${study.problem}</p>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-step">
          <strong>Outcome</strong>
          <p>${study.outcome.improvement}</p>
        </div>
      </div>
      <blockquote class="case-study-testimonial">
        "${study.testimonial}"
        <footer>— ${study.patientName}</footer>
      </blockquote>
      <a href="#" class="read-more">Read Full Case Study →</a>
    </article>
  `).join("");

  // Add click handlers
  document.querySelectorAll(".case-study-card").forEach(card => {
    card.addEventListener("click", () => {
      const slug = card.dataset.studySlug;
      showCaseStudyDetail(slug);
    });
  });
}

/**
 * Show detailed case study view
 */
function showCaseStudyDetail(slug) {
  const study = CASE_STUDIES.find(s => s.slug === slug);
  if (!study) return;

  // TODO: Implement modal view similar to blog articles
  console.log("Case study detail:", study);
}

// Export for use in other modules
if (typeof window !== "undefined") {
  window.serviceRoutes = SERVICE_ROUTES;
  window.caseStudies = CASE_STUDIES;
  window.resourceHubTopics = RESOURCE_HUB_TOPICS;
  window.renderResourceHubTabs = renderResourceHubTabs;
  window.renderCaseStudies = renderCaseStudies;
  window.getFeaturedServices = getFeaturedServices;
  window.getServicesByCategory = getServicesByCategory;
}
