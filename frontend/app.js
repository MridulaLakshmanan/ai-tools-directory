// AI Tools Directory JavaScript
const aiToolsData = {
  "aiTools": [
    {
      "id": 1,
      "name": "ChatGPT",
      "category": "AI Assistant",
      "description": "Advanced conversational AI that can help with writing, coding, analysis, and creative tasks using GPT-4 technology.",
      "rating": 4.8,
      "pricing": "Free / $20/month",
      "trending": true,
      "popularity": 95,
      "website": "https://chatgpt.com",
      "logo": "🤖",
      "reviews": [
        {"user": "Sarah K.", "rating": 5, "comment": "Absolutely game-changing for my workflow. The responses are incredibly human-like and helpful.", "sentiment": "positive"},
        {"user": "Mike R.", "rating": 4, "comment": "Great tool but sometimes gives outdated information. Still very useful overall.", "sentiment": "positive"},
        {"user": "Alex P.", "rating": 3, "comment": "Decent but can be repetitive. The free version has too many limitations.", "sentiment": "neutral"}
      ]
    },
    {
      "id": 2,
      "name": "Midjourney",
      "category": "Image Generation",
      "description": "Create stunning, artistic images from text prompts using advanced AI image generation technology.",
      "rating": 4.7,
      "pricing": "$10-60/month",
      "trending": true,
      "popularity": 88,
      "website": "https://midjourney.com",
      "logo": "🎨",
      "reviews": [
        {"user": "Emma L.", "rating": 5, "comment": "Mind-blowing image quality! Creates artwork better than I could ever imagine.", "sentiment": "positive"},
        {"user": "David T.", "rating": 4, "comment": "Amazing results but the Discord interface is a bit clunky to use.", "sentiment": "positive"}
      ]
    },
    {
      "id": 3,
      "name": "Cursor",
      "category": "Development",
      "description": "AI-powered code editor that helps developers write, edit, and debug code faster with intelligent suggestions.",
      "rating": 4.6,
      "pricing": "Free / $20/month",
      "trending": true,
      "popularity": 82,
      "website": "https://cursor.sh",
      "logo": "💻",
      "reviews": [
        {"user": "Jake M.", "rating": 5, "comment": "Revolutionary coding experience. It's like having a senior developer as a pair programmer.", "sentiment": "positive"},
        {"user": "Lisa W.", "rating": 4, "comment": "Great autocomplete and code suggestions. Saves me hours of work daily.", "sentiment": "positive"}
      ]
    },
    {
      "id": 4,
      "name": "Claude",
      "category": "AI Assistant",
      "description": "Anthropic's AI assistant focused on being helpful, harmless, and honest with advanced reasoning capabilities.",
      "rating": 4.5,
      "pricing": "Free / $20/month",
      "trending": false,
      "popularity": 79,
      "website": "https://claude.ai",
      "logo": "🧠",
      "reviews": [
        {"user": "Maria S.", "rating": 5, "comment": "More thoughtful and nuanced responses compared to other AI assistants.", "sentiment": "positive"},
        {"user": "Tom H.", "rating": 4, "comment": "Excellent for complex analysis tasks. Very reliable and ethical.", "sentiment": "positive"}
      ]
    },
    {
      "id": 5,
      "name": "Synthesia",
      "category": "Video Generation",
      "description": "Create professional AI videos with realistic avatars speaking your script in 140+ languages.",
      "rating": 4.4,
      "pricing": "$22-90/month",
      "trending": false,
      "popularity": 73,
      "website": "https://synthesia.io",
      "logo": "🎬",
      "reviews": [
        {"user": "Rachel B.", "rating": 4, "comment": "Perfect for creating training videos quickly. The avatars look very realistic.", "sentiment": "positive"},
        {"user": "Kevin J.", "rating": 3, "comment": "Good concept but avatars sometimes look a bit robotic in movements.", "sentiment": "neutral"}
      ]
    },
    {
      "id": 6,
      "name": "Perplexity AI",
      "category": "Research",
      "description": "AI-powered search engine that provides accurate answers with real-time web citations and sources.",
      "rating": 4.6,
      "pricing": "Free / $20/month",
      "trending": true,
      "popularity": 85,
      "website": "https://perplexity.ai",
      "logo": "🔍",
      "reviews": [
        {"user": "Anna C.", "rating": 5, "comment": "Amazing for research! Always provides sources and up-to-date information.", "sentiment": "positive"},
        {"user": "Paul D.", "rating": 4, "comment": "Great alternative to traditional search. Love the citation feature.", "sentiment": "positive"}
      ]
    },
    {
      "id": 7,
      "name": "Canva",
      "category": "Design",
      "description": "AI-enhanced graphic design platform with smart templates, background removal, and automated design suggestions.",
      "rating": 4.3,
      "pricing": "Free / $15/month",
      "trending": false,
      "popularity": 92,
      "website": "https://canva.com",
      "logo": "🎯",
      "reviews": [
        {"user": "Sophie F.", "rating": 4, "comment": "Great for quick designs. The AI features make it super easy to create professional graphics.", "sentiment": "positive"},
        {"user": "Mark L.", "rating": 4, "comment": "Very user-friendly with good AI suggestions. Sometimes limited customization options.", "sentiment": "positive"}
      ]
    },
    {
      "id": 8,
      "name": "ElevenLabs",
      "category": "Voice Generation",
      "description": "Generate lifelike speech in any voice and style with advanced AI voice cloning and text-to-speech technology.",
      "rating": 4.5,
      "pricing": "Free / $5-330/month",
      "trending": false,
      "popularity": 76,
      "website": "https://elevenlabs.io",
      "logo": "🎙️",
      "reviews": [
        {"user": "Chris G.", "rating": 5, "comment": "Incredibly realistic voice generation. Perfect for audiobooks and podcasts.", "sentiment": "positive"},
        {"user": "Amy R.", "rating": 4, "comment": "High quality voices but can be expensive for heavy usage.", "sentiment": "positive"}
      ]
    },
    {
      "id": 9,
      "name": "Jasper",
      "category": "Content Writing",
      "description": "AI writing assistant that helps create blog posts, marketing copy, and social media content at scale.",
      "rating": 4.2,
      "pricing": "$49-125/month",
      "trending": false,
      "popularity": 71,
      "website": "https://jasper.ai",
      "logo": "✍️",
      "reviews": [
        {"user": "Jennifer M.", "rating": 4, "comment": "Solid writing assistant for marketing content. Good templates and workflows.", "sentiment": "positive"},
        {"user": "Steve K.", "rating": 3, "comment": "Decent output but requires a lot of editing. Can be expensive.", "sentiment": "neutral"}
      ]
    },
    {
      "id": 10,
      "name": "Runway ML",
      "category": "Video Generation",
      "description": "Advanced AI video editing and generation tools including text-to-video, image-to-video, and video effects.",
      "rating": 4.4,
      "pricing": "Free / $12-76/month",
      "trending": true,
      "popularity": 78,
      "website": "https://runwayml.com",
      "logo": "🎥",
      "reviews": [
        {"user": "Daniel W.", "rating": 4, "comment": "Impressive video generation capabilities. Great for creative projects.", "sentiment": "positive"},
        {"user": "Nicole P.", "rating": 4, "comment": "Love the variety of AI video tools. Interface could be more intuitive.", "sentiment": "positive"}
      ]
    },
    {
      "id": 11,
      "name": "Notion AI",
      "category": "Productivity",
      "description": "AI-powered workspace for notes, docs, and project management with intelligent writing and organization features.",
      "rating": 4.3,
      "pricing": "Free / $10/month",
      "trending": false,
      "popularity": 89,
      "website": "https://notion.so",
      "logo": "📝",
      "reviews": [
        {"user": "Taylor S.", "rating": 4, "comment": "Great integration with Notion workspace. Helpful for writing and brainstorming.", "sentiment": "positive"},
        {"user": "Jordan K.", "rating": 4, "comment": "AI features are useful but sometimes feel like an afterthought to the main product.", "sentiment": "positive"}
      ]
    },
    {
      "id": 12,
      "name": "DeepL",
      "category": "Translation",
      "description": "AI-powered translation service that provides more accurate and natural translations than traditional tools.",
      "rating": 4.7,
      "pricing": "Free / $6.99-57.49/month",
      "trending": false,
      "popularity": 87,
      "website": "https://deepl.com",
      "logo": "🌐",
      "reviews": [
        {"user": "Carlos R.", "rating": 5, "comment": "Best translation tool available. Much more natural than Google Translate.", "sentiment": "positive"},
        {"user": "Marie L.", "rating": 4, "comment": "Excellent translation quality, especially for European languages.", "sentiment": "positive"}
      ]
    },
    {
      "id": 13,
      "name": "Copy.ai",
      "category": "Content Writing",
      "description": "AI copywriting tool that generates marketing copy, product descriptions, and social media content.",
      "rating": 4.1,
      "pricing": "Free / $36-186/month",
      "trending": false,
      "popularity": 68,
      "website": "https://copy.ai",
      "logo": "📄",
      "reviews": [
        {"user": "Hannah T.", "rating": 4, "comment": "Good for generating initial drafts. Saves time on brainstorming copy ideas.", "sentiment": "positive"},
        {"user": "Ryan B.", "rating": 3, "comment": "Helpful but output often needs significant editing to match brand voice.", "sentiment": "neutral"}
      ]
    },
    {
      "id": 14,
      "name": "Stable Diffusion",
      "category": "Image Generation",
      "description": "Open-source AI image generation model that creates high-quality images from text descriptions.",
      "rating": 4.4,
      "pricing": "Free / Self-hosted",
      "trending": false,
      "popularity": 74,
      "website": "https://stability.ai",
      "logo": "🖼️",
      "reviews": [
        {"user": "Alex H.", "rating": 4, "comment": "Great open-source alternative. More control over the generation process.", "sentiment": "positive"},
        {"user": "Maya P.", "rating": 4, "comment": "Powerful but requires technical knowledge to set up and use effectively.", "sentiment": "positive"}
      ]
    },
    {
      "id": 15,
      "name": "Grammarly",
      "category": "Writing Assistant",
      "description": "AI-powered writing assistant that checks grammar, spelling, and provides style suggestions for better writing.",
      "rating": 4.5,
      "pricing": "Free / $12-30/month",
      "trending": false,
      "popularity": 94,
      "website": "https://grammarly.com",
      "logo": "📚",
      "reviews": [
        {"user": "Emily R.", "rating": 5, "comment": "Essential tool for all my writing. Catches errors I always miss.", "sentiment": "positive"},
        {"user": "James L.", "rating": 4, "comment": "Very helpful for professional writing. Premium features are worth it.", "sentiment": "positive"}
      ]
    }
  ],
  "categories": [
    {"name": "AI Assistant", "icon": "🤖", "color": "#00ffff", "count": 3},
    {"name": "Image Generation", "icon": "🎨", "color": "#f472b6", "count": 3},
    {"name": "Video Generation", "icon": "🎬", "color": "#8b5cf6", "count": 2},
    {"name": "Development", "icon": "💻", "color": "#10b981", "count": 1},
    {"name": "Content Writing", "icon": "✍️", "color": "#f59e0b", "count": 2},
    {"name": "Research", "icon": "🔍", "color": "#3b82f6", "count": 1},
    {"name": "Design", "icon": "🎯", "color": "#ef4444", "count": 1},
    {"name": "Voice Generation", "icon": "🎙️", "color": "#06b6d4", "count": 1},
    {"name": "Productivity", "icon": "📝", "color": "#84cc16", "count": 1},
    {"name": "Translation", "icon": "🌐", "color": "#6366f1", "count": 1},
    {"name": "Writing Assistant", "icon": "📚", "color": "#ec4899", "count": 1}
  ]
};


// --- Remote recommendations integration ---
// If backend is available, this will fetch recommended tools and replace the displayed tool list.
// It safely falls back to local data if the backend call fails.
// ✅ Connect search bar to FastAPI backend
async function fetchRecommendationsFromBackend(query, limit = 12) {
  if (!query) return [];
  try {
    const resp = await fetch("http://127.0.0.1:8000/api/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query, limit })
    });

    if (!resp.ok) {
      console.error("Backend error:", resp.status, await resp.text());
      return [];
    }

    const data = await resp.json();

    // Expecting { recommendations: [...] } from backend
    const recs = data && Array.isArray(data.recommendations) ? data.recommendations : [];

    // Map backend shape to frontend expected shape
    return recs.map((t, idx) => ({
      id: t.id ?? `r${idx}`,
      name: t.name ?? t.title ?? '',
      category: t.category ?? (t.categories ? t.categories[0] : '') ?? '',
      description: t.description ?? '',
      rating: t.rating ?? 4.2,
      pricing: t.pricing ?? t.price ?? '',
      trending: t.trending ?? false,
      popularity: t.popularity ?? 50,
      website: t.website ?? t.url ?? '',
      logo: t.logo ?? '🤖',
      reviews: t.reviews ?? []
    }));
  } catch (err) {
    console.error('Failed to fetch recommendations from backend:', err);
    return [];
  }
}

// ---------------------- Global state ----------------------
let filteredTools = []; // will be initialized after merging user tools
let activeFilters = {
  categories: [],
  ratings: [],
  search: ''
};

// ---------------------- Initialization ----------------------
document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  loadAndMergeData();
  initializeParticles();
  renderTrendingTools();
  renderCategoryFilters();
  renderToolsGrid();
  setupEventListeners();
  populateSubmissionForm();
}

// Load saved tools from localStorage and merge
function loadAndMergeData() {
  const userAddedTools = JSON.parse(localStorage.getItem('userAddedAITools')) || [];
  aiToolsData.aiTools.push(...userAddedTools);

  userAddedTools.forEach(tool => {
    const category = aiToolsData.categories.find(cat => cat.name === tool.category);
    if (category) category.count++;
    else {
      aiToolsData.categories.push({ name: tool.category, icon: '🔧', color: '#cccccc', count: 1 });
    }
  });

  filteredTools = [...aiToolsData.aiTools];
}

// ---------------------- Particles (unchanged) ----------------------
function initializeParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();

  const particles = [];
  const particleCount = 80;
  const connectionDistance = 150;

  class Particle {
    constructor() {
      this.reset();
      this.y = Math.random() * canvas.height;
      this.opacity = Math.random() * 0.6 + 0.2;
    }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 3 + 1;
      this.speedX = (Math.random() - 0.5) * 0.8;
      this.speedY = (Math.random() - 0.5) * 0.8;
      this.color = this.getRandomColor();
      this.pulse = Math.random() * 0.02 + 0.01;
      this.pulseDirection = 1;
    }
    getRandomColor() {
      const colors = ['#00ffff', '#8b5cf6', '#f472b6', '#10b981', '#fbbf24'];
      return colors[Math.floor(Math.random() * colors.length)];
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.x > canvas.width + 10) this.x = -10;
      if (this.x < -10) this.x = canvas.width + 10;
      if (this.y > canvas.height + 10) this.y = -10;
      if (this.y < -10) this.y = canvas.height + 10;
      this.opacity += this.pulse * this.pulseDirection;
      if (this.opacity >= 0.8 || this.opacity <= 0.2) this.pulseDirection *= -1;
    }
    draw() {
      ctx.save();
      ctx.globalAlpha = this.opacity;
      ctx.fillStyle = this.color;
      ctx.shadowBlur = 20;
      ctx.shadowColor = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = this.opacity * 0.3;
      ctx.shadowBlur = 40;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  for (let i = 0; i < particleCount; i++) particles.push(new Particle());

  function animate() {
    ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle, index) => {
      particle.update();
      particle.draw();

      particles.slice(index + 1).forEach(other => {
        const dx = particle.x - other.x;
        const dy = particle.y - other.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < connectionDistance) {
          const opacity = (connectionDistance - distance) / connectionDistance * 0.3;
          ctx.save();
          ctx.globalAlpha = opacity;
          ctx.strokeStyle = '#00ffff';
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(particle.x, particle.y);
          ctx.lineTo(other.x, other.y);
          ctx.stroke();
          ctx.restore();
        }
      });
    });

    requestAnimationFrame(animate);
  }
  animate();
  window.addEventListener('resize', resizeCanvas);
}

// ---------------------- Renderers ----------------------
function renderTrendingTools() {
  const container = document.getElementById('trending-tools');
  if (!container) return;
  const trendingTools = aiToolsData.aiTools.filter(tool => tool.trending);
  container.innerHTML = trendingTools.map(tool => `
    <div class="trending-card" onclick="openToolModal(${tool.id})">
      <div class="trending-badge">🔥 Trending</div>
      <div class="tool-header">
        <div class="tool-logo">${tool.logo}</div>
        <div class="tool-info">
          <h3>${tool.name}</h3>
          <span class="tool-category" style="background: ${getCategoryColor(tool.category)}20; color: ${getCategoryColor(tool.category)}">
            ${getCategoryIcon(tool.category)} ${tool.category}
          </span>
        </div>
      </div>
      <p class="tool-description">${tool.description}</p>
      <div class="tool-meta">
        <div class="tool-rating">
          <span class="rating-stars-display">${generateStars(tool.rating)}</span>
          <span class="rating-number">${tool.rating}</span>
        </div>
        <div class="tool-pricing">${tool.pricing}</div>
      </div>
    </div>
  `).join('');
}

function renderCategoryFilters() {
  const container = document.getElementById('category-filters');
  if (!container) return;
  container.innerHTML = aiToolsData.categories.map(category => `
    <label class="filter-checkbox">
      <input type="checkbox" value="${category.name}" onchange="handleCategoryFilter('${category.name}')">
      <span class="checkmark"></span>
      <span>${category.icon} ${category.name} (${category.count})</span>
    </label>
  `).join('');
}

function renderToolsGrid() {
  const container = document.getElementById('tools-grid-container');
  const noResults = document.getElementById('no-results');
  if (!container || !noResults) return;

  if (filteredTools.length === 0) {
    container.innerHTML = '';
    noResults.classList.remove('hidden');
    return;
  }
  noResults.classList.add('hidden');

  container.innerHTML = filteredTools.map(tool => `
    <div class="tool-card" onclick="openToolModal(${tool.id})">
      ${tool.trending ? '<div class="trending-indicator">🔥 Trending</div>' : ''}
      <div class="tool-header">
        <div class="tool-logo">${tool.logo}</div>
        <div class="tool-info">
          <h3>${tool.name}</h3>
          <span class="tool-category" style="background: ${getCategoryColor(tool.category)}20; color: ${getCategoryColor(tool.category)}">
            ${getCategoryIcon(tool.category)} ${tool.category}
          </span>
        </div>
      </div>
      <p class="tool-description">${tool.description}</p>
      <div class="tool-meta">
        <div class="tool-rating">
          <span class="rating-stars-display">${generateStars(tool.rating)}</span>
          <span class="rating-number">${tool.rating}</span>
        </div>
        <div class="tool-pricing">${tool.pricing}</div>
      </div>
      <div class="tool-actions">
        <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); window.open('${tool.website}', '_blank')">
          Try Tool
        </button>
        <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); openToolModal(${tool.id})">
          View Details
        </button>
      </div>
    </div>
  `).join('');
}

// ---------------------- Event listeners ----------------------
function setupEventListeners() {
  const searchInput = document.getElementById('search-input');
const searchButton = document.querySelector('.hero-search-btn');

// ✅ Remove real-time input listener
// Search will now happen ONLY when the user clicks the button or presses Enter

if (searchInput && searchButton) {
  searchButton.addEventListener('click', () => {
    handleSearch({ target: searchInput });
  });

  searchInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
      handleSearch({ target: searchInput });
    }
  });
}


  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) sortSelect.addEventListener('change', handleSort);

  document.querySelectorAll('input[id^="rating-"]').forEach(input => input.addEventListener('change', handleRatingFilter));
  document.querySelectorAll('.view-btn').forEach(btn => btn.addEventListener('click', handleViewToggle));

  const submissionForm = document.getElementById('submission-form');
  if (submissionForm) submissionForm.addEventListener('submit', handleSubmissionForm);

  document.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', handleNavigation));
}

// ---------------------- Navigation ----------------------
function handleNavigation(event) {
  const href = event.target.getAttribute('href');
  if (href && href.startsWith('#')) {
    event.preventDefault();
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');

    const targetId = href.substring(1);
    switch (targetId) {
      case 'home': scrollToTop(); break;
      case 'categories': showCategoriesOverview(); break;
      case 'trending': scrollToSection('trending'); break;
      case 'about': showAboutModal(); break;
      default: scrollToSection(targetId);
    }
  }
}

// ---------------------- Categories overview & filtering ----------------------
function showCategoriesOverview() {
  const modal = document.getElementById('tool-modal');
  const modalBody = document.getElementById('modal-body');
  if (!modal || !modalBody) return;

  modalBody.innerHTML = `
    <div class="categories-overview">
      <h2 style="margin-bottom: 24px; color: #00ffff;">AI Tool Categories</h2>
      <p style="margin-bottom: 32px; color: rgba(255,255,255,0.7);">Explore our comprehensive collection of AI tools organized by category.</p>
      <div class="categories-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
        ${aiToolsData.categories.map(category => {
          const categoryTools = aiToolsData.aiTools.filter(tool => tool.category === category.name);
          return `
            <div class="category-card" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; cursor: pointer;" onclick="filterByCategory('${category.name}')">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <span style="font-size: 32px;">${category.icon}</span>
                <div>
                  <h3 style="margin: 0; color: ${category.color};">${category.name}</h3>
                  <p style="margin: 0; font-size: 14px; color: rgba(255,255,255,0.6);">${category.count} tools</p>
                </div>
              </div>
              <div class="category-tools" style="font-size: 14px; color: rgba(255,255,255,0.7);">
                ${categoryTools.slice(0, 3).map(tool => tool.name).join(', ')}${categoryTools.length > 3 ? '...' : ''}
              </div>
            </div>
          `;
        }).join('')}
      </div>
      <div style="margin-top: 32px; text-align: center;">
        <button class="btn btn-outline" onclick="closeModal()">Close</button>
      </div>
    </div>
  `;

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

// Filter by category from categories overview (local only)
function filterByCategory(categoryName) {
  closeModal();

  activeFilters.categories = [categoryName];
  activeFilters.search = '';
  activeFilters.ratings = [];

  const searchInput = document.getElementById('search-input');
  if (searchInput) searchInput.value = '';

  document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
  const selected = document.querySelector(`input[value="${categoryName}"]`);
  if (selected) selected.checked = true;
  document.querySelectorAll('input[id^="rating-"]').forEach(cb => cb.checked = false);

  applyFilters();
  setTimeout(() => scrollToSection('tools-grid'), 300);
}

// ---------------------- Modal helpers ----------------------
function openToolModal(toolId) {
  const tool = aiToolsData.aiTools.find(t => t.id === toolId);
  if (!tool) return;
  const modal = document.getElementById('tool-modal');
  const modalBody = document.getElementById('modal-body');
  if (!modal || !modalBody) return;

  modalBody.innerHTML = `
    <div class="tool-detail">
      <div class="tool-header">
        <div class="tool-logo" style="font-size: 60px; width: 80px; height: 80px;">${tool.logo}</div>
        <div class="tool-info">
          <h2>${tool.name}</h2>
          <span class="tool-category" style="background: ${getCategoryColor(tool.category)}20; color: ${getCategoryColor(tool.category)}">
            ${getCategoryIcon(tool.category)} ${tool.category}
          </span>
          <div class="tool-rating" style="margin-top: 12px;">
            <span class="rating-stars-display">${generateStars(tool.rating)}</span>
            <span class="rating-number">${tool.rating}</span>
          </div>
        </div>
      </div>

      <p class="tool-description" style="font-size: 16px; line-height: 1.6; margin: 24px 0;">${tool.description}</p>

      <div class="tool-meta" style="margin-bottom: 32px;">
        <div><strong>Pricing:</strong> ${tool.pricing}</div>
        <div><strong>Popularity:</strong> ${tool.popularity}%</div>
        ${tool.trending ? '<div class="trending-indicator" style="position: static; margin-left: 16px;">🔥 Trending</div>' : ''}
      </div>

      <div class="reviews-section">
        <h3 style="margin-bottom: 20px; color: #00ffff;">Reviews & Sentiment Analysis</h3>
        <div class="reviews-list">
          ${tool.reviews.map(review => `
            <div class="review-item" style="background: rgba(255,255,255,0.05); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong>${review.user}</strong>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span>${generateStars(review.rating)}</span>
                  <span class="sentiment-indicator">${getSentimentEmoji(review.sentiment)}</span>
                </div>
              </div>
              <p style="margin: 0; color: rgba(255,255,255,0.8);">${review.comment}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="tool-actions" style="margin-top: 32px; display: flex; gap: 16px;">
        <button class="btn btn-primary" onclick="window.open('${tool.website}', '_blank')">
          <span>Try ${tool.name}</span>
          <span class="btn-glow"></span>
        </button>
        <button class="btn btn-outline" onclick="closeModal()">Close</button>
        <!-- ⭐ Favorite button -->
  <button id="favoriteBtn-${tool.id}" class="favorite-btn">⭐ Add to Favorites</button>
      </div>
      
    </div>
  `;

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  // --- Supabase Favorites Logic ---
import("https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm").then(async ({ createClient }) => {
  const supabaseUrl = "https://pjxrjytcurqrmbuhgyoi.supabase.co";
  const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqeHJqeXRjdXJxcm1idWhneW9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExMjYxNTcsImV4cCI6MjA3NjcwMjE1N30.H5xP2ZlKFl_-h41I_ZjCcGmt0NLK64eOwO8Ipr2sfZQ";
  const supabase = createClient(supabaseUrl, supabaseKey);

  const favoriteBtn = document.getElementById(`favoriteBtn-${tool.id}`);

  async function getUser() {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  }

  async function toggleFavorite() {
    const user = await getUser();
    if (!user) {
      alert("Please log in to save favorites!");
      return;
    }

    const { data: existing } = await supabase
      .from('favorites')
      .select('*')
      .eq('user_id', user.id)
      .eq('tool_id', tool.id)
      .single();

    if (existing) {
      await supabase.from('favorites').delete().eq('id', existing.id);
      favoriteBtn.classList.remove('active');
      favoriteBtn.textContent = "⭐ Add to Favorites";
    } else {
      await supabase.from('favorites').insert({
        user_id: user.id,
        tool_id: tool.id,
        tool_name: tool.name,
        category: tool.category,
        url: tool.website
      });
      favoriteBtn.classList.add('active');
      favoriteBtn.textContent = "★ Added to Favorites";
    }
  }

  favoriteBtn.addEventListener('click', toggleFavorite);

  // On open, check if tool is already favorited
  const user = await getUser();
  if (user) {
    const { data: existing } = await supabase
      .from('favorites')
      .select('id')
      .eq('user_id', user.id)
      .eq('tool_id', tool.id)
      .single();
    if (existing) {
      favoriteBtn.classList.add('active');
      favoriteBtn.textContent = "★ Added to Favorites";
    }
  }
});

}

function closeModal() {
  const modal = document.getElementById('tool-modal');
  if (!modal) return;
  modal.classList.add('hidden');
  document.body.style.overflow = 'auto';
}

// ---------------------- Submission form ----------------------
function openSubmissionModal() {
  const modal = document.getElementById('submission-modal');
  if (!modal) return;
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeSubmissionModal() {
  const modal = document.getElementById('submission-modal');
  if (!modal) return;
  modal.classList.add('hidden');
  document.body.style.overflow = 'auto';
  const form = document.getElementById('submission-form');
  if (form) form.reset();
}

function populateSubmissionForm() {
  const categorySelect = document.getElementById('tool-category');
  if (!categorySelect) return;
  categorySelect.innerHTML = '<option value="">Select a category...</option>' +
    aiToolsData.categories.map(category => 
      `<option value="${category.name}">${category.icon} ${category.name}</option>`
    ).join('');
}

function handleSubmissionForm(event) {
  event.preventDefault();

  const toolName = document.getElementById('tool-name')?.value;
  const toolWebsite = document.getElementById('tool-website')?.value;
  const toolCategory = document.getElementById('tool-category')?.value;
  const toolDescription = document.getElementById('tool-description')?.value;

  if (!toolName || !toolWebsite || !toolCategory || !toolDescription) {
    alert("Please fill out all fields.");
    return;
  }

  const newTool = {
    id: Date.now(),
    name: toolName,
    category: toolCategory,
    description: toolDescription,
    rating: 4.0,
    pricing: "Free / Varies",
    trending: false,
    popularity: 50,
    website: toolWebsite.startsWith('http') ? toolWebsite : `https://${toolWebsite}`,
    logo: getCategoryIcon(toolCategory),
    reviews: []
  };

  aiToolsData.aiTools.push(newTool);

  const cat = aiToolsData.categories.find(c => c.name === newTool.category);
  if (cat) cat.count++;
  else aiToolsData.categories.push({ name: newTool.category, icon: '🔧', color: '#cccccc', count: 1 });

  // Save to localStorage and update UI (local filtering only)
  const userAddedTools = JSON.parse(localStorage.getItem('userAddedAITools')) || [];
  userAddedTools.push(newTool);
  localStorage.setItem('userAddedAITools', JSON.stringify(userAddedTools));

  applyFilters();
  renderCategoryFilters();
  closeSubmissionModal();
  showSuccessMessage();
}

// Simulated auto category detection (unchanged)
function autoCategorize(event) {
  const btn = event.target.closest('.btn');
  const spinner = btn.querySelector('.loading-spinner');
  const description = document.getElementById('tool-description')?.value;
  const categorySelect = document.getElementById('tool-category');
  if (!description || !categorySelect) {
    alert('Please enter a description first!');
    return;
  }

  spinner?.classList.remove('hidden');
  if (btn) btn.disabled = true;

  setTimeout(() => {
    const keywords = {
      'AI Assistant': ['assistant', 'chat', 'conversation', 'help'],
      'Image Generation': ['image', 'art', 'visual', 'generate', 'picture'],
      'Video Generation': ['video', 'film', 'movie', 'animation'],
      'Development': ['code', 'programming', 'developer', 'software'],
      'Content Writing': ['writing', 'content', 'blog', 'copy'],
      'Research': ['research', 'search', 'information', 'data'],
      'Design': ['design', 'graphic', 'template', 'creative'],
      'Voice Generation': ['voice', 'speech', 'audio', 'sound'],
      'Productivity': ['productivity', 'workspace', 'organization', 'notes'],
      'Translation': ['translate', 'language', 'multilingual']
    };

    let bestMatch = 'AI Assistant';
    let maxMatches = 0;

    Object.entries(keywords).forEach(([category, categoryKeywords]) => {
      const matches = categoryKeywords.filter(keyword => description.toLowerCase().includes(keyword)).length;
      if (matches > maxMatches) {
        maxMatches = matches;
        bestMatch = category;
      }
    });

    categorySelect.value = bestMatch;
    spinner?.classList.add('hidden');
    if (btn) btn.disabled = false;
    categorySelect.style.borderColor = '#00ffff';
    categorySelect.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.3)';
    setTimeout(() => {
      categorySelect.style.borderColor = '';
      categorySelect.style.boxShadow = '';
    }, 2000);
  }, 1200);
}

// Success message
function showSuccessMessage() {
  const successMessage = document.getElementById('success-message');
  if (!successMessage) return;
  successMessage.classList.remove('hidden');
  setTimeout(() => successMessage.classList.add('hidden'), 3000);
}

// ---------------------- Search, filters, sort ----------------------
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase().trim();
  activeFilters.search = searchTerm;

  const searchContainer = event.target.closest('.search-container') || event.target.closest('.hero-search-container');
  if (searchTerm) {
    if (searchContainer) {
      searchContainer.style.borderColor = '#00ffff';
      searchContainer.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.3)';
    }
  } else {
    if (searchContainer) {
      searchContainer.style.borderColor = '';
      searchContainer.style.boxShadow = '';
    }
  }

  // Try remote recommendations first for richer results
  (async () => {
    if (!searchTerm) {
      // If empty, restore local data if backup exists, then apply local filters
      if (aiToolsData._localBackup) {
        aiToolsData.aiTools = aiToolsData._localBackup;
        delete aiToolsData._localBackup;
      }
      applyFilters();
      return;
    }
    const remote = await fetchRecommendationsFromBackend(searchTerm, 12);
    if (remote && remote.length > 0) {
      // Temporarily replace tools with remote results
      if (!aiToolsData._localBackup) aiToolsData._localBackup = [...aiToolsData.aiTools];
      aiToolsData.aiTools = remote;
      applyFilters();
      return;
    }
    // fallback to local filtering
    if (aiToolsData._localBackup) {
      aiToolsData.aiTools = aiToolsData._localBackup;
      delete aiToolsData._localBackup;
    }
    applyFilters();
  })();

  if (searchTerm) setTimeout(() => scrollToSection('tools-grid'), 300);
}

function handleCategoryFilter(category) {
  // toggle category in activeFilters (local only)
  const idx = activeFilters.categories.indexOf(category);
  if (idx > -1) activeFilters.categories.splice(idx, 1);
  else activeFilters.categories.push(category);
  applyFilters();
}

function handleRatingFilter() {
  activeFilters.ratings = Array.from(document.querySelectorAll('input[id^="rating-"]:checked')).map(input => parseFloat(input.value));
  applyFilters();
}

function handleSort(event) {
  const sortBy = event.target.value;
  filteredTools.sort((a, b) => {
    switch (sortBy) {
      case 'popularity': return b.popularity - a.popularity;
      case 'rating': return b.rating - a.rating;
      case 'newest': return b.id - a.id;
      case 'trending': return (b.trending ? 1 : 0) - (a.trending ? 1 : 0);
      default: return 0;
    }
  });
  renderToolsGrid();
}

// Apply filters (local)
function applyFilters() {
  filteredTools = aiToolsData.aiTools.filter(tool => {
    if (activeFilters.search) {
      const searchTerm = activeFilters.search;
      const searchableText = [
        tool.name,
        tool.description,
        tool.category,
        tool.pricing,
        ...(tool.reviews || []).map(r => r.comment)
      ].join(' ').toLowerCase();
      if (!searchableText.includes(searchTerm)) return false;
    }

    if (activeFilters.categories.length > 0 && !activeFilters.categories.includes(tool.category)) return false;

    if (activeFilters.ratings.length > 0 && !activeFilters.ratings.some(rating => tool.rating >= rating)) return false;

    return true;
  });

  renderToolsGrid();

  if (activeFilters.search) window.history.replaceState(null, null, `#search=${encodeURIComponent(activeFilters.search)}`);
}

// ---------------------- View toggle ----------------------
function handleViewToggle(event) {
  document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  const view = event.target.dataset.view;
  const container = document.getElementById('tools-grid-container');
  if (!container) return;
  if (view === 'list') container.classList.add('tools-list');
  else container.classList.remove('tools-list');
}

// ---------------------- Utilities ----------------------
function getCategoryColor(category) {
  const c = aiToolsData.categories.find(cat => cat.name === category);
  return c ? c.color : '#00ffff';
}
function getCategoryIcon(category) {
  const c = aiToolsData.categories.find(cat => cat.name === category);
  return c ? c.icon : '🔧';
}
function generateStars(rating) {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
  return '⭐'.repeat(fullStars) + (hasHalfStar ? '✨' : '') + '☆'.repeat(emptyStars);
}
function getSentimentEmoji(sentiment) {
  switch (sentiment) {
    case 'positive': return '😊';
    case 'neutral': return '😐';
    case 'negative': return '😢';
    default: return '😐';
  }
}

function scrollToTop() { window.scrollTo({ top: 0, behavior: 'smooth' }); }
function scrollToSection(sectionId) {
  const el = document.getElementById(sectionId);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ---------------------- Intersection observer for animations ----------------------
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tool-card, .trending-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
  });
});