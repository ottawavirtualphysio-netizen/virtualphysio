# Virtual Physio.ca – Modular Features Implementation Guide

## Overview

This document explains the new modular systems integrated into Virtual Physio.ca for dynamic blog articles, enhanced physiotherapist profile, and content architecture expansion.

## 🎯 Modules Overview

### 1. **Blog Articles System** (`blog-articles.js` + `blog-articles.css`)

Provides dynamic, distraction-free article reading experience with smooth transitions.

#### Features:
- ✅ Click blog cards to open full-article modal
- ✅ Beautifully typeset prose layout with Tailwind-like spacing
- ✅ Smooth fade-in animations
- ✅ Keyboard support (ESC to close)
- ✅ Google Analytics tracking

#### File Structure:
```
blog-articles.js       // Core logic, article data, event handlers
blog-articles.css      // Article modal styling, animations
blog.html              // Updated with blog-articles.css + script
```

#### How to Use:

**Add Article to the System:**

Edit `blog-articles.js` and add to `BLOG_ARTICLES` array:

```javascript
{
  id: 4,
  slug: "your-article-slug",
  title: "Your Article Title",
  category: "Your Category",
  excerpt: "Short excerpt for card preview",
  readTime: "6 min read",
  date: "2024-03-20",
  author: "Drashti Chauhan",
  content: `
<div class="prose-article">
  <h2>Main Section</h2>
  <p>Your article content here...</p>
</div>
  `
}
```

**Add Clickable Blog Card to HTML:**

```html
<article class="blog-card reveal" data-article-slug="your-article-slug">
  <span>Your Category</span>
  <h3>Your Article Title</h3>
  <p>Your excerpt</p>
  <a href="#" data-slot="read-button">Read Full Article</a>
</article>
```

#### Styling Available:
- `.prose-article` – Main article container
- `h2`, `h3` – Typography hierarchy
- `.article-cta` – Call-to-action box styling
- All uses standard color tokens from `style.css`

---

### 2. **Premium Profile Page** (`profile-page.js` + `profile-page.css`)

Renders Drashti Chauhan's comprehensive professional profile with scroll animations.

#### Features:
- ✅ Hero section with professional info & quick stats
- ✅ Scroll-triggered fade-in animations
- ✅ Credentials grid with certifications
- ✅ Interactive specialty cards
- ✅ Community involvement timeline
- ✅ High-converting CTA section
- ✅ Fully responsive design

#### File Structure:
```
profile-page.js       // Profile data structure, rendering logic
profile-page.css      // Professional styling with animations
about.html            // Updated with profile-page.css + script
```

#### How to Update Profile Data:

Edit the `THERAPIST_PROFILE` object in `profile-page.js`:

```javascript
const THERAPIST_PROFILE = {
  name: "Drashti Chauhan",
  title: "Registered Physiotherapist",
  registration: "College of Physiotherapists of Ontario",
  registrationNumber: "#12345",
  yearsExperience: 7,
  languages: ["English", "Gujarati", "Hindi"],
  
  credentials: [
    { title: "Degree Title", institution: "University", year: 2018 },
    // ... more credentials
  ],
  
  specialties: [
    {
      name: "Specialty Name",
      description: "Description",
      icon: "❤️"  // Use emoji or Unicode
    },
    // ... more specialties
  ],
  
  communityInvolvement: [
    { title: "Activity", description: "Description", date: "Ongoing" },
    // ... more activities
  ]
};
```

#### Rendering Functions:

The module automatically populates these containers on `about.html`:

- `.profile-header` – Main introduction section
- `.credentials-grid` – Education & certifications
- `.specialties-grid` – Areas of expertise
- `.community-grid` – Community involvement
- `.profile-cta` – Call-to-action section

---

### 3. **Content Routing & Architecture** (`content-routing.js` + `content-routing.css`)

Provides structured arrays and rendering functions for multi-page expansion.

#### Features:
- ✅ Service routing paths (locations + specialties)
- ✅ Case study template structure
- ✅ Resource hub topic organization
- ✅ Helper functions for navigation

#### File Structure:
```
content-routing.js      // Data arrays, rendering functions
content-routing.css     // Grid layouts, styling for resource hub
```

#### Available Data Structures:

**1. SERVICE_ROUTES** – 13 predefined service pages

```javascript
// Access featured services:
getFeaturedServices()  // Returns featured services only

// Get services by category:
getServicesByCategory("location")    // All location-based services
getServicesByCategory("specialty")   // All specialty services

// Direct access:
window.serviceRoutes
```

**2. CASE_STUDIES** – Success story templates

```javascript
{
  id: 1,
  slug: "case-study-slug",
  title: "Case Study Title",
  problem: "Patient problem description",
  approach: ["Step 1", "Step 2", ...],
  outcome: {
    improvement: "Results",
    confidence: "Patient quote",
    timeline: "Duration"
  },
  testimonial: "Patient testimonial",
  patientName: "Name, Age"
}
```

**3. RESOURCE_HUB_TOPICS** – Content discovery structure

```javascript
// Organized by:
// - Pain Management
// - Specialized Conditions
// - Recovery & Rehabilitation
// Each with priority levels (high/medium)
```

#### Rendering Functions:

```javascript
// Generate resource hub filter tabs
renderResourceHubTabs(".resource-hub-container")

// Render case study grid
renderCaseStudies(".case-studies-grid")

// Get featured services for homepage
getFeaturedServices()

// Get services by category
getServicesByCategory("location")
```

---

## 📦 Installation & Setup

### Step 1: Verify File Locations

All new files should be in your root directory:
```
├── blog-articles.js
├── blog-articles.css
├── profile-page.js
├── profile-page.css
├── content-routing.js
├── content-routing.css
├── blog.html (updated)
├── about.html (updated)
└── script.js (existing)
```

### Step 2: Verify HTML Links

**In `blog.html`:**
```html
<link rel="stylesheet" href="blog-articles.css">
<!-- ... existing content ... -->
<script src="blog-articles.js" defer></script>
```

**In `about.html`:**
```html
<link rel="stylesheet" href="profile-page.css">
<!-- ... existing content ... -->
<script src="profile-page.js" defer></script>
```

### Step 3: Test in Browser

1. Go to `/blog` → Click a blog card → Article should open in modal
2. Go to `/about` → Profile should render with animations
3. Open browser console → No JavaScript errors

---

## 🎨 Color & Styling Guide

All modules use existing CSS variables from `style.css`:

```css
--blue: #2E86DE              /* Primary action color */
--blue-dark: #1a6bbf         /* Darker variant */
--blue-light: #e8f4ff        /* Light background */
--green: #27AE60             /* Accent color */
--white: #ffffff             /* Text on colored backgrounds */
--ink: #0d2137               /* Primary text */
--ink-soft: #1e3a52          /* Secondary text */
--grey: #6b7c93              /* Muted text */
--bg: #F8FAFC                /* Page background */
--muted: #f5f9fc             /* Card backgrounds */
--line: #dce8f0              /* Borders */

/* Shadows */
--shadow-sm, --shadow-md, --shadow-lg, --shadow-blue

/* Spacing (assumed) */
--space-sm, --space-md, --space-lg, --space-xl

/* Transitions */
--transition: 240ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Extend Styling:

Each module's CSS is self-contained. To override:

```css
/* In your custom CSS file */
.article-container {
  /* Your overrides */
}

.specialty-card {
  /* Your overrides */
}
```

---

## 🚀 Advanced Usage

### Adding Blog Articles Programmatically:

```javascript
// Renders blog grid with first 3 articles
renderBlogGrid(".blog-grid", 3);

// Directly access article data
const article = BLOG_ARTICLES.find(a => a.slug === "in-home-physiotherapy-ottawa");
console.log(article.content);
```

### Tracking Events:

The modules automatically track events using your existing `trackConversion()` function:

```javascript
// Blog article opened
trackConversion("blog_article_opened", {
  article_title: "...",
  article_slug: "..."
});

// Therapist profile viewed
trackConversion("view_therapist_profile", {
  therapist_name: "Drashti Chauhan",
  page_path: "/about"
});
```

### Creating New Case Studies:

```javascript
// Add to CASE_STUDIES in content-routing.js
{
  id: 3,
  slug: "new-case-study",
  title: "Your Case Study Title",
  problem: "...",
  approach: ["...", "..."],
  outcome: { /* ... */ },
  testimonial: "...",
  patientName: "Name, Age"
}

// Render:
renderCaseStudies(".case-studies-grid");
```

---

## 📱 Responsive Breakpoints

All modules are fully responsive with breakpoints at:
- **Desktop**: 1024px+
- **Tablet**: 768px – 1023px
- **Mobile**: < 768px

### Mobile Considerations:

- Blog article modal: Full-width with padding
- Profile sections: Stack vertically
- Resource hub: Single column grid
- Case studies: Full-width cards

---

## 🔗 Integration Paths for Future Features

### Add to Services Page:

```html
<section class="service-routes-section">
  <h2>Our Service Locations & Specialties</h2>
  <div class="service-routes-grid">
    <!-- Will render from content-routing.js -->
  </div>
</section>

<script>
  // Render featured services
  const featured = getFeaturedServices();
  // Create cards from featured array
</script>
```

### Add Resource Hub to Homepage:

```html
<section class="resource-hub-section">
  <h2>The Ultimate Ottawa Physiotherapy Resource</h2>
  <div class="resource-hub-container"></div>
</section>

<script src="content-routing.js"></script>
<script>
  renderResourceHubTabs(".resource-hub-container");
</script>
```

### Add Case Studies Page:

```html
<section class="case-studies-section">
  <h2>Patient Success Stories</h2>
  <div class="case-studies-grid"></div>
</section>

<script src="content-routing.js"></script>
<script>
  renderCaseStudies(".case-studies-grid");
</script>
```

---

## ✅ Checklist for Production

- [ ] All 6 new files added to root directory
- [ ] `blog.html` includes `blog-articles.css` + `blog-articles.js`
- [ ] `about.html` includes `profile-page.css` + `profile-page.js`
- [ ] Tested blog article modal on desktop & mobile
- [ ] Tested profile page animations & scroll behavior
- [ ] Verified no console JavaScript errors
- [ ] Checked Google Analytics tracking fires
- [ ] Updated article data with correct author/dates
- [ ] Tested all internal links in articles work
- [ ] Updated profile credentials from Drashti's actual credentials

---

## 🐛 Troubleshooting

**Blog cards don't open articles:**
- Verify `data-article-slug` attribute matches article slug in `BLOG_ARTICLES`
- Check `blog-articles.js` is loading (DevTools > Network)
- Ensure blog card has class `.blog-card` and data attribute

**Profile sections not rendering:**
- Check `profile-page.js` loaded (DevTools > Network)
- Verify container selectors match exactly (`.profile-header`, `.credentials-grid`, etc.)
- Check browser console for errors

**Styling looks wrong:**
- Verify color tokens in `style.css` are defined
- Check CSS specificity – modular CSS might need `!important` for overrides
- Test in different browsers for vendor-specific issues

**Articles won't close:**
- Ensure ESC key handler is attached (`document.addEventListener("keydown", ...)`)
- Check backdrop click listener is working

---

## 📝 Content Updates

### To Add New Blog Article:

1. Edit `blog-articles.js`
2. Add entry to `BLOG_ARTICLES` array
3. Add corresponding blog card to `blog.html` with matching `data-article-slug`
4. Test article opens correctly

### To Update Therapist Profile:

1. Edit `profile-page.js`
2. Update `THERAPIST_PROFILE` object
3. Changes auto-render on page load
4. No HTML changes needed

### To Add Service Route:

1. Edit `content-routing.js`
2. Add entry to `SERVICE_ROUTES` array
3. Use `getServicesByCategory()` or `getFeaturedServices()` to display
4. Add corresponding HTML page at the URL path

---

## 🎓 Next Steps

1. **Verify everything works** – Test all three modules in browser
2. **Customize profile data** – Update Drashti's actual credentials
3. **Add more articles** – Expand blog with remaining topics from SEO plan
4. **Build service pages** – Create individual pages for each service route
5. **Add case studies** – Publish patient testimonials with the case study template
6. **Build resource hub** – Create mega-resource directory landing

---

**Questions?** Check the module comments in `blog-articles.js`, `profile-page.js`, and `content-routing.js` for detailed function documentation.

