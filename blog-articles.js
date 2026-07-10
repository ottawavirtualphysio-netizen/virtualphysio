/* ============================================================
   Blog Articles Module – Dynamic routing and article rendering
   Handles blog card clicks → article view with distraction-free reading
   ============================================================ */

/**
 * Article data store – structured for SEO and dynamic routing
 * Each article has: id, slug, title, category, excerpt, readTime, content
 */
const BLOG_ARTICLES = [
  {
    id: 1,
    slug: "in-home-physiotherapy-ottawa",
    title: "In-Home Physiotherapy in Ottawa: Who Benefits Most?",
    category: "In-Home Care",
    excerpt: "Learn who can benefit most from in-home physiotherapy, what to expect during your first appointment, and how to get started.",
    readTime: "7 min read",
    date: "2024-01-15",
    author: "Drashti Chauhan",
    content: `
<div class="prose-article">
  <h2>What Is In-Home Physiotherapy?</h2>
  <p>In-home physiotherapy is an evidence-based treatment approach delivered directly at a patient's residence, rather than in a clinic. This service is designed for individuals who face barriers to attending appointments—whether due to mobility limitations, transportation challenges, chronic pain, recovery from surgery, or simply preference for receiving care in their familiar environment.</p>
  <p>At Virtual Physio, we bring our full therapeutic toolkit to your home: assessment, exercise prescription, postural correction, manual therapy, education and ongoing progress monitoring. The treatment plan is tailored to your specific needs, living space and recovery goals.</p>

  <h2>Who Can Benefit Most from In-Home Physiotherapy?</h2>
  <p>In-home physiotherapy is particularly effective for:</p>
  <ul>
    <li><strong>Seniors and older adults:</strong> Those with balance challenges, fall risk or limited mobility who need accessible care.</li>
    <li><strong>Post-surgical patients:</strong> Individuals recovering from joint replacement, spinal surgery or other procedures during the critical early recovery window.</li>
    <li><strong>Chronic pain sufferers:</strong> People managing long-term conditions like osteoarthritis or fibromyalgia who benefit from personalized home exercise programming.</li>
    <li><strong>Mobility-limited individuals:</strong> Those with severe pain, temporary disability or limited transportation access.</li>
    <li><strong>Home-based workers:</strong> Professionals who prefer integrating physiotherapy seamlessly into their home schedule.</li>
    <li><strong>Prenatal and postpartum patients:</strong> Women seeking specialized pelvic floor and core recovery support in a private, comfortable setting.</li>
    <li><strong>Sports injury recovery:</strong> Athletes recovering from injury who want sport-specific rehabilitation in a familiar environment.</li>
  </ul>

  <h2>Key Advantages of In-Home Treatment</h2>
  <ul>
    <li><strong>Accessibility:</strong> No travel, parking or waiting room—care comes to you.</li>
    <li><strong>Real-world environment:</strong> Therapists can assess how you move in your actual living space and modify exercises for safety.</li>
    <li><strong>Comfort and privacy:</strong> Receive treatment in your familiar, private setting.</li>
    <li><strong>Family involvement:</strong> Loved ones can learn exercises and support your recovery.</li>
    <li><strong>Reduced infection risk:</strong> Single-patient environment minimizes exposure.</li>
    <li><strong>Continuity:</strong> Treatment can begin immediately, especially important for post-surgical cases.</li>
  </ul>

  <h2>When Is In-Home Physiotherapy Right for You?</h2>
  <p>Consider in-home treatment if you:</p>
  <ul>
    <li>Are recovering from recent surgery or acute injury</li>
    <li>Experience significant pain with movement or travel</li>
    <li>Have mobility limitations or balance concerns</li>
    <li>Lack reliable transportation to a clinic</li>
    <li>Prefer privacy during treatment</li>
    <li>Want family members present for education and support</li>
    <li>Need home-specific adaptations or safety modifications</li>
  </ul>

  <h2>What to Expect During Your First In-Home Visit</h2>
  <p>Your first appointment typically follows a structured five-step process:</p>

  <h3>1. Initial Assessment and Goal Setting (15-20 minutes)</h3>
  <p>Your physiotherapist will conduct a detailed interview about your medical history, current symptoms, pain patterns and functional limitations. You'll discuss your recovery goals and lifestyle factors. This conversation helps us understand what matters most to you and tailor the treatment accordingly.</p>

  <h3>2. Physical Examination and Movement Screening (15-20 minutes)</h3>
  <p>We'll perform a thorough physical assessment including posture analysis, range of motion testing, strength evaluation and functional movement screening. This might include simple tests like standing up from a chair, walking across your room or balance assessments. These tests reveal what's contributing to your symptoms and guide our treatment approach.</p>

  <h3>3. Home Environment Review and Safety Planning (10 minutes)</h3>
  <p>Your therapist will walk through your home to identify fall hazards, accessibility barriers and safe spaces for exercise. We'll note handrails, floor conditions, furniture placement and lighting. This assessment ensures your home environment supports safe recovery and helps us prescribe exercises that work in your actual living space.</p>

  <h3>4. Treatment and Exercise Introduction (20-25 minutes)</h3>
  <p>Based on the assessment findings, we'll perform evidence-based treatments which may include hands-on manual therapy, corrective exercise instruction and movement education. You'll learn specific exercises tailored to your condition, and we'll practice them together to ensure proper form and safety. Family members are welcome to observe and learn.</p>

  <h3>5. Home Exercise Program Planning and Follow-Up Scheduling (10 minutes)</h3>
  <p>Before we leave, you'll receive a personalized home exercise program with clear, written instructions or video demonstrations. We'll discuss expected recovery timelines, precautions to follow and when to call with concerns. Your next appointment will be scheduled based on your condition and recovery goals.</p>

  <h2>Typical Frequency and Duration</h2>
  <p>Most patients start with 2-3 visits per week for 2-4 weeks, then transition to weekly visits as they progress. Treatment length varies by condition—acute post-surgical cases may require 4-8 weeks of intensive support, while chronic pain management might involve ongoing monthly maintenance visits. We'll adjust frequency based on your progress and functional goals.</p>

  <h2>Cost and Coverage</h2>
  <p>In-home physiotherapy is often covered by private health insurance plans and extended health benefits. Some plans may have specific requirements or limits. We recommend verifying your coverage before your first appointment. At Virtual Physio, we provide detailed invoicing to support insurance claims.</p>

  <h2>Is Virtual Physiotherapy an Alternative?</h2>
  <p>For some patients, virtual physiotherapy is an excellent option—particularly for ongoing exercise coaching, check-ins and follow-up support. However, virtual care requires you to be able to move safely independently and have appropriate home space. In-home in-person treatment is better for initial hands-on assessment, manual therapy and detailed movement correction in your actual environment.</p>

  <h2>Getting Started with In-Home Physiotherapy in Ottawa</h2>
  <p>Ready to explore whether in-home physiotherapy is right for you? Contact Virtual Physio to schedule your initial consultation. We'll discuss your specific situation, answer your questions and create a plan that fits your recovery goals and lifestyle.</p>

  <div class="article-cta">
    <p><strong>Have questions about in-home physiotherapy?</strong></p>
    <p>Call us at +1 (343) 202-4226 or book a free 15-minute consultation.</p>
    <a href="/booking" class="cta-button">Schedule Your Assessment</a>
  </div>
</div>
    `
  },
  {
    id: 2,
    slug: "post-surgery-rehabilitation-timeline",
    title: "Post-Surgery Rehabilitation Timeline: What Patients Should Expect",
    category: "Rehabilitation",
    excerpt: "A detailed guide to the post-surgical recovery phases, milestones and what to expect at each stage of rehabilitation.",
    readTime: "8 min read",
    date: "2024-02-10",
    author: "Drashti Chauhan",
    content: `
<div class="prose-article">
  <p>Post-surgical rehabilitation is not one-size-fits-all, but understanding the general phases helps set realistic expectations and keep you motivated through recovery. Below is a framework for most orthopedic surgeries (joint replacement, ACL reconstruction, rotator cuff repair, etc.) with typical timelines.</p>
  
  <h2>Phase 1: Immediate Post-Operative (0–2 Weeks)</h2>
  <p><strong>Goals:</strong> Protect the surgical site, manage swelling, prevent complications, begin gentle movement.</p>
  <p><strong>What happens:</strong> Expect pain, swelling, limited motion and fatigue. You may be in a sling, cast or immobilizer. Your physiotherapist will teach you gentle range-of-motion exercises, proper positioning and swelling management strategies.</p>
  <p><strong>Red flags:</strong> Sudden increased pain, fever, excessive bleeding or signs of infection warrant immediate medical attention.</p>

  <h2>Phase 2: Early Mobilization (Weeks 2–6)</h2>
  <p><strong>Goals:</strong> Restore pain-free range of motion, improve strength, reduce swelling.</p>
  <p><strong>What happens:</strong> Gradual progression of exercises. Pain begins decreasing. You may start light functional activities (like walking or gentle gripping). Swelling should steadily improve with consistent treatment and home exercise compliance.</p>

  <h2>Phase 3: Intermediate Strengthening (Weeks 6–12)</h2>
  <p><strong>Goals:</strong> Build muscle strength, improve endurance, restore normal movement patterns.</p>
  <p><strong>What happens:</strong> Resistance exercises are introduced. Walking or cardiovascular activity increases. You might begin sport-specific or activity-specific training. Most people return to light duties at work during this phase.</p>

  <h2>Phase 4: Advanced Strengthening & Return to Function (Weeks 12–26)</h2>
  <p><strong>Goals:</strong> Return to pre-injury activity level, prevent re-injury.</p>
  <p><strong>What happens:</strong> Progressive sports training, plyometrics, heavy load tolerance. Most competitive athletes return to sport in this phase, though individual variation is significant.</p>

  <h2>Long-Term Management (Beyond 6 Months)</h2>
  <p><strong>Goals:</strong> Maintain strength, prevent chronic pain, support independence.</p>
  <p><strong>What happens:</strong> Gradual discharge from physiotherapy with a long-term maintenance exercise program. Regular activity and strength work prevent re-injury and future complications.</p>

  <div class="article-cta">
    <a href="/booking" class="cta-button">Book Your Rehabilitation Consultation</a>
  </div>
</div>
    `
  },
  {
    id: 3,
    slug: "sports-injury-prevention",
    title: "Sports Injury Prevention Tips for Weekend Athletes",
    category: "Sports Injury",
    excerpt: "Evidence-based strategies to prevent sports injuries, including warm-up protocols, load management and movement screening.",
    readTime: "6 min read",
    date: "2024-02-15",
    author: "Drashti Chauhan",
    content: `
<div class="prose-article">
  <p>Weekend athletes are at particular risk for sports injuries due to the stop-start nature of recreational activity. Here are key prevention strategies to keep you active safely.</p>
  
  <h2>The 80/20 Rule: Consistency Over Intensity</h2>
  <p>Many weekend injuries occur when athletes push too hard too fast. Aim for consistent, moderate activity throughout the week rather than "saving it all for the weekend." A short 30-minute walk on Monday, Wednesday and Friday reduces injury risk far more than a single aggressive Saturday game.</p>

  <h2>Dynamic Warm-Up Protocol (Before Sport)</h2>
  <ul>
    <li>5 minutes easy cardio (light jogging, cycling)</li>
    <li>Dynamic stretching: leg swings, arm circles, walking lunges</li>
    <li>Sport-specific movements: practice shots, easy passes, graduated intensity</li>
    <li>Mental preparation: visualize successful movement</li>
  </ul>

  <div class="article-cta">
    <a href="/booking" class="cta-button">Get a Sport-Specific Injury Prevention Plan</a>
  </div>
</div>
    `
  }
];

/**
 * Initialize blog article system
 * Attaches event listeners to blog cards for dynamic article viewing
 */
function handleBlogArticleCloseClick(event) {
  const closeButton = event.target.closest(".article-close, [data-back-to-blog]");
  const clickedBackdrop = event.target.classList.contains("article-backdrop");

  if (closeButton || clickedBackdrop) {
    closeArticleView();
  }
}

function handleBlogArticleKeydown(event) {
  if (event.key === "Escape" && document.querySelector(".article-modal.is-open")) {
    closeArticleView();
  }
}

function initBlogArticles() {
  const blogCards = document.querySelectorAll(".blog-card[data-article-slug]");

  blogCards.forEach(card => {
    card.style.cursor = "pointer";
    card.addEventListener("click", (e) => {
      const readLink = e.target.closest("a[data-slot='read-button']");
      if (readLink) {
        e.preventDefault();
      }

      const slug = card.dataset.articleSlug;
      const article = BLOG_ARTICLES.find(a => a.slug === slug);

      if (article) {
        showArticleView(article);
      }
    });
  });

  document.removeEventListener("click", handleBlogArticleCloseClick);
  document.addEventListener("click", handleBlogArticleCloseClick);
  document.removeEventListener("keydown", handleBlogArticleKeydown);
  document.addEventListener("keydown", handleBlogArticleKeydown);
}

/**
 * Display full article in modal view
 */
function showArticleView(article) {
  let modal = document.querySelector(".article-modal");
  
  if (!modal) {
    modal = document.createElement("div");
    modal.className = "article-modal";
    document.body.appendChild(modal);
  }

  const formattedDate = new Date(article.date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric"
  });

  modal.innerHTML = `
    <div class="article-backdrop"></div>
    <div class="article-container">
      <div class="article-header">
        <button class="article-close" aria-label="Close article" data-back-to-blog>
          ← Back to Blog
        </button>
      </div>
      <article class="article-content">
        <div class="article-meta">
          <span class="category">${article.category}</span>
          <time datetime="${article.date}">${formattedDate}</time>
          <span class="meta-sep" aria-hidden="true">•</span>
          <span class="read-time">${article.readTime}</span>
        </div>
        <h1>${article.title}</h1>
        <p class="article-excerpt">${article.excerpt}</p>
        <div class="divider"></div>
        ${article.content}
      </article>
    </div>
  `;

  modal.classList.add("is-open");
  document.body.style.overflow = "hidden";

  // Scroll to top
  modal.querySelector(".article-container").scrollTop = 0;

  // Track event
  if (typeof trackConversion === "function") {
    trackConversion("blog_article_opened", {
      article_title: article.title,
      article_slug: article.slug
    });
  }
}

/**
 * Close article modal view
 */
function closeArticleView() {
  const modal = document.querySelector(".article-modal");
  if (modal) {
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
    
    // Optional: remove modal after animation
    setTimeout(() => {
      if (modal && !modal.classList.contains("is-open")) {
        modal.remove();
      }
    }, 300);
  }
}

/**
 * Generate blog grid dynamically with clickable cards
 * Useful for updating blog.html with dynamic articles
 */
function renderBlogGrid(containerId = ".blog-grid", articlesToShow = 3) {
  const container = document.querySelector(containerId);
  if (!container) return;

  const articles = BLOG_ARTICLES.slice(0, articlesToShow);
  
  container.innerHTML = articles.map((article, index) => `
    <article class="blog-card reveal${index > 0 ? ` delay-${Math.min(index, 2)}` : ""}" data-article-slug="${article.slug}">
      <span>${article.category}</span>
      <h3>${article.title}</h3>
      <p>${article.excerpt}</p>
      <div class="card-footer">
        <small>${article.readTime} • ${article.date}</small>
      </div>
      <a href="#" data-slot="read-button">Read Full Article</a>
    </article>
  `).join("");

  // Re-initialize article system
  initBlogArticles();
}

// Initialize on DOM ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initBlogArticles);
} else {
  initBlogArticles();
}
